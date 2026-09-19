# scripts/sections/sec_05_chapter3.py
import sys
sys.path.insert(0, 'scripts')
import report_data
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter3(doc, helpers):
    add_h1 = helpers['add_heading_1']
    add_h2 = helpers['add_heading_2']
    add_h3 = helpers['add_heading_3']
    add_p = helpers['add_body_p']
    add_bullet = helpers['add_bullet_p']
    add_tbl = helpers['add_table']
    add_callout = helpers['add_callout_box']

    # -------------------------------------------------------------
    # CHAPTER 3: SOFTWARE REQUIREMENTS SPECIFICATION (IEEE 830 SRS)
    # -------------------------------------------------------------
    add_h1("CHAPTER 3: SOFTWARE REQUIREMENTS SPECIFICATION (IEEE 830 SRS)")

    add_h2("3.1 Overview & Conformance to IEEE 830 SRS Standard")
    add_p("This chapter defines the formal Software Requirements Specification (SRS) for the Multi-Crop Plant Disease Detection and Advisory System. Conforming strictly to the IEEE 830-1998 Recommended Practice for Software Requirements Specifications, this document delineates the functional boundaries, operational constraints, system performance parameters, hardware infrastructure prerequisites, and feasibility criteria governing system development.")
    add_p("The primary engineering purpose of this system is to provide an accessible, fault-tolerant, and clinically actionable diagnostic service that accepts unconstrained foliar imagery from field farmers and extension agronomists, executes high-confidence dual-head Vision Transformer inference across 55 crops, and outputs five-pillar agronomic prescriptions accompanied by official clinical PDF reports.")

    add_h2("3.2 User Characteristics & Operational Environment")
    add_p("The system interfaces with three distinct user personas, each characterized by specific technical proficiencies and operational requirements:")
    add_bullet("Possess basic smartphone literacy. Primary requirement is a zero-friction, drag-and-drop or camera-capture interface with immediate visual diagnostic feedback in local languages, clear confidence indicators, and simple organic and chemical remedies without technical jargon.", bold_prefix="1. Primary Producers (Smallholder & Commercial Farmers): ")
    add_bullet("Possess formal agricultural training. Require access to Top-3 differential diagnostic alternatives, marginal plant and disease probabilities, chemical fungicide dosages, active chemical ingredients, and downloadable clinical PDF reports for field advisory documentation.", bold_prefix="2. Agricultural Extension Officers & Agronomists: ")
    add_bullet("Possess computer science and database proficiency. Require system health monitoring endpoints (/health, /health/ready), audit logging, database backup mechanisms in SQLite WAL mode, and secure administrative authentication.", bold_prefix="3. System Administrators & Research Analysts: ")

    add_p("The operational environment encompasses client devices operating on modern HTML5 web browsers (Google Chrome, Mozilla Firefox, Safari) across mobile (Android/iOS) and desktop platforms, communicating via HTTPS REST protocols with an asynchronous FastAPI application container hosted on Linux (Ubuntu 22.04 LTS / Debian 12) with optional NVIDIA CUDA acceleration.")

    add_h2("3.3 Functional Requirements Specification (FR-01 to FR-12)")
    add_p("The functional scope of the platform is decomposed into twelve formal Functional Requirements (FR-01 to FR-12), covering the complete diagnostic lifecycle from binary ingestion to persistent record storage.")

    fr_headers = ["Req ID", "Requirement Title", "Operational Functional Description", "Input Data Payload", "Expected Output"]
    fr_rows = [
        [
            fr['id'],
            fr['name'],
            fr['desc'],
            fr['input'],
            fr['output']
        ] for fr in report_data.FUNCTIONAL_REQUIREMENTS
    ]
    add_tbl(
        fr_headers,
        fr_rows,
        col_widths=[Inches(0.8), Inches(1.5), Inches(2.2), Inches(1.3), Inches(1.4)],
        caption="Table 3.1: Formal IEEE 830 Functional Requirements Specification (FR-01 to FR-12)"
    )

    add_h2("3.4 Non-Functional Requirements Specification (NFR-01 to NFR-10)")
    add_p("Non-functional requirements dictate the operational quality, security posture, computational efficiency, and maintainability of the software system under production workloads.")

    nfr_headers = ["Req ID", "Quality Category", "Metric Evaluated", "Technical Specification & Target", "Verification Method"]
    nfr_rows = [
        [
            nfr['id'],
            nfr['category'],
            nfr['metric'],
            nfr['specification'],
            nfr['verification']
        ] for nfr in report_data.NON_FUNCTIONAL_REQUIREMENTS
    ]
    add_tbl(
        nfr_headers,
        nfr_rows,
        col_widths=[Inches(0.8), Inches(1.1), Inches(1.3), Inches(2.2), Inches(1.8)],
        caption="Table 3.2: Formal IEEE 830 Non-Functional Requirements Specification (NFR-01 to NFR-10)"
    )

    add_h2("3.5 System Hardware & Infrastructure Specifications")
    add_p("To support both high-throughput neural inference and distributed edge access, the system specifies three tiers of hardware infrastructure:")

    hw_headers = ["Infrastructure Tier", "Component", "Minimum Specification", "Recommended Production Specification"]
    hw_rows = [
        ["Model Training Node", "Processor (CPU)", "8-Core Intel Core i7 / AMD Ryzen 7", "16-Core AMD EPYC / Intel Xeon Scalable"],
        ["Model Training Node", "Graphics (GPU)", "NVIDIA RTX 3060 (12 GB VRAM)", "NVIDIA A100 / RTX 4090 (24 GB VRAM)"],
        ["Model Training Node", "System Memory (RAM)", "32 GB DDR4-3200", "64 GB DDR5-4800 ECC"],
        ["Model Training Node", "Storage", "512 GB NVMe M.2 SSD", "2 TB PCIe Gen4 NVMe SSD (7000 MB/s)"],
        ["Inference Server Node", "Processor (CPU)", "4-Core x86_64 Processor (2.4 GHz)", "8-Core Intel Xeon / AMD EPYC (3.2 GHz)"],
        ["Inference Server Node", "Graphics (GPU)", "None (CPU Inference Fallback)", "NVIDIA T4 / RTX 3060 (Sub-150ms Latency)"],
        ["Inference Server Node", "System Memory (RAM)", "8 GB DDR4", "16 GB DDR4/DDR5"],
        ["Inference Server Node", "Storage", "50 GB Available SSD Space", "250 GB Enterprise NVMe SSD"],
        ["Inference Server Node", "Network Interface", "100 Mbps Ethernet", "1 Gbps Full-Duplex Optical Uplink"],
        ["Edge Client Device", "Form Factor", "Smartphone / Tablet / Laptop", "Modern Smartphone (Android 10+ / iOS 14+)"],
        ["Edge Client Device", "Browser Engine", "Chromium 90+, Safari 14+, Firefox 88+", "Latest Stable Chrome / Safari with WebGL"],
        ["Edge Client Device", "Camera Sensor", "5 Megapixel Auto-Focus Sensor", "12+ Megapixel Sensor with Macro Capability"],
        ["Edge Client Device", "Connectivity", "3G Cellular (>=384 Kbps)", "4G LTE / 5G / Wi-Fi (>=10 Mbps)"]
    ]
    add_tbl(
        hw_headers,
        hw_rows,
        col_widths=[Inches(1.5), Inches(1.3), Inches(2.1), Inches(2.3)],
        caption="Table 3.3: Hardware specifications for model training, production hosting, and edge client access"
    )

    add_h2("3.6 Software Stack & Runtime Dependency Specifications")
    add_p("The software environment is engineered around modern, open-source computational libraries optimized for asynchronous I/O and hardware-accelerated deep learning:")

    sw_headers = ["Software Layer", "Technology / Framework", "Version", "Architectural Role & Functional Justification"]
    sw_rows = [
        ["Operating System", "Ubuntu Linux / Debian", "22.04 LTS", "Stable POSIX runtime environment with robust kernel process isolation."],
        ["Programming Language", "Python", "3.10 / 3.11 / 3.12", "Primary execution runtime for machine learning and asynchronous backend."],
        ["Deep Learning Framework", "PyTorch", "2.0.0+", "Dynamic computational graph execution and tensor acceleration."],
        ["Vision Model Library", "Timm (PyTorch Image Models)", "0.9.2+", "Pre-trained Vision Transformer backbone (vit_base_patch16_224)."],
        ["Image Preprocessing", "Torchvision & PIL (Pillow)", "0.15.0+ / 10.0+", "Bicubic resizing, center cropping, and ImageNet tensor normalization."],
        ["Web API Framework", "FastAPI (Starlette / Pydantic)", "0.104.0+", "Asynchronous ASGI routing, OpenAPI schema generation, and validation."],
        ["ASGI Web Server", "Uvicorn", "0.24.0+", "Production-grade lightning-fast ASGI server with uvloop event loops."],
        ["Database Engine", "SQLite3 (WAL Mode Enabled)", "3.37.0+", "Embedded zero-configuration database with multi-reader concurrency."],
        ["Security & Auth", "PyJWT & Passlib (Bcrypt)", "2.8.0+ / 1.7.4+", "RFC 7519 JSON Web Token signing and salted password hashing."],
        ["Clinical PDF Generation", "ReportLab", "4.0.0+", "Programmable Flowable PDF layout engine for official agronomic reports."],
        ["Frontend Presentation", "HTML5 / Tailwind CSS / Vanilla JS", "ES6+ Standards", "Responsive, zero-dependency client UI with drag-and-drop file ingestion."]
    ]
    add_tbl(
        sw_headers,
        sw_rows,
        col_widths=[Inches(1.4), Inches(1.5), Inches(1.0), Inches(3.3)],
        caption="Table 3.4: Production software environment and runtime dependency specifications"
    )

    add_h2("3.7 Comprehensive Feasibility Study")
    add_p("Prior to full-scale architectural implementation, a four-tier feasibility assessment was conducted:")
    add_bullet("The technical feasibility is confirmed by the availability of mature, open-source Vision Transformer backbones (vit_base_patch16_224) capable of fine-tuning on consumer-grade GPUs (NVIDIA RTX 3060). Model forward pass latency is established at 138ms on GPU and 1350ms on CPU—well within real-time agricultural requirements. FastAPI provides mature asynchronous event loops, while SQLite WAL mode satisfies multi-reader transaction needs without heavyweight database server overhead.", bold_prefix="1. Technical Feasibility: ")
    add_bullet("The operational feasibility is exceptionally high. The platform requires zero native application installation; farmers access the service via standard mobile web browsers. The drag-and-drop interface provides immediate diagnostic results, while the 5-pillar advisory eliminates complex technical jargon, delivering actionable organic and chemical treatment instructions directly to field producers.", bold_prefix="2. Operational Feasibility: ")
    add_bullet("The economic feasibility is compelling. Traditional laboratory PCR foliar testing incurs 0 to 00 per sample. The proposed computational solution operates at near-zero marginal cost per scan (<bash.001 in electricity and cloud compute). Open-source licensing across all libraries (PyTorch, FastAPI, SQLite) eliminates commercial software license expenditures.", bold_prefix="3. Economic Feasibility: ")
    add_bullet("The system adheres strictly to user data privacy guidelines. Only foliar imagery and scan timestamps are recorded; personal farmer identities remain decoupled. Chemical treatment advisories comply with standard Integrated Pest Management (IPM) regulatory guidelines, explicitly noting chemical pre-harvest intervals (PHI) to prevent food contamination.", bold_prefix="4. Legal, Ethical & Safety Feasibility: ")

    doc.add_page_break()