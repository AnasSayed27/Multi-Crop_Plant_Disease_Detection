import os
import io
import re
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

import html

def _clean_markdown_for_reportlab(text: str) -> str:
    """Sanitizes text and converts Markdown asterisks to ReportLab XML tags (<i>, <b>)."""
    if not text:
        return ""
    # Escape raw XML special characters
    escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Convert **bold** to <b>bold</b>
    formatted = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escaped)
    # Convert *italic* to <i>italic</i>
    formatted = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted)
    # Convert newlines to breaks
    formatted = formatted.replace('\n', '<br/>')
    return formatted

def generate_prediction_pdf(
    prediction: Dict[str, Any],
    user: Dict[str, Any],
    advisory_info: Dict[str, Any],
    base_dir: str = "."
) -> io.BytesIO:
    """
    Generates a professional PDF diagnostic report for a crop disease prediction record.
    Returns a BytesIO stream containing the generated PDF binary data.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom ReportLab Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1b5e20'),
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#555555'),
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2e7d32'),
        spaceBefore=10,
        spaceAfter=6
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#333333')
    )

    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#222222')
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#333333')
    )

    module_header_style = ParagraphStyle(
        'ModuleHeader',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1b5e20'),
        spaceAfter=4
    )

    story = []

    # 1. HEADER BANNER
    story.append(Paragraph("🌿 Multi-Crop Disease Advisory & Diagnostic Report", title_style))
    story.append(Paragraph("AI-Powered Deep Learning Crop Health Analysis • Vision Transformer Architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2e7d32'), spaceAfter=12))

    # 2. METADATA & USER INFORMATION TABLE
    user_name = html.escape(str(user.get('username', 'N/A')))
    user_email = html.escape(str(user.get('email', 'N/A')))
    pred_id = prediction.get('id', 'N/A')
    created_at = prediction.get('created_at', 'N/A')

    meta_data = [
        [
            Paragraph("Report ID:", meta_label_style), Paragraph(f"#{pred_id}", meta_val_style),
            Paragraph("Farmer / User:", meta_label_style), Paragraph(f"{user_name} ({user_email})", meta_val_style)
        ],
        [
            Paragraph("Scan Date:", meta_label_style), Paragraph(str(created_at), meta_val_style),
            Paragraph("System Model:", meta_label_style), Paragraph("Vision Transformer (DPD ViT-Base Dual-Head)", meta_val_style)
        ]
    ]

    meta_table = Table(meta_data, colWidths=[1.1*inch, 2.3*inch, 1.2*inch, 2.6*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f8e9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#c8e6c9')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e8f5e9')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # 3. DIAGNOSIS RESULT & EMBEDDED LEAF IMAGE
    story.append(Paragraph("Diagnostic Analysis Summary", h2_style))

    crop = prediction.get('crop', 'Unknown Crop')
    disease = prediction.get('disease', 'Unknown Disease')
    confidence = prediction.get('confidence', 0.0)
    img_rel_path = prediction.get('image_path', '')

    # Image element handling
    img_element = None
    if img_rel_path:
        img_full_path = os.path.join(base_dir, img_rel_path.lstrip("/\\"))
        if os.path.exists(img_full_path):
            try:
                img_element = Image(img_full_path, width=2.0*inch, height=2.0*inch)
            except Exception:
                img_element = None

    if not img_element:
        # Fallback placeholder box
        placeholder_data = [[Paragraph("<font color='#888888'>[ Uploaded Leaf Image ]</font>", body_style)]]
        img_element = Table(placeholder_data, colWidths=[2.0*inch], rowHeights=[2.0*inch])
        img_element.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eeeeee')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cccccc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))

    status_color = "#2e7d32" if "healthy" in disease.lower() else "#c62828"
    status_text = "HEALTHY" if "healthy" in disease.lower() else "DISEASED"

    diag_text = (
        f"<b>Target Crop:</b> {crop}<br/><br/>"
        f"<b>Detected Status:</b> <font color='{status_color}'><b>{disease}</b></font><br/><br/>"
        f"<b>Condition Category:</b> {status_text}<br/><br/>"
        f"<b>Model Confidence Score:</b> {confidence:.2f}%"
    )

    diag_table_data = [
        [img_element, Paragraph(diag_text, body_style)]
    ]

    diag_table = Table(diag_table_data, colWidths=[2.2*inch, 5.0*inch])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fafafa')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e0e0e0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 14))

    # 4. ADVISORY GUIDANCE MODULES
    story.append(Paragraph("5-Pillar Comprehensive Advisory Guidance", h2_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#a5d6a7'), spaceAfter=10))

    # Extract advisory modules
    symptoms_text = _clean_markdown_for_reportlab(advisory_info.get("symptoms", "No symptom data available."))
    cause_text = _clean_markdown_for_reportlab(advisory_info.get("cause", "No cause data available."))
    organic_text = _clean_markdown_for_reportlab(advisory_info.get("organic_treatment", "No organic treatment available."))
    chemical_text = _clean_markdown_for_reportlab(advisory_info.get("chemical_treatment", "No chemical treatment available."))
    prevention_text = _clean_markdown_for_reportlab(advisory_info.get("prevention", "No prevention guidance available."))

    modules = [
        ("🔍 1. Visual Symptoms & Leaf Diagnostic Markers", symptoms_text, "#fff8e1", "#f57c00"),
        ("🧪 2. Pathogen, Cause & Weather Triggers", cause_text, "#f3e5f5", "#7b1fa2"),
        ("🌿 3. Organic & Biological Control Measures", organic_text, "#e8f5e9", "#2e7d32"),
        ("💊 4. Chemical Solutions & Targeted Dosage", chemical_text, "#ffebee", "#c62828"),
        ("🛡️ 5. Proactive Cultural Prevention Manual (Long-Term Sanitation)", prevention_text, "#e3f2fd", "#1565c0"),
    ]

    for title, text, bg_hex, border_hex in modules:
        mod_header_p = Paragraph(f"<font color='{border_hex}'><b>{title}</b></font>", module_header_style)
        mod_body_p = Paragraph(text, body_style)

        mod_table_data = [[mod_header_p], [mod_body_p]]
        mod_table = Table(mod_table_data, colWidths=[7.2*inch])
        mod_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_hex)),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))

        story.append(KeepTogether([mod_table, Spacer(1, 10)]))

    # FOOTER DISCLAIMER
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc'), spaceBefore=10, spaceAfter=8))
    footer_text = (
        "<i>Notice: This automated diagnostic report is generated by an artificial intelligence deep learning model "
        "trained on plant leaf datasets. For severe disease outbreaks or commercial crop protection, consult your local "
        "agricultural university extension officer.</i>"
    )
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor('#777777'))))

    doc.build(story)
    buffer.seek(0)
    return buffer
