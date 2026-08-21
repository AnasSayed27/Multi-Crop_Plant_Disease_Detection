# 🌿 Multi-Crop Plant Disease Detection & Farmer Advisory System
### *An AI-Powered Agricultural Diagnosis Platform using Vision Transformers*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Project Overview

This project is an end-to-end **Artificial Intelligence platform for diagnosing crop diseases** from leaf photographs and providing **actionable treatment advice** to farmers.

### The Problem
- Traditional plant disease classification models are trained on only a single crop (like Potato or Tomato) using laboratory photos with clean backgrounds.
- In real-world fields, these models fail because:
  1. Real farm images have complex backgrounds (soil, weeds, shadows, hands).
  2. Many crops share similar diseases (for example, *Early Blight* looks almost identical on Potato and Tomato leaves, confusing standard models).

### Our Solution
- We built a **Dual-Head Vision Transformer (ViT)** system that looks at two things simultaneously:
  1. **What plant is it?** (Classifies across **55 crop types**)
  2. **What disease does it have?** (Classifies across **175 disease types**)
- The system then combines both answers to find the exact matching crop-disease pair and delivers:
  - **Top-1 Primary Diagnosis** with confidence percentage
  - **Top-3 Alternative Possibilities**
  - **Complete Treatment Plan** (Organic remedies, Chemical sprays, and Prevention steps)
  - **Downloadable 2-Page PDF Clinical Report**

---

## 💡 How the System Works (Simple Explanation)

```text
       [ User Uploads / Captures Leaf Photo ]
                         │
                         ▼
        [ Vision Transformer (ViT Backbone) ]
      (Breaks image into patches and scans leaf patterns)
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
 [ Plant Head ]                   [ Disease Head ]
 "This leaf is Tomato"            "The disease is Early Blight"
 (Checks 55 Crops)                (Checks 175 Diseases)
        │                                 │
        └────────────────┬────────────────┘
                         ▼
           [ Combined Match & Verification ]
             "Tomato — Early Blight (96.8% Confidence)"
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │  1. Instant Web Diagnosis               │
        │  2. Symptoms & Pathogen Cause           │
        │  3. Organic & Bio-Control Remedies      │
        │  4. Chemical Sprays (Fungicides/IPM)    │
        │  5. Prevention & Crop Rotation Steps    │
        │  6. Downloadable PDF Diagnostic Report  │
        └─────────────────────────────────────────┘
```

---

## 📊 Key Results & Performance

We tested our model under two different conditions:

### 1. Lab Test Benchmark (Clean Dataset — 8,226 Images)
- **Overall Accuracy**: **99.91%**
- **Precision / Macro F1**: **0.9730**
- **Confidence Calibration**: Near-zero error (predictions are highly confident only when correct).

### 2. Real-World Farm Benchmark (PlantDoc Field Photos — 236 Images)
- **Top-1 Accuracy**: **61.86%** (Correct primary diagnosis on real farm images with dirt, background noise, and sunlight).
- **Top-3 Accuracy**: **87.29%** (Correct diagnosis is within the top 3 suggestions in nearly 9 out of 10 cases).

---

## 🌾 Supported Crops (55 Total Agricultural Crops)

The system supports diagnosis and advisory across **55 major crops** grouped into 7 agricultural categories:

- **Cereals & Grains**: Rice (Paddy), Wheat, Corn (Maize), Bajra (Pearl Millet), Ragi (Finger Millet), Sorghum.
- **Cash Crops**: Sugarcane, Cotton, Jute, Tobacco, Sugar Beet.
- **Pulses & Beans**: Chickpea (Gram), Arhar (Pigeon Pea), Moong (Green Gram), Urad (Black Gram), Lentil, Soybean, Kidney Bean, Field Pea.
- **Vegetables**: Potato, Tomato, Bell Pepper, Chilli, Brinjal (Eggplant), Cabbage, Cauliflower, Squash / Cucurbits.
- **Fruits**: Apple, Banana, Citrus (Orange/Lemon), Grape, Mango, Guava, Papaya, Pomegranate, Peach, Plum, Apricot, Cherry, Strawberry, Blueberry.
- **Spices & Plantation**: Coffee, Tea, Cardamom, Coriander, Cumin, Fennel, Fenugreek, Garlic, Ginger, Onion, Turmeric.
- **Oilseeds**: Mustard, Groundnut (Peanut), Sunflower, Sesame, Castor.

---

## 🌿 5-Pillar Agricultural Advisory System

For every diagnosis, the system provides a structured 5-part treatment guide:

1. **Symptoms**: What to look for (spot colors, ring patterns, leaf curling, wilting).
2. **Cause**: The biological reason (fungus, bacteria, virus, or pest name and weather triggers).
3. **Organic Treatments**: Natural remedies (*Trichoderma*, *Neem oil*, bio-fungicides, copper soap).
4. **Chemical Treatments**: Recommended commercial sprays (Mancozeb, Azoxystrobin, Propiconazole) with dosage instructions.
5. **Prevention**: Long-term farm practices (crop rotation, proper spacing, drip irrigation).

