"""
======================================================================
 PRODUCTION PYTORCH INFERENCE MODULE: MODEL B (DPD ViT-Base)
======================================================================
Dual-Head Vision Transformer Base for Multi-Crop Plant Pathology:
- Backbone: vit_base_patch16_224 (768-dim latent embeddings)
- Plant Head: linear_plant (768 -> 55 crops)
- Disease Head: linear_disease (768 -> 175 diseases)
- Supported Scope: 333 Biologically Valid Crop-Disease Pairs across 55 Crops
======================================================================
"""

import os
import io
import json
from typing import List, Dict, Tuple, Any, Optional
from PIL import Image
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import timm

# ---------------------------------------------------------------------------
# SUPPORTED 38 CROP-DISEASE PAIRS (Legacy PlantVillage Baseline Fallback)
# ---------------------------------------------------------------------------
PV_TO_DPD_MAPPING = {
    'Apple___Apple_scab': ('apple', 'scab', 0, 15, 15),
    'Apple___Black_rot': ('apple', 'black_rot', 0, 3, 3),
    'Apple___Cedar_apple_rust': ('apple', 'cedar_apple_rust', 0, 5, 5),
    'Apple___healthy': ('apple', 'healthy', 0, 9, 9),
    'Blueberry___healthy': ('blueberry', 'healthy', 7, 9, 51),
    'Cherry___Powdery_mildew': ('cherry', 'powdery_mildew', 16, 14, 87),
    'Cherry___healthy': ('cherry', 'healthy', 16, 9, 85),
    'Corn___Cercospora_leaf_spot Gray_leaf_spot': ('corn', 'gray_leaf_spot', 21, 70, 109),
    'Corn___Common_rust': ('corn', 'common_rust', 21, 93, 163),
    'Corn___Northern_Leaf_Blight': ('corn', 'northern_leaf_blight', 21, 74, 116),
    'Corn___healthy': ('corn', 'healthy', 21, 9, 110),
    'Grape___Black_rot': ('grape', 'black_rot', 27, 3, 144),
    'Grape___Esca_(Black_Measles)': ('grape', 'esca', 27, 88, 146),
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': ('grape', 'leaf_blight', 27, 72, 148),
    'Grape___healthy': ('grape', 'healthy', 27, 9, 147),
    'Orange___Haunglongbing_(Citrus_greening)': ('citrus', 'greening', 18, 61, 94),
    'Peach___Bacterial_spot': ('peach', 'bacterial_spot', 36, 33, 216),
    'Peach___healthy': ('peach', 'healthy', 36, 9, 218),
    'Pepper,_bell___Bacterial_spot': ('pepper_bell', 'bacterial_spot', 5, 33, 39),
    'Pepper,_bell___healthy': ('pepper_bell', 'healthy', 5, 9, 42),
    'Potato___Early_blight': ('potato', 'early_blight', 40, 55, 240),
    'Potato___Late_blight': ('potato', 'late_blight', 40, 139, 242),
    'Potato___healthy': ('potato', 'healthy', 40, 9, 241),
    'Raspberry___healthy': ('raspberry', 'healthy', 42, 9, 246),
    'Soybean___healthy': ('soybean', 'healthy', 44, 9, 261),
    'Squash___Powdery_mildew': ('squash', 'powdery_mildew', 45, 14, 264),
    'Strawberry___Leaf_scorch': ('strawberry', 'scorch', 46, 40, 267),
    'Strawberry___healthy': ('strawberry', 'healthy', 46, 9, 266),
    'Tomato___Bacterial_spot': ('tomato', 'bacterial_spot', 51, 33, 300),
    'Tomato___Early_blight': ('tomato', 'early_blight', 51, 55, 303),
    'Tomato___Late_blight': ('tomato', 'late_blight', 51, 139, 305),
    'Tomato___Leaf_Mold': ('tomato', 'leaf_mold', 51, 163, 308),
    'Tomato___Septoria_leaf_spot': ('tomato', 'septoria_leaf_spot', 51, 165, 312),
    'Tomato___Spider_mites Two-spotted_spider_mite': ('tomato', 'spider_mites', 51, 68, 313),
    'Tomato___Target_Spot': ('tomato', 'target_spot', 51, 82, 314),
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': ('tomato', 'yellow_leaf_curl_virus', 51, 167, 316),
    'Tomato___Tomato_mosaic_virus': ('tomato', 'mosaic_virus', 51, 13, 309),
    'Tomato___healthy': ('tomato', 'healthy', 51, 9, 304)
}

PAIR_LOOKUP = {(v[2], v[3]): k for k, v in PV_TO_DPD_MAPPING.items()}
ALL_SUPPORTED_PAIRS = list(PV_TO_DPD_MAPPING.items())


