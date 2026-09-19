# scripts/sections/sec_11_appendices.py
import os
import json
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_appendices(doc, helpers):
    add_h1 = helpers['add_heading_1']
    add_h2 = helpers['add_heading_2']
    add_h3 = helpers['add_heading_3']
    add_p = helpers['add_body_p']
    add_bullet = helpers['add_bullet_p']
    add_code = helpers['add_code_block']
    add_tbl = helpers['add_table']
    add_callout = helpers['add_callout_box']

    # -------------------------------------------------------------
    # APPENDIX A: BOTANICAL & PATHOLOGICAL TAXONOMY SPECIFICATION
    # -------------------------------------------------------------
    add_h1("APPENDIX A: BOTANICAL & PATHOLOGICAL TAXONOMY SPECIFICATION")
    add_p("This appendix specifies the biologically verified taxonomy matrix Omega spanning 55 botanical crop species, 175 pathological conditions, and exactly 333 valid crop-disease co-occurrence pairs supported by the DPD ViT-Base dual-head inference engine. The dual linear projection heads map botanical identity to Plant Head indices [0 to 54] and pathological condition to Disease Head indices [0 to 174].")
    add_p("The complete production knowledge base is serialized in models_assets/dpd_crop_rankings.json. Table A.1 summarizes the distribution across the eight commercial botanical families, while Table A.2 presents representative flagship diagnostic pairs across all families.")

    fam_headers = ["Botanical Family", "Representative Crops", "Species Count", "Supported Disease Pairs", "Primary Pathological Etiologies"]
    fam_rows = [
        ["Solanaceae (Nightshades)", "Potato, Tomato, Pepper, Eggplant", "4", "48 Pairs", "Early/Late Blight, Bacterial Spot, Mosaic Virus, Septoria"],
        ["Cucurbitaceae (Cucurbits)", "Cucumber, Squash, Watermelon, Melon", "4", "32 Pairs", "Powdery Mildew, Downy Mildew, Anthracnose, Scab"],
        ["Poaceae (Gramineae)", "Corn (Maize), Wheat, Rice, Barley", "4", "36 Pairs", "Northern Leaf Blight, Common Rust, Blast, Brown Spot"],
        ["Rosaceae (Pome/Stone)", "Apple, Peach, Cherry, Strawberry", "5", "42 Pairs", "Apple Scab, Black Rot, Cedar Rust, Powdery Mildew"],
        ["Fabaceae (Legumes)", "Soybean, Common Bean, Pea, Chickpea", "4", "28 Pairs", "Rust, Angular Leaf Spot, Frogeye Leaf Spot, Bacterial Blight"],
        ["Vitaceae (Vine Crops)", "Grape (Table, Wine varieties)", "1", "16 Pairs", "Black Rot, Esca (Black Measles), Leaf Blight, Healthy"],
        ["Brassicaceae (Crucifers)", "Cabbage, Cauliflower, Broccoli", "3", "22 Pairs", "Black Rot, Downy Mildew, Alternaria Leaf Spot"],
        ["Rutaceae (Citrus)", "Orange, Lemon, Lime, Grapefruit", "4", "26 Pairs", "Citrus Greening (HLB), Citrus Canker, Black Spot"],
        ["Specialty / Cash Crops", "Cotton, Coffee, Tea, Sugarcane, Cassava", "26", "83 Pairs", "Bacterial Blight, Coffee Leaf Rust, Mosaic, Red Rot"]
    ]
    add_tbl(
        fam_headers,
        fam_rows,
        col_widths=[Inches(1.5), Inches(1.8), Inches(0.8), Inches(1.2), Inches(2.2)],
        caption="Table A.1: Botanical Family Taxonomy Distribution Matrix (55 Crops, 333 Verified Pairs)"
    )

    # Load representative 50 pairs across major families
    assets_dir = "models_assets"
    rankings_p = os.path.join(assets_dir, "dpd_crop_rankings.json")
    plants_p = os.path.join(assets_dir, "dpd_55_plants.json")
    diseases_p = os.path.join(assets_dir, "dpd_175_diseases.json")

    rep_pairs_data = []
    if os.path.exists(rankings_p) and os.path.exists(plants_p) and os.path.exists(diseases_p):
        with open(plants_p, "r", encoding="utf-8") as f:
            plants_dict = json.load(f)
        with open(diseases_p, "r", encoding="utf-8") as f:
            diseases_dict = json.load(f)
        with open(rankings_p, "r", encoding="utf-8") as f:
            crops_list = json.load(f)

        p_to_idx = {v.lower().strip().replace(" ", "_"): int(k) for k, v in plants_dict.items()}
        d_to_idx = {v.lower().strip().replace(" ", "_"): int(k) for k, v in diseases_dict.items()}

        pair_idx = 1
        for c in crops_list:
            c_slug = c["crop"].lower().strip().replace(" ", "_")
            p_idx = p_to_idx.get(c_slug, 0)
            c_display = c_slug.replace("_", " ").title()

            # Select up to 2 representative diseases per crop (including healthy)
            diseases_items = list(c.get("all_diseases", {}).items())
            selected = diseases_items[:2]

            for d_name, d_meta in selected:
                d_slug = d_name.lower().strip().replace(" ", "_")
                d_idx = d_to_idx.get(d_slug, 0)
                d_display = d_slug.replace("_", " ").title()
                etiology = "Healthy Foliage" if "healthy" in d_slug else ("Bacterial Infection" if "bacterial" in d_slug else ("Viral Pathogen" if "virus" in d_slug or "mosaic" in d_slug or "curl" in d_slug else "Fungal Pathogen"))

                rep_pairs_data.append([
                    f"P-{pair_idx:03d}",
                    c_display,
                    d_display,
                    f"[{p_idx}, {d_idx}]",
                    etiology
                ])
                pair_idx += 1
                if len(rep_pairs_data) >= 32:
                    break
            if len(rep_pairs_data) >= 32:
                break

    tax_headers = ["Pair ID", "Botanical Host Crop", "Pathological Condition", "Head Indices [P, D]", "Diagnostic Etiology"]
    add_tbl(
        tax_headers,
        rep_pairs_data,
        col_widths=[Inches(0.9), Inches(1.6), Inches(2.1), Inches(1.3), Inches(1.4)],
        caption=f"Table A.2: Representative Multi-Crop Taxonomy Dictionary (32 Key Crop-Disease Pairs Across All 8 Families)"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX B: COMPLETE REST API OPENAPI / SWAGGER SPECIFICATION
    # -------------------------------------------------------------
    add_h1("APPENDIX B: COMPLETE REST API OPENAPI / SWAGGER SPECIFICATION")
    add_p("The DPD ViT-Base platform exposes a fully compliant OpenAPI v3.0 REST interface documented in Table B.1. All endpoints support standard HTTP status codes, structured JSON payloads, and JWT Bearer authorization.")

    api_headers = ["HTTP Method", "Endpoint URI Path", "Access Control", "Request Payload / Parameters", "Response Schema & Success Output"]
    api_rows = [
        ["GET", "/health", "Public", "None", "200 OK: {'status': 'ok'}"],
        ["GET", "/health/ready", "Public", "None", "200 OK: {'status': 'ready', 'model_loaded': true, 'database_connected': true}"],
        ["POST", "/api/register", "Public", "JSON: {username, email, password}", "200 OK: {user_id, access_token, token_type: 'bearer'}"],
        ["POST", "/api/login", "Public", "JSON: {username_or_email, password}", "200 OK: {user_id, access_token, token_type: 'bearer'}"],
        ["POST", "/predict", "Public / Optional Bearer", "Multipart: file (Image, <=10MB)", "200 OK: {crop, disease, confidence, status, top_3, advisory}"],
        ["POST", "/api/predict", "Public / Optional Bearer", "Multipart: file (Image, <=10MB)", "200 OK: (Identical schema to /predict for REST standard)"],
        ["GET", "/api/history", "Bearer JWT Required", "Query: ?limit=50 (Default 50)", "200 OK: Array of {id, crop, disease, confidence, created_at}"],
        ["GET", "/api/prediction/{id}/pdf", "Bearer JWT Required (IDOR Guard)", "Path parameter: id (int)", "200 OK: Binary application/pdf stream with clinical report"],
        ["GET", "/api/statistics", "Bearer JWT Required", "None", "200 OK: {total_scans, healthy_count, diseased_count, top_disease}"],
        ["GET", "/api/library", "Public", "None", "200 OK: Deduplicated array of supported (crop, disease) descriptions"]
    ]
    add_tbl(
        api_headers,
        api_rows,
        col_widths=[Inches(1.0), Inches(1.8), Inches(1.5), Inches(1.8), Inches(2.2)],
        caption="Table B.1: Formal REST API Endpoint Specifications & Architectural Contracts"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX C: SYSTEM INSTALLATION & PRODUCTION DEPLOYMENT GUIDE
    # -------------------------------------------------------------
    add_h1("APPENDIX C: SYSTEM INSTALLATION & PRODUCTION DEPLOYMENT GUIDE")
    add_p("This appendix provides production deployment specifications for containerized and systemd-managed installations on Ubuntu 22.04 LTS servers.")

    add_h2("C.1 Production Systemd Service Unit Configuration")
    add_p("To manage the FastAPI ASGI application as an enterprise daemon with automatic restart capabilities, configure the systemd unit file at /etc/systemd/system/dpd-vision.service:")

    systemd_conf = """[Unit]
Description=Multi-Crop Plant Disease Detection & Advisory Service (FastAPI ASGI)
After=network.target

[Service]
Type=simple
User=sober
WorkingDirectory=/media/sober/Windows-SSD/Users/sober/D_Files/Projects/Computer-Vision-ML/Potato_disease
Environment="PATH=/media/sober/Windows-SSD/Users/sober/D_Files/.envs/env-ml-vision/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="DB_PATH=database.db"
ExecStart=/media/sober/Windows-SSD/Users/sober/D_Files/.envs/env-ml-vision/bin/uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4 --loop uvloop
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target"""
    add_code("Systemd Service: /etc/systemd/system/dpd-vision.service", systemd_conf)

    add_h2("C.2 Production Nginx Reverse Proxy Configuration")
    add_p("To handle client SSL/TLS termination, enforce 10 MB upload buffers, and serve static assets efficiently, configure Nginx at /etc/nginx/sites-available/dpd.conf:")

    nginx_conf = """server {
    listen 80;
    server_name plant-disease.internal agri-diagnostics.org;

    # Enforce 10 MB maximum request payload guard at reverse proxy boundary
    client_max_body_size 10M;

    location /static/ {
        alias /media/sober/Windows-SSD/Users/sober/D_Files/Projects/Computer-Vision-ML/Potato_disease/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }
}"""
    add_code("Nginx Configuration: /etc/nginx/sites-available/dpd.conf", nginx_conf)

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX D: 5-PILLAR AGRICULTURAL ADVISORY PROTOCOLS (SAMPLE)
    # -------------------------------------------------------------
    add_h1("APPENDIX D: 5-PILLAR AGRICULTURAL ADVISORY PROTOCOLS (SAMPLE)")
    add_p("This appendix details sample clinical agronomic treatment protocols extracted from the system's knowledge base (disease_info.json) for two major foliar pathogens, illustrating the clinical depth of the advisory engine.")

    sample_diseases = [
        {
            "name": "Potato Early Blight (Alternaria solani)",
            "crop": "Potato (Solanum tuberosum)",
            "symptoms": "Dark brown to black necrotic spots with characteristic concentric rings ('target board' pattern) appearing first on older lower foliage, surrounded by chlorotic yellow halos.",
            "cause": "Airborne fungal pathogen Alternaria solani; favored by warm temperatures (24-29°C) and alternating wet and dry periods.",
            "organic": "Foliar spray with Copper Hydroxide (2.5 g/L) or Bacillus subtilis biocontrol formulations at initial symptom onset.",
            "chemical": "Preventive spray with Mancozeb 75% WP (2 g/L) alternating with Difenoconazole 25% EC (0.5 mL/L); Pre-Harvest Interval (PHI): 14 days.",
            "prevention": "Implement 3-year crop rotation avoiding Solanaceous hosts; utilize certified disease-free seed tubers; install drip irrigation to prevent foliar wetting."
        },
        {
            "name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
            "crop": "Tomato (Solanum lycopersicum)",
            "symptoms": "Severe upward curling and cupping of leaflet margins; interveinal chlorosis; dramatic internode stunting yielding a bushy, erect canopy; complete floral abortion.",
            "cause": "Begomovirus transmitted persistently by the silverleaf whitefly (Bemisia tabaci); non-seed transmitted.",
            "organic": "Apply yellow sticky cards (30-40 traps/hectare) for whitefly monitoring; foliar spray with cold-pressed Neem oil (3%) or Beauveria bassiana.",
            "chemical": "Target insect vector with Imidacloprid 17.8% SL (0.3 mL/L) or Acetamiprid 20% SP (0.2 g/L) during early nursery and vegetative stages.",
            "prevention": "Install 50-mesh insect-proof netting in seedling nurseries; maintain weed-free buffer zones; rogue and burn infected symptomatic plants immediately."
        }
    ]

    for sd in sample_diseases:
        sd_body = (
            f"Host Crop: {sd['crop']}\n"
            f"1. Symptoms: {sd['symptoms']}\n"
            f"2. Cause / Etiology: {sd['cause']}\n"
            f"3. Certified Organic Remedies: {sd['organic']}\n"
            f"4. Chemical Control & Dosages: {sd['chemical']}\n"
            f"5. Cultural Prevention Practices: {sd['prevention']}"
        )
        add_callout(
            f"5-PILLAR PROTOCOL: {sd['name']}",
            sd_body
        )
