import os
import sys
from PIL import Image

DATASET_DIR = r"d:\Projects\AI-ML Portfolio\Potato_disease\Dataset\Plant_leave_diseases_dataset_without_augmentation"

def audit_dataset():
    print("=" * 70)
    print(" STEP 0 — DATASET AUDIT REPORT ")
    print(" Source Path:", DATASET_DIR)
    print("=" * 70)

    if not os.path.exists(DATASET_DIR):
        print(f"Error: Dataset directory '{DATASET_DIR}' not found.")
        return

    class_folders = sorted([
        d for d in os.listdir(DATASET_DIR)
        if os.path.isdir(os.path.join(DATASET_DIR, d))
    ])

    print(f"\nDiscovered {len(class_folders)} total subdirectories in dataset.\n")

    audit_results = []
    flagged_low_count = []
    total_valid_images = 0
    total_corrupt_images = 0

    print(f"{'Idx':<4} | {'Class Name':<48} | {'Valid':<7} | {'Corrupted':<9} | {'Status/Flag'}")
    print("-" * 85)

    for idx, class_name in enumerate(class_folders, 1):
        class_path = os.path.join(DATASET_DIR, class_name)
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

        print(f"{idx:<4} | {class_name:<48} | {valid_cnt:<7} | {corrupt_cnt:<9} | {status}")

        audit_results.append({
            "idx": idx,
            "class_name": class_name,
            "valid_cnt": valid_cnt,
            "corrupt_cnt": corrupt_cnt,
            "status": status
        })

    print("-" * 85)
    print(f"TOTAL SUMMARY:")
    print(f"  Total Subdirectories:    {len(class_folders)}")
    print(f"  Total Valid Images:      {total_valid_images:,}")
    print(f"  Total Corrupted Images:  {total_corrupt_images}")
    print(f"  Classes Flagged (< 200): {len(flagged_low_count)}")
    print("-" * 85)

    if flagged_low_count:
        print("\nFLAGGED CLASSES (< 200 images):")
        for name, cnt in flagged_low_count:
            print(f"  - '{name}': {cnt} valid images")
    else:
        print("\nNo classes found with fewer than 200 images.")

if __name__ == "__main__":
    audit_dataset()
