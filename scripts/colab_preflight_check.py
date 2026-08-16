import os
import sys
import glob
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import timm

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

def run_preflight_check(dataset_dir=None):
    print("=" * 70)
    print(" GOOGLE COLAB PREFLIGHT CHECK — 72-CLASS DPD ViT TRAINING ")
    print("=" * 70)

    # 1. GPU Verification
    print("\n--- 1. GPU Verification ---")
    cuda_avail = torch.cuda.is_available()
    print(f"CUDA Available: {cuda_avail}")
    if cuda_avail:
        device_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        print(f"GPU Device Name: {device_name}")
        print(f"GPU VRAM: {vram_gb:.2f} GB")
        device = torch.device("cuda")
    else:
        print("WARNING: CUDA is NOT available. Running on CPU.")
        device = torch.device("cpu")

    # 2. Verify 72 Class Names
    print("\n--- 2. Class Names Verification ---")
    class_names_path = os.path.join("models_assets", "class_names.json")
    if not os.path.exists(class_names_path):
        print(f"ERROR: '{class_names_path}' not found!")
        sys.exit(1)
    
    with open(class_names_path, 'r', encoding='utf-8') as f:
        class_names = json.load(f)

    print(f"Loaded class names count: {len(class_names)} (Expected: 72)")
    assert len(class_names) == 72, f"Expected 72 classes, found {len(class_names)}"
    print(f"First 3 classes: {class_names[:3]}")
    print(f"Last 3 classes: {class_names[-3:]}")

    # 3. Verify Dataset Availability & Distribution
    print("\n--- 3. Dataset Availability Verification ---")
    resolved_dir = resolve_dataset_dir(dataset_dir)
    print(f"Checking Dataset Directory: '{resolved_dir}'")
    if not os.path.exists(resolved_dir):
        print(f"ERROR: Dataset directory '{resolved_dir}' not found!")
        sys.exit(1)

    class_dirs = [d for d in os.listdir(resolved_dir) if os.path.isdir(os.path.join(resolved_dir, d))]
    print(f"Found {len(class_dirs)} class directories in '{resolved_dir}'.")
    
    total_imgs = 0
    populated_classes = 0
    for c_name in class_names:
        c_path = os.path.join(resolved_dir, c_name)
        if os.path.exists(c_path):
            n_imgs = len(glob.glob(os.path.join(c_path, "*.*")))
            total_imgs += n_imgs
            if n_imgs > 0:
                populated_classes += 1

    print(f"Total Physical Images Available: {total_imgs:,}")
    print(f"Populated Classes: {populated_classes}/72")
    assert populated_classes == 72, f"Expected 72 populated classes, found {populated_classes}"

    # 4. Check DPD Pretrained Checkpoint
    print("\n--- 4. DPD Pretrained Checkpoint Verification ---")
    dpd_ckpt_path = os.path.join("dpd", "DPD_pretrained_weight.pth")
    if not os.path.exists(dpd_ckpt_path):
        print(f"ERROR: DPD pretrained checkpoint '{dpd_ckpt_path}' not found!")
        sys.exit(1)

    file_size_mb = os.path.getsize(dpd_ckpt_path) / (1024 * 1024)
    print(f"DPD Checkpoint File Size: {file_size_mb:.2f} MB")
    
    # Load DPD weights and inspect backbone state
    dpd_ckpt = torch.load(dpd_ckpt_path, map_location="cpu")
    backbone_keys = [k for k in dpd_ckpt.keys() if k.startswith("model.") and not k.startswith("model.head.")]
    print(f"Extracted {len(backbone_keys)} ViT-Base backbone tensors.")
    assert len(backbone_keys) > 100, "Incomplete backbone checkpoint!"

    # 5. Model Instantiation & GPU Forward Pass Verification
    print("\n--- 5. Model Instantiation & GPU Forward Pass ---")
    model = timm.create_model("vit_base_patch16_224", pretrained=False, num_classes=72, drop_rate=0.3)
    
    # Load backbone
    backbone_state = {k[6:]: v for k, v in dpd_ckpt.items() if k.startswith("model.") and not k.startswith("model.head.")}
    load_res = model.load_state_dict(backbone_state, strict=False)
    
    assert set(load_res.missing_keys) == {"head.weight", "head.bias"}, f"Unexpected missing keys: {load_res.missing_keys}"
    assert len(load_res.unexpected_keys) == 0, f"Unexpected extra keys: {load_res.unexpected_keys}"
    print(">> Backbone weight loading 100% CLEAN!")

    model.to(device)
    model.eval()

    # Create dummy batch on GPU
    dummy_input = torch.randn(4, 3, 224, 224, device=device)
    with torch.no_grad():
        logits = model(dummy_input)
        probs = F.softmax(logits, dim=-1)

    print(f"Forward Pass Output Shape: {list(logits.shape)} (Expected: [4, 72])")
    assert list(logits.shape) == [4, 72], f"Invalid output shape: {list(logits.shape)}"

    prob_sums = probs.sum(dim=-1).cpu().numpy()
    for idx, s in enumerate(prob_sums):
        assert abs(s - 1.0) < 1e-4, f"Sample {idx} probability sum {s} != 1.0"
    print(">> GPU Forward pass & Softmax normalization VERIFIED SUCCESSFUL!")

    print("\n=" * 70)
    print(" PREFLIGHT CHECK PASSED 100% — READY FOR COLAB GPU TRAINING ")
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-dir', type=str, default=None, help="Dataset directory path")
    args = parser.parse_args()
    run_preflight_check(dataset_dir=args.dataset_dir)
