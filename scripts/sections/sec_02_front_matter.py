# scripts/sections/sec_02_front_matter.py
import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_front_matter(doc, helpers):
    add_h1 = helpers['add_heading_1']
    add_h2 = helpers['add_heading_2']
    add_p = helpers['add_body_p']
    add_tbl = helpers['add_table']
    set_bg = helpers['set_cell_background']
    set_mar = helpers['set_cell_margins']
    set_cant_split = helpers['set_row_cant_split']

    # -------------------------------------------------------------
    # 1. COVER / TITLE PAGE (PAGE 1)
    # -------------------------------------------------------------
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(24)
    p_top.paragraph_format.space_after = Pt(12)
    r_deg = p_top.add_run("A DISSERTATION REPORT ON\n")
    r_deg.font.name = 'Calibri'
    r_deg.font.size = Pt(12)
    r_deg.font.bold = True
    r_deg.font.color.rgb = RGBColor(85, 85, 85)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(18)
    r_t = p_title.add_run("MULTI-CROP PLANT DISEASE DETECTION AND ADVISORY SYSTEM USING DUAL-HEAD VISION TRANSFORMER (DPD ViT-BASE)")
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(16)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(27, 94, 32)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(28)
    r_sub = p_sub.add_run("Submitted in partial fulfillment of the requirements for the Degree of\nBachelor of Science in Computer Science (B.Sc. CS)\n")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(60, 60, 60)

    # Author Box Table
    author_table = doc.add_table(rows=1, cols=2)
    author_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_l = author_table.cell(0, 0)
    cell_r = author_table.cell(0, 1)
    cell_l.width = Inches(3.0)
    cell_r.width = Inches(3.0)
    set_cant_split(author_table.rows[0])

    p_l1 = cell_l.paragraphs[0]
    p_l1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l1.paragraph_format.space_before = Pt(4)
    p_l1.paragraph_format.space_after = Pt(2)
    r_sub = p_l1.add_run("SUBMITTED BY:")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(9.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(85, 85, 85)

    p_l2 = cell_l.add_paragraph()
    p_l2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l2.paragraph_format.space_before = Pt(0)
    p_l2.paragraph_format.space_after = Pt(2)
    r_name = p_l2.add_run("ANAS MOINUDDIN SAYED")
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(11)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(27, 94, 32)

    p_l3 = cell_l.add_paragraph()
    p_l3.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l3.paragraph_format.space_before = Pt(0)
    p_l3.paragraph_format.space_after = Pt(1)
    r_roll = p_l3.add_run("Roll No: CS-9130")
    r_roll.font.name = 'Calibri'
    r_roll.font.size = Pt(9.5)
    r_roll.font.color.rgb = RGBColor(50, 50, 50)

    p_l4 = cell_l.add_paragraph()
    p_l4.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l4.paragraph_format.space_before = Pt(0)
    p_l4.paragraph_format.space_after = Pt(4)
    r_dept = p_l4.add_run("Department of Computer Science")
    r_dept.font.name = 'Calibri'
    r_dept.font.size = Pt(9.5)
    r_dept.font.color.rgb = RGBColor(50, 50, 50)

    p_r1 = cell_r.paragraphs[0]
    p_r1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_r1.paragraph_format.space_before = Pt(4)
    p_r1.paragraph_format.space_after = Pt(2)
    r_guide_title = p_r1.add_run("UNDER THE GUIDANCE OF:")
    r_guide_title.font.name = 'Calibri'
    r_guide_title.font.size = Pt(9.5)
    r_guide_title.font.bold = True
    r_guide_title.font.color.rgb = RGBColor(85, 85, 85)

    p_r2 = cell_r.add_paragraph()
    p_r2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_r2.paragraph_format.space_before = Pt(0)
    p_r2.paragraph_format.space_after = Pt(2)
    r_guide = p_r2.add_run("PROF. AARTI GAWAI")
    r_guide.font.name = 'Calibri'
    r_guide.font.size = Pt(11)
    r_guide.font.bold = True
    r_guide.font.color.rgb = RGBColor(27, 94, 32)

    p_r3 = cell_r.add_paragraph()
    p_r3.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_r3.paragraph_format.space_before = Pt(0)
    p_r3.paragraph_format.space_after = Pt(4)
    r_gdept = p_r3.add_run("Department of Computer Science")
    r_gdept.font.name = 'Calibri'
    r_gdept.font.size = Pt(9.5)
    r_gdept.font.color.rgb = RGBColor(50, 50, 50)

    for c in [cell_l, cell_r]:
        set_bg(c, "F1F8E9")
        set_mar(c, top=100, bottom=100, left=120, right=120)

    p_demo = doc.add_paragraph()
    p_demo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_demo.paragraph_format.space_before = Pt(36)
    p_demo.paragraph_format.space_after = Pt(6)
    r_d = p_demo.add_run("Interactive Project Repository & Live Prototype:\n")
    r_d.font.name = 'Calibri'
    r_d.font.size = Pt(10)
    r_d.font.bold = True

    if os.path.exists('docs/report_figures/qr_github_repo.png'):
        p_qr = doc.add_paragraph()
        p_qr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_qr.add_run().add_picture('docs/report_figures/qr_github_repo.png', width=Inches(1.15))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE\nACADEMIC YEAR 2026–2027 (SEMESTER 5)")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(38, 50, 56)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. CERTIFICATE OF AUTHENTICITY (PAGE 2)
    # -------------------------------------------------------------
    add_h1("CERTIFICATE OF AUTHENTICITY")
    add_p("This is to certify that the dissertation report entitled 'Multi-Crop Plant Disease Detection and Advisory System Using Dual-Head Vision Transformer (DPD ViT-Base)' submitted by Anas Moinuddin Sayed (Roll No. CS-9130) is a bonafide record of independent project work carried out under my supervision in partial fulfillment of the requirements for the Degree of Bachelor of Science in Computer Science (B.Sc. CS).")
    add_p("The research methodology, mathematical models, decoupled neural network architectures, and experimental results embodied in this report have been thoroughly evaluated, independently verified across 25 rigorous test cases, and not been submitted to any other University or Institution for the award of any degree, diploma, or fellowship.")

    p_spc = doc.add_paragraph()
    p_spc.paragraph_format.space_after = Pt(60)

    sig_tbl = doc.add_table(rows=1, cols=3)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cant_split(sig_tbl.rows[0])
    sig_titles = [
        "Prof. Aarti Gawai\nProject Guide\nDept. of Computer Science",
        "Head of Department\nDept. of Computer Science",
        "Principal / Dean\nCollege / Institute"
    ]
    for idx, cell in enumerate(sig_tbl.rows[0].cells):
        cell.width = Inches(2.0)
        p_s = cell.paragraphs[0]
        p_s.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_s.add_run("_____________________\n").font.color.rgb = RGBColor(160, 160, 160)
        p_s.add_run(sig_titles[idx]).font.size = Pt(9.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. CANDIDATE'S DECLARATION (PAGE 3)
    # -------------------------------------------------------------
    add_h1("CANDIDATE'S DECLARATION")
    add_p("I hereby declare that the project work presented in this dissertation entitled 'Multi-Crop Plant Disease Detection and Advisory System Using Dual-Head Vision Transformer (DPD ViT-Base)' is entirely my own original work conducted under the guidance of Prof. Aarti Gawai, Department of Computer Science.")
    add_p("I have adhered to all academic ethics, professional guidelines, and principles of scientific integrity. All source code implementations, neural network training pipelines, mathematical calibrations, architectural schemas, dataset annotations, and testing frameworks referenced from external literature, benchmark repositories, or open-source libraries have been properly cited and acknowledged.")
    add_p("I further declare that this work contains zero fabricated data, zero unauthorized software engineering claims, and represents a faithful, reproducible record of my final year capstone dissertation.")

    p_dec_sig = doc.add_paragraph()
    p_dec_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_dec_sig.paragraph_format.space_before = Pt(70)
    r_ds = p_dec_sig.add_run("_____________________\nANAS MOINUDDIN SAYED\nRoll No. CS-9130\nB.Sc. Computer Science (Semester 5)")
    r_ds.font.name = 'Calibri'
    r_ds.font.size = Pt(11)
    r_ds.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ACKNOWLEDGEMENTS (PAGE 4)
    # -------------------------------------------------------------
    add_h1("ACKNOWLEDGEMENTS")
    add_p("The completion of this dissertation report marks a significant academic milestone, and I would like to express my deepest gratitude to all individuals and organizations who contributed their valuable guidance, encouragement, and technical resources throughout the research and development phases of this project.")
    add_p("First and foremost, I express my profound gratitude to my project guide, Prof. Aarti Gawai, Department of Computer Science, for her invaluable mentorship, constructive technical critiques, and steadfast encouragement. Her profound insights into software architecture, rigorous engineering principles, and academic writing provided the essential foundation for structuring this dissertation.")
    add_p("I extend my sincere thanks to the Head of the Department of Computer Science and all faculty members for fostering an intellectually stimulating environment and providing access to computational infrastructure and laboratory facilities essential for executing deep learning experiments.")
    add_p("I am equally grateful to the open-source artificial intelligence, computer vision, and agricultural research communities. The open availability of benchmark repositories—notably PyTorch, Ross Wightman's Timm library, FastAPI ASGI framework, and the open-access PlantVillage and PlantDoc datasets—has been instrumental in driving the empirical validation of our dual-head vision transformer.")
    add_p("Finally, I express my heartfelt gratitude to my family and peers for their continuous moral support, patience, and understanding during the intensive hours devoted to model benchmarking, system optimization, and dissertation preparation.")

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ack_sig.paragraph_format.space_before = Pt(40)
    p_ack_sig.add_run("ANAS MOINUDDIN SAYED\nRoll No. CS-9130").font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. ABSTRACT & KEYWORDS (PAGE 5)
    # -------------------------------------------------------------
    add_h1("ABSTRACT")
    add_p("Foliar plant diseases account for an estimated 20% to 40% loss in global agricultural crop yields annually, posing severe threats to international food security, rural economies, and smallholder farmer livelihoods. While deep learning has demonstrated remarkable computer vision capabilities in plant pathology over the past decade, prevailing state-of-the-art implementations suffer from three critical deployment bottlenecks: (1) restriction to single-crop narrow classifications (e.g., standard PlantVillage benchmarks restricted to 14 crops and 38 laboratory-isolated classes), (2) uncalibrated probability estimates that output high confidence on non-leaf background objects, and (3) a complete disconnect between computer vision classification outputs and actionable agronomic treatment recommendations.")
    add_p("To overcome these fundamental limitations, this dissertation presents the design, mathematical calibration, full-stack implementation, and empirical verification of a production-grade Multi-Crop Plant Disease Detection and Decision Support System. At its computational core, the system utilizes a Vision Transformer (DPD ViT-Base/16) backbone with a 768-dimensional latent space driving two simultaneous linear classification heads: a 55-class Plant Head and a 175-class Disease Head, structured across a biologically verified taxonomy of 333 supported crop-disease pairs.")
    add_p("To guarantee diagnostic integrity, the system implements a calibrated geometric-mean joint likelihood confidence formula: Conf = sqrt(max(0, P_P * P_D)) * 100, which provably guarantees strict monotonic probability ordering across Top-3 differential candidate diagnoses. Furthermore, an Out-Of-Distribution (OOD) gating threshold at 40.0% confidence actively filters non-crop artifacts and blurry inputs, preventing catastrophic false-positive pesticide prescriptions. Every verified diagnosis resolves into an actionable 5-pillar agronomic prescription (symptoms, cause, organic remedies, targeted chemical dosages, and cultural prevention) and generates an official clinical PDF report via ReportLab.")
    add_p("The complete platform is engineered using asynchronous FastAPI, PyTorch 2.0+, and SQLite with Write-Ahead Logging (WAL) concurrency, fortified with IDOR authorization barriers and MIME payload validation. Automated verification across 25 exhaustive test cases spanning tensor invariants, taxonomy contracts, and security audits confirms a 100% pass rate, delivering an enterprise-ready, mobile-accessible diagnostic solution for precision agriculture.")

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(14)
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.font.bold = True
    r_kwt.font.color.rgb = RGBColor(27, 94, 32)
    p_kw.add_run("Vision Transformer (ViT), Dual-Head Classification, Plant Pathology, Geometric Confidence Calibration, Out-of-Distribution Gating, 5-Pillar Agronomic Advisory, Precision Agriculture, FastAPI, Write-Ahead Logging.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. TABLE OF CONTENTS (PAGES 6-7)
    # -------------------------------------------------------------
    add_h1("TABLE OF CONTENTS")
    toc_items = [
        ("CERTIFICATE OF AUTHENTICITY", "ii"),
        ("CANDIDATE'S DECLARATION", "iii"),
        ("ACKNOWLEDGEMENTS", "iv"),
        ("ABSTRACT & KEYWORDS", "v"),
        ("LIST OF FIGURES", "viii"),
        ("LIST OF TABLES", "ix"),
        ("LIST OF ABBREVIATIONS", "ix"),
        ("CHAPTER 1: INTRODUCTION & PROBLEM DEFINITION", "1"),
        ("    1.1 Agricultural Background & Economic Impact of Foliar Pathogens", "1"),
        ("    1.2 Existing Diagnostic Paradigms & Their Bottlenecks", "3"),
        ("    1.3 Computer Vision in Precision Agriculture & CNN Inductive Bias", "4"),
        ("    1.4 Motivation for Vision Transformers & Decoupled Dual-Head Modeling", "5"),
        ("    1.5 Problem Statement & Research Objectives", "6"),
        ("    1.6 Scope & Limitations of the Dissertation", "7"),
        ("    1.7 Organization of the Dissertation", "7"),
        ("CHAPTER 2: LITERATURE SURVEY & THEORETICAL FOUNDATIONS", "8"),
        ("    2.1 Deep Learning Architectures in Plant Disease Classification", "8"),
        ("    2.2 Mathematical Foundations of Vision Transformers (ViT)", "11"),
        ("    2.3 Decoupled Dual-Head Architectures vs. Monolithic Classifiers", "14"),
        ("    2.4 Agricultural Advisory Systems & Integrated Pest Management", "16"),
        ("    2.5 Comprehensive Literature Review Matrix (12 Benchmark Papers)", "17"),
        ("    2.6 Identified Research Gaps & Proposed Technical Novelties", "19"),
        ("CHAPTER 3: SOFTWARE REQUIREMENTS SPECIFICATION (IEEE 830 SRS)", "20"),
        ("    3.1 Overview & Conformance to IEEE 830 SRS Standard", "20"),
        ("    3.2 User Characteristics & Operational Environment", "21"),
        ("    3.3 Functional Requirements Specification (FR-01 to FR-12)", "22"),
        ("    3.4 Non-Functional Requirements Specification (NFR-01 to NFR-10)", "24"),
        ("    3.5 System Hardware & Infrastructure Specifications", "25"),
        ("    3.6 Software Stack & Runtime Dependency Specifications", "26"),
        ("    3.7 Comprehensive Feasibility Study", "27"),
        ("CHAPTER 4: SYSTEM DESIGN AND ARCHITECTURE", "28"),
        ("    4.1 High-Level Layered System Architecture (Archify System View)", "28"),
        ("    4.2 End-to-End Clinical Diagnostic Workflow (Archify Clinical View)", "31"),
        ("    4.3 Unified Modeling Language (UML) Structural & Behavioral Modeling", "33"),
        ("        4.3.1 UML Use Case Modeling & 4 Formal Use Case Specifications", "33"),
        ("        4.3.2 UML Class Diagram & Object-Oriented Component Architecture", "36"),
        ("        4.3.3 UML Sequence Diagram & Diagnostic Asynchronous Lifecycle", "38"),
        ("        4.3.4 UML Activity Diagram & Decision Branches", "39"),
        ("        4.3.5 UML State Machine Diagram & Prediction Record Lifecycle", "40"),
        ("    4.4 Data Flow Diagrams (DFD Levels 0, 1, and 2)", "41"),
        ("    4.5 Relational Database Design & Schema Architecture", "44"),
        ("    4.6 Mathematical Confidence Calibration & OOD Gating Formulation", "46"),
        ("CHAPTER 5: IMPLEMENTATION AND METHODOLOGIES", "48"),
        ("    5.1 Project Directory Structure & Modular Decomposition", "48"),
        ("    5.2 Deep Learning Inference Pipeline (dpd_model.py)", "50"),
        ("    5.3 Asynchronous Web Server & REST API Implementation (app.py)", "53"),
        ("    5.4 Database Access Layer & Transaction Management (database.py)", "56"),
        ("    5.5 Clinical Report Generation Engine (pdf_generator.py)", "58"),
        ("    5.6 Front-End User Interface & Farmer Interaction Workflow", "60"),
        ("CHAPTER 6: SOFTWARE TESTING AND QUALITY ASSURANCE", "62"),
        ("    6.1 Testing Methodology & Test Pyramid Strategy", "62"),
        ("    6.2 Test Environment, Tooling & Automation Fixtures", "63"),
        ("    6.3 Comprehensive Test Suite Execution (25 Verified Scenarios)", "64"),
        ("    6.4 Master Software Test Execution Summary Log", "70"),
        ("    6.5 Security Audits & Robustness Verification", "72"),
        ("    6.6 Requirements Traceability Matrix", "73"),
        ("CHAPTER 7: RESULTS, EVALUATION AND DISCUSSION", "74"),
        ("    7.1 Multi-Crop Dataset Composition & 333 Class Distribution", "74"),
        ("    7.2 Model Performance Metrics & Crop Family Breakdown", "75"),
        ("    7.3 Comparative Benchmarking Against Baselines", "77"),
        ("    7.4 Out-of-Distribution Gating & Rejection Performance", "78"),
        ("    7.5 System Inference Latency & Scalability Benchmarks", "79"),
        ("    7.6 Real-World Field Case Studies & UI Validation", "80"),
        ("CHAPTER 8: CONCLUSION, LIMITATIONS AND FUTURE WORK", "83"),
        ("    8.1 Summary of Engineering Contributions", "83"),
        ("    8.2 Practical Agronomic Impact on Precision Farming", "84"),
        ("    8.3 Current System Limitations & Field Constraints", "84"),
        ("    8.4 Future Research Directions", "85"),
        ("REFERENCES (32 Peer-Reviewed IEEE / Springer Citations)", "82"),
        ("APPENDIX A: BOTANICAL & PATHOLOGICAL TAXONOMY SPECIFICATION", "85"),
        ("APPENDIX B: COMPLETE REST API OPENAPI / SWAGGER SPECIFICATION", "88"),
        ("APPENDIX C: SYSTEM INSTALLATION & PRODUCTION DEPLOYMENT GUIDE", "90"),
        ("APPENDIX D: 5-PILLAR AGRICULTURAL ADVISORY PROTOCOLS (SAMPLE)", "92")
    ]

    for title, pg in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(1)
        p_toc.paragraph_format.space_after = Pt(2)
        r_title = p_toc.add_run(title)
        r_title.font.name = 'Calibri'
        r_title.font.size = Pt(10)
        if "CHAPTER" in title or "REFERENCES" in title or "APPENDIX" in title or "CERTIFICATE" in title:
            r_title.font.bold = True
            r_title.font.color.rgb = RGBColor(27, 94, 32)
        else:
            r_title.font.color.rgb = RGBColor(55, 71, 79)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. LIST OF FIGURES (PAGE 8)
    # -------------------------------------------------------------
    add_h1("LIST OF FIGURES")
    figures_data = [
        ("Fig. 1.1", "Resolution and environmental gap between PlantVillage lab samples and noisy real-world field leaves", "5"),
        ("Fig. 4.1", "High-level layered system architecture of the Multi-Crop Disease Detection & Advisory Platform (Archify)", "29"),
        ("Fig. 4.2", "End-to-end clinical diagnostic workflow — leaf ingestion to 5-pillar prescription delivery (Archify)", "31"),
        ("Fig. 4.3", "UML Use Case diagram — Farmer/Analyst and Agronomist/Administrator interaction boundaries", "34"),
        ("Fig. 4.4", "UML Class diagram — DPDInferenceEngine, DPDViTDualHead, FastAPI routing, and Database schemas", "37"),
        ("Fig. 4.5", "UML Sequence diagram — Upload-to-Diagnosis asynchronous execution and storage lifecycle", "38"),
        ("Fig. 4.6", "Data Flow Diagram Level 1 — Ingestion, ViT Inference, OOD Gating, and Advisory Delivery (Archify)", "42"),
        ("Fig. 4.9", "Entity-Relationship (ER) diagram — users and predictions SQLite WAL relational architecture", "44"),
        ("Fig. 6.1", "Comprehensive Testing Pyramid — Unit, Contract Invariants, Security, and End-to-End API Integration", "62"),
        ("Fig. 7.1", "Interactive Web Portal Interface — Desktop and Mobile responsive navigation dashboard", "80"),
        ("Fig. 7.2", "Foliar Diagnostic Assessment Card — Top-1 disease detection with calibrated confidence meter", "81"),
        ("Fig. 7.5", "Comprehensive 5-Pillar Clinical Treatment Advisory Modal (Symptoms, Cause, Organic, Chemical, Prevention)", "82"),
        ("Fig. 7.6", "Official Clinical PDF Diagnostic Report Export rendered via automated ReportLab engine", "82")
    ]

    for fid, fcaption, fpage in figures_data:
        p_fig = doc.add_paragraph()
        p_fig.paragraph_format.space_before = Pt(1)
        p_fig.paragraph_format.space_after = Pt(2)
        r_fid = p_fig.add_run(f"{fid}:  ")
        r_fid.font.bold = True
        r_fid.font.color.rgb = RGBColor(46, 125, 50)
        r_fcap = p_fig.add_run(fcaption)
        r_fcap.font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. LIST OF TABLES & LIST OF ABBREVIATIONS (PAGE 9)
    # -------------------------------------------------------------
    add_h1("LIST OF TABLES")
    tables_data = [
        ("Table 2.1", "Comparative analysis of 12 existing plant pathology approaches vs. proposed DPD ViT-Base", "17"),
        ("Table 3.1", "Hardware specifications for model training, offline benchmarking, and production hosting", "25"),
        ("Table 3.2", "Production software environment and runtime dependency specifications", "26"),
        ("Table 4.1", "Relational database schema — users and predictions entities with indexing strategies", "45"),
        ("Table 6.1", "Master Software Test Case Log (25 formal test cases across 8 functional modules)", "70"),
        ("Table 6.2", "Requirements Traceability Matrix (RTM) mapping FR/NFR to test case identifiers", "73"),
        ("Table 7.1", "Quantitative evaluation metrics across 8 multi-crop botanical families", "75"),
        ("Table 7.2", "Comparative benchmarking of DPD ViT-Base against 5 baseline deep learning architectures", "77"),
        ("Table 7.3", "Granular stage-by-stage end-to-end inference and report generation latency breakdown", "79"),
        ("Table A.1", "Complete 333-Pair Botanical & Pathological Taxonomy Dictionary (Appendix A)", "89")
    ]

    for tid, tcaption, tpage in tables_data:
        p_tbl = doc.add_paragraph()
        p_tbl.paragraph_format.space_before = Pt(1)
        p_tbl.paragraph_format.space_after = Pt(2)
        r_tid = p_tbl.add_run(f"{tid}:  ")
        r_tid.font.bold = True
        r_tid.font.color.rgb = RGBColor(46, 125, 50)
        r_tcap = p_tbl.add_run(tcaption)
        r_tcap.font.size = Pt(10)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(8)

    add_h1("LIST OF ABBREVIATIONS")
    abbreviations = [
        ("ViT", "Vision Transformer"),
        ("DPD", "Dual-head Plant Disease (ViT-Base Model Architecture)"),
        ("OOD", "Out-Of-Distribution (Detection / Gating Guard)"),
        ("CNN", "Convolutional Neural Network"),
        ("MHSA", "Multi-Head Self-Attention"),
        ("JWT", "JSON Web Token (RFC 7519)"),
        ("WAL", "Write-Ahead Logging (SQLite Concurrency Journaling)"),
        ("IPM", "Integrated Pest Management"),
        ("IDOR", "Insecure Direct Object Reference (Access Control Vulnerability)"),
        ("MIME", "Multipurpose Internet Mail Extensions (File Type Validation)"),
        ("DFD", "Data Flow Diagram"),
        ("ERD", "Entity-Relationship Diagram"),
        ("SRS", "Software Requirements Specification (IEEE 830 Standard)"),
        ("UML", "Unified Modeling Language"),
        ("PV", "PlantVillage Dataset Benchmark"),
        ("API", "Application Programming Interface"),
        ("REST", "Representational State Transfer"),
        ("ASGI", "Asynchronous Server Gateway Interface"),
        ("RTM", "Requirements Traceability Matrix"),
        ("DoS", "Denial of Service (Payload Guard Protection)")
    ]

    abbr_headers = ["Abbreviation", "Full Form / Domain Definition"]
    abbr_rows = [[a, full] for a, full in abbreviations]
    add_tbl(abbr_headers, abbr_rows, col_widths=[Inches(1.8), Inches(4.2)])

    doc.add_page_break()
