"""
======================================================================
 Automated Integration & Unit Test Suite (Pytest)
 Multi-Crop Plant Disease Detection & Advisory System
======================================================================
"""

import os
import io
import pytest
from PIL import Image

# Ensure test environment uses test database
os.environ["DB_PATH"] = "test_database.db"
os.environ["JWT_SECRET_KEY"] = "test_secret_key_12345"
os.environ["CONFIDENCE_THRESHOLD"] = "50.0"

import database
database.DB_PATH = "test_database.db"
database.init_db()

from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    if os.path.exists("test_database.db"):
        try:
            os.remove("test_database.db")
        except Exception:
            pass


def create_dummy_image(color=(34, 139, 34), size=(224, 224)) -> bytes:
    """Generates a valid green JPEG leaf image in-memory."""
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format="JPEG")
    return buf.getvalue()


# --------------------------------------------------------------------
# 1. Health Probe Verification
# --------------------------------------------------------------------
def test_health_liveness():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data


def test_health_readiness():
    response = client.get("/health/ready")
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert "database_connected" in data


# --------------------------------------------------------------------
# 2. Authentication & Case-Insensitive Login Tests
# --------------------------------------------------------------------
def test_user_registration_and_case_insensitive_login():
    email = "Farmer.Test@AgriSystem.org"
    username = "farmer_test_user"
    password = "secure_password_123"

    # Register
    reg_resp = client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    assert reg_resp.status_code == 200
    reg_data = reg_resp.json()
    assert reg_data["success"] is True
    assert "token" in reg_data
    token = reg_data["token"]

    # Login with exact email
    login_resp_exact = client.post("/auth/login", json={
        "username_or_email": email,
        "password": password
    })
    assert login_resp_exact.status_code == 200
    assert "token" in login_resp_exact.json()

    # Login with lowercase email (Testing Case-Insensitive Fix)
    login_resp_lower = client.post("/auth/login", json={
        "username_or_email": email.lower(),
        "password": password
    })
    assert login_resp_lower.status_code == 200
    assert "token" in login_resp_lower.json()

    # Login with username
    login_resp_user = client.post("/auth/login", json={
        "username_or_email": username,
        "password": password
    })
    assert login_resp_user.status_code == 200


def test_invalid_login():
    response = client.post("/auth/login", json={
        "username_or_email": "non_existent_user@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


# --------------------------------------------------------------------
# 3. Disease Library & Catalog Tests
# --------------------------------------------------------------------
def test_disease_library():
    response = client.get("/api/library")
    assert response.status_code == 200
    data = response.json()
    assert "library" in data
    assert len(data["library"]) > 0
    first_item = data["library"][0]
    assert "crop" in first_item
    assert "disease" in first_item


# --------------------------------------------------------------------
# 4. Upload Size Guard & Negative Input Tests
# --------------------------------------------------------------------
def test_predict_empty_file():
    response = client.post("/predict", files={"file": ("empty.jpg", b"", "image/jpeg")})
    assert response.status_code == 400


def test_predict_invalid_mime_type():
    response = client.post("/predict", files={"file": ("test.txt", b"not an image", "text/plain")})
    assert response.status_code == 400


def test_predict_payload_too_large():
    # 11 MB dummy bytes
    large_bytes = b"0" * (11 * 1024 * 1024)
    response = client.post("/predict", files={"file": ("large.jpg", large_bytes, "image/jpeg")})
    assert response.status_code == 413


# --------------------------------------------------------------------
# 5. Prediction Flow, History & PDF Export Tests
# --------------------------------------------------------------------
def test_predict_and_pdf_generation():
    # 1. Register test farmer
    email = "pdf_test_farmer@agri.com"
    username = "pdf_tester"
    password = "pdf_password_123"

    reg_resp = client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    token = reg_resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload dummy leaf image
    dummy_img = create_dummy_image()
    pred_resp = client.post(
        "/predict",
        files={"file": ("leaf_test.jpg", dummy_img, "image/jpeg")},
        headers=headers
    )
    assert pred_resp.status_code == 200
    pred_data = pred_resp.json()
    assert pred_data["success"] is True
    assert "confidence" in pred_data
    assert "top_3_predictions" in pred_data
    prediction_id = pred_data.get("prediction_id")

    # 3. Check user history
    hist_resp = client.get("/api/history", headers=headers)
    assert hist_resp.status_code == 200
    history = hist_resp.json()["history"]
    assert len(history) >= 1

    # 4. Check user stats
    stats_resp = client.get("/api/statistics", headers=headers)
    assert stats_resp.status_code == 200
    stats = stats_resp.json()["statistics"]
    assert stats["total_scans"] >= 1

    # 5. Download PDF Report if prediction_id exists
    if prediction_id:
        pdf_resp = client.get(f"/api/prediction/{prediction_id}/pdf", headers=headers)
        assert pdf_resp.status_code == 200
        assert pdf_resp.headers["content-type"] == "application/pdf"
        assert len(pdf_resp.content) > 1000  # Non-empty valid PDF binary
