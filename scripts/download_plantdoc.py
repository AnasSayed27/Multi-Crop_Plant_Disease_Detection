import os
import shutil
import urllib.request
import zipfile

PLANTDOC_REPO_ZIP = "https://github.com/pratikkayal/PlantDoc-Dataset/archive/refs/heads/master.zip"
ZIP_DEST = "plantdoc_temp.zip"
EXTRACT_DIR = "plantdoc_temp_extract"
TARGET_DIR = "plantdoc_realworld"

def download_and_setup_plantdoc():
    print("=" * 70)
    print(" DOWNLOADING PLANTDOC REAL-WORLD FIELD BENCHMARK DATASET ")
    print("=" * 70)

    os.makedirs(TARGET_DIR, exist_ok=True)

    if not os.path.exists(ZIP_DEST) and len(os.listdir(TARGET_DIR)) == 0:
        print("\n📥 Downloading PlantDoc GitHub dataset archive (~20 MB)...")
        try:
            urllib.request.urlretrieve(PLANTDOC_REPO_ZIP, ZIP_DEST)
            print("✅ Download completed successfully!")
        except Exception as e:
            print(f"❌ Failed to download PlantDoc archive: {e}")
            return False

    if os.path.exists(ZIP_DEST) and len(os.listdir(TARGET_DIR)) == 0:
        print("\n📦 Extracting test images...")
        try:
            with zipfile.ZipFile(ZIP_DEST, 'r') as zip_ref:
                zip_ref.extractall(EXTRACT_DIR)
            
            # Locate test directory inside extracted repo
            test_src = os.path.join(EXTRACT_DIR, "PlantDoc-Dataset-master", "test")
            if not os.path.exists(test_src):
                test_src = os.path.join(EXTRACT_DIR, "PlantDoc-Dataset-master", "TRAIN")

            if os.path.exists(test_src):
                for item in os.listdir(test_src):
                    s = os.path.join(test_src, item)
                    d = os.path.join(TARGET_DIR, item)
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                print(f"✅ Successfully setup PlantDoc test dataset in '{TARGET_DIR}/'!")
            
            # Clean up temporary zip and extraction folder
            if os.path.exists(ZIP_DEST):
                os.remove(ZIP_DEST)
            if os.path.exists(EXTRACT_DIR):
                shutil.rmtree(EXTRACT_DIR)

        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return False

    total_images = 0
    subdirs = [d for d in os.listdir(TARGET_DIR) if os.path.isdir(os.path.join(TARGET_DIR, d))]
    for sd in subdirs:
        imgs = [f for f in os.listdir(os.path.join(TARGET_DIR, sd)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        total_images += len(imgs)

    print(f"\n📊 PlantDoc Benchmark Dataset Ready: {len(subdirs)} classes, {total_images} field images.")
    return True

if __name__ == "__main__":
    download_and_setup_plantdoc()
