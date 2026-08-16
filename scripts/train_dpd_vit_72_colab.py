import os
import sys
import glob
import json
import time
import argparse
import numpy as np
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import timm
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix, accuracy_score

# ---------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------
SEED = 42
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 72
MODELS_ASSETS_DIR = "models_assets"
CLASS_NAMES_PATH = os.path.join(MODELS_ASSETS_DIR, "class_names.json")
DPD_CKPT_PATH = os.path.join("dpd", "DPD_pretrained_weight.pth")
INITIALIZED_CKPT_PATH = os.path.join(MODELS_ASSETS_DIR, "dpd_vit_72class_initialized.pth")
BEST_MODEL_PATH = os.path.join(MODELS_ASSETS_DIR, "dpd_vit_72class_best.pth")
HISTORY_SAVE_PATH = os.path.join(MODELS_ASSETS_DIR, "dpd_vit_72class_history.json")
METRICS_SAVE_PATH = os.path.join(MODELS_ASSETS_DIR, "dpd_vit_72class_test_metrics.json")

torch.manual_seed(SEED)
np.random.seed(SEED)
os.makedirs(MODELS_ASSETS_DIR, exist_ok=True)

# ---------------------------------------------------------
# Custom PyTorch Dataset Loader
# ---------------------------------------------------------
class MultiCropDataset(Dataset):
    def __init__(self, samples, transform=None):
        self.samples = samples
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item, label = self.samples[idx]
        if isinstance(item, str):
            try:
                img = Image.open(item).convert('RGB')
            except Exception as e:
                img = Image.new('RGB', IMAGE_SIZE, (0, 0, 0))
        else:
            img = item.convert('RGB')

        if self.transform:
            img = self.transform(img)

        return img, label

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def load_class_names():
    with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def resolve_dataset_dir(custom_path=None):
    if custom_path and os.path.exists(custom_path) and os.path.isdir(custom_path):
        return os.path.abspath(custom_path)
    
    candidates = [
        custom_path,
        "/content/Plant_leave_diseases_dataset_without_augmentation",
        "/content/Dataset/Plant_leave_diseases_dataset_without_augmentation",
        "/content/Dataset",
        "Dataset/Plant_leave_diseases_dataset_without_augmentation",
        "Plant_leave_diseases_dataset_without_augmentation",
        "Dataset",
        "../Dataset/Plant_leave_diseases_dataset_without_augmentation",
        "/content/drive/MyDrive/Potato_disease/Dataset/Plant_leave_diseases_dataset_without_augmentation",
        "/content/drive/My Drive/Potato_disease/Dataset/Plant_leave_diseases_dataset_without_augmentation",
    ]
    for p in candidates:
        if p and os.path.exists(p) and os.path.isdir(p):
            subdirs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]
            if len(subdirs) >= 10:
                return os.path.abspath(p)
    return os.path.abspath(custom_path or "Dataset/Plant_leave_diseases_dataset_without_augmentation")