---

## 💻 Full Application Features

- **Instant Image Diagnosis**: Drag-and-drop file upload or direct camera capture from phone/laptop.
- **User Accounts & Security**: Register and login system using secure JWT tokens and encrypted passwords.
- **Scan History**: Automatically saves every scan for logged-in users.
- **Personal Analytics Dashboard**: Visual charts showing total scans, healthy vs diseased breakdown, and most frequent crops.
- **Downloadable PDF Report**: Generates a professional 2-page diagnostic report with the leaf photo, confidence score, and complete treatment plan.
- **Disease Library**: A searchable public catalog containing detailed information on all 333 crop-disease categories.

---

## 📁 Project Directory Structure

```text
├── app.py                             # FastAPI backend web server & API routes
├── dpd_model.py                       # PyTorch Vision Transformer inference module
├── database.py                        # SQLite database & user authentication
├── pdf_generator.py                   # ReportLab 2-page PDF report generator
├── requirements.txt                   # List of Python dependencies
├── Dockerfile                         # Docker container configuration
├── templates/
│   └── index.html                     # Web frontend UI (HTML, CSS, JavaScript)
├── models_assets/
│   ├── model_b_partial_adapted.pth    # Trained ViT model weights (328 MB — see Setup)
│   ├── disease_info.json              # Complete advisory database (333 crop-disease pairs)
│   ├── class_names.json               # Supported category names
│   ├── dpd_55_plants.json             # 55 crops list
│   └── dpd_175_diseases.json          # 175 diseases list
├── scripts/                           # Training, evaluation & data preparation scripts
├── docs/                              # Research analysis & taxonomy documentation
├── test_app_e2e.py                    # End-to-end integration test suite
└── test_pdf_report.py                 # PDF report authorization test suite
```

---

## 🚀 How to Run the Project Locally

### Step 1: Clone the Project
```bash
git clone https://github.com/AnasSayed27/Multi-Crop_Plant_Disease_Detection.git
cd Multi-Crop_Plant_Disease_Detection
```

### Step 2: Create a Virtual Environment
```bash
# Windows:
python -m venv .venv
.venv\Scripts\activate

# Linux / Mac:
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Download Model Weights (Vision Transformer)

The trained ViT production model checkpoint (`model_b_partial_adapted.pth`, **328 MB**) can be downloaded automatically or manually:

**Option A — Automated Download (Recommended):**
```bash
python scripts/download_model.py
```

**Option B — Manual Download from Google Drive:**
1. Download [`model_b_partial_adapted.pth`](https://drive.google.com/file/d/1GdjtTcepE_VpGlrjZhBqDBBLma3rj_Bo/view?usp=sharing) (Direct Google Drive Link).
2. Save or move the file into the **`models_assets/`** folder:
   ```text
   models_assets/model_b_partial_adapted.pth
   ```

### Step 5: Configure Environment Variables (Optional)
```bash
cp .env.example .env
```

### Step 6: Start the Web Application
```bash
python app.py
```
Or with Uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to: **`http://localhost:8000`**

---

## 🧪 Automated Testing & Quality Assurance

Run the automated Pytest integration and unit test suite with one command:
```bash
pytest tests/ -v
```

---

## 🐳 Docker Deployment

You can build and deploy the application as a standalone container:
```bash
# Build container image
docker build -t crop-disease-detection .

# Run container
docker run -d -p 7860:7860 \
  -v $(pwd)/uploads:/code/uploads \
  -v $(pwd)/database.db:/code/database.db \
  --name plant-disease-app \
  crop-disease-detection
```

Access the containerized application at: **`http://localhost:7860`**

---

## 🛠️ Technology Stack

| Component | Technology Used | Purpose |
|---|---|---|
| **Deep Learning Framework** | PyTorch & Timm | Vision Transformer model training & inference |
| **Model Architecture** | ViT-Base (Dual Head) | Dual-head plant species and disease classification |
| **Backend API** | FastAPI (Python) | High-performance asynchronous REST API |
| **Database** | SQLite (WAL Mode) | Persistent transactional storage for users & scan history |
| **Authentication** | PyJWT & PBKDF2/Bcrypt | Secure token-based user login & constant-time password verification |
| **PDF Generation** | ReportLab | Automated clinical diagnostic report creation |
| **Testing & CI/CD** | Pytest & GitHub Actions | Automated integration testing and quality gates |
| **Containerization** | Docker | Reproducible container runtime with health probes |
| **Frontend UI** | HTML5, CSS3, JavaScript | Responsive user interface with Chart.js analytics |

---

## ⚖️ License
This project is licensed under the **MIT License**.
