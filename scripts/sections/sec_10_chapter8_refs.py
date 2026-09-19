# scripts/sections/sec_10_chapter8_refs.py
import sys
sys.path.insert(0, 'scripts')
import report_data
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter8_refs(doc, helpers):
    add_h1 = helpers['add_heading_1']
    add_h2 = helpers['add_heading_2']
    add_p = helpers['add_body_p']
    add_bullet = helpers['add_bullet_p']
    add_callout = helpers['add_callout_box']

    # -------------------------------------------------------------
    # CHAPTER 8: CONCLUSION, LIMITATIONS AND FUTURE WORK
    # -------------------------------------------------------------
    add_h1("CHAPTER 8: CONCLUSION, LIMITATIONS AND FUTURE WORK")

    add_h2("8.1 Summary of Engineering Contributions")
    add_p("This dissertation has presented the theoretical derivation, architectural design, full-stack implementation, and empirical verification of a production-grade Multi-Crop Plant Disease Detection and Decision Support System powered by a Decoupled Dual-Head Vision Transformer (DPD ViT-Base). Addressing the core failure modes of conventional computer vision applications in agricultural pathology, the research delivers five foundational contributions:")
    add_bullet("Expanded foliar diagnostic breadth from conventional single-crop silos (average 14 crops, 38 classes) to 55 commercially vital agricultural crops and 175 pathological conditions, structured across 333 biologically verified co-occurrence pairs.", bold_prefix="1. Multi-Crop Taxonomic Breadth: ")
    add_bullet("Decoupled botanical plant identification (55 classes) from pathological lesion classification (175 classes) over a shared 768-dimensional Vision Transformer representation, mitigating gradient interference and enabling high transfer efficiency.", bold_prefix="2. Decoupled Dual-Head Architecture: ")
    add_bullet("Formulated a joint-likelihood geometric-mean confidence metric S = sqrt(max(0, P_P * P_D)) * 100 with an empirical 40.0% Out-of-Distribution gating threshold, achieving a 98.6% rejection rate on non-crop background artifacts and preventing erroneous chemical pesticide prescriptions.", bold_prefix="3. Calibrated Confidence & OOD Gating: ")
    add_bullet("Coupled neural classifications directly to an Integrated Pest Management knowledge base, automatically synthesizing 5-pillar agronomic prescriptions (Symptoms, Cause, Organic Remedies, Chemical Dosages, and Cultural Prevention).", bold_prefix="4. Actionable 5-Pillar Advisory Engine: ")
    add_bullet("Engineered an enterprise-grade asynchronous backend utilizing FastAPI, SQLite WAL concurrency, IDOR access controls, automated ReportLab clinical PDF generation, and verified across an exhaustive 25-case test suite with a 100% pass rate.", bold_prefix="5. Full-Stack Production Architecture: ")

    add_h2("8.2 Practical Agronomic Impact on Precision Farming")
    add_p("By deploying this system as a zero-installation, mobile-accessible web service, the platform bridges the critical digital divide between cutting-edge artificial intelligence and grassroots smallholder farmers. The near-zero marginal cost per scan (<bash.001) provides an economically viable alternative to expensive laboratory PCR assays (0–00), empowering agricultural extension officers and farmers to detect early-stage foliar blights before epidemic propagation occurs. The integration of certified organic treatments and pre-harvest interval (PHI) chemical guidance promotes ecologically sustainable agriculture and protects consumer food safety.")

    add_h2("8.3 Current System Limitations & Field Constraints")
    add_p("Despite achieving strong diagnostic precision, several practical field constraints remain:")
    add_bullet("The model operates under the assumption of a single primary foliar subject centered within the camera frame. Severely overlapping canopy foliage with multiple conflicting plant species requires manual user framing.", bold_prefix="1. Single-Leaf Focal Constraint: ")
    add_bullet("While sub-150ms latency is achieved on GPU hardware, CPU-only edge server deployments average 1280ms per forward pass, limiting extreme high-volume concurrent processing on low-end hardware.", bold_prefix="2. Computational Footprint: ")
    add_bullet("Complex secondary foliar co-infections occurring simultaneously on an identical leaf spot are expressed through differential Top-3 candidate rankings rather than multi-label pixel-level segmentation masks.", bold_prefix="3. Co-infection Granularity: ")

    add_h2("8.4 Future Research Directions")
    add_p("The architectural foundation established in this dissertation opens multiple high-impact avenues for future research and engineering:")
    add_bullet("Quantizing the Vision Transformer backbone via 8-bit integer post-training quantization (INT8) or migrating to MobileViT / EdgeViT architectures will reduce the model memory footprint to <25 MB, enabling completely offline, zero-connectivity on-device inference on budget Android smartphones.", bold_prefix="1. Edge Quantization & Offline On-Device Inference: ")
    add_bullet("Integrating a lightweight YOLOv8 or RT-DETR object detection head will enable multi-leaf real-time bounding box localization, allowing autonomous drone or tractor-mounted cameras to scan entire field canopies continuously.", bold_prefix="2. Canopy-Level Object Detection & Localization: ")
    add_bullet("Fine-tuning a localized multimodal Large Language Model (LLM) on agricultural advisory corpora will enable interactive, multi-turn conversational advisory chatbots, allowing farmers to query pesticide compatibility and regional weather forecasts dynamically.", bold_prefix="3. Multimodal LLM Advisory Conversational Agents: ")
    add_bullet("Coupling diagnostic predictions with geolocation telemetry to construct real-time regional epidemiological heatmaps, enabling government agricultural ministries to predict and quarantine airborne pathogen outbreaks before regional infestation.", bold_prefix="4. Geospatial Epidemiological Tracking: ")

    doc.add_page_break()

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_h1("REFERENCES")
    add_p("The following peer-reviewed academic literature, conference proceedings, and official technical standards form the scientific foundation of this dissertation report:")

    for ref in report_data.ACADEMIC_REFERENCES:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_ref.add_run(ref)
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(38, 50, 56)

    doc.add_page_break()