import os
import io
import uuid
import json
import asyncio
import numpy as np
from PIL import Image
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Request, Depends, HTTPException, Header, status
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
import pdf_generator
import dpd_model

# ---------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------
CLASS_NAMES_PATH = os.path.join("models_assets", "class_names.json")
DISEASE_INFO_PATH = os.path.join("models_assets", "disease_info.json")
UPLOADS_DIR = "uploads"
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "50.0"))  # Gating threshold
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")) * 1024 * 1024  # 10 MB limit

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs("models_assets", exist_ok=True)

# ---------------------------------------------------------
# App Initialization & Database Setup
# ---------------------------------------------------------
app = FastAPI(
    title="Multi-Crop Disease Detection & Advisory System",
    version="3.0",
    description="Vision Transformer (DPD ViT-Base) multi-crop plant pathology diagnostic and advisory platform."
)

# Initialize SQLite schema and indexes
database.init_db()

# Mount Static Files for Uploaded History Thumbnails
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------
# Model & Asset Loading
# ---------------------------------------------------------
dpd_engine = None
class_names: List[str] = []
disease_info: Dict[str, Any] = {}


def load_assets():
    """Loads class names, disease metadata, and initializes Vision Transformer model."""
    global dpd_engine, class_names, disease_info

    # 1. Load Class Names
    if os.path.exists(CLASS_NAMES_PATH):
        try:
            with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
                class_names = json.load(f)
            print(f"Loaded {len(class_names)} class names from '{CLASS_NAMES_PATH}'.")
        except Exception as e:
            print(f"Error loading class names: {e}")
            class_names = []

    # 2. Load Disease Information & Advisory Knowledge Base
    if os.path.exists(DISEASE_INFO_PATH):
        try:
            with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
                disease_info = json.load(f)
            print(f"Loaded advisory details for {len(disease_info)} classes from '{DISEASE_INFO_PATH}'.")
        except Exception as e:
            print(f"Error loading disease info: {e}")
            disease_info = {}

    # 3. Initialize PyTorch Vision Transformer Inference Engine
    try:
        dpd_engine = dpd_model.DPDInferenceEngine()
    except Exception as e:
        print(f"Error initializing DPD Inference Engine: {e}")
        dpd_engine = None


# Load assets on startup
load_assets()

# ---------------------------------------------------------
# Authentication Dependency Helpers
# ---------------------------------------------------------
def get_current_user(
    request: Request,
    authorization: Optional[str] = Header(None)
) -> Optional[Dict[str, Any]]:
    """Extracts and validates current user from Authorization header if present."""
    auth_header = authorization or request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header:
        return None

    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None

    payload = database.decode_access_token(token)
    if not payload or "sub" not in payload:
        return None

    try:
        user_id = int(payload["sub"])
        user = database.get_user_by_id(user_id)
        return user
    except Exception:
        return None


def require_auth(
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Enforces authentication; raises HTTP 401 if user is not authenticated."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in to access this resource.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return current_user


# ---------------------------------------------------------
# Health & Readiness Probes
# ---------------------------------------------------------
@app.get("/health")
async def health_check():
    """Fast liveness check."""
    return {"status": "ok", "service": "multi-crop-disease-detection", "version": "3.0"}


@app.get("/health/ready")
async def readiness_check():
    """Deep readiness check verifying model loading and database connectivity."""
    is_model_ready = dpd_engine is not None and getattr(dpd_engine, "loaded", False)
    is_db_ready = False
    try:
        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        is_db_ready = cursor.fetchone() is not None
        conn.close()
    except Exception:
        is_db_ready = False

    status_code = status.HTTP_200_OK if (is_model_ready and is_db_ready) else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if (is_model_ready and is_db_ready) else "degraded",
            "model_loaded": is_model_ready,
            "database_connected": is_db_ready
        }
    )


