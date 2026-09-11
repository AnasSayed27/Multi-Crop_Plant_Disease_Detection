# Multi-Crop Disease Detection & Advisory — System Diagrams

These diagrams are compiled using **Archify** (`tt-a1i/archify`) into deterministic, standalone, interactive HTML artifacts with inline SVGs, dark/light themes, route tracing, and crisp export capabilities (PNG, SVG, WebM, 1200×630 share cards).

Every diagram passed all 9 showcase artifact and layout validation checks with 0 errors and 0 warnings.

---

## 1. System Runtime Architecture (`architecture`)
* **Interactive HTML**: [`system-architecture.html`](./system-architecture.html)
* **Typed IR Source**: [`system-architecture.architecture.json`](./system-architecture.architecture.json)
* **What It Covers**:
  * **Client Layer**: SPA frontend, camera capture, Chart.js analytics, and mobile drawer.
  * **Application Gateway**: FastAPI backend (`:8000`), bcrypt authentication, and PyJWT token guard.
  * **Deep Learning Runtime**: Dual-Head Vision Transformer (Timm ViT-B/16, 768-d latent features, $768 \to 55$ plant logits, $768 \to 175$ disease logits) with model checkpoint `model_b_partial.pth`.
  * **Taxonomy & Knowledge Assets**: 333 supported crop-disease pairings across 55 crops, and 5-pillar clinical treatment protocols in `disease_info.json`.
  * **Data & Reporting**: SQLite database in Write-Ahead Logging (WAL) mode, sandboxed `/uploads/` directory, and ReportLab clinical PDF engine.

---

## 2. Clinical Diagnostic Workflow (`workflow`)
* **Interactive HTML**: [`diagnostic-workflow.html`](./diagnostic-workflow.html)
* **Typed IR Source**: [`diagnostic-workflow.workflow.json`](./diagnostic-workflow.workflow.json)
* **What It Covers**:
  * **Intake & Validation**: Leaf photo upload, MIME validation (JPEG/PNG/WebP), $\le$ 10 MB payload check, and image sandboxing with `uuid4`.
  * **ViT Dual-Head Inference**: PIL $224 \times 224$ preprocessing, ViT 768-d forward pass, and parallel softmax heads.
  * **Probabilistic Gating & Scoring**: Joint likelihood ranking $P(\text{Plant}) \times P(\text{Disease})$ across 333 pairs, geometric-mean confidence calculation, and non-crop uncertainty gating ($< 40\%$).
  * **Resolution & Delivery**: 5-pillar prescription mapping (organic, chemical, prevention, pesticides, fertilizers), SQLite WAL audit logging, and responsive UI delivery with top-3 differential diagnoses.

---

## 3. Dual-Head ViT Machine Learning & Advisory Data Flow (`dataflow`)
* **Interactive HTML**: [`ml-inference-dataflow.html`](./ml-inference-dataflow.html)
* **Typed IR Source**: [`ml-inference-dataflow.dataflow.json`](./ml-inference-dataflow.dataflow.json)
* **What It Covers**:
  * **Capture**: Foliar leaf images and authenticated farmer session context.
  * **Ingest & Gate**: Decoded into $[1, 3, 224, 224]$ normalized Float32 tensors; session credentials validated.
  * **Feature & Assets**: ViT patch attention generates 768-dimensional global visual representations; 333 viable agricultural pairs indexed.
  * **Score & Prescribe**: $55 \times 175$ softmax matrices evaluated; joint likelihoods calculated; clinical treatment protocols linked.
  * **Deliver & Persist**: Top-3 differential diagnoses returned as JSON; telemetry committed to SQLite WAL; printable diagnostic PDF generated on demand.

---

## Interactive Viewer Hotkeys
Open any `.html` file in any modern web browser:
| Key | Action |
| :---: | :--- |
| `T` | Toggle Dark / Light theme |
| `F` | Enter Presentation Stage |
| `E` | Open Export menu (PNG, SVG, WebM, Share Cards) |
| `?` | Open factual Diagram Guide |
| `/` | Find and focus semantic node |
| `R` | Probe directed route / path |
| `P` or `[` / `]` | Play guided story chapters |
| `+` / `-` / `0` | Zoom in / Zoom out / Reset view |