def load_333_supported_pairs(assets_dir: str = "models_assets") -> List[Dict[str, Any]]:
    """
    Constructs the complete 333 biologically valid crop-disease pairs across 55 crops.
    Maps each crop to its plant head index (0-54) and disease to its disease head index (0-174).
    """
    rankings_p = os.path.join(assets_dir, "dpd_crop_rankings.json")
    plants_p = os.path.join(assets_dir, "dpd_55_plants.json")
    diseases_p = os.path.join(assets_dir, "dpd_175_diseases.json")

    if os.path.exists(rankings_p) and os.path.exists(plants_p) and os.path.exists(diseases_p):
        try:
            with open(plants_p, "r", encoding="utf-8") as f:
                plants_dict = json.load(f)
            with open(diseases_p, "r", encoding="utf-8") as f:
                diseases_dict = json.load(f)
            with open(rankings_p, "r", encoding="utf-8") as f:
                crops_list = json.load(f)

            p_to_idx = {v.lower().strip().replace(" ", "_"): int(k) for k, v in plants_dict.items()}
            d_to_idx = {v.lower().strip().replace(" ", "_"): int(k) for k, v in diseases_dict.items()}

            pairs = []
            for c in crops_list:
                c_slug = c["crop"].lower().strip().replace(" ", "_")
                p_idx = p_to_idx.get(c_slug)
                if p_idx is None:
                    continue
                c_display = c_slug.replace("_", " ").title()

                for d_name in c.get("all_diseases", {}).keys():
                    d_slug = d_name.lower().strip().replace(" ", "_")
                    d_idx = d_to_idx.get(d_slug)
                    if d_idx is None:
                        continue
                    d_display = d_slug.replace("_", " ").title()

                    pairs.append({
                        "raw_class": f"{c_slug}_{d_slug}",
                        "crop": c_display,
                        "disease": d_display,
                        "crop_slug": c_slug,
                        "disease_slug": d_slug,
                        "plant_idx": p_idx,
                        "disease_idx": d_idx
                    })

            if len(pairs) == 333:
                return pairs
        except Exception as e:
            print(f"[DPD Engine] Notice loading 333 pairs: {e}. Falling back to 38 pairs.")

    # Fallback to 38 benchmark pairs if asset files are inaccessible
    fallback_pairs = []
    for pv_cls, (p_name, d_name, p_idx, d_idx, _) in PV_TO_DPD_MAPPING.items():
        fallback_pairs.append({
            "raw_class": pv_cls,
            "crop": p_name.replace("_", " ").title(),
            "disease": d_name.replace("_", " ").title(),
            "crop_slug": p_name,
            "disease_slug": d_name,
            "plant_idx": p_idx,
            "disease_idx": d_idx
        })
    return fallback_pairs


# ---------------------------------------------------------------------------
# MODEL ARCHITECTURE
# ---------------------------------------------------------------------------
class DPDViTDualHead(nn.Module):
    def __init__(self, num_plants: int = 55, num_diseases: int = 175):
        super().__init__()
        self.model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=0)
        self.linear_plant = nn.Linear(768, num_plants)
        self.linear_disease = nn.Linear(768, num_diseases)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        feat = self.model(x)
        return self.linear_plant(feat), self.linear_disease(feat)