# ---------------------------------------------------------
# Web Interface & Page Route
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    """Renders the comprehensive single-page web portal."""
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------------------------------------
# User Authentication Routes
# ---------------------------------------------------------
@app.post("/auth/register")
async def register(payload: Dict[str, str]):
    """Registers a new user account."""
    username = payload.get("username", "").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")

    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="Username, email, and password are required.")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    try:
        user = database.register_user(username, email, password)
        token = database.create_access_token({"sub": user["id"], "username": user["username"]})
        return {
            "success": True,
            "message": "User registered successfully.",
            "token": token,
            "user": user
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@app.post("/auth/login")
async def login(payload: Dict[str, str]):
    """Authenticates an existing user and returns a JWT access token."""
    username_or_email = payload.get("username_or_email", "").strip()
    password = payload.get("password", "")

    if not username_or_email or not password:
        raise HTTPException(status_code=400, detail="Username/email and password are required.")

    user = database.authenticate_user(username_or_email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username/email or password.")

    token = database.create_access_token({"sub": user["id"], "username": user["username"]})
    return {
        "success": True,
        "message": "Login successful.",
        "token": token,
        "user": user
    }


# ---------------------------------------------------------
# Image Classification & Prediction Route
# ---------------------------------------------------------
@app.post("/predict")
async def predict_crop_disease(
    file: UploadFile = File(...),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """
    Handles leaf image upload, validates file type and size, runs DPD ViT Model B prediction
    asynchronously, extracts Top-1 & Top-3 predictions, formats advisory details, and logs history.
    """
    global dpd_engine, class_names, disease_info
    
    if dpd_engine is None or not dpd_engine.loaded:
        load_assets()
        if dpd_engine is None or not dpd_engine.loaded:
            raise HTTPException(
                status_code=503,
                detail="Model is currently initializing. Please try again in a moment."
            )

    # 1. Validate File Format & MIME Type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid crop leaf image (JPEG/PNG/WebP).")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # 2. Enforce Maximum File Size Limit (10MB)
    if len(image_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum allowed upload size of {MAX_UPLOAD_SIZE // (1024 * 1024)} MB."
        )

    try:
        # 3. Save Uploaded Image to Local uploads/ Directory
        filename = f"scan_{uuid.uuid4().hex[:10]}.jpg"
        save_path = os.path.join(UPLOADS_DIR, filename)
        relative_image_path = f"uploads/{filename}"

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img.save(save_path, "JPEG", quality=90)

        # 4. Asynchronous Model B Inference (Dual-Head ViT-Base) via Threadpool
        pred_result = await asyncio.to_thread(dpd_engine.predict, img, disease_info)

        crop_name = pred_result["crop"]
        disease_name = pred_result["disease"]
        confidence = pred_result["confidence"]
        is_healthy = pred_result["is_healthy"]
        top3_predictions = pred_result["top_3_predictions"]
        advisory_data = pred_result["advisory"]

        is_low_confidence = confidence < CONFIDENCE_THRESHOLD

        # 5. GATING: Non-Leaf or Low-Confidence Out-of-Distribution Image
        if is_low_confidence or pred_result.get("is_uncertain", False):
            response_payload = {
                "success": True,
                "is_background": True,
                "label": "No Plant Leaf Detected",
                "crop": "Non-Crop / Low Confidence",
                "disease": "No Plant Leaf Detected",
                "status": "Uncertain",
                "confidence": confidence,
                "is_low_confidence": True,
                "confidence_threshold": CONFIDENCE_THRESHOLD,
                "message": f"No crop leaf recognized with high confidence (Confidence: {confidence:.1f}%, Threshold: {CONFIDENCE_THRESHOLD}%). Please upload a clear, well-lit, close-up photo of a plant leaf.",
                "image_path": relative_image_path,
                "top_3_predictions": top3_predictions,
                "advisory": None  # Bypasses false advisory treatment cards
            }

            if current_user:
                try:
                    pred_id = database.save_prediction(
                        user_id=current_user["id"],
                        crop="Non-Crop",
                        disease="No Plant Leaf Detected",
                        confidence=confidence,
                        image_path=relative_image_path
                    )
                    response_payload["prediction_id"] = pred_id
                except Exception as db_err:
                    print(f"Warning: Failed to save low-confidence prediction to history: {db_err}")

            return JSONResponse(content=response_payload)

        # 6. CONFIDENT PLANT DISEASE PREDICTION RESPONSE
        status_text = "Healthy" if is_healthy else "Diseased"

        response_payload = {
            "success": True,
            "is_background": False,
            "crop": crop_name,
            "disease": disease_name,
            "status": status_text,
            "confidence": confidence,
            "is_low_confidence": False,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "warning": None,
            "image_path": relative_image_path,
            "top_3_predictions": top3_predictions,
            "advisory": {
                "symptoms": advisory_data.get("symptoms", "Visible foliar lesions or discoloration."),
                "cause": advisory_data.get("cause", "Pathogen infection identified."),
                "organic_treatment": advisory_data.get("organic_treatment", advisory_data.get("treatment", "Apply recommended cultural and biological practices.")),
                "chemical_treatment": advisory_data.get("chemical_treatment", "Apply recommended protective fungicides/bactericides according to IPM thresholds."),
                "prevention": advisory_data.get("prevention", "Maintain crop scouting and proper spacing.")
            }
        }

        # 7. Log Confident Prediction to SQLite Database (Resilient)
        if current_user:
            try:
                pred_id = database.save_prediction(
                    user_id=current_user["id"],
                    crop=crop_name,
                    disease=disease_name,
                    confidence=confidence,
                    image_path=relative_image_path
                )
                response_payload["prediction_id"] = pred_id
            except Exception as db_err:
                print(f"Warning: Failed to save prediction to history: {db_err}")

        return JSONResponse(content=response_payload)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction processing: {str(e)}")

# ---------------------------------------------------------
# History & Library Endpoints (Truncated for brevity, logic remains identical)
# ---------------------------------------------------------
@app.get("/api/prediction/{prediction_id}/pdf")
async def download_prediction_pdf(
    prediction_id: int,
    user: Dict[str, Any] = Depends(require_auth)
):
    """
    Generates and returns a downloadable PDF report for a prediction record.
    Enforces strict authorization: Users can ONLY access their own records.
    """
    pred = database.get_prediction_by_id(prediction_id)
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction record not found.")

    if pred["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Forbidden: You are not authorized to access this prediction report.")

    # Match advisory info
    crop_disease_key = None
    for key, info in disease_info.items():
        if info.get("crop") == pred["crop"] and info.get("disease") == pred["disease"]:
            crop_disease_key = key
            break

    info_data = disease_info.get(crop_disease_key, {}) if crop_disease_key else {
        "symptoms": "No symptom details recorded.",
        "cause": "No cause details recorded.",
        "organic_treatment": "No organic treatment details recorded.",
        "chemical_treatment": "No chemical treatment details recorded.",
        "prevention": "No prevention details recorded."
    }

    pdf_stream = pdf_generator.generate_prediction_pdf(
        prediction=pred,
        user=user,
        advisory_info=info_data,
        base_dir="."
    )

    pdf_bytes = pdf_stream.getvalue()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=crop_disease_report_{prediction_id}.pdf"
        }
    )


@app.get("/api/history")
async def get_history(user: Dict[str, Any] = Depends(require_auth)):
    """Returns prediction history records for logged-in user."""
    records = database.get_user_history(user["id"])
    return {"history": records}


@app.get("/api/statistics")
async def get_statistics(user: Dict[str, Any] = Depends(require_auth)):
    """Returns user-level personal prediction statistics."""
    stats = database.get_user_stats(user["id"])
    return {"statistics": stats}


@app.get("/api/library")
async def get_disease_library():
    """Returns public browsable catalog of supported crops, diseases, and advisory details."""
    global disease_info
    if not disease_info:
        load_assets()
    
    library_items = []
    for raw_cls, info in disease_info.items():
        if info.get("is_background", False):
            continue
        library_items.append({
            "raw_class": raw_cls,
            "crop": info.get("crop", "Unknown"),
            "disease": info.get("disease", "Unknown"),
            "status": info.get("status", "Unknown"),
            "symptoms": info.get("symptoms", ""),
            "cause": info.get("cause", ""),
            "organic_treatment": info.get("organic_treatment", ""),
            "chemical_treatment": info.get("chemical_treatment", ""),
            "prevention": info.get("prevention", "")
        })
    
    return {"library": library_items}

# Hugging Face Space Gradio & FastAPI Integration
try:
    import gradio as gr
    with gr.Blocks(title="Multi-Crop Disease Detection & Advisory System") as gradio_ui:
        gr.HTML('<iframe src="/" width="100%" height="900px" style="border:none; width:100%; height:900px;"></iframe>')
    app = gr.mount_gradio_app(app, gradio_ui, path="/gradio")
except Exception as e:
    print(f"Gradio mount notice: {e}")

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)