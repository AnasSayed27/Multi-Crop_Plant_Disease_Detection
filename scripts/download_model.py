"""
======================================================================
 Automated Model Weights Downloader (Model B — Vision Transformer)
======================================================================
Downloads `model_b_partial_adapted.pth` (~328 MB) from Google Drive
directly into the `models_assets/` directory.

Usage:
    python scripts/download_model.py
======================================================================
"""

import os
import sys
import shutil

FILE_ID = "1GdjtTcepE_VpGlrjZhBqDBBLma3rj_Bo"
DESTINATION = os.path.join("models_assets", "model_b_partial_adapted.pth")
MANUAL_DRIVE_URL = "https://drive.google.com/file/d/1GdjtTcepE_VpGlrjZhBqDBBLma3rj_Bo/view?usp=sharing"


def download_with_gdown(file_id: str, dest: str) -> bool:
    try:
        import gdown
        print("[Downloader] Attempting download via gdown...")
        url = f"https://drive.google.com/uc?id={file_id}"
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        output = gdown.download(url, dest, quiet=False)
        return output is not None and os.path.exists(dest) and os.path.getsize(dest) > 100_000_000
    except Exception as e:
        print(f"[Downloader] gdown not available or failed: {e}")
        return False


def download_with_requests(file_id: str, dest: str) -> bool:
    try:
        import requests
        print("[Downloader] Attempting streaming download via requests...")
        url = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        
        response = session.get(url, params={"id": file_id, "confirm": "t"}, stream=True)
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                response = session.get(url, params={"id": file_id, "confirm": value}, stream=True)
                break

        os.makedirs(os.path.dirname(dest), exist_ok=True)
        chunk_size = 64 * 1024
        downloaded = 0

        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    sys.stdout.write(f"\r[Progress] Downloaded: {downloaded / (1024 * 1024):.1f} MB")
                    sys.stdout.flush()

        print(f"\n[Downloader] Download finished ({downloaded / (1024 * 1024):.1f} MB).")
        return os.path.exists(dest) and os.path.getsize(dest) > 100_000_000
    except Exception as e:
        print(f"[Downloader] requests stream failed: {e}")
        return False


def main():
    print("=" * 70)
    print(" Multi-Crop Disease Diagnosis System: Model Weights Downloader")
    print("=" * 70)
    
    if os.path.exists(DESTINATION) and os.path.getsize(DESTINATION) > 100_000_000:
        size_mb = os.path.getsize(DESTINATION) / (1024 * 1024)
        print(f"\n[OK] Model checkpoint already exists at: '{DESTINATION}' ({size_mb:.1f} MB).")
        print("No download needed!\n")
        return

    print(f"\nTarget path: {DESTINATION}")
    print(f"Google Drive Link: {MANUAL_DRIVE_URL}\n")

    # Method 1: gdown
    success = download_with_gdown(FILE_ID, DESTINATION)

    # Method 2: requests fallback
    if not success:
        success = download_with_requests(FILE_ID, DESTINATION)

    if success:
        print(f"\n[SUCCESS] Model B checkpoint verified at '{DESTINATION}'!")
        print("You can now start the application with: python app.py\n")
    else:
        print("\n" + "!" * 70)
        print("[MANUAL STEP REQUIRED] Automated download could not complete.")
        print(f"1. Please open this link in your browser:")
        print(f"   {MANUAL_DRIVE_URL}")
        print(f"2. Download 'model_b_partial_adapted.pth'")
        print(f"3. Save/move it to:")
        print(f"   {DESTINATION}")
        print("!" * 70 + "\n")


if __name__ == "__main__":
    main()
