# scripts/sections/sec_04_chapter2.py
import sys
sys.path.insert(0, 'scripts')
import report_data
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter2(doc, helpers):
    add_h1 = helpers['add_heading_1']
    add_h2 = helpers['add_heading_2']
    add_h3 = helpers['add_heading_3']
    add_p = helpers['add_body_p']
    add_bullet = helpers['add_bullet_p']
    add_tbl = helpers['add_table']
    add_callout = helpers['add_callout_box']

    # -------------------------------------------------------------
    # CHAPTER 2: LITERATURE SURVEY & THEORETICAL FOUNDATIONS
    # -------------------------------------------------------------
    add_h1("CHAPTER 2: LITERATURE SURVEY & THEORETICAL FOUNDATIONS")

    add_h2("2.1 Deep Learning Architectures in Plant Disease Classification")
    add_p("Automated plant pathology using computational methods has progressed through distinct technological paradigms over the past two decades. Early research (2005–2014) demonstrated the viability of automated foliar feature extraction using hand-crafted computer vision operators. Camargo and Smith (2009) utilized color co-occurrence matrices (CCM) to classify fungal lesions in cotton leaves, while Pydipati et al. (2006) extracted Gray-Level Co-occurrence Matrix (GLCM) texture descriptors paired with Mahalanobis distance classifiers to detect citrus canker.")
    add_p("Although these pioneer studies proved that foliar lesions possess distinct chromatic and statistical textures, hand-crafted features were fragile to natural field variability. The diagnostic accuracy of GLCM and SIFT pipelines declined by 30% to 50% when tested on leaves photographed under varying cloud cover, ambient shadows, or natural outdoor backgrounds. Furthermore, these pipelines required manual segmentation of individual lesions, rendering automated farm-scale deployment impossible.")
    add_p("The breakthrough of deep Convolutional Neural Networks (CNNs) initiated the modern era of automated plant disease recognition. In a seminal study, Mohanty et al. (2016) trained AlexNet and GoogleNet architectures on the PlantVillage dataset—a benchmark containing 54,306 foliar images across 14 crop species and 26 diseases. Their models achieved a test accuracy of 99.35% on holdout validation data. However, the authors explicitly noted a catastrophic limitation: when their laboratory-trained models were evaluated on real-world field photographs collected from commercial farms, classification accuracy plummeted to approximately 31.4%.")
    add_p("Subsequent research focused on addressing this domain generalization gap using deeper and more expressive CNN architectures:")
    add_bullet("Demonstrated that deeper residual representations and DenseNet connectivity significantly outperformed shallower networks on foliar disease classification, achieving 99.75% accuracy. However, VGG-16 models required over 138 million parameters, imposing an immense computational memory footprint incompatible with mobile or edge deployment.", bold_prefix="1. Too et al. (2019): ")
    add_bullet("Investigated lightweight depthwise separable convolutions (MobileNetV2) and Inception-v4 for multi-crop classification under field conditions. While MobileNetV2 achieved 89.50% field accuracy with only 3.4 million parameters, the authors observed that depthwise convolutions suffered from high sensitivity to background weed clutter and soil textures.", bold_prefix="2. Chen et al. (2020): ")
    add_bullet("Introduced the PlantDoc benchmark, compiling 2,598 field-acquired images across 13 plant species and 27 disease categories. Evaluating baseline CNN models, they reported a dramatic drop in performance, with standard classifiers achieving Top-1 accuracies between 65% and 72%—empirically demonstrating that lab-clean datasets fail to reflect genuine agricultural field complexity.", bold_prefix="3. Singh et al. (2020): ")
    add_bullet("Explored shifted-window hierarchical Vision Transformers (Swin Transformer) to capture multi-scale foliar symptoms, achieving 94.80% accuracy. However, hierarchical windowing constrained self-attention within local windows (typically 7x7 patches), diminishing the model's capacity to correlate distant symptoms on broad leaves (such as banana or corn blades).", bold_prefix="4. Borhani et al. (2022): ")

    add_h2("2.2 Mathematical Foundations of Vision Transformers (ViT)")
    add_p("The Vision Transformer architecture (Dosovitskiy et al., 2020) eliminates spatial convolutions entirely, relying exclusively on Multi-Head Self-Attention (MHSA) mechanisms to model global relationships across image patches. This mathematical formulation is detailed below.")

    add_h3("2.2.1 Patch Embedding & Linear Projection")
    add_p("Given an input RGB foliar image x in R^{H x W x C}, where H = W = 224 and C = 3, standard Transformer encoders cannot process 2D spatial pixel arrays directly. Therefore, the image is partitioned into a sequence of non-overlapping 2D patches x_p in R^{N x (P^2 * C)}, where P = 16 denotes the patch spatial resolution, and N is the resulting sequence length:")
    add_callout(
        "PATCH SEQUENCE LENGTH DERIVATION",
        "N = (H * W) / (P^2) = (224 * 224) / (16 * 16) = 50,176 / 256 = 196 patches.\n"
        "Each patch contains P * P * C = 16 * 16 * 3 = 768 raw pixel values."
    )
    add_p("Each flattened patch x_p^k in R^{768} is mapped into the model's latent embedding dimension D = 768 using a trainable linear projection matrix E in R^{(P^2 * C) x D}. To perform classification, a learnable [CLS] classification token x_{class} in R^{1 x D} is prepended to the patch sequence. To retain 2D spatial awareness, learnable 1D positional embeddings E_{pos} in R^{(N+1) x D} are added element-wise:")
    add_callout(
        "INITIAL EMBEDDING EQUATION",
        "z_0 = [ x_{class} ; x_p^1 E ; x_p^2 E ; ... ; x_p^N E ] + E_{pos}, \n"
        "where z_0 in R^{(197 x 768)}, E in R^{(768 x 768)}, and E_{pos} in R^{(197 x 768)}."
    )

    add_h3("2.2.2 Multi-Head Self-Attention (MHSA) Formulation")
    add_p("The embedded sequence z_0 passes through L = 12 stacked Transformer Encoder layers. Each layer consists of a Multi-Head Self-Attention (MHSA) block followed by a Multi-Layer Perceptron (MLP) block, with Pre-Layer Normalization (LN) and residual skip connections:")
    add_callout(
        "TRANSFORMER ENCODER LAYER EQUATIONS",
        "z'_l = MHSA( LN(z_{l-1}) ) + z_{l-1},  l = 1, ..., 12\n"
        "z_l  = MLP( LN(z'_l) ) + z'_l,         l = 1, ..., 12"
    )
    add_p("Within each MHSA block with h = 12 attention heads, the latent dimension per head is d_k = D / h = 768 / 12 = 64. For each attention head i in {1, ..., 12}, the normalized input sequence is projected into Query (Q), Key (K), and Value (V) matrices via learned projection matrices W_i^Q, W_i^K, W_i^V in R^{D x d_k}:")
    add_callout(
        "SCALED DOT-PRODUCT ATTENTION MATHEMATICAL EQUATION",
        "Q_i = z * W_i^Q,  K_i = z * W_i^K,  V_i = z * W_i^V\n"
        "Attention(Q_i, K_i, V_i) = softmax( (Q_i * K_i^T) / sqrt(d_k) ) * V_i\n"
        "MultiHead(Q, K, V) = Concat( head_1, head_2, ..., head_h ) * W^O\n"
        "where W^O in R^{(h * d_k) x D} = R^{768 x 768}, and sqrt(d_k) = sqrt(64) = 8."
    )
    add_p("The scaling factor 1 / sqrt(d_k) is mathematically crucial: for large projection dimensions, the dot products grow large in magnitude, pushing the softmax function into regions with vanishingly small gradients. Scaling by 1 / 8 preserves gradient stability throughout backpropagation.")

    add_h3("2.2.3 Multi-Layer Perceptron (MLP) Block")
    add_p("The MLP block consists of two dense linear layers with a Gaussian Error Linear Unit (GELU) non-linearity. The hidden dimension expands by a factor of 4 to D_{mlp} = 4 * 768 = 3,072 dimensions, enabling non-linear feature transformation before projecting back to 768:")
    add_callout(
        "MLP BLOCK EQUATION",
        "MLP(x) = GELU( x * W_1 + b_1 ) * W_2 + b_2\n"
        "where W_1 in R^{768 x 3072}, b_1 in R^{3072}, W_2 in R^{3072 x 768}, b_2 in R^{768}."
    )

    add_h2("2.3 Decoupled Dual-Head Architectures vs. Monolithic Classifiers")
    add_p("Traditional deep learning classifiers formulate multi-crop disease diagnosis as a monolithic single-head classification task. For a system supporting 55 crops and 175 diseases across 333 valid pairs, a monolithic model defines an output layer with C = 333 logits, applying a single 333-way Softmax function.")
    add_p("This monolithic formulation suffers from severe theoretical and practical deficiencies:")
    add_bullet("In a 333-way single head, the model must simultaneously learn botanical taxonomy and pathological lesions within a single dense weight matrix W in R^{333 x 768}. A gradient update for 'Potato Late Blight' interferes directly with the weights for 'Tomato Late Blight', despite both conditions sharing the identical biological pathogen (Phytophthora infestans).", bold_prefix="1. Gradient Interference & Catastrophic Forgetting: ")
    add_bullet("If an untrained or noisy leaf image is ingested, the monolithic Softmax function enforces the constraint sum_{k=1}^{333} p_k = 1.0. The model is mathematically forced to distribute probability mass among the 333 classes, inevitably selecting a winning class even when the image contains a blank wall, human hand, or weed.", bold_prefix="2. Uncalibrated Closed-World Softmax: ")
    add_p("To resolve this, our DPD ViT-Base decouples classification into two parallel, independent linear projection heads attached to the final encoder output vector z_L^0 (the 768-dimensional [CLS] token representation):")
    add_callout(
        "DECOUPLED DUAL-HEAD EQUATIONS",
        "Plant Head:    y_{plant}   = W_{plant}   * z_L^0 + b_{plant},   W_{plant}   in R^{55 x 768},  b_{plant}   in R^{55}\n"
        "Disease Head:  y_{disease} = W_{disease} * z_L^0 + b_{disease}, W_{disease} in R^{175 x 768}, b_{disease} in R^{175}"
    )
    add_p("Each head independently computes a normalized marginal probability distribution via Softmax:")
    add_callout(
        "INDEPENDENT SOFTMAX MARGINAL DISTRIBUTIONS",
        "P_P[i] = exp( y_{plant}[i] ) / sum_{m=0}^{54} exp( y_{plant}[m] ),   for i in {0, ..., 54}\n"
        "P_D[j] = exp( y_{disease}[j] ) / sum_{n=0}^{174} exp( y_{disease}[n] ), for j in {0, ..., 174}"
    )

    add_h3("2.3.1 Mathematical Derivation of Calibrated Geometric-Mean Joint Likelihood")
    add_p("Under biological co-occurrence rules, a plant cannot suffer from a pathogen that does not infect that botanical species (e.g., Apple Scab cannot infect Rice). We define the biological co-occurrence matrix Omega in {0, 1}^{55 x 175}, containing exactly 333 valid non-zero entries (Omega_{ij} = 1). The joint probability of observing plant i and disease j is given by the product of marginals:")
    add_callout(
        "JOINT PROBABILITY EQUATION",
        "P( Plant = i AND Disease = j | x ) = P_P[i] * P_D[j]"
    )
    add_p("To map this joint probability into a robust percentage confidence score S_{calibrated} while strictly punishing low confidence in either individual head, we implement the calibrated geometric-mean likelihood:")
    add_callout(
        "CALIBRATED GEOMETRIC-MEAN CONFIDENCE FORMULA",
        "S_{calibrated}(k) = sqrt( max( 0, P_P[i_k] * P_D[j_k] ) ) * 100.0,  for k in {1, ..., 333}"
    )
    add_p("The geometric mean is mathematically superior to the arithmetic mean S_{arithmetic} = 0.5 * (P_P + P_D) * 100 in eliminating false-positive out-of-distribution classifications. Consider an out-of-distribution image (e.g., a green wooden desk). The plant head may produce an accidental false match of P_P = 0.85 (due to green color similarity), while the disease head produces P_D = 0.04 (as no fungal lesion pattern exists):")
    add_bullet("S_{arithmetic} = 0.5 * (0.85 + 0.04) * 100 = 44.5%. Because 44.5% > 40.0% threshold, the arithmetic mean fails and outputs a false disease diagnosis!", bold_prefix="Arithmetic Mean Failure: ")
    add_bullet("S_{geometric} = sqrt(0.85 * 0.04) * 100 = sqrt(0.0340) * 100 = 18.44%. Because 18.44% << 40.0% threshold, the geometric mean correctly suppresses the false alarm and triggers OOD non-crop gating!", bold_prefix="Geometric Mean Success: ")

    add_h2("2.4 Agricultural Advisory Systems & Integrated Pest Management")
    add_p("A primary shortcoming of computer vision literature in agricultural diagnostics is the stopping of the computational pipeline at classification labels. Informing a smallholder farmer that a leaf has 'Potato Late Blight' with 94% accuracy is clinically useless unless accompanied by immediate, actionable, and environmentally sustainable treatment protocols.")
    add_p("Our system couples vision inference directly with Integrated Pest Management (IPM) protocols structured across five clinical pillars: (1) Symptoms verification checklist, (2) Biological etiology and causal organism identification, (3) Certified organic treatments (copper sulfates, neem extracts, Trichoderma biocontrol), (4) Targeted chemical fungicides with strict dosage concentrations and pre-harvest intervals (PHI), and (5) Cultural prevention practices (crop rotation, drip irrigation, sanitized pruning).")

    add_h2("2.5 Comprehensive Literature Review Matrix (12 Benchmark Papers)")
    add_p("To establish the theoretical and empirical justification for the proposed DPD ViT-Base architecture, Table 2.1 provides an exhaustive comparative synthesis of 12 landmark publications in plant pathology computer vision over the past decade.")

    lit_headers = ["Study & Authors", "Architecture", "Dataset & Scope", "Classes", "Accuracy", "Operational Limitations"]
    lit_rows = [
        [
            p['citation'],
            p['architecture'],
            p['dataset'],
            p['crops_diseases'],
            p['accuracy'],
            p['limitations']
        ] for p in report_data.LITERATURE_PAPERS
    ]
    add_tbl(
        lit_headers, 
        lit_rows, 
        col_widths=[Inches(1.1), Inches(1.3), Inches(1.3), Inches(1.0), Inches(0.9), Inches(1.8)],
        caption="Table 2.1: Comparative analysis of 12 existing plant pathology approaches vs. proposed DPD ViT-Base"
    )

    add_h2("2.6 Identified Research Gaps & Proposed Technical Novelties")
    add_p("Based on the exhaustive literature synthesis in Table 2.1, five critical research gaps were identified:")
    add_bullet("Existing benchmarks artificially constrain scope to single-crop narrow classifications (average 14 crops, 38 classes). In commercial farming, multi-crop operations require a single unified diagnostic platform supporting 50+ crops.", bold_prefix="Gap 1 (Taxonomic Breadth): ")
    add_bullet("Standard CNN classifiers enforce monolithic single-head outputs, forcing 300+ classes into a single Softmax layer that suffers from severe gradient interference.", bold_prefix="Gap 2 (Head Decoupling): ")
    add_bullet("Traditional models lack calibration, outputting high confidence on non-leaf background objects and inducing false chemical application.", bold_prefix="Gap 3 (Confidence Calibration): ")
    add_bullet("Existing academic vision systems terminate at text class labels, failing to provide actionable chemical, organic, and preventive treatment guidance.", bold_prefix="Gap 4 (Clinical Advisory Linkage): ")
    add_bullet("Prevailing systems lack enterprise software qualities, such as asynchronous ASGI event loops, WAL-based database concurrency, IDOR authorization, and automated clinical PDF reporting.", bold_prefix="Gap 5 (Production Architecture): ")

    doc.add_page_break()
