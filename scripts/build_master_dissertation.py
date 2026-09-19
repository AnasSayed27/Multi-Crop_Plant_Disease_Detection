# scripts/build_master_dissertation.py
"""
======================================================================
 MASTER ACADEMIC DISSERTATION BUILDER (75+ PAGES)
======================================================================
Compiles the complete, publication-grade academic dissertation report:
- Format: Strict Portrait A4 (.docx) with zero landscape variations
- Eliminates all layout flaws: cantSplit on rows, tblHeader on multi-page tables,
  keep_with_next on headings/captions, 12pt standard typography.
======================================================================
"""

import os
import sys
import time

# Ensure scripts directory and sections are on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, 'sections'))

import sec_01_preamble
import sec_02_front_matter
import sec_03_chapter1
import sec_04_chapter2
import sec_05_chapter3
import sec_06_chapter4
import sec_07_chapter5
import sec_08_chapter6
import sec_09_chapter7
import sec_10_chapter8_refs
import sec_11_appendices

def build_complete_dissertation():
    print("[1/12] Initializing Document & Styles...")
    doc, helpers = sec_01_preamble.init_document()

    print("[2/12] Building Front Matter (Cover, Certificate, Declaration, Abstract, TOC, Lists)...")
    sec_02_front_matter.build_front_matter(doc, helpers)

    print("[3/12] Building Chapter 1: Introduction & Problem Definition...")
    sec_03_chapter1.build_chapter1(doc, helpers)

    print("[4/12] Building Chapter 2: Literature Survey & Mathematical Foundations...")
    sec_04_chapter2.build_chapter2(doc, helpers)

    print("[5/12] Building Chapter 3: Software Requirements Specification (IEEE 830)...")
    sec_05_chapter3.build_chapter3(doc, helpers)

    print("[6/12] Building Chapter 4: System Design & Architecture (Archify, UML, DFDs, ERD)...")
    sec_06_chapter4.build_chapter4(doc, helpers)

    print("[7/12] Building Chapter 5: Implementation & Methodologies (Code Listings & Pipeline)...")
    sec_07_chapter5.build_chapter5(doc, helpers)

    print("[8/12] Building Chapter 6: Software Testing & Quality Assurance (All 25 Scenarios)...")
    sec_08_chapter6.build_chapter6(doc, helpers)

    print("[9/12] Building Chapter 7: Results, Evaluation & Discussion (Metrics, Benchmarks)...")
    sec_09_chapter7.build_chapter7(doc, helpers)

    print("[10/12] Building Chapter 8: Conclusion, Limitations & Future Scope + References...")
    sec_10_chapter8_refs.build_chapter8_refs(doc, helpers)

    print("[11/12] Building Appendices (Appendix A: 333-Pair Table, Appendix B, C, D)...")
    sec_11_appendices.build_appendices(doc, helpers)

    output_path = "Multi_Crop_Plant_Disease_Detection_Dissertation_Report.docx"
    print(f"[12/12] Saving master document to {output_path}...")
    t0 = time.time()
    doc.save(output_path)
    t1 = time.time()
    print(f"Master document successfully compiled in {t1 - t0:.2f} seconds!")
    print(f"File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")

if __name__ == '__main__':
    build_complete_dissertation()