# ---------------------------------------------------------------------------
# PRODUCTION INFERENCE ENGINE
# ---------------------------------------------------------------------------
class DPDInferenceEngine:
    def __init__(self, checkpoint_path: Optional[str] = None, device: Optional[str] = None, assets_dir: str = "models_assets"):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)

        self.assets_dir = assets_dir
        self.model = DPDViTDualHead(num_plants=55, num_diseases=175).to(self.device)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # Load all 333 biologically valid DPD pairs across 55 crops
        self.supported_pairs = load_333_supported_pairs(self.assets_dir)
        print(f"[DPD Engine] Initialized with {len(self.supported_pairs)} biologically valid crop-disease pairs.")

        self.loaded = False
        self.checkpoint_path = self._resolve_checkpoint(checkpoint_path)
        self._load_weights()

    def _resolve_checkpoint(self, path: Optional[str]) -> str:
        if path and os.path.exists(path):
            return path
        candidates = [
            os.path.join(self.assets_dir, "model_b_partial_adapted.pth"),
            "models_assets/model_b_partial_adapted.pth",
            "dpd/DPD_pretrained_weight.pth",
            "DPD_pretrained_weight.pth"
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return candidates[0]

    def _load_weights(self):
        if os.path.exists(self.checkpoint_path):
            try:
                try:
                    ckpt = torch.load(self.checkpoint_path, map_location=self.device, weights_only=True)
                except TypeError:
                    ckpt = torch.load(self.checkpoint_path, map_location=self.device)
                self.model.load_state_dict(ckpt, strict=False)
                self.model.eval()
                self.loaded = True
                print(f"[DPD Engine] Successfully loaded model checkpoint from '{self.checkpoint_path}' on {self.device}.")
            except Exception as e:
                print(f"[DPD Engine] Error loading checkpoint '{self.checkpoint_path}': {e}")
        else:
            print(f"[DPD Engine] Checkpoint not found at '{self.checkpoint_path}'.")

    def _match_advisory(self, entry: Dict[str, Any], disease_info: Dict[str, Any]) -> Dict[str, Any]:
        """Robust multi-key clinical advisory matching across PlantVillage and DPD naming conventions."""
        if not disease_info:
            return {}

        c_slug = entry["crop_slug"]
        d_slug = entry["disease_slug"]
        raw = entry["raw_class"]

        candidates = [
            raw,
            f"{c_slug}_{d_slug}",
            f"{c_slug}___{d_slug}",
            f"{c_slug.capitalize()}___{d_slug}",
            f"{c_slug.capitalize()}___{d_slug.replace('_', ' ')}",
            f"{c_slug.capitalize()}___{d_slug.title().replace(' ', '_')}",
            d_slug
        ]

        for cand in candidates:
            if cand in disease_info:
                return disease_info[cand]

        # Case-insensitive normalized fallback lookup
        target_norm = f"{c_slug}_{d_slug}".lower()
        for k, v in disease_info.items():
            if k.lower().replace("___", "_").replace(" ", "_") == target_norm:
                return v

        return {}

    def predict(self, image: Image.Image, disease_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.loaded:
            raise RuntimeError("DPD Model checkpoint is not loaded.")

        if disease_info is None:
            disease_info = {}

        # 1. Image Preprocessing (ImageNet Normalization Pipeline)
        img_rgb = image.convert('RGB')
        tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)

        # 2. Forward Pass through Dual Heads
        with torch.no_grad():
            p_logits, d_logits = self.model(tensor)
            p_probs = F.softmax(p_logits, dim=-1)[0]
            d_probs = F.softmax(d_logits, dim=-1)[0]

        # 3. Score all 333 Supported Pairs using Joint Likelihood P(Plant=c) * P(Disease=d)
        pair_scores = []
        for pair in self.supported_pairs:
            p_idx = pair["plant_idx"]
            d_idx = pair["disease_idx"]
            prob_p = p_probs[p_idx].item()
            prob_d = d_probs[d_idx].item()

            # Joint likelihood score
            joint_prob = prob_p * prob_d
            # Calibrated geometric mean confidence (strictly monotonic with joint likelihood)
            conf = float(np.sqrt(max(0.0, joint_prob)) * 100.0)

            pair_scores.append({
                "raw_class": pair["raw_class"],
                "crop": pair["crop"],
                "disease": pair["disease"],
                "crop_slug": pair["crop_slug"],
                "disease_slug": pair["disease_slug"],
                "joint_score": joint_prob,
                "conf": conf,
                "plant_prob": prob_p * 100.0,
                "disease_prob": prob_d * 100.0,
                "plant_idx": p_idx,
                "disease_idx": d_idx
            })

        # Sort descending by joint likelihood score
        pair_scores.sort(key=lambda x: x["joint_score"], reverse=True)

        top1_entry = pair_scores[0]
        top1_conf = round(float(top1_entry["conf"]), 2)

        # 4. Extract Top-3 Predictions with Differential Advisory Metadata
        top_3_predictions = []
        for entry in pair_scores[:3]:
            c_info = self._match_advisory(entry, disease_info)
            crop_name = c_info.get("crop", entry["crop"])
            disease_name = c_info.get("disease", entry["disease"])
            top_3_predictions.append({
                "raw_class": entry["raw_class"],
                "crop": crop_name,
                "disease": disease_name,
                "confidence": round(float(entry["conf"]), 2)
            })

        # 5. Format Top-1 Result & Clinical Treatment Prescription
        top1_info = self._match_advisory(top1_entry, disease_info)
        crop_name = top1_info.get("crop", top1_entry["crop"])
        disease_name = top1_info.get("disease", top1_entry["disease"])
        is_healthy = ("healthy" in top1_entry["disease_slug"].lower()) or top1_info.get("is_healthy", False)

        return {
            "success": True,
            "raw_class": top1_entry["raw_class"],
            "crop": crop_name,
            "disease": disease_name,
            "confidence": top1_conf,
            "is_healthy": is_healthy,
            "is_background": False,
            "is_uncertain": top1_conf < 40.0,
            "top_3_predictions": top_3_predictions,
            "advisory": {
                "cause": top1_info.get("cause", "Pathogen infection identified."),
                "symptoms": top1_info.get("symptoms", "Visible foliar lesions or discoloration."),
                "organic_treatment": top1_info.get("organic_treatment", top1_info.get("treatment", "Apply recommended cultural and biological practices.")),
                "chemical_treatment": top1_info.get("chemical_treatment", "Apply recommended protective fungicides/bactericides according to IPM thresholds."),
                "prevention": top1_info.get("prevention", "Maintain balanced crop nutrition and sanitation."),
                "pesticides": top1_info.get("pesticides", []),
                "fertilizers": top1_info.get("fertilizers", [])
            }
        }


# Global singleton
engine = None

def get_inference_engine(checkpoint_path: Optional[str] = None, assets_dir: str = "models_assets") -> DPDInferenceEngine:
    global engine
    if engine is None:
        engine = DPDInferenceEngine(checkpoint_path=checkpoint_path, assets_dir=assets_dir)
    return engine
