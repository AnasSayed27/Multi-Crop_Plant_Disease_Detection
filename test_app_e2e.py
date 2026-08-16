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
    token = data_login["access_token"]
    assert token, "JWT access token missing in login response"
    print(f"[PASS] 3. User Login & JWT Token issuance (POST /auth/login) verified.")

    headers = {"Authorization": f"Bearer {token}"}

    # 4. Test Authenticated User Profile (GET /auth/me)
    res_me = requests.get(BASE_URL + "/auth/me", headers=headers)
    assert res_me.status_code == 200, f"GET /auth/me failed: {res_me.text}"
    print(f"[PASS] 4. Authenticated profile lookup (GET /auth/me) verified.")

    # 5. Test Leaf Prediction (POST /predict with a Potato Healthy image)
    potato_dir = r"d:\Projects\AI-ML Portfolio\Potato_disease\Dataset\Plant_leave_diseases_dataset_without_augmentation\Potato___healthy"
    potato_files = [os.path.join(potato_dir, f) for f in os.listdir(potato_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    assert potato_files, "No potato test images found."
    test_leaf_path = potato_files[0]

    with open(test_leaf_path, "rb") as f:
        res_pred = requests.post(BASE_URL + "/predict", files={"file": ("leaf.jpg", f, "image/jpeg")}, headers=headers)
    assert res_pred.status_code == 200, f"Prediction failed: {res_pred.text}"
    pred_data = res_pred.json()
    assert pred_data["success"] == True, f"Prediction payload unsuccessful: {pred_data}"
    assert pred_data["is_background"] == False, "Leaf image incorrectly flagged as background"
    assert "crop" in pred_data and "disease" in pred_data and "confidence" in pred_data, f"Missing fields: {pred_data}"
    assert "top_3_predictions" in pred_data and len(pred_data["top_3_predictions"]) == 3, "Missing Top-3 breakdown"
    assert "advisory" in pred_data and pred_data["advisory"]["symptoms"], "Missing advisory guidance"
    print(f"[PASS] 5. Crop Disease Prediction (POST /predict) verified:")
    print(f"       Detected: {pred_data['crop']} — {pred_data['disease']} ({pred_data['confidence']}%)")
    print(f"       Top-3 Predictions: {[p['disease'] + ' (' + str(p['confidence']) + '%)' for p in pred_data['top_3_predictions']]}")

    # 6. Test Non-Leaf Background Prediction (POST /predict with a Background_without_leaves image)
    bg_dir = r"d:\Projects\AI-ML Portfolio\Potato_disease\Dataset\Plant_leave_diseases_dataset_without_augmentation\Background_without_leaves"
    bg_files = [os.path.join(bg_dir, f) for f in os.listdir(bg_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    assert bg_files, "No background test images found."
    test_bg_path = bg_files[0]

    with open(test_bg_path, "rb") as f:
        res_bg_pred = requests.post(BASE_URL + "/predict", files={"file": ("background.jpg", f, "image/jpeg")}, headers=headers)
    assert res_bg_pred.status_code == 200, f"Background prediction failed: {res_bg_pred.text}"
    bg_pred_data = res_bg_pred.json()
    assert bg_pred_data["is_background"] == True or bg_pred_data["label"] == "No Plant Leaf Detected", f"Background handling failed: {bg_pred_data}"
    assert bg_pred_data["advisory"] is None, "Advisory card should be None for non-leaf background"
    print(f"[PASS] 6. Special Non-Leaf Background Detection (POST /predict) verified:")
    print(f"       Label: {bg_pred_data['label']} | Message: {bg_pred_data['message']}")

    # 7. Test User Scan History (GET /api/history)
    res_hist = requests.get(BASE_URL + "/api/history", headers=headers)
    assert res_hist.status_code == 200, f"GET /api/history failed: {res_hist.text}"
    hist_data = res_hist.json()["history"]
    assert len(hist_data) >= 2, f"Expected history records, got {len(hist_data)}"
    print(f"[PASS] 7. Personal Prediction History (GET /api/history) verified ({len(hist_data)} records logged).")

    # 8. Test User Statistics (GET /api/statistics)
    res_stats = requests.get(BASE_URL + "/api/statistics", headers=headers)
    assert res_stats.status_code == 200, f"GET /api/statistics failed: {res_stats.text}"
    stats_data = res_stats.json()["statistics"]
    assert stats_data["total_scans"] >= 2, f"Invalid total scans: {stats_data}"
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
