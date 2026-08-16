import os
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_pdf_report_feature():
    print("======================================================================")
    print("   PHASE 7: AUTOMATED PDF REPORT FEATURE & SECURITY TEST SUITE       ")
    print("======================================================================\n")

    session = requests.Session()

    # 1. Register User A
    user_a_credentials = {
        "username": "pdf_farmer_a",
        "email": "farmer_a@example.com",
        "password": "secure_password_a_123"
    }
    reg_a_res = session.post(f"{BASE_URL}/auth/register", json=user_a_credentials)
    if reg_a_res.status_code == 200:
        token_a = reg_a_res.json()["access_token"]
    else:
        login_a_res = session.post(f"{BASE_URL}/auth/login", json={
            "username_or_email": user_a_credentials["username"],
            "password": user_a_credentials["password"]
        })
        token_a = login_a_res.json()["access_token"]
    
    print("[PASS] 1. User A authenticated successfully.")

    # 2. Register User B
    user_b_credentials = {
        "username": "pdf_farmer_b",
        "email": "farmer_b@example.com",
        "password": "secure_password_b_123"
    }
    reg_b_res = session.post(f"{BASE_URL}/auth/register", json=user_b_credentials)
    if reg_b_res.status_code == 200:
        token_b = reg_b_res.json()["access_token"]
    else:
        login_b_res = session.post(f"{BASE_URL}/auth/login", json={
            "username_or_email": user_b_credentials["username"],
            "password": user_b_credentials["password"]
        })
        token_b = login_b_res.json()["access_token"]

    print("[PASS] 2. User B authenticated successfully.")

    # 3. User A submits prediction scan
    sample_folder = r"Dataset/Plant_leave_diseases_dataset_without_augmentation/Potato___Early_blight"
    sample_img_name = os.listdir(sample_folder)[0]
    sample_img_path = os.path.join(sample_folder, sample_img_name)

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    with open(sample_img_path, "rb") as f:
        files = {"file": ("leaf.jpg", f, "image/jpeg")}
        pred_res = session.post(f"{BASE_URL}/predict", files=files, headers=headers_a)
    
    assert pred_res.status_code == 200, f"Prediction failed: {pred_res.text}"
    pred_data = pred_res.json()
    prediction_id = pred_data.get("prediction_id")
    assert prediction_id is not None, "Missing prediction_id in prediction response"
    print(f"[PASS] 3. User A executed prediction scan. Issued Prediction ID: #{prediction_id}")

    # 4. TEST 1: Authorized PDF Report Download (User A downloading User A's prediction)
    pdf_res_a = session.get(f"{BASE_URL}/api/prediction/{prediction_id}/pdf", headers=headers_a)
    assert pdf_res_a.status_code == 200, f"Expected 200 OK, got {pdf_res_a.status_code}: {pdf_res_a.text}"
    assert pdf_res_a.headers.get("content-type") == "application/pdf", "Expected application/pdf content-type"
    assert pdf_res_a.content.startswith(b"%PDF"), "Response binary stream is not a valid PDF document"
    assert len(pdf_res_a.content) > 1000, f"PDF payload too small ({len(pdf_res_a.content)} bytes)"
    print(f"[PASS] 4. Authorized PDF Report Generation verified (PDF Size: {len(pdf_res_a.content)} bytes).")

    # 5. TEST 2: Unauthorized Cross-User Access Attempt (User B attempting to download User A's PDF)
    pdf_res_b = session.get(f"{BASE_URL}/api/prediction/{prediction_id}/pdf", headers=headers_b)
    assert pdf_res_b.status_code == 403, f"Security Violation: Expected 403 Forbidden, got {pdf_res_b.status_code}"
    print("[PASS] 5. Unauthorized Cross-User Access blocked with HTTP 403 Forbidden.")

    # 6. TEST 3: Unauthenticated PDF Download Attempt
    pdf_res_no_auth = session.get(f"{BASE_URL}/api/prediction/{prediction_id}/pdf")
    assert pdf_res_no_auth.status_code == 401, f"Security Violation: Expected 401 Unauthorized, got {pdf_res_no_auth.status_code}"
    print("[PASS] 6. Unauthenticated PDF Download blocked with HTTP 401 Unauthorized.")

    # 7. TEST 4: Missing Prediction ID Attempt
    pdf_res_404 = session.get(f"{BASE_URL}/api/prediction/999999/pdf", headers=headers_a)
    assert pdf_res_404.status_code == 404, f"Expected 404 Not Found, got {pdf_res_404.status_code}"
    print("[PASS] 7. Non-existent Prediction ID returned HTTP 404 Not Found.")

    print("\n======================================================================")
    print("   PDF REPORT FEATURE & SECURITY SUITE: 100% SUCCESSFUL!   ")
    print("======================================================================\n")

if __name__ == "__main__":
    test_pdf_report_feature()
