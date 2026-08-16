import os
import io
import uuid
import json
import numpy as np
from PIL import Image
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Request, Depends, HTTPException, Header, status
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request, Header
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
CONFIDENCE_THRESHOLD = 50.0  # Configurable low-confidence threshold percentage

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

# Initialize SQLite schema
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
    global dpd_engine, class_names, disease_info
    
    # Load class names
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            class_names = json.load(f)
        print(f"Loaded {len(class_names)} class names.")
    else:
        print("Warning: class_names.json not found.")

    # Load disease advisory knowledge base
    if os.path.exists(DISEASE_INFO_PATH):
        with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
            disease_info = json.load(f)
        print(f"Loaded disease advisory information for {len(disease_info)} classes.")
    else:
        print("Warning: disease_info.json not found.")

    # Initialize Production PyTorch Model B Inference Engine
    try:
        dpd_engine = dpd_model.get_inference_engine()
        print("Successfully initialized DPD ViT Model B Inference Engine.")
    except Exception as e:
        print(f"Error initializing DPD ViT Engine: {e}")

load_assets()

# ---------------------------------------------------------
# Authentication Dependency Helper
# ---------------------------------------------------------
def get_current_user(request: Request, authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """Extracts and validates JWT token from Authorization: Bearer <token> header."""
    auth_header = authorization or request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        token = parts[1]
        payload = database.decode_access_token(token)
        if not payload or "sub" not in payload:
            return None
        user = database.get_user_by_id(int(payload["sub"]))
        return user
    except Exception:
        return None

def require_auth(user: Optional[Dict[str, Any]] = Depends(get_current_user)) -> Dict[str, Any]:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# ---------------------------------------------------------
# Web Template & Auth Endpoints
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    """Serves the main application user interface."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/auth/register")
async def register(payload: Dict[str, str]):
    username = payload.get("username", "").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")

    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="All fields (username, email, password) are required.")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    try:
        user = database.register_user(username, email, password)
        token = database.create_access_token({"sub": str(user["id"]), "username": user["username"]})
        return {
            "message": "Registration successful.",
            "user": user,
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@app.post("/auth/login")
async def login(payload: Dict[str, str]):
    username_or_email = payload.get("username_or_email", "").strip()
    password = payload.get("password", "")

    if not username_or_email or not password:
        raise HTTPException(status_code=400, detail="Username/email and password are required.")

    user = database.authenticate_user(username_or_email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username/email or password.")

    token = database.create_access_token({"sub": str(user["id"]), "username": user["username"]})
    return {
        "message": "Login successful.",
        "user": user,
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/auth/me")
async def get_me(user: Dict[str, Any] = Depends(require_auth)):
    return {"user": user}

# ---------------------------------------------------------
# Image Classification & Prediction Route
# ---------------------------------------------------------
@app.post("/predict")
async def predict_crop_disease(
    file: UploadFile = File(...),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """
    Handles leaf image upload, validates file type, runs DPD ViT Model B prediction,
    extracts Top-1 & Top-3 predictions, formats advisory details, and logs history.
    """
    global dpd_engine, class_names, disease_info
    
    if dpd_engine is None or not dpd_engine.loaded:
        load_assets()
        if dpd_engine is None or not dpd_engine.loaded:
            raise HTTPException(
                status_code=503,
                detail="Model is currently initializing. Please try again in a moment."
            )

    # 1. Validate File Format
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid crop leaf image (JPEG/PNG/WebP).")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        # 2. Save Uploaded Image to Local uploads/ Directory
        filename = f"scan_{uuid.uuid4().hex[:10]}.jpg"
        save_path = os.path.join(UPLOADS_DIR, filename)
        relative_image_path = f"uploads/{filename}"

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img.save(save_path, "JPEG", quality=90)

        # 3. Model B Inference (Dual-Head ViT-Base)
        pred_result = dpd_engine.predict(img, disease_info=disease_info)

        crop_name = pred_result["crop"]
        disease_name = pred_result["disease"]
        confidence = pred_result["confidence"]
        is_healthy = pred_result["is_healthy"]
        top3_predictions = pred_result["top_3_predictions"]
        advisory_data = pred_result["advisory"]

        is_low_confidence = confidence < CONFIDENCE_THRESHOLD

        # 4. GATING: Non-Leaf or Low-Confidence Out-of-Distribution Image
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
                database.save_prediction(
                    user_id=current_user["id"],
                    crop="Non-Crop",
                    disease="No Plant Leaf Detected",
                    confidence=confidence,
                    image_path=relative_image_path
                )

            return JSONResponse(content=response_payload)

        # 5. CONFIDENT PLANT DISEASE PREDICTION RESPONSE
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

        # 6. Log Confident Prediction to SQLite Database
        if current_user:
            pred_id = database.save_prediction(
                user_id=current_user["id"],
                crop=crop_name,
                disease=disease_name,
                confidence=confidence,
                image_path=relative_image_path
            )
            response_payload["prediction_id"] = pred_id

        return JSONResponse(content=response_payload)

    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction processing: {str(e)}")

# ---------------------------------------------------------
# User History, Statistics, Library & PDF Report API Endpoints
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