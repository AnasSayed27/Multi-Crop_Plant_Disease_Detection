"""
======================================================================
 EVALUATION SCRIPT: 10 MANUAL REAL-WORLD TEST IMAGES (MODEL A vs B)
======================================================================
"""

import os
import sys
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import pandas as pd
import timm

# Ground Truth Mapping for the 10 manual test images
GROUND_TRUTH = {
    'Apple_blackRot_1.webp': ('apple', 'black_rot', 0, 3, 3, 'Apple___Black_rot'),
    'Apple_blackRot_2.jpg': ('apple', 'black_rot', 0, 3, 3, 'Apple___Black_rot'),
    'Corn_commonRust_1.jpg': ('corn', 'common_rust', 21, 93, 163, 'Corn___Common_rust'),
    'Corn_commonRust_2.jpg': ('corn', 'common_rust', 21, 93, 163, 'Corn___Common_rust'),
    'Potato_Early-Blight-1.jpg': ('potato', 'early_blight', 40, 55, 240, 'Potato___Early_blight'),
    'Potato_Early-Blight-2.jpg': ('potato', 'early_blight', 40, 55, 240, 'Potato___Early_blight'),
    'Tomato_earlyBlight_1.webp': ('tomato', 'early_blight', 51, 55, 303, 'Tomato___Early_blight'),
    'Tomato_earlyBlight_2.webp': ('tomato', 'early_blight', 51, 55, 303, 'Tomato___Early_blight'),
    'peach_Bacterialspot_1.webp': ('peach', 'bacterial_spot', 36, 33, 216, 'Peach___Bacterial_spot'),
    'peach_Bacterialspot_2.webp': ('peach', 'bacterial_spot', 36, 33, 216, 'Peach___Bacterial_spot')
}

# DPD 38 Supported Pairs for Top-3 lookup
PV_TO_DPD = {
    (0, 15): 'Apple___Apple_scab',
    (0, 3): 'Apple___Black_rot',
    (0, 5): 'Apple___Cedar_apple_rust',
    (0, 9): 'Apple___healthy',
    (7, 9): 'Blueberry___healthy',
    (16, 14): 'Cherry___Powdery_mildew',
    (16, 9): 'Cherry___healthy',
    (21, 70): 'Corn___Cercospora_leaf_spot Gray_leaf_spot',
    (21, 93): 'Corn___Common_rust',
    (21, 74): 'Corn___Northern_Leaf_Blight',
    (21, 9): 'Corn___healthy',
    (27, 3): 'Grape___Black_rot',
    (27, 88): 'Grape___Esca_(Black_Measles)',
    (27, 72): 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    (27, 9): 'Grape___healthy',
    (18, 61): 'Orange___Haunglongbing_(Citrus_greening)',
    (36, 33): 'Peach___Bacterial_spot',
    (36, 9): 'Peach___healthy',
    (5, 33): 'Pepper,_bell___Bacterial_spot',
    (5, 9): 'Pepper,_bell___healthy',
    (40, 55): 'Potato___Early_blight',
    (40, 139): 'Potato___Late_blight',
    (40, 9): 'Potato___healthy',
    (42, 9): 'Raspberry___healthy',
    (44, 9): 'Soybean___healthy',
    (45, 14): 'Squash___Powdery_mildew',
    (46, 40): 'Strawberry___Leaf_scorch',
    (46, 9): 'Strawberry___healthy',
    (51, 33): 'Tomato___Bacterial_spot',
    (51, 55): 'Tomato___Early_blight',
    (51, 139): 'Tomato___Late_blight',
    (51, 163): 'Tomato___Leaf_Mold',
    (51, 165): 'Tomato___Septoria_leaf_spot',
    (51, 68): 'Tomato___Spider_mites Two-spotted_spider_mite',
    (51, 82): 'Tomato___Target_Spot',
    (51, 167): 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    (51, 13): 'Tomato___Tomato_mosaic_virus',
    (51, 9): 'Tomato___healthy'
}

