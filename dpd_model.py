"""
======================================================================
 PRODUCTION PYTORCH INFERENCE MODULE: MODEL B (DPD ViT-Base)
======================================================================
Dual-Head Vision Transformer Base for Multi-Crop Plant Pathology:
- Backbone: vit_base_patch16_224 (768-dim features)
- Plant Head: linear_plant (768 -> 55)
- Disease Head: linear_disease (768 -> 175)
- Supported Scope: 38 Valid Crop-Disease Pairs with Full Advisory Triage
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
# SUPPORTED 38 CROP-DISEASE PAIRS & INDEX MAPPING
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

# ---------------------------------------------------------------------------
# MODEL ARCHITECTURE
# ---------------------------------------------------------------------------
class DPDViTDualHead(nn.Module):
    def __init__(self, num_plants=55, num_diseases=175):
        super().__init__()
        self.model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=0)
        self.linear_plant = nn.Linear(768, num_plants)
        self.linear_disease = nn.Linear(768, num_diseases)

    def forward(self, x):
        feat = self.model(x)
        return self.linear_plant(feat), self.linear_disease(feat)

# ---------------------------------------------------------------------------
# PRODUCTION INFERENCE ENGINE
# ---------------------------------------------------------------------------
class DPDInferenceEngine:
    def __init__(self, checkpoint_path: Optional[str] = None, device: Optional[str] = None):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)

        self.model = DPDViTDualHead(num_plants=55, num_diseases=175).to(self.device)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        self.loaded = False
        self.checkpoint_path = self._resolve_checkpoint(checkpoint_path)
        self._load_weights()

    def _resolve_checkpoint(self, path: Optional[str]) -> str:
        if path and os.path.exists(path):
            return path
        candidates = [
            os.path.join("models_assets", "model_b_partial_adapted.pth"),
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
                ckpt = torch.load(self.checkpoint_path, map_location=self.device)
                self.model.load_state_dict(ckpt, strict=False)
                self.model.eval()
                self.loaded = True
                print(f"[DPD Engine] Successfully loaded model checkpoint from '{self.checkpoint_path}' on {self.device}.")
            except Exception as e:
                print(f"[DPD Engine] Error loading checkpoint '{self.checkpoint_path}': {e}")
        else:
            print(f"[DPD Engine] Checkpoint not found at '{self.checkpoint_path}'.")

    def predict(self, image: Image.Image, disease_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.loaded:
            raise RuntimeError("DPD Model checkpoint is not loaded.")

        if disease_info is None:
            disease_info = {}

        # 1. Image Preprocessing (Exact Colab Benchmark Pipeline)
        img_rgb = image.convert('RGB')
        tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)

        # 2. Forward Pass
        with torch.no_grad():
            p_logits, d_logits = self.model(tensor)
            p_probs = F.softmax(p_logits, dim=-1)[0]
            d_probs = F.softmax(d_logits, dim=-1)[0]

        # 3. Score all 38 Supported Pairs using Joint Likelihood
        pair_scores = []
        for pv_cls, (p_name, d_name, p_idx, d_idx, pair_idx) in ALL_SUPPORTED_PAIRS:
            prob_p = p_probs[p_idx].item()
            prob_d = d_probs[d_idx].item()
            # Joint geometric likelihood score
            joint_prob = (prob_p * prob_d)
            # Calibrated arithmetic mean confidence
            conf = ((prob_p + prob_d) / 2.0) * 100.0
            pair_scores.append({
                'raw_class': pv_cls,
                'joint_score': joint_prob,
                'conf': conf,
                'plant_prob': prob_p * 100.0,
                'disease_prob': prob_d * 100.0,
                'plant_idx': p_idx,
                'disease_idx': d_idx
            })

        # Sort by joint likelihood descending
        pair_scores.sort(key=lambda x: x['joint_score'], reverse=True)

        top1_entry = pair_scores[0]
        top1_raw_class = top1_entry['raw_class']
        top1_conf = round(float(top1_entry['conf']), 2)

        # 4. Extract Top-3 Predictions
        top_3_predictions = []
        for entry in pair_scores[:3]:
            raw_c = entry['raw_class']
            c_info = disease_info.get(raw_c, {})
            crop_name = c_info.get("crop", raw_c.split("___")[0].replace("_", " "))
            disease_name = c_info.get("disease", raw_c.split("___")[-1].replace("_", " "))
            top_3_predictions.append({
                "raw_class": raw_c,
                "crop": crop_name,
                "disease": disease_name,
                "confidence": round(float(entry['conf']), 2)
            })

        # 5. Format Top-1 Result
        c_info = disease_info.get(top1_raw_class, {})
        crop_name = c_info.get("crop", top1_raw_class.split("___")[0].replace("_", " "))
        disease_name = c_info.get("disease", top1_raw_class.split("___")[-1].replace("_", " "))
        is_healthy = ("healthy" in top1_raw_class.lower()) or c_info.get("is_healthy", False)

        return {
            "success": True,
            "raw_class": top1_raw_class,
            "crop": crop_name,
            "disease": disease_name,
            "confidence": top1_conf,
            "is_healthy": is_healthy,
            "is_background": False,
            "is_uncertain": top1_conf < 40.0,
            "top_3_predictions": top_3_predictions,
            "advisory": {
                "cause": c_info.get("cause", "Pathogen infection identified."),
                "symptoms": c_info.get("symptoms", "Visible foliar lesions or discoloration."),
                "organic_treatment": c_info.get("organic_treatment", c_info.get("treatment", "Apply recommended cultural and biological practices.")),
                "chemical_treatment": c_info.get("chemical_treatment", "Apply recommended protective fungicides/bactericides according to IPM thresholds."),
                "prevention": c_info.get("prevention", "Maintain balanced crop nutrition and sanitation."),
                "pesticides": c_info.get("pesticides", []),
                "fertilizers": c_info.get("fertilizers", [])
            }
        }

# Global singleton
engine = None

def get_inference_engine(checkpoint_path: Optional[str] = None) -> DPDInferenceEngine:
    global engine
    if engine is None:
        engine = DPDInferenceEngine(checkpoint_path=checkpoint_path)
    return engine
