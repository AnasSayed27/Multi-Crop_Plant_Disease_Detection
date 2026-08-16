import os
import time
import json
import argparse
import numpy as np
from PIL import Image
import tensorflow as tf

# ---------------------------------------------------------
# Configuration & Paths
# ---------------------------------------------------------
MODELS_DIR = "models_assets"
MODEL_PATH = os.path.join(MODELS_DIR, "mobilenet_v2_plantvillage.keras")
CLASS_NAMES_PATH = os.path.join(MODELS_DIR, "class_names.json")
DISEASE_INFO_PATH = os.path.join(MODELS_DIR, "disease_info.json")
CUSTOM_TEST_DIR = "test_real_images"
PLANTDOC_TEST_DIR = "plantdoc_realworld"
BENCHMARK_LOG_PATH = "REAL_WORLD_BENCHMARK_LOG.md"

def load_model_and_metadata(custom_model_path=None):
    target_path = custom_model_path if (custom_model_path and os.path.exists(custom_model_path)) else MODEL_PATH
    if not os.path.exists(target_path):
        # Try checking models_assets directory
        alt_path = os.path.join(MODELS_DIR, os.path.basename(target_path))
        if os.path.exists(alt_path):
            target_path = alt_path
        else:
            raise FileNotFoundError(f"Model file missing: '{target_path}'.")
    
    print(f"📦 Loading model artifact from: '{target_path}'")
    model = tf.keras.models.load_model(
        target_path,
        custom_objects={"preprocess_input": tf.keras.applications.mobilenet_v2.preprocess_input}
    )
    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
        class_names = json.load(f)
    with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
        disease_info = json.load(f)
    return model, class_names, disease_info

def remove_background_if_enabled(pil_img):
    try:
        from rembg import remove
        # Convert RGBA result from rembg to RGB with clean white background
        no_bg = remove(pil_img)
        background = Image.new("RGB", no_bg.size, (255, 255, 255))
        if no_bg.mode == 'RGBA':
            background.paste(no_bg, mask=no_bg.split()[3])
        else:
            background.paste(no_bg)
        return background
    except Exception as e:
        print(f"Background removal notice: {e}")
        return pil_img

def preprocess_image(img_path, use_rembg=False):
    img = Image.open(img_path).convert("RGB")
    if use_rembg:
        img = remove_background_if_enabled(img)
    img_resized = img.resize((224, 224))
    img_arr = np.array(img_resized, dtype=np.float32)
    return np.expand_dims(img_arr, axis=0)

def predict_single(model, img_arr):
    probs = model.predict(img_arr, verbose=0)[0]
    return probs

def predict_tta(model, img_arr):
    # 5-View Test-Time Augmentation (TTA) matching trained spatial invariances:
    # 1: Original photo
    # 2: Horizontal flip
    # 3: Vertical flip
    # 4: Slight rotation (15 degrees)
    # 5: Center zoom (90% crop + resize to 224x224)
    
    img_orig = img_arr[0]
    img_hflip = np.fliplr(img_orig)
    img_vflip = np.flipud(img_orig)
    
    # Slight Rotation (15 degrees clockwise)
    pil_img = Image.fromarray(img_orig.astype(np.uint8))
    pil_rot = pil_img.rotate(15, resample=Image.BICUBIC)
    img_rot = np.array(pil_rot, dtype=np.float32)
    
    # Center Crop Zoom (90%)
    h, w, c = img_orig.shape
    crop_h, crop_w = int(h * 0.9), int(w * 0.9)
    start_h, start_w = (h - crop_h) // 2, (w - crop_w) // 2
    pil_crop = Image.fromarray(img_orig[start_h:start_h+crop_h, start_w:start_w+crop_w].astype(np.uint8))
    img_zoom = np.array(pil_crop.resize((224, 224)), dtype=np.float32)

    tta_batch = np.array([img_orig, img_hflip, img_vflip, img_rot, img_zoom])
    probs_batch = model.predict(tta_batch, verbose=0)
    avg_probs = np.mean(probs_batch, axis=0)
    return avg_probs

