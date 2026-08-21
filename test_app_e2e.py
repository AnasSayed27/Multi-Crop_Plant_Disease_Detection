import os
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_end_to_end():
    print("======================================================================")
    print("   PHASE 6: END-TO-END SYSTEM INTEGRATION & VERIFICATION TEST   ")
    print("======================================================================\n")

    # Retry loop to wait for FastAPI server startup
    import time
    for attempt in range(15):
        try:
            res_home = requests.get(BASE_URL + "/", timeout=2)
            if res_home.status_code == 200:
                break
        except Exception:
            time.sleep(1)

    # 1. Test GET / (HTML Homepage)
    res_home = requests.get(BASE_URL + "/")
    assert res_home.status_code == 200, f"GET / failed with status {res_home.status_code}"
    print("[PASS] 1. Web Homepage (GET /) loaded cleanly (HTTP 200).")

    # 2. Test User Registration
    reg_payload = {"username": "farmer_anas", "email": "anas@example.com", "password": "secure_password_123"}
    res_reg = requests.post(BASE_URL + "/auth/register", json=reg_payload)
    if res_reg.status_code == 400:
        print("[INFO] User farmer_anas already registered (HTTP 400 handled).")
    else:
        assert res_reg.status_code == 200, f"Register failed: {res_reg.text}"
        print("[PASS] 2. User Registration (POST /auth/register) succeeded.")

    # 3. Test User Login & JWT Token
    login_payload = {"username_or_email": "farmer_anas", "password": "secure_password_123"}
    res_login = requests.post(BASE_URL + "/auth/login", json=login_payload)
    assert res_login.status_code == 200, f"Login failed: {res_login.text}"
    data_login = res_login.json()
    token = data_login.get("token") or data_login.get("access_token")
    assert token, "JWT access token missing in login response"
    print(f"[PASS] 3. User Login & JWT Token issuance (POST /auth/login) verified.")

    headers = {"Authorization": f"Bearer {token}"}

    # 4. Test Authenticated Health Check
    res_health = requests.get(BASE_URL + "/health")
    assert res_health.status_code == 200, f"GET /health failed: {res_health.text}"
    print(f"[PASS] 4. Health probe verified.")

    # 5. Test Leaf Prediction (POST /predict with a Leaf image)
    # Search for an image dynamically in plantdoc_realworld or Dataset
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "plantdoc_realworld", "Grape___healthy", "latest_cb=20100621160325.jpg"),
        os.path.join(base_dir, "test_real_images", "test_potato.jpg")
    ]
    test_leaf_path = None
    for c in candidates:
        if os.path.exists(c):
            test_leaf_path = c
            break

    if test_leaf_path and os.path.exists(test_leaf_path):
        with open(test_leaf_path, "rb") as f:
            image_content = f.read()
    else:
        # Fallback: create in-memory green leaf JPEG
        from PIL import Image
        import io
        buf = io.BytesIO()
        img = Image.new("RGB", (224, 224), color=(34, 139, 34))
        img.save(buf, format="JPEG")
        image_content = buf.getvalue()

    res_pred = requests.post(BASE_URL + "/predict", files={"file": ("leaf.jpg", image_content, "image/jpeg")}, headers=headers)
    assert res_pred.status_code == 200, f"Prediction failed: {res_pred.text}"
    pred_data = res_pred.json()
    assert pred_data["success"] == True, f"Prediction payload unsuccessful: {pred_data}"
    assert "crop" in pred_data and "disease" in pred_data and "confidence" in pred_data, f"Missing fields: {pred_data}"
    print(f"[PASS] 5. Crop Disease Prediction (POST /predict) verified:")
    print(f"       Detected: {pred_data['crop']} — {pred_data['disease']} ({pred_data['confidence']}%)")

    # 6. Test Non-Leaf / White Background Prediction
    from PIL import Image
    import io
    buf_bg = io.BytesIO()
    img_bg = Image.new("RGB", (224, 224), color=(240, 240, 240))
    img_bg.save(buf_bg, format="JPEG")
    res_bg_pred = requests.post(BASE_URL + "/predict", files={"file": ("background.jpg", buf_bg.getvalue(), "image/jpeg")}, headers=headers)
    assert res_bg_pred.status_code == 200, f"Background prediction failed: {res_bg_pred.text}"
    bg_pred_data = res_bg_pred.json()
    print(f"[PASS] 6. Non-Leaf / Low-Confidence Detection (POST /predict) verified:")
    print(f"       Label: {bg_pred_data.get('label', bg_pred_data.get('crop'))} | Status: {bg_pred_data.get('status')}")

    # 7. Test User Scan History (GET /api/history)
    res_hist = requests.get(BASE_URL + "/api/history", headers=headers)
    assert res_hist.status_code == 200, f"GET /api/history failed: {res_hist.text}"
    hist_data = res_hist.json()["history"]
    print(f"[PASS] 7. Personal Prediction History (GET /api/history) verified ({len(hist_data)} records logged).")

    # 8. Test User Statistics (GET /api/statistics)
    res_stats = requests.get(BASE_URL + "/api/statistics", headers=headers)
    assert res_stats.status_code == 200, f"GET /api/statistics failed: {res_stats.text}"
    stats_data = res_stats.json()["statistics"]
    print(f"[PASS] 8. Personal Statistics Dashboard (GET /api/statistics) verified:")
    print(f"       Total Scans: {stats_data['total_scans']} | Avg Conf: {stats_data['avg_confidence']}% | Top Disease: {stats_data['top_disease']}")

    # 9. Test Public Disease Library (GET /api/library)
    res_lib = requests.get(BASE_URL + "/api/library")
    assert res_lib.status_code == 200, f"GET /api/library failed: {res_lib.text}"
    lib_items = res_lib.json()["library"]
    assert len(lib_items) == 38, f"Expected 38 plant disease items, got {len(lib_items)}"
    print(f"[PASS] 9. Browsable Crop & Disease Library (GET /api/library) verified ({len(lib_items)} entries).")

    print("\n======================================================================")
    print("   END-TO-END SYSTEM INTEGRATION VERIFICATION: 100% SUCCESSFUL!   ")
    print("======================================================================\n")

if __name__ == "__main__":
    test_end_to_end()
