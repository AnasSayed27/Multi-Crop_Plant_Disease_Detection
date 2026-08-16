import os
import sys
import shutil
import subprocess
from PIL import Image

DATASET_TARGET_DIR = "Potato_disease_dataset"
REPO_URL = "https://github.com/ai-agriculture-circuits-and-systems/plant_village.git"
CLONE_DIR = "temp_plantvillage_repo"

def find_class_root(search_dir):
    """Recursively searches for the directory containing class folders with images."""
    for root, dirs, files in os.walk(search_dir):
        # Check if current directory has multiple subdirectories with images
        subdirs_with_images = 0
        for d in dirs:
            subdir_path = os.path.join(root, d)
            if any(f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')) for f in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, f))):
                subdirs_with_images += 1
        if subdirs_with_images > 3:
            return root
    return search_dir

def download_plantvillage():
    print("=" * 60)
    print(" Step 0.1: Downloading Full 38-Class PlantVillage Dataset ")
    print(f" Source: {REPO_URL}")
    print("=" * 60)

    if os.path.exists(CLONE_DIR):
        print(f"Removing previous temporary folder '{CLONE_DIR}'...")
        shutil.rmtree(CLONE_DIR, ignore_errors=True)

    print(f"Cloning PlantVillage repository from '{REPO_URL}'...")
    cmd = ["git", "clone", "--depth", "1", REPO_URL, CLONE_DIR]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Git clone failed:", result.stderr)
        raise RuntimeError(f"Failed to clone PlantVillage dataset from '{REPO_URL}'.")
    print("Git clone completed successfully.")

    source_root = find_class_root(CLONE_DIR)
    print(f"Source class directory located at: '{source_root}'")
    
    os.makedirs(DATASET_TARGET_DIR, exist_ok=True)
    class_folders = [
        d for d in os.listdir(source_root) 
        if os.path.isdir(os.path.join(source_root, d)) and not d.startswith('.')
    ]
    print(f"Found {len(class_folders)} class folders in source repository.")


    for folder in class_folders:
        src_path = os.path.join(source_root, folder)
        dst_path = os.path.join(DATASET_TARGET_DIR, folder)
        if not os.path.exists(dst_path):
            shutil.copytree(src_path, dst_path)
            print(f"Copied class: {folder}")
        else:
            # Sync files if folder already exists
            src_files = os.listdir(src_path)
            dst_files = os.listdir(dst_path)
            if len(src_files) > len(dst_files):
                for f in src_files:
                    s_file = os.path.join(src_path, f)
                    d_file = os.path.join(dst_path, f)
                    if not os.path.exists(d_file) and os.path.isfile(s_file):
                        shutil.copy2(s_file, d_file)
                print(f"Synced class: {folder} ({len(src_files)} files)")

    print(f"All {len(class_folders)} classes populated in '{DATASET_TARGET_DIR}'.")

def audit_dataset():
    print("\n" + "=" * 60)
    print(" Step 0.2: Full Dataset Audit & Image Verification ")
    print("=" * 60)

    class_folders = sorted([
        d for d in os.listdir(DATASET_TARGET_DIR)
        if os.path.isdir(os.path.join(DATASET_TARGET_DIR, d))
    ])

    audit_results = []
    flagged_low_count = []
    total_valid_images = 0
    total_corrupt_images = 0

    print(f"Auditing {len(class_folders)} classes...\n")
    print(f"{'Index':<6} | {'Class Name':<45} | {'Valid':<8} | {'Corrupt':<8} | {'Flag/Status'}")
    print("-" * 80)

    for idx, class_name in enumerate(class_folders, 1):
        class_path = os.path.join(DATASET_TARGET_DIR, class_name)
        valid_cnt = 0
        corrupt_cnt = 0

        for file_name in os.listdir(class_path):
            file_path = os.path.join(class_path, file_name)
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                    valid_cnt += 1
                except Exception:
                    corrupt_cnt += 1

        total_valid_images += valid_cnt
        total_corrupt_images += corrupt_cnt

        status = "OK"
        if valid_cnt < 200:
            status = "FLAG: < 200 images"
            flagged_low_count.append((class_name, valid_cnt))

        print(f"{idx:<6} | {class_name:<45} | {valid_cnt:<8} | {corrupt_cnt:<8} | {status}")

        audit_results.append({
            "index": idx,
            "class_name": class_name,
            "valid_count": valid_cnt,
            "corrupt_count": corrupt_cnt,
            "status": status
        })

    print("-" * 80)
    print(f"Audit Summary:")
    print(f"  Total Classes Discovered: {len(class_folders)}")
    print(f"  Total Valid Images:       {total_valid_images}")
    print(f"  Total Corrupt Images:     {total_corrupt_images}")
    print(f"  Classes Flagged (< 200):  {len(flagged_low_count)}")
    if flagged_low_count:
        print("  Flagged Classes Details:")
        for name, cnt in flagged_low_count:
            print(f"    - {name}: {cnt} images")

    return audit_results, flagged_low_count

if __name__ == "__main__":
    download_plantvillage()
    audit_dataset()