def parse_truth_from_filename(filename):
    fn = filename.lower()
    if 'apple_blackrot' in fn or 'apple_black_rot' in fn: return 'Apple___Black_rot'
    if 'apple_scab' in fn: return 'Apple___Apple_scab'
    if 'apple_cedar' in fn or 'apple_rust' in fn: return 'Apple___Cedar_apple_rust'
    if 'apple_healthy' in fn: return 'Apple___healthy'
    if 'corn_commonrust' in fn or 'corn_rust' in fn: return 'Corn___Common_rust'
    if 'corn_blight' in fn: return 'Corn___Northern_Leaf_Blight'
    if 'corn_gray' in fn: return 'Corn___Cercospora_leaf_spot Gray_leaf_spot'
    if 'corn_healthy' in fn: return 'Corn___healthy'
    if 'potato_early-blight' in fn or 'potato_early_blight' in fn: return 'Potato___Early_blight'
    if 'potato_late-blight' in fn or 'potato_late_blight' in fn: return 'Potato___Late_blight'
    if 'potato_healthy' in fn: return 'Potato___healthy'
    if 'tomato_early' in fn: return 'Tomato___Early_blight'
    if 'tomato_late' in fn: return 'Tomato___Late_blight'
    if 'tomato_yellow' in fn: return 'Tomato___Tomato_Yellow_Leaf_Curl_Virus'
    if 'tomato_healthy' in fn: return 'Tomato___healthy'
    if 'pepper_bacterial' in fn: return 'Pepper,_bell___Bacterial_spot'
    if 'pepper_healthy' in fn: return 'Pepper,_bell___healthy'
    if 'grape_black' in fn: return 'Grape___Black_rot'
    if 'grape_healthy' in fn: return 'Grape___healthy'
    return None