# Plant and Disease names dictionaries from DPD CSV
train = pd.read_csv('dpd/csv/default/train.csv', encoding='latin1', header=None) if os.path.exists('dpd/csv/default/train.csv') else None
if train is not None:
    PLANT_NAMES = dict(train[[1, 4]].drop_duplicates().values)
    DISEASE_NAMES = dict(train[[2, 5]].drop_duplicates().values)
else:
    PLANT_NAMES = {}
    DISEASE_NAMES = {}

class DPDViTDualHead(nn.Module):
    def __init__(self, num_plants=55, num_diseases=175):
        super().__init__()
        self.model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=0)
        self.linear_plant = nn.Linear(768, num_plants)
        self.linear_disease = nn.Linear(768, num_diseases)

    def forward(self, x):
        feat = self.model(x)
        return self.linear_plant(feat), self.linear_disease(feat)

def evaluate_images(images_dir, model_a_path, model_b_path=None):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("=" * 80)
    print(" 10 MANUAL REAL-WORLD IMAGES BENCHMARK EVALUATION")
    print(f" Execution Device: {device}")
    print("=" * 80)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # 1. Load Model A
    print(f"\nLoading Model A from: '{model_a_path}'...")
    model_a = DPDViTDualHead().to(device)
    model_a.load_state_dict(torch.load(model_a_path, map_location=device), strict=False)
    model_a.eval()

    # 2. Load Model B (if available)
    model_b = None
    if model_b_path and os.path.exists(model_b_path):
        print(f"Loading Model B from: '{model_b_path}'...")
        model_b = DPDViTDualHead().to(device)
        model_b.load_state_dict(torch.load(model_b_path, map_location=device), strict=False)
        model_b.eval()
    else:
        print("Model B checkpoint not found (evaluating Model A only).")

    results = []
    files = sorted([f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])

    correct_a = 0
    correct_b = 0
    top3_a = 0
    top3_b = 0
    total = len(files)

    for f in files:
        img_path = os.path.join(images_dir, f)
        img = Image.open(img_path).convert('RGB')
        t_img = transform(img).unsqueeze(0).to(device)

        gt_info = GROUND_TRUTH.get(f, ("Unknown", "Unknown", -1, -1, -1, "Unknown"))
        gt_plant_name, gt_disease_name, gt_p_id, gt_d_id, gt_pair_id, gt_pv_cls = gt_info

        # Inference Model A
        with torch.no_grad():
            p_logits_a, d_logits_a = model_a(t_img)
            p_probs_a = F.softmax(p_logits_a, dim=-1)
            d_probs_a = F.softmax(d_logits_a, dim=-1)

            pred_p_a = p_probs_a.argmax(dim=-1).item()
            pred_d_a = d_probs_a.argmax(dim=-1).item()
            conf_a = (p_probs_a[0, pred_p_a].item() + d_probs_a[0, pred_d_a].item()) / 2.0

            pred_pv_a = PV_TO_DPD.get((pred_p_a, pred_d_a), f"{PLANT_NAMES.get(pred_p_a, pred_p_a)}_{DISEASE_NAMES.get(pred_d_a, pred_d_a)}")
            hit_a = (pred_p_a == gt_p_id and pred_d_a == gt_d_id)
            if hit_a:
                correct_a += 1

            # Top-3 Model A
            scores_a = [(p_probs_a[0, p].item() * d_probs_a[0, d].item(), (p, d)) for (p, d) in PV_TO_DPD.keys()]
            scores_a.sort(key=lambda x: x[0], reverse=True)
            top3_pairs_a = [x[1] for x in scores_a[:3]]
            hit3_a = (gt_p_id, gt_d_id) in top3_pairs_a
            if hit3_a:
                top3_a += 1

        # Inference Model B
        pred_pv_b = "N/A"
        conf_b = 0.0
        hit_b = False
        hit3_b = False

        if model_b:
            with torch.no_grad():
                p_logits_b, d_logits_b = model_b(t_img)
                p_probs_b = F.softmax(p_logits_b, dim=-1)
                d_probs_b = F.softmax(d_logits_b, dim=-1)

                pred_p_b = p_probs_b.argmax(dim=-1).item()
                pred_d_b = d_probs_b.argmax(dim=-1).item()
                conf_b = (p_probs_b[0, pred_p_b].item() + d_probs_b[0, pred_d_b].item()) / 2.0

                pred_pv_b = PV_TO_DPD.get((pred_p_b, pred_d_b), f"{PLANT_NAMES.get(pred_p_b, pred_p_b)}_{DISEASE_NAMES.get(pred_d_b, pred_d_b)}")
                hit_b = (pred_p_b == gt_p_id and pred_d_b == gt_d_id)
                if hit_b:
                    correct_b += 1

                # Top-3 Model B
                scores_b = [(p_probs_b[0, p].item() * d_probs_b[0, d].item(), (p, d)) for (p, d) in PV_TO_DPD.keys()]
                scores_b.sort(key=lambda x: x[0], reverse=True)
                top3_pairs_b = [x[1] for x in scores_b[:3]]
                hit3_b = (gt_p_id, gt_d_id) in top3_pairs_b
                if hit3_b:
                    top3_b += 1

        results.append({
            'filename': f,
            'ground_truth': gt_pv_cls,
            'model_a_pred': pred_pv_a,
            'model_a_conf': conf_a,
            'model_a_hit': hit_a,
            'model_a_top3': hit3_a,
            'model_b_pred': pred_pv_b,
            'model_b_conf': conf_b,
            'model_b_hit': hit_b,
            'model_b_top3': hit3_b,
        })

    # Print results
    print("\n" + "=" * 110)
    print(f"{'Image Filename':<28} | {'Ground Truth':<25} | {'Model A Pred (Conf)':<30} | {'Model B Pred (Conf)':<30}")
    print("-" * 110)
    for r in results:
        mark_a = "✅" if r['model_a_hit'] else ("🟡(T3)" if r['model_a_top3'] else "❌")
        mark_b = "✅" if r['model_b_hit'] else ("🟡(T3)" if r['model_b_top3'] else "❌")
        
        pred_a_str = f"{mark_a} {r['model_a_pred'][:18]} ({r['model_a_conf']*100:.1f}%)"
        pred_b_str = f"{mark_b} {r['model_b_pred'][:18]} ({r['model_b_conf']*100:.1f}%)" if model_b else "N/A"
        print(f"{r['filename']:<28} | {r['ground_truth']:<25} | {pred_a_str:<30} | {pred_b_str:<30}")

    print("=" * 110)
    print(f"\n--- SUMMARY METRICS ON 10 MANUAL TEST IMAGES ---")
    print(f"Model A Top-1 Accuracy: {correct_a}/{total} ({correct_a/total*100:.1f}%) | Top-3 Accuracy: {top3_a}/{total} ({top3_a/total*100:.1f}%)")
    if model_b:
        print(f"Model B Top-1 Accuracy: {correct_b}/{total} ({correct_b/total*100:.1f}%) | Top-3 Accuracy: {top3_b}/{total} ({top3_b/total*100:.1f}%)")

if __name__ == '__main__':
    images_dir = sys.argv[1] if len(sys.argv) > 1 else 'test_real_images'
    model_a = sys.argv[2] if len(sys.argv) > 2 else ('dpd/DPD_pretrained_weight.pth' if os.path.exists('dpd/DPD_pretrained_weight.pth') else 'DPD_pretrained_weight.pth')
    model_b = sys.argv[3] if len(sys.argv) > 3 else ('models_assets/model_b_partial_adapted.pth' if os.path.exists('models_assets/model_b_partial_adapted.pth') else None)
    
    evaluate_images(images_dir, model_a, model_b)