def build_dataset_samples(dataset_dir=None, sanity_check=False):
    class_names = load_class_names()
    class_to_idx = {c: i for i, c in enumerate(class_names)}
    local_pv_dir = resolve_dataset_dir(dataset_dir)
    print(f"Resolved Dataset Directory: '{local_pv_dir}'")
    
    samples_by_class = {i: [] for i in range(len(class_names))}

    if os.path.exists(local_pv_dir):
        for dir_name in sorted(os.listdir(local_pv_dir)):
            full_d = os.path.join(local_pv_dir, dir_name)
            if not os.path.isdir(full_d) or dir_name not in class_to_idx:
                continue
            
            c_idx = class_to_idx[dir_name]
            files = sorted(glob.glob(os.path.join(full_d, "*.*")))
            samples_by_class[c_idx].extend([(f, c_idx) for f in files])
    else:
        print(f"ERROR: Dataset directory '{local_pv_dir}' does not exist!")

    train_samples = []
    val_samples = []
    test_samples = []

    for c_idx, files in samples_by_class.items():
        if len(files) == 0:
            continue
        
        n_files = len(files)
        rng = np.random.RandomState(SEED + c_idx)
        perm = rng.permutation(n_files)

        if sanity_check:
            n_tr = min(5, n_files)
            n_val = min(2, n_files - n_tr) if n_files > n_tr else 0
            n_te = min(2, n_files - n_tr - n_val) if n_files > (n_tr + n_val) else 0

            for i in perm[:n_tr]:
                train_samples.append(files[i])
            for i in perm[n_tr:n_tr + n_val]:
                val_samples.append(files[i])
            for i in perm[n_tr + n_val:n_tr + n_val + n_te]:
                test_samples.append(files[i])
        else:
            n_tr = int(n_files * 0.70)
            n_val = int(n_files * 0.15)
            
            for i in perm[:n_tr]:
                train_samples.append(files[i])
            for i in perm[n_tr:n_tr + n_val]:
                val_samples.append(files[i])
            for i in perm[n_tr + n_val:]:
                test_samples.append(files[i])

    print(f"Dataset Partitions Created:")
    print(f"  Train Samples: {len(train_samples):,} across {len(set(s[1] for s in train_samples))} unique classes")
    print(f"  Val Samples:   {len(val_samples):,} across {len(set(s[1] for s in val_samples))} unique classes")
    print(f"  Test Samples:  {len(test_samples):,} across {len(set(s[1] for s in test_samples))} unique classes")

    if len(train_samples) == 0:
        raise ValueError(
            f"No images found in dataset directory '{local_pv_dir}'!\n"
            f"Please verify where you unzipped the dataset in Colab.\n"
            f"Example: !python train_dpd_vit_72_colab.py --dataset-dir /content/Plant_leave_diseases_dataset_without_augmentation"
        )

    return train_samples, val_samples, test_samples, class_names

def compute_class_weights(train_samples, num_classes):
    counts = np.zeros(num_classes, dtype=np.float32)
    for _, label in train_samples:
        counts[label] += 1.0

    counts = np.maximum(counts, 1.0)
    total = np.sum(counts)
    weights = total / (num_classes * np.sqrt(counts))
    weights = weights / np.mean(weights)
    return torch.tensor(weights, dtype=torch.float32)

