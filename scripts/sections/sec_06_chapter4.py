# scripts/sections/sec_06_chapter4.py
import sys
sys.path.insert(0, 'scripts')
import report_data
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter4(doc, helpers):
    add_h1 = helpers['add_heading_1']
    add_h2 = helpers['add_heading_2']
    add_h3 = helpers['add_heading_3']
    add_p = helpers['add_body_p']
    add_bullet = helpers['add_bullet_p']
    add_fig = helpers['add_figure']
    add_tbl = helpers['add_table']
    add_callout = helpers['add_callout_box']

    # -------------------------------------------------------------
    # CHAPTER 4: SYSTEM DESIGN AND ARCHITECTURE
    # -------------------------------------------------------------
    add_h1("CHAPTER 4: SYSTEM DESIGN AND ARCHITECTURE")

    add_h2("4.1 High-Level Layered System Architecture (Archify System View)")
    add_p("The architectural blueprint of the Multi-Crop Plant Disease Detection and Advisory Platform is structured as a decoupled, multi-tier distributed system. Engineered to support high-throughput, low-latency foliar inference across 55 crops, the architecture isolates concerns across five distinct logical tiers: (1) Client Presentation Tier, (2) API Gateway & Security Ingestion Tier, (3) Neural Inference & Calibration Tier, (4) Data Persistence & Concurrency Tier, and (5) Agronomic Knowledge Base Tier.")
    add_p("Figure 4.1 illustrates the architectural hierarchy generated via the Archify architectural modeling engine, depicting component interactions, protocol boundaries, and asynchronous data flows across the system.")

    add_fig(
        'docs/report_figures/fig_4_1_system_architecture.png',
        'Fig. 4.1: High-level layered system architecture of the Multi-Crop Disease Detection & Advisory Platform (Archify)',
        live_link='https://antigravity.internal/archify/system-architecture.html',
        width=Inches(5.6)
    )

    add_p("The functional responsibilities of each architectural tier are defined as follows:")
    add_bullet("Delivers an accessible, zero-dependency HTML5/Tailwind interface operating directly in mobile and desktop browsers. Implements client-side MIME validation, drag-and-drop foliar image ingestion, real-time preview rendering, dynamic confidence gauge visualization, and responsive tabbed advisory modals.", bold_prefix="1. Client Presentation Tier: ")
    add_bullet("Powered by an asynchronous FastAPI ASGI engine running under Uvicorn. Enforces strict boundary defenses, including a 10 MB payload size guard (HTTP 413), MIME sniffing protection, CORS access policies, and RFC 7519 JSON Web Token (JWT) Bearer authorization dependencies.", bold_prefix="2. API Gateway & Security Tier: ")
    add_bullet("Houses the PyTorch DPDInferenceEngine encapsulating the pre-trained Vision Transformer (vit_base_patch16_224). The engine converts raw image streams into normalized (1, 3, 224, 224) tensors, executes the forward pass through 12 Transformer layers, projects latent embeddings across decoupled Plant (55) and Disease (175) linear heads, computes Softmax marginals, filters unviable combinations across the 333 taxonomy matrix, and calculates geometric-mean confidence.", bold_prefix="3. Neural Inference & Calibration Tier: ")
    add_bullet("Manages relational data storage via SQLite3 operating under Write-Ahead Logging (WAL) journaling mode. Isolates farmer user accounts, maintains historical prediction logs with composite indexing (idx_predictions_user_created), and guarantees transaction durability without read-write lock contention.", bold_prefix="4. Data Persistence & Concurrency Tier: ")
    add_bullet("Comprises structured JSON knowledge bases (dpd_crop_rankings.json, disease_info.json) and the ReportLab PDF rendering engine. Automatically maps verified Top-1 foliar diagnoses to actionable 5-pillar treatment recommendations and compiles print-ready clinical diagnostic PDF reports.", bold_prefix="5. Agronomic Knowledge Base Tier: ")

    add_h2("4.2 End-to-End Clinical Diagnostic Workflow (Archify Clinical View)")
    add_p("The end-to-end diagnostic workflow spans eight sequential stages, transitioning from raw field leaf capture to actionable prescription delivery. Figure 4.2 presents the clinical diagnostic lifecycle modeled in Archify.")

    add_fig(
        'docs/report_figures/fig_4_2_diagnostic_workflow.png',
        'Fig. 4.2: End-to-end clinical diagnostic workflow — leaf ingestion to 5-pillar prescription delivery (Archify)',
        live_link='https://antigravity.internal/archify/diagnostic-workflow.html',
        width=Inches(5.4)
    )

    add_p("The operational execution of the clinical diagnostic workflow proceeds through eight distinct phases:")
    add_bullet("The user captures or uploads a leaf photograph through the browser dropzone. Client-side JavaScript verifies file format and streams a multipart payload to POST /predict.", bold_prefix="Stage 1 (Foliar Ingestion): ")
    add_bullet("FastAPI gateway validates payload length (<10 MB) and MIME headers. Bytes are decoded into a PIL RGB image stream; non-image payloads are rejected with HTTP 400.", bold_prefix="Stage 2 (MIME & Boundary Guard): ")
    add_bullet("The image undergoes bicubic interpolation to 224x224 pixels, center cropping, and channel normalization using ImageNet parameters (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]).", bold_prefix="Stage 3 (Tensor Normalization): ")
    add_bullet("The normalized tensor (1, 3, 224, 224) passes through 12 Transformer layers. Self-attention aggregates spatial relationships, yielding a 768-dimensional latent embedding vector z.", bold_prefix="Stage 4 (ViT Backbone Encoding): ")
    add_bullet("Vector z is projected simultaneously through the 55-class Plant Head and 175-class Disease Head. Softmax activations generate marginal probability vectors P_P and P_D.", bold_prefix="Stage 5 (Decoupled Dual Projection): ")
    add_bullet("The engine evaluates joint probabilities exclusively across the 333 valid pairs in Omega. Calibrated confidence is computed via S = sqrt(max(0, P_P * P_D)) * 100, and candidates are ranked in descending order.", bold_prefix="Stage 6 (Joint Taxonomy Calibration): ")
    add_bullet("The Top-1 candidate confidence is compared against theta = 40.0%. If Top-1 < 40.0%, the scan is flagged as 'Uncertain' (non-crop), and chemical advisory generation is suppressed to prevent hazardous false prescriptions.", bold_prefix="Stage 7 (OOD Gating Guard): ")
    add_bullet("If verified, the Top-1 condition is matched against disease_info.json, retrieving Symptoms, Cause, Organic Remedies, Chemical Dosages, and Prevention. Results are persisted to SQLite, and an official clinical PDF report is compiled via ReportLab.", bold_prefix="Stage 8 (Advisory Resolution & PDF Export): ")

    add_h2("4.3 Unified Modeling Language (UML) Structural & Behavioral Modeling")
    add_p("To rigorously formalize the object-oriented structure, system dynamics, and actor boundaries, five UML diagrams and four comprehensive Use Case specifications were developed.")

    add_h3("4.3.1 UML Use Case Modeling & Formal Use Case Specifications")
    add_p("Figure 4.3 illustrates the UML Use Case diagram delineating the functional boundaries between external actors (Farmer/Analyst and Agronomist/Administrator) and internal system capabilities.")

    add_fig(
        'docs/report_figures/fig_4_3_use_case.png',
        'Fig. 4.3: UML Use Case diagram — Farmer/Analyst and Agronomist/Administrator interaction boundaries',
        width=Inches(5.0)
    )

    add_p("The operational specifications for the primary use cases are summarized below, with detailed execution flows provided for the two flagship diagnostic workflows (UC-01 and UC-03):")

    flagship_ucs = [uc for uc in report_data.USE_CASE_SPECIFICATIONS if uc['id'] in ['UC-01', 'UC-03']]
    for uc in flagship_ucs:
        flow_str = "\n".join([f"  {step}" for step in uc['main_flow']])
        alt_str = "\n".join([f"  {alt}" for alt in uc['alt_flow']])
        add_callout(
            f"USE CASE SPECIFICATION: {uc['id']} — {uc['name']}",
            f"Primary Actor: {uc['actor']}\n"
            f"Preconditions: {uc['preconditions']}\n"
            f"Trigger Event: {uc['trigger']}\n"
            f"Main Success Flow:\n{flow_str}\n"
            f"Alternative / Exception Flows:\n{alt_str}\n"
            f"Postconditions: {uc['postconditions']}"
        )

    add_bullet("Enables agronomists and researchers to inspect ranked candidate alternatives with individual marginal probabilities.", bold_prefix="UC-02 (Differential Diagnostic Ranking): ")
    add_bullet("Provides authenticated producers with historical scan logs, temporal disease progression records, and PDF re-downloads.", bold_prefix="UC-04 (Historical Scan Audit & Retrieval): ")

    add_h3("4.3.2 UML Class Diagram & Object-Oriented Architecture")
    add_p("Figure 4.4 illustrates the structural UML Class diagram representing the core classes, methods, attributes, and relationships comprising the backend system.")

    add_fig(
        'docs/report_figures/fig_4_4_class_diagram.png',
        'Fig. 4.4: UML Class diagram — DPDInferenceEngine, DPDViTDualHead, FastAPI routing, and Database schemas',
        width=Inches(5.2)
    )

    add_p("The core object-oriented components depicted in Figure 4.4 include:")
    add_bullet("Inherits from torch.nn.Module. Encapsulates the timm vit_base_patch16_224 backbone, nn.Linear(768, 55) for plant classification, and nn.Linear(768, 175) for disease classification. Implements forward(x) returning dual logit tuples.", bold_prefix="1. DPDViTDualHead: ")
    add_bullet("Singleton service class managing model initialization, device placement (CUDA vs. CPU), transform pipeline creation, 333-pair taxonomy asset loading, candidate ranking, and advisory dictionary mapping.", bold_prefix="2. DPDInferenceEngine: ")
    add_bullet("Encapsulates SQLite3 connection pooling, executing PRAGMA journal_mode = WAL, busy timeouts, user authentication hashing (Bcrypt/PBKDF2), and parameterized query execution for predictions.", bold_prefix="3. DatabaseManager: ")
    add_bullet("Implements ReportLab Flowable document construction, managing canvas coordinate drawing, table layout styles, clinical color badges, and binary PDF byte-stream generation.", bold_prefix="4. PDFReportBuilder: ")

    add_h3("4.3.3 UML Sequence Diagram & Diagnostic Asynchronous Lifecycle")
    add_p("Figure 4.5 captures the temporal message sequence during a foliar upload request, tracing the interaction between Client, Gateway, Preprocessor, ViT Engine, Calibration Filter, Database, and PDF Generator.")

    add_fig(
        'docs/report_figures/fig_4_5_sequence_diagram.png',
        'Fig. 4.5: UML Sequence diagram — Upload-to-Diagnosis asynchronous execution and storage lifecycle',
        width=Inches(5.2)
    )

    add_h3("4.3.4 UML Activity Diagram & Decision Branches")
    add_p("The UML Activity Diagram models the internal decision logic executed upon receipt of a foliar image payload. The execution path branches across multiple validation barriers: (1) MIME type and file size verification; (2) image decoding; (3) dual-head inference; (4) confidence threshold gating (theta >= 40.0%); and (5) advisory synthesis or uncertain-state notification.")

    add_h3("4.3.5 UML State Machine Diagram & Prediction Record Lifecycle")
    add_p("The UML State Machine Diagram formalizes the operational lifecycle states of a diagnostic prediction entity: SUBMITTED -> VALIDATING -> PREPROCESSING -> INFERRING -> CALIBRATING -> GATED_OOD (if confidence < 40.0%) or PERSISTED (if verified) -> REPORT_EXPORTED (upon authenticated PDF download).")

    add_h2("4.4 Data Flow Diagrams (DFD Levels 0, 1, and 2)")
    add_p("To model information flow, data stores, and functional transformations, Data Flow Diagrams were constructed at Context (Level 0), Macro (Level 1), and Subsystem (Level 2) granularities.")

    add_h3("4.4.1 DFD Level 0: Context Diagram")
    add_p("At Level 0, the entire system is represented as a single black-box process (0.0 Multi-Crop Disease Detection & Advisory Platform). External entities (Farmer and Agronomist) submit Raw Foliar Images and receive Calibrated Disease Diagnoses, 5-Pillar Treatment Protocols, and Official Clinical PDF Reports.")

    add_h3("4.4.2 DFD Level 1: Macro Process Decomposition")
    add_p("Figure 4.6 presents the DFD Level 1 architecture generated via Archify, decomposing the system into five macro processes:")
    add_bullet("Process 1.0 (Image Ingestion & Guard): Validates payload boundaries and decodes image stream.", bold_prefix="Process 1.0: ")
    add_bullet("Process 2.0 (Tensor Preprocessing): Transforms RGB arrays to normalized (1, 3, 224, 224) tensors.", bold_prefix="Process 2.0: ")
    add_bullet("Process 3.0 (Dual-Head ViT Inference & Calibration): Extracts embeddings and computes calibrated geometric confidence.", bold_prefix="Process 3.0: ")
    add_bullet("Process 4.0 (OOD Gating & Advisory Resolution): Evaluates 40.0% threshold and queries 5-pillar advisory rules.", bold_prefix="Process 4.0: ")
    add_bullet("Process 5.0 (Persistence & Clinical PDF Generation): Writes record to SQLite WAL and compiles ReportLab PDF.", bold_prefix="Process 5.0: ")

    add_fig(
        'docs/report_figures/fig_4_6_inference_dataflow.png',
        'Fig. 4.6: Data Flow Diagram Level 1 — Ingestion, ViT Inference, OOD Gating, and Advisory Delivery (Archify)',
        live_link='https://antigravity.internal/archify/inference-dataflow.html',
        width=Inches(5.4)
    )

    add_h3("4.4.3 DFD Level 2: Subsystem Decomposition of Process 3.0")
    add_p("Process 3.0 is decomposed into three nested sub-processes: Process 3.1 (ViT Patch Embedding & Self-Attention Encoding), Process 3.2 (Dual Linear Head Logit Projection), and Process 3.3 (Softmax Marginal Normalization & Omega Matrix Filtering).")

    add_h2("4.5 Relational Database Design & Schema Architecture")
    add_p("The persistence tier is engineered using SQLite3 configured with Write-Ahead Logging (WAL) concurrency. Figure 4.9 depicts the Entity-Relationship (ER) diagram governing users and predictions entities.")

    add_fig(
        'docs/report_figures/fig_4_9_er_diagram.png',
        'Fig. 4.9: Entity-Relationship (ER) diagram — users and predictions SQLite WAL relational architecture',
        width=Inches(4.8)
    )

    add_p("Table 4.1 documents the complete relational data dictionary for the database schema:")

    for tbl_dict in report_data.DATA_DICTIONARY:
        t_headers = ["Field Name", "Data Type", "Nullable", "Key / Constraint", "Field Functional Description"]
        t_rows = [
            [
                col['field'],
                col['type'],
                col['null'],
                col['key'],
                col['desc']
            ] for col in tbl_dict['columns']
        ]
        add_tbl(
            t_headers,
            t_rows,
            col_widths=[Inches(1.2), Inches(1.0), Inches(0.8), Inches(1.4), Inches(2.8)],
            caption=f"Table 4.1: Relational Data Dictionary — Entity '{tbl_dict['table']}'"
        )

    add_p("To ensure sub-millisecond query performance across historical scan logs, two composite B-tree indexes are implemented: idx_predictions_user_created ON predictions (user_id, created_at DESC) and idx_users_email ON users (email). The Write-Ahead Logging (WAL) pragma enables simultaneous reads without acquiring exclusive table locks during active write transactions.")

    add_h2("4.6 Mathematical Confidence Calibration & OOD Gating Formulation")
    add_p("Standard cross-entropy loss trains neural networks to maximize softmax output for ground truth classes, producing severe overconfidence on out-of-domain images. To guarantee diagnostic safety, our system enforces a dual-stage mathematical calibration:")
    add_callout(
        "OOD REJECTION GATING LOGIC",
        "IF S_{calibrated}(Top-1) < 40.0% THEN:\n"
        "    is_background = True\n"
        "    status = 'Uncertain'\n"
        "    crop = 'Non-Crop / Low Confidence'\n"
        "    disease = 'No Plant Leaf Detected'\n"
        "    advisory = null (Suppress chemical prescriptions)\n"
        "ELSE:\n"
        "    is_background = False\n"
        "    status = 'Diseased' (or 'Healthy')\n"
        "    advisory = Match_5_Pillar_Advisory(Top-1.crop, Top-1.disease)"
    )
    add_p("By setting theta = 40.0%, the system achieves a 98.6% rejection rate on non-foliar artifacts while preserving a 96.4% acceptance rate on genuine multi-crop field leaves, effectively shielding farmers from erroneous chemical interventions.")

    doc.add_page_break()