def run_benchmark(use_tta=False, use_rembg=False, milestone_name="Baseline (Lab Model)", custom_model_path=None):
    print("=" * 78)
    print(f" REAL-WORLD FIELD BENCHMARK RUN: {milestone_name.upper()} ")
    print(f" Mode: TTA={'YES' if use_tta else 'NO'} | Rembg Preprocessing={'YES' if use_rembg else 'NO'}")
    print("=" * 78)

    model, class_names, disease_info = load_model_and_metadata(custom_model_path=custom_model_path)

    test_files = []
    
    if os.path.exists(CUSTOM_TEST_DIR):
        custom_imgs = [os.path.join(CUSTOM_TEST_DIR, f) for f in os.listdir(CUSTOM_TEST_DIR) 
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for c in custom_imgs:
            truth = parse_truth_from_filename(os.path.basename(c))
            test_files.append((c, truth, "Custom Upload"))

    if os.path.exists(PLANTDOC_TEST_DIR):
        for root, _, files in os.walk(PLANTDOC_TEST_DIR):
            for f in files:
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    parent_folder = os.path.basename(root)
                    if parent_folder in class_names:
                        test_files.append((os.path.join(root, f), parent_folder, "PlantDoc Benchmark"))

    if len(test_files) == 0:
        print(f"\n⚠️ No test images found.")
        return

    print(f"\n🔍 Found {len(test_files)} real-world field photographs for testing.\n")

    results = []
    latencies = []
    confidences = []
    correct_top1 = 0
    correct_top3 = 0
    total_evaluated = 0

    print("-" * 78)
    print(f"{'Filename / Sample':<28} | {'Top Prediction':<26} | {'Conf':<6} | {'Match'} | {'Time'}")
    print("-" * 78)

    for img_path, truth_class, source in test_files:
        img_name = os.path.basename(img_path)
        try:
            t0 = time.time()
            img_tensor = preprocess_image(img_path, use_rembg=use_rembg)
            if use_tta:
                probs = predict_tta(model, img_tensor)
            else:
                probs = predict_single(model, img_tensor)
            elapsed_ms = (time.time() - t0) * 1000

            top_idx = int(np.argmax(probs))
            top_class = class_names[top_idx]
            conf = float(probs[top_idx] * 100)

            # Top 3 indices
            top3_indices = np.argsort(probs)[-3:][::-1]
            top3_classes = [class_names[idx] for idx in top3_indices]

            is_top1_correct = (truth_class is not None) and (top_class == truth_class)
            is_top3_correct = (truth_class is not None) and (truth_class in top3_classes)

            if truth_class:
                total_evaluated += 1
                if is_top1_correct: correct_top1 += 1
                if is_top3_correct: correct_top3 += 1

            crop_name = disease_info.get(top_class, {}).get("crop", top_class)
            disease_name = disease_info.get(top_class, {}).get("disease", "")
            short_pred = f"{crop_name} - {disease_name}"[:26]

            match_str = "✅ YES" if is_top1_correct else ("⚠️ TOP3" if is_top3_correct else "❌ NO ")

            latencies.append(elapsed_ms)
            confidences.append(conf)

            results.append({
                "file": img_name,
                "truth": truth_class or "Unknown",
                "predicted": top_class,
                "confidence": conf,
                "is_correct": is_top1_correct,
                "latency_ms": elapsed_ms
            })

            print(f"{img_name[:26]:<28} | {short_pred:<26} | {conf:5.1f}% | {match_str}  | {elapsed_ms:4.0f}ms")

        except Exception as e:
            print(f"{img_name[:26]:<28} | ERROR: {str(e)[:35]}")

    avg_lat = float(np.mean(latencies)) if latencies else 0.0
    avg_conf = float(np.mean(confidences)) if confidences else 0.0
    top1_acc = (correct_top1 / total_evaluated * 100) if total_evaluated > 0 else 0.0
    top3_acc = (correct_top3 / total_evaluated * 100) if total_evaluated > 0 else 0.0

    print("-" * 78)
    print(f"📊 REAL-WORLD BENCHMARK SUMMARY ({milestone_name}):")
    print(f"   • Total Evaluated Samples : {total_evaluated}")
    print(f"   • Top-1 Real-World Accuracy: {top1_acc:.2f}% ({correct_top1}/{total_evaluated})")
    print(f"   • Top-3 Real-World Accuracy: {top3_acc:.2f}% ({correct_top3}/{total_evaluated})")
    print(f"   • Mean Model Confidence   : {avg_conf:.2f}%")
    print(f"   • Mean Latency Per-Image  : {avg_lat:.1f} ms")
    print("=" * 78)

    log_benchmark_to_markdown(milestone_name, use_tta, use_rembg, total_evaluated, top1_acc, top3_acc, avg_conf, avg_lat)

def log_benchmark_to_markdown(milestone, use_tta, use_rembg, total_eval, top1_acc, top3_acc, avg_conf, avg_lat):
    header_needed = not os.path.exists(BENCHMARK_LOG_PATH)
    
    with open(BENCHMARK_LOG_PATH, "a" if not header_needed else "w", encoding="utf-8") as f:
        if header_needed:
            f.write("# Real-World Field Performance & Optimization Benchmark Log\n\n")
            f.write("Official audit trail evaluating model accuracy, confidence, and latency across real-world field photos.\n\n")
            f.write("| Timestamp | Milestone / Phase | TTA | Rembg | Samples | Top-1 Acc (%) | Top-3 Acc (%) | Mean Conf (%) | Latency (ms) |\n")
            f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        
        t_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"| {t_stamp} | {milestone} | {'YES' if use_tta else 'NO'} | {'YES' if use_rembg else 'NO'} | {total_eval} | {top1_acc:.2f}% | {top3_acc:.2f}% | {avg_conf:.2f}% | {avg_lat:.1f}ms |\n")

    print(f"\n📝 Benchmark results logged to '{BENCHMARK_LOG_PATH}' successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-World Field Benchmark Suite")
    parser.add_argument("--tta", action="store_true", help="Enable 5-View Spatial Test-Time Augmentation")
    parser.add_argument("--rembg", action="store_true", help="Enable Background Removal Preprocessing")
    parser.add_argument("--milestone", type=str, default="Baseline (Lab Model)", help="Milestone title for log")
    parser.add_argument("--model-path", type=str, default=None, help="Custom Keras model artifact path")
    args = parser.parse_args()

    run_benchmark(use_tta=args.tta, use_rembg=args.rembg, milestone_name=args.milestone, custom_model_path=args.model_path)