# ---------------------------------------------------------
# Training & Audit Pipeline (Google Colab Optimized)
# ---------------------------------------------------------
def train_pipeline(dataset_dir=None, sanity_check=False, epochs_stage1=5, epochs_stage2=15):
    print("=" * 70)
    print(" GOOGLE COLAB 72-CLASS DPD ViT TRAINING PIPELINE ")
    print("=" * 70)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Execution Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
        torch.backends.cudnn.benchmark = True

    # 1. Load Dataset Splits
    train_samples, val_samples, test_samples, class_names = build_dataset_samples(dataset_dir=dataset_dir, sanity_check=sanity_check)

    # 2. Preprocessing & Augmentation Transforms
    train_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_ds = MultiCropDataset(train_samples, transform=train_transform)
    val_ds = MultiCropDataset(val_samples, transform=val_transform)
    test_ds = MultiCropDataset(test_samples, transform=val_transform)

    num_workers = 2 if torch.cuda.is_available() else 0
    pin_memory = torch.cuda.is_available()

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)

    # 3. Class Weights & Loss Function
    class_weights = compute_class_weights(train_samples, NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)

    # 4. Instantiate ViT-Base & Load DPD Pretrained Backbone
    print(f"\n--- Instantiating ViT-Base Model & Loading DPD Backbone ---")
    model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=NUM_CLASSES, drop_rate=0.3)
    
    if os.path.exists(INITIALIZED_CKPT_PATH):
        ckpt = torch.load(INITIALIZED_CKPT_PATH, map_location='cpu')
        model.load_state_dict(ckpt['model_state_dict'])
        print(f"Successfully loaded initialized 72-class checkpoint from '{INITIALIZED_CKPT_PATH}'.")
    elif os.path.exists(DPD_CKPT_PATH):
        dpd_ckpt = torch.load(DPD_CKPT_PATH, map_location='cpu')
        backbone_state = {k[6:]: v for k, v in dpd_ckpt.items() if k.startswith("model.") and not k.startswith("model.head.")}
        model.load_state_dict(backbone_state, strict=False)
        print(f"Successfully loaded backbone weights from '{DPD_CKPT_PATH}'.")
    else:
        print("Warning: Neither initialized nor DPD checkpoint found. Model started from scratch.")

    model.to(device)
    scaler = torch.cuda.amp.GradScaler(enabled=torch.cuda.is_available())

    # ---------------------------------------------------------
    # Stage 1: Head Warmup (Backbone Frozen)
    # ---------------------------------------------------------
    print(f"\n==================================================")
    print(f" STAGE 1: HEAD WARMUP ({epochs_stage1} Epochs) ")
    print(f"==================================================")
    
    for name, param in model.named_parameters():
        param.requires_grad = name.startswith("head.")

    optimizer_stage1 = torch.optim.AdamW(model.head.parameters(), lr=1e-3, weight_decay=0.01)

    best_val_loss = float('inf')
    history = {"train_loss": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, epochs_stage1 + 1):
        model.train()
        running_loss = 0.0
        start_t = time.time()

        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer_stage1.zero_grad()

            with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                logits = model(imgs)
                loss = criterion(logits, labels)

            scaler.scale(loss).backward()
            scaler.step(optimizer_stage1)
            scaler.update()

            running_loss += loss.item() * imgs.size(0)

        epoch_train_loss = running_loss / len(train_ds)

        model.eval()
        val_loss = 0.0
        correct = 0

        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                    logits = model(imgs)
                    loss = criterion(logits, labels)
                val_loss += loss.item() * imgs.size(0)
                preds = torch.argmax(logits, dim=-1)
                correct += (preds == labels).sum().item()

        epoch_val_loss = val_loss / len(val_ds)
        epoch_val_acc = correct / len(val_ds)
        elapsed = time.time() - start_t

        history["train_loss"].append(epoch_train_loss)
        history["val_loss"].append(epoch_val_loss)
        history["val_acc"].append(epoch_val_acc)

        print(f"Stage 1 - Epoch [{epoch}/{epochs_stage1}] ({elapsed:.1f}s) - "
              f"Train Loss: {epoch_train_loss:.4f} | Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc*100:.2f}%")

        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            torch.save({"model_state_dict": model.state_dict(), "val_loss": best_val_loss}, BEST_MODEL_PATH)
            print(f"  -> Saved best model checkpoint to '{BEST_MODEL_PATH}'")

    # ---------------------------------------------------------
    # Stage 2: Discriminative Fine-Tuning
    # ---------------------------------------------------------
    print(f"\n==================================================")
    print(f" STAGE 2: DISCRIMINATIVE FINE-TUNING ({epochs_stage2} Epochs) ")
    print(f"==================================================")

    for name, param in model.named_parameters():
        param.requires_grad = any(f"blocks.{b}." in name for b in [8, 9, 10, 11]) or name.startswith("norm.") or name.startswith("head.")

    optimizer_stage2 = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=1e-4,
        weight_decay=0.05
    )

    for epoch in range(1, epochs_stage2 + 1):
        model.train()
        running_loss = 0.0
        start_t = time.time()

        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer_stage2.zero_grad()

            with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                logits = model(imgs)
                loss = criterion(logits, labels)

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer_stage2)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer_stage2)
            scaler.update()

            running_loss += loss.item() * imgs.size(0)

        epoch_train_loss = running_loss / len(train_ds)

        model.eval()
        val_loss = 0.0
        correct = 0

        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                    logits = model(imgs)
                    loss = criterion(logits, labels)
                val_loss += loss.item() * imgs.size(0)
                preds = torch.argmax(logits, dim=-1)
                correct += (preds == labels).sum().item()

        epoch_val_loss = val_loss / len(val_ds)
        epoch_val_acc = correct / len(val_ds)
        elapsed = time.time() - start_t

        history["train_loss"].append(epoch_train_loss)
        history["val_loss"].append(epoch_val_loss)
        history["val_acc"].append(epoch_val_acc)

        print(f"Stage 2 - Epoch [{epoch}/{epochs_stage2}] ({elapsed:.1f}s) - "
              f"Train Loss: {epoch_train_loss:.4f} | Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc*100:.2f}%")

        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            torch.save({"model_state_dict": model.state_dict(), "val_loss": best_val_loss}, BEST_MODEL_PATH)
            print(f"  -> Saved best model checkpoint to '{BEST_MODEL_PATH}'")

    with open(HISTORY_SAVE_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

    # ---------------------------------------------------------
    # Final Held-Out Test Evaluation
    # ---------------------------------------------------------
    print(f"\n==================================================")
    print(f" FINAL HELD-OUT TEST METRIC EVALUATION ")
    print(f"==================================================")
    
    if os.path.exists(BEST_MODEL_PATH):
        best_ckpt = torch.load(BEST_MODEL_PATH, map_location='cpu')
        model.load_state_dict(best_ckpt['model_state_dict'])
        print(f"Loaded best checkpoint from '{BEST_MODEL_PATH}' for test evaluation.")

    model.eval()
    all_preds = []
    all_targets = []
    top3_matches = 0
    total_samples = 0

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                logits = model(imgs) # [B, 72]
            
            preds = torch.argmax(logits, dim=-1)
            
            top3_indices = torch.topk(logits, k=min(3, logits.size(1)), dim=-1).indices # [B, 3]
            match_in_top3 = torch.any(top3_indices == labels.unsqueeze(1), dim=-1) # [B]
            top3_matches += match_in_top3.sum().item()
            total_samples += imgs.size(0)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)

    top1_acc = accuracy_score(all_targets, all_preds)
    top3_acc = top3_matches / total_samples
    
    precision, recall, f1_macro, _ = precision_recall_fscore_support(all_targets, all_preds, average='macro', zero_division=0)
    _, _, f1_weighted, _ = precision_recall_fscore_support(all_targets, all_preds, average='weighted', zero_division=0)
    cm = confusion_matrix(all_targets, all_preds).tolist()

    unique_preds, pred_counts = np.unique(all_preds, return_counts=True)
    unique_targets, target_counts = np.unique(all_targets, return_counts=True)

    print("\n--- FINAL TEST EVALUATION RESULTS ---")
    print(f"Total Test Samples:            {total_samples}")
    print(f"Unique Target Classes in Test: {len(unique_targets)}")
    print(f"Unique Predicted Classes:      {len(unique_preds)}")
    print(f"Top-1 Accuracy:                {top1_acc * 100:.2f}%")
    print(f"Top-3 Accuracy:                {top3_acc * 100:.2f}%")
    print(f"Macro Precision:               {precision:.4f}")
    print(f"Macro Recall:                  {recall:.4f}")
    print(f"Macro F1-Score:                {f1_macro:.4f}")
    print(f"Weighted F1-Score:             {f1_weighted:.4f}")

    metrics = {
        "top1_accuracy": float(top1_acc),
        "top3_accuracy": float(top3_acc),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "f1_macro": float(f1_macro),
        "f1_weighted": float(f1_weighted),
        "unique_predicted_classes": len(unique_preds),
        "confusion_matrix": cm
    }

    with open(METRICS_SAVE_PATH, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved final test metrics to '{METRICS_SAVE_PATH}'")
    print("==================================================")
    print(" COLAB TRAINING & EVALUATION COMPLETED SUCCESSFUL ")
    print("==================================================")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train 72-Class DPD ViT Model on Google Colab")
    parser.add_argument('--dataset-dir', type=str, default=None, help="Path to Plant_leave_diseases_dataset_without_augmentation folder")
    parser.add_argument('--sanity-check', action='store_true', help="Run 1-epoch sanity check on stratified subset")
    parser.add_argument('--epochs-stage1', type=int, default=5, help="Stage 1 warmup epochs")
    parser.add_argument('--epochs-stage2', type=int, default=15, help="Stage 2 fine-tuning epochs")
    args = parser.parse_args()

    train_pipeline(
        dataset_dir=args.dataset_dir,
        sanity_check=args.sanity_check,
        epochs_stage1=args.epochs_stage1,
        epochs_stage2=args.epochs_stage2
    )
