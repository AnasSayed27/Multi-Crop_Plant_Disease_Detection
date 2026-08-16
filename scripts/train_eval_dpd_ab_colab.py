"""
======================================================================
 GOOGLE COLAB: DPD ViT MODEL A vs MODEL B COMPARATIVE EXPERIMENT
======================================================================
- Model A: Untouched Original DPD ViT (55-Plant + 175-Disease Heads, Zero-Shot)
- Model B: Partial Head Adaptation (ViT Backbone Frozen, ONLY 14 Plant Rows
           and 21 Disease Rows updated on genuine PlantVillage data; all other
           41 plant and 154 disease rows remain 100% bitwise identical).
- Benchmark: Pretraining-Leakage-Free Held-Out Test Set (8,226 images)
             + Real-World Out-of-Domain Benchmark (plantdoc_realworld, 236 images)
======================================================================
"""

import os
import sys
import glob
import json
import random
import argparse
import numpy as np
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import timm
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

# ---------------------------------------------------------------------------
# REPRODUCIBILITY SEED
# ---------------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

# ---------------------------------------------------------------------------
# PATH RESOLUTION HELPERS
# ---------------------------------------------------------------------------
def resolve_dataset_dir(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    candidates = [
        '/content/Plant_leave_diseases_dataset_without_augmentation',
        '/content/Dataset/Plant_leave_diseases_dataset_without_augmentation',
        'Dataset/Plant_leave_diseases_dataset_without_augmentation',
        'Plant_leave_diseases_dataset_without_augmentation'
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]

def resolve_realworld_dir(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    candidates = [
        '/content/plantdoc_realworld',
        '/content/drive/MyDrive/Potato_disease/plantdoc_realworld',
        'plantdoc_realworld',
        'Dataset/plantdoc_realworld'
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def resolve_checkpoint_path(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    candidates = [
        'dpd/DPD_pretrained_weight.pth',
        'DPD_pretrained_weight.pth',
        '/content/drive/MyDrive/Potato_disease/DPD_pretrained_weight.pth',
        '/content/DPD_pretrained_weight.pth'
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return 'DPD_pretrained_weight.pth'

# ---------------------------------------------------------------------------
# PLANTVILLAGE TO DPD 55/175 TAXONOMY MAPPING
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

ACTIVE_PLANTS = sorted(list(set(v[2] for v in PV_TO_DPD_MAPPING.values())))
ACTIVE_DISEASES = sorted(list(set(v[3] for v in PV_TO_DPD_MAPPING.values())))
ACTIVE_PAIRS = sorted(list(set(v[4] for v in PV_TO_DPD_MAPPING.values())))

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
# DATASET CLASS
# ---------------------------------------------------------------------------
class PlantDiseaseDataset(Dataset):
    def __init__(self, samples, transform=None):
        self.samples = samples
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, plant_idx, disease_idx, pair_idx, pv_cls_name = self.samples[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, plant_idx, disease_idx, pair_idx, pv_cls_name

# ---------------------------------------------------------------------------
# EVALUATION & METRICS ENGINE
# ---------------------------------------------------------------------------
def compute_ece(confidences, predictions, labels, n_bins=15):
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(predictions[in_bin] == labels[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
    return float(ece)

def evaluate_model(model, dataloader, device, dataset_name="Test"):
    model.eval()
    all_plant_preds = []
    all_plant_trues = []
    all_disease_preds = []
    all_disease_trues = []
    all_pair_preds = []
    all_pair_trues = []
    all_top3_hits = []
    all_confidences = []
    all_pv_classes = []

    # Map (plant_id, disease_id) to pair_id lookup
    pair_lookup = {(v[2], v[3]): v[4] for v in PV_TO_DPD_MAPPING.values()}

    with torch.no_grad():
        for images, plant_trues, disease_trues, pair_trues, pv_names in dataloader:
            images = images.to(device)
            p_logits, d_logits = model(images)

            p_probs = F.softmax(p_logits, dim=-1)
            d_probs = F.softmax(d_logits, dim=-1)

            # Top-1 predictions
            p_conf, p_pred = torch.max(p_probs, dim=-1)
            d_conf, d_pred = torch.max(d_probs, dim=-1)

            # Pair probability = p_prob * d_prob
            # Compute composite pair probability for supported pairs
            for b in range(images.size(0)):
                p_p = p_pred[b].item()
                d_p = d_pred[b].item()
                p_t = plant_trues[b].item()
                d_t = disease_trues[b].item()
                pair_t = pair_trues[b].item()
                pv_name = pv_names[b]

                all_plant_preds.append(p_p)
                all_plant_trues.append(p_t)
                all_disease_preds.append(d_p)
                all_disease_trues.append(d_t)
                all_pair_trues.append(pair_t)
                all_pv_classes.append(pv_name)

                # Composite Top-1 Pair
                pred_pair = pair_lookup.get((p_p, d_p), -1)
                all_pair_preds.append(pred_pair)

                # Combined confidence
                comb_conf = (p_conf[b].item() + d_conf[b].item()) / 2.0
                all_confidences.append(comb_conf)

                # Top-3 Pair Accuracy
                # Score all 38 supported pairs
                pair_scores = []
                for (pl_id, dis_id), pr_id in pair_lookup.items():
                    score = p_probs[b, pl_id].item() * d_probs[b, dis_id].item()
                    pair_scores.append((score, pr_id))
                pair_scores.sort(key=lambda x: x[0], reverse=True)
                top3_pairs = [x[1] for x in pair_scores[:3]]
                all_top3_hits.append(1 if pair_t in top3_pairs else 0)

    # Convert to numpy
    plant_acc = accuracy_score(all_plant_trues, all_plant_preds)
    disease_acc = accuracy_score(all_disease_trues, all_disease_preds)
    pair_acc = accuracy_score(all_pair_trues, all_pair_preds)
    top3_acc = np.mean(all_top3_hits)

    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(
        all_pair_trues, all_pair_preds, average='macro', zero_division=0
    )
    prec_wt, rec_wt, f1_wt, _ = precision_recall_fscore_support(
        all_pair_trues, all_pair_preds, average='weighted', zero_division=0
    )

    ece = compute_ece(np.array(all_confidences), np.array(all_pair_preds), np.array(all_pair_trues))
    mean_conf = float(np.mean(all_confidences))

    # Per-class sensitivity table
    df_eval = pd.DataFrame({
        'pv_class': all_pv_classes,
        'true_pair': all_pair_trues,
        'pred_pair': all_pair_preds
    })
    per_class_results = {}
    for cls_name in sorted(list(set(all_pv_classes))):
        sub = df_eval[df_eval['pv_class'] == cls_name]
        correct = (sub['true_pair'] == sub['pred_pair']).sum()
        total = len(sub)
        per_class_results[cls_name] = {
            'total_samples': total,
            'correct': int(correct),
            'accuracy': float(correct / total) if total > 0 else 0.0
        }

    return {
        'dataset': dataset_name,
        'total_samples': len(all_pair_trues),
        'crop_accuracy': float(plant_acc),
        'disease_accuracy': float(disease_acc),
        'pair_top1_accuracy': float(pair_acc),
        'pair_top3_accuracy': float(top3_acc),
        'precision_macro': float(prec_macro),
        'recall_macro': float(rec_macro),
        'f1_macro': float(f1_macro),
        'f1_weighted': float(f1_wt),
        'mean_confidence': mean_conf,
        'expected_calibration_error': ece,
        'per_class_results': per_class_results
    }

# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------
def run_experiment(dataset_dir=None, realworld_dir=None, ckpt_path=None, epochs=10, batch_size=32):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("=" * 70)
    print(" DPD ViT A/B COMPARATIVE EXPERIMENT PIPELINE")
    print(f" Execution Device: {device}")
    if device.type == 'cuda':
        print(f" GPU Name: {torch.cuda.get_device_name(0)}")
    print("=" * 70)

    dataset_path = resolve_dataset_dir(dataset_dir)
    realworld_path = resolve_realworld_dir(realworld_dir)
    checkpoint_path = resolve_checkpoint_path(ckpt_path)

    print(f"Resolved Dataset Directory:   '{dataset_path}'")
    print(f"Resolved RealWorld Benchmark: '{realworld_path}'")
    print(f"Resolved DPD Checkpoint:      '{checkpoint_path}'")

    # 1. Build Pretraining-Leakage-Free Partitions across 38 PV classes
    train_samples = []
    val_samples = []
    test_samples = []

    for pv_cls, (p_name, d_name, p_idx, d_idx, pair_idx) in PV_TO_DPD_MAPPING.items():
        cls_dir = os.path.join(dataset_path, pv_cls)
        if not os.path.exists(cls_dir):
            continue
        all_imgs = sorted([
            os.path.join(cls_dir, f) for f in os.listdir(cls_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('synth_')
        ])
        n = len(all_imgs)
        if n == 0:
            continue

        # Deterministic 70/15/15 partition
        n_test = int(0.15 * n)
        n_val = int(0.15 * n)
        n_train = n - n_val - n_test

        tr_imgs = all_imgs[:n_train]
        va_imgs = all_imgs[n_train:n_train + n_val]
        te_imgs = all_imgs[n_train + n_val:]

        for img in tr_imgs:
            train_samples.append((img, p_idx, d_idx, pair_idx, pv_cls))
        for img in va_imgs:
            val_samples.append((img, p_idx, d_idx, pair_idx, pv_cls))
        for img in te_imgs:
            test_samples.append((img, p_idx, d_idx, pair_idx, pv_cls))

    print("\n--- Partitions Created ---")
    print(f"  Train Samples (Model B Adaptation): {len(train_samples):,}")
    print(f"  Val Samples (Validation Tuning):    {len(val_samples):,}")
    print(f"  Test Samples (Leak-Free Test Set):  {len(test_samples):,}")

    # RealWorld Benchmark Samples
    rw_samples = []
    if realworld_path and os.path.exists(realworld_path):
        for pv_cls, (p_name, d_name, p_idx, d_idx, pair_idx) in PV_TO_DPD_MAPPING.items():
            rw_cls_dir = os.path.join(realworld_path, pv_cls)
            if os.path.exists(rw_cls_dir):
                for f in os.listdir(rw_cls_dir):
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        rw_samples.append((os.path.join(rw_cls_dir, f), p_idx, d_idx, pair_idx, pv_cls))
        print(f"  RealWorld Out-of-Domain Samples:    {len(rw_samples):,}")

    # Transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    num_workers = 2 if torch.cuda.is_available() else 0
    pin_memory = torch.cuda.is_available()

    train_loader = DataLoader(PlantDiseaseDataset(train_samples, train_transform), batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)
    val_loader = DataLoader(PlantDiseaseDataset(val_samples, eval_transform), batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)
    test_loader = DataLoader(PlantDiseaseDataset(test_samples, eval_transform), batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)
    rw_loader = DataLoader(PlantDiseaseDataset(rw_samples, eval_transform), batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=pin_memory) if rw_samples else None

    # Load Base DPD Checkpoint
    ckpt = torch.load(checkpoint_path, map_location='cpu')

    # =======================================================================
    # STEP 1: MODEL A — UNTOUCHED ORIGINAL DPD (ZERO-SHOT)
    # =======================================================================
    print("\n" + "=" * 50)
    print(" EVALUATING MODEL A (ORIGINAL UNTOUCHED DPD ViT)")
    print("=" * 50)
    model_a = DPDViTDualHead(num_plants=55, num_diseases=175)
    model_a.load_state_dict(ckpt, strict=False)
    model_a = model_a.to(device)

    model_a_test_metrics = evaluate_model(model_a, test_loader, device, dataset_name="PlantVillage_HeldOut_Test")
    print(f"Model A Test Results:")
    print(f"  Crop Acc:     {model_a_test_metrics['crop_accuracy']*100:.2f}%")
    print(f"  Disease Acc:  {model_a_test_metrics['disease_accuracy']*100:.2f}%")
    print(f"  Pair Top-1:   {model_a_test_metrics['pair_top1_accuracy']*100:.2f}%")
    print(f"  Pair Top-3:   {model_a_test_metrics['pair_top3_accuracy']*100:.2f}%")
    print(f"  Macro F1:     {model_a_test_metrics['f1_macro']:.4f}")
    print(f"  ECE:          {model_a_test_metrics['expected_calibration_error']:.4f}")

    model_a_rw_metrics = None
    if rw_loader:
        model_a_rw_metrics = evaluate_model(model_a, rw_loader, device, dataset_name="PlantDoc_RealWorld")
        print(f"Model A RealWorld Results:")
        print(f"  Pair Top-1:   {model_a_rw_metrics['pair_top1_accuracy']*100:.2f}%")
        print(f"  Pair Top-3:   {model_a_rw_metrics['pair_top3_accuracy']*100:.2f}%")
        print(f"  Macro F1:     {model_a_rw_metrics['f1_macro']:.4f}")

    os.makedirs('models_assets', exist_ok=True)
    with open('models_assets/model_a_benchmark_metrics.json', 'w', encoding='utf-8') as f:
        json.dump({'test_metrics': model_a_test_metrics, 'realworld_metrics': model_a_rw_metrics}, f, indent=2)

    # Free Model A GPU memory
    del model_a
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # =======================================================================
    # STEP 2: MODEL B — PARTIAL HEAD ADAPTATION
    # =======================================================================
    print("\n" + "=" * 50)
    print(" TRAINING MODEL B (PARTIAL HEAD ADAPTATION)")
    print("=" * 50)
    model_b = DPDViTDualHead(num_plants=55, num_diseases=175)
    model_b.load_state_dict(ckpt, strict=False)

    # Original head copies for invariance check
    orig_p_w = ckpt['linear_plant.weight'].clone()
    orig_p_b = ckpt['linear_plant.bias'].clone()
    orig_d_w = ckpt['linear_disease.weight'].clone()
    orig_d_b = ckpt['linear_disease.bias'].clone()

    # Freeze entire ViT backbone
    for p in model_b.model.parameters():
        p.requires_grad = False

    model_b = model_b.to(device)

    # Active and inactive indices
    inactive_plants = [i for i in range(55) if i not in ACTIVE_PLANTS]
    inactive_diseases = [j for j in range(175) if j not in ACTIVE_DISEASES]

    optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, model_b.parameters()), lr=1e-3, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()
    scaler = torch.amp.GradScaler('cuda', enabled=torch.cuda.is_available())

    plant_mask = torch.zeros(55, dtype=torch.bool, device=device)
    plant_mask[ACTIVE_PLANTS] = True
    disease_mask = torch.zeros(175, dtype=torch.bool, device=device)
    disease_mask[ACTIVE_DISEASES] = True

    best_val_acc = 0.0
    best_weights = None

    for epoch in range(1, epochs + 1):
        model_b.train()
        running_loss = 0.0
        correct_p = 0
        correct_d = 0
        total = 0

        for images, p_trues, d_trues, _, _ in train_loader:
            images, p_trues, d_trues = images.to(device), p_trues.to(device), d_trues.to(device)
            optimizer.zero_grad()

            with torch.amp.autocast('cuda', enabled=torch.cuda.is_available()):
                p_out, d_out = model_b(images)
                loss = criterion(p_out, p_trues) + criterion(d_out, d_trues)

            scaler.scale(loss).backward()

            # Mask gradients for frozen rows
            model_b.linear_plant.weight.grad[~plant_mask] = 0.0
            model_b.linear_plant.bias.grad[~plant_mask] = 0.0
            model_b.linear_disease.weight.grad[~disease_mask] = 0.0
            model_b.linear_disease.bias.grad[~disease_mask] = 0.0

            scaler.step(optimizer)
            scaler.update()

            # Guarantee bit-for-bit invariance against weight decay
            with torch.no_grad():
                model_b.linear_plant.weight.data[inactive_plants] = orig_p_w[inactive_plants].to(device)
                model_b.linear_plant.bias.data[inactive_plants] = orig_p_b[inactive_plants].to(device)
                model_b.linear_disease.weight.data[inactive_diseases] = orig_d_w[inactive_diseases].to(device)
                model_b.linear_disease.bias.data[inactive_diseases] = orig_d_b[inactive_diseases].to(device)

            running_loss += loss.item() * images.size(0)
            correct_p += (p_out.argmax(dim=-1) == p_trues).sum().item()
            correct_d += (d_out.argmax(dim=-1) == d_trues).sum().item()
            total += images.size(0)

        train_p_acc = correct_p / total
        train_d_acc = correct_d / total
        train_loss = running_loss / total

        # Validation
        val_eval = evaluate_model(model_b, val_loader, device, dataset_name="Val")
        val_pair_acc = val_eval['pair_top1_accuracy']

        print(f"Epoch [{epoch:02d}/{epochs:02d}] - Loss: {train_loss:.4f} | Train Plant Acc: {train_p_acc*100:.2f}% | Train Dis Acc: {train_d_acc*100:.2f}% | Val Pair Top-1: {val_pair_acc*100:.2f}%")

        if val_pair_acc > best_val_acc:
            best_val_acc = val_pair_acc
            best_weights = {k: v.cpu().clone() for k, v in model_b.state_dict().items()}

    # Load best weights
    model_b.load_state_dict(best_weights)

    # Invariance verification
    p_w_diff = (model_b.linear_plant.weight.data.cpu()[inactive_plants] - orig_p_w[inactive_plants]).abs().max().item()
    p_b_diff = (model_b.linear_plant.bias.data.cpu()[inactive_plants] - orig_p_b[inactive_plants]).abs().max().item()
    d_w_diff = (model_b.linear_disease.weight.data.cpu()[inactive_diseases] - orig_d_w[inactive_diseases]).abs().max().item()
    d_b_diff = (model_b.linear_disease.bias.data.cpu()[inactive_diseases] - orig_d_b[inactive_diseases]).abs().max().item()

    print("\n--- Bitwise Invariance Verification on Model B ---")
    print(f"  Max Diff on 41 Frozen Plant Weights:   {p_w_diff:.10f}")
    print(f"  Max Diff on 41 Frozen Plant Biases:    {p_b_diff:.10f}")
    print(f"  Max Diff on 154 Frozen Disease Weights: {d_w_diff:.10f}")
    print(f"  Max Diff on 154 Frozen Disease Biases:  {d_b_diff:.10f}")

    assert p_w_diff == 0.0 and p_b_diff == 0.0, "Plant head frozen rows violated!"
    assert d_w_diff == 0.0 and d_b_diff == 0.0, "Disease head frozen rows violated!"
    print("  VERIFICATION RESULT: 100.00% BIT-FOR-BIT IDENTICAL!")

    # Save Model B adapted checkpoint
    torch.save(model_b.state_dict(), 'models_assets/model_b_partial_adapted.pth')
    print("Saved Model B checkpoint to 'models_assets/model_b_partial_adapted.pth'")

    # Evaluate Model B
    print("\n" + "=" * 50)
    print(" EVALUATING MODEL B ON BENCHMARK")
    print("=" * 50)
    model_b_test_metrics = evaluate_model(model_b, test_loader, device, dataset_name="PlantVillage_HeldOut_Test")
    print(f"Model B Test Results:")
    print(f"  Crop Acc:     {model_b_test_metrics['crop_accuracy']*100:.2f}%")
    print(f"  Disease Acc:  {model_b_test_metrics['disease_accuracy']*100:.2f}%")
    print(f"  Pair Top-1:   {model_b_test_metrics['pair_top1_accuracy']*100:.2f}%")
    print(f"  Pair Top-3:   {model_b_test_metrics['pair_top3_accuracy']*100:.2f}%")
    print(f"  Macro F1:     {model_b_test_metrics['f1_macro']:.4f}")
    print(f"  ECE:          {model_b_test_metrics['expected_calibration_error']:.4f}")

    model_b_rw_metrics = None
    if rw_loader:
        model_b_rw_metrics = evaluate_model(model_b, rw_loader, device, dataset_name="PlantDoc_RealWorld")
        print(f"Model B RealWorld Results:")
        print(f"  Pair Top-1:   {model_b_rw_metrics['pair_top1_accuracy']*100:.2f}%")
        print(f"  Pair Top-3:   {model_b_rw_metrics['pair_top3_accuracy']*100:.2f}%")
        print(f"  Macro F1:     {model_b_rw_metrics['f1_macro']:.4f}")

    with open('models_assets/model_b_benchmark_metrics.json', 'w', encoding='utf-8') as f:
        json.dump({'test_metrics': model_b_test_metrics, 'realworld_metrics': model_b_rw_metrics}, f, indent=2)

    # =======================================================================
    # STEP 3: COMPARATIVE REPORT EXPORT
    # =======================================================================
    comparison = {
        'model_a': {'test': model_a_test_metrics, 'realworld': model_a_rw_metrics},
        'model_b': {'test': model_b_test_metrics, 'realworld': model_b_rw_metrics}
    }
    with open('models_assets/ab_experiment_comparison.json', 'w', encoding='utf-8') as f:
        json.dump(comparison, f, indent=2)

    print("\n" + "=" * 70)
    print(" A/B EXPERIMENT COMPARATIVE RESULTS SUMMARY")
    print("=" * 70)
    print(f"{'Metric':<30} | {'Model A (Original DPD)':<22} | {'Model B (Partial Adapted)':<25}")
    print("-" * 85)
    print(f"{'Crop Accuracy':<30} | {model_a_test_metrics['crop_accuracy']*100:>20.2f}% | {model_b_test_metrics['crop_accuracy']*100:>23.2f}%")
    print(f"{'Disease Accuracy':<30} | {model_a_test_metrics['disease_accuracy']*100:>20.2f}% | {model_b_test_metrics['disease_accuracy']*100:>23.2f}%")
    print(f"{'Crop+Disease Pair Top-1':<30} | {model_a_test_metrics['pair_top1_accuracy']*100:>20.2f}% | {model_b_test_metrics['pair_top1_accuracy']*100:>23.2f}%")
    print(f"{'Crop+Disease Pair Top-3':<30} | {model_a_test_metrics['pair_top3_accuracy']*100:>20.2f}% | {model_b_test_metrics['pair_top3_accuracy']*100:>23.2f}%")
    print(f"{'Macro Precision':<30} | {model_a_test_metrics['precision_macro']:>21.4f} | {model_b_test_metrics['precision_macro']:>24.4f}")
    print(f"{'Macro Recall':<30} | {model_a_test_metrics['recall_macro']:>21.4f} | {model_b_test_metrics['recall_macro']:>24.4f}")
    print(f"{'Macro F1-Score':<30} | {model_a_test_metrics['f1_macro']:>21.4f} | {model_b_test_metrics['f1_macro']:>24.4f}")
    print(f"{'Weighted F1-Score':<30} | {model_a_test_metrics['f1_weighted']:>21.4f} | {model_b_test_metrics['f1_weighted']:>24.4f}")
    print(f"{'Mean Confidence':<30} | {model_a_test_metrics['mean_confidence']*100:>20.2f}% | {model_b_test_metrics['mean_confidence']*100:>23.2f}%")
    print(f"{'Expected Calibration Error (ECE)':<30} | {model_a_test_metrics['expected_calibration_error']:>21.4f} | {model_b_test_metrics['expected_calibration_error']:>24.4f}")

    if model_a_rw_metrics and model_b_rw_metrics:
        print("-" * 85)
        print(f"{'RealWorld Pair Top-1':<30} | {model_a_rw_metrics['pair_top1_accuracy']*100:>20.2f}% | {model_b_rw_metrics['pair_top1_accuracy']*100:>23.2f}%")
        print(f"{'RealWorld Pair Top-3':<30} | {model_a_rw_metrics['pair_top3_accuracy']*100:>20.2f}% | {model_b_rw_metrics['pair_top3_accuracy']*100:>23.2f}%")
        print(f"{'RealWorld Macro F1':<30} | {model_a_rw_metrics['f1_macro']:>21.4f} | {model_b_rw_metrics['f1_macro']:>24.4f}")
    print("=" * 85)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Model A vs Model B comparative experiment on Colab GPU")
    parser.add_argument('--dataset-dir', type=str, default=None, help='Path to PlantVillage dataset')
    parser.add_argument('--realworld-dir', type=str, default=None, help='Path to plantdoc_realworld dataset')
    parser.add_argument('--checkpoint', type=str, default=None, help='Path to DPD_pretrained_weight.pth')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs for Model B partial adaptation')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size for training/eval')
    args = parser.parse_args()

    run_experiment(
        dataset_dir=args.dataset_dir,
        realworld_dir=args.realworld_dir,
        ckpt_path=args.checkpoint,
        epochs=args.epochs,
        batch_size=args.batch_size
    )
