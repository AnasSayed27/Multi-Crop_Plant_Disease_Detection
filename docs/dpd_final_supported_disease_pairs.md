# Final Supported Crop-Disease Pairs Specification

This document defines the exact supported crop-disease pairs filtered strictly by the objective minimum-data criteria:

- **Total Images per Class**: $\ge 100$ DPD images
- **Official Test Set per Class**: $\ge 20$ DPD test images
- **Healthy Baseline**: Required for crops supporting healthy-vs-disease diagnostic triage
- **Intra-Crop Imbalance Audit**: Evaluates and flags crops where $\text{Max} / \text{Min} > 10\times$
- **Agricultural Advisory**: Confirmed standard agronomic management protocols available

---

## 1. Summary of Qualified Crops & Pairs

- **Total Qualified Crops with Healthy Triage Support**: **32 crops** (192 pairs, 227,949 images)
- **Specialized Single-Condition / Pathology-Only Crops (No Healthy Baseline)**: **13 crops** (22 pairs, 14,773 images)

---

## 2. Core Recommended Crops (With Healthy Baseline Triage)

### 1. **Tomato** (`tomato`) — 17 Supported Classes (37,638 Total Images)
- **Triage Support**: Healthy baseline verified (`tomato_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (53.7×)** (Min: 104 | Max: 5,580)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `yellow_leaf_curl_virus` | `tomato_yellow_leaf_curl_virus` | 4,464 | 1,116 | **5,580** | Standard cultural / chemical / IPM management |
| 2 | `septoria_leaf_spot` | `tomato_septoria_leaf_spot` | 4,456 | 1,114 | **5,570** | Standard cultural / chemical / IPM management |
| 3 | `healthy` | `tomato_healthy` | 2,868 | 718 | **3,586** | Maintain standard preventive nutrition & monitoring |
| 4 | `late_blight` | `tomato_late_blight` | 2,644 | 661 | **3,305** | Standard cultural / chemical / IPM management |
| 5 | `bacterial_spot` | `tomato_bacterial_spot` | 2,511 | 628 | **3,139** | Standard cultural / chemical / IPM management |
| 6 | `mosaic_virus` | `tomato_mosaic_virus` | 2,188 | 548 | **2,736** | Standard cultural / chemical / IPM management |
| 7 | `leaf_mold` | `tomato_leaf_mold` | 2,047 | 512 | **2,559** | Standard cultural / chemical / IPM management |
| 8 | `early_blight` | `tomato_early_blight` | 1,884 | 472 | **2,356** | Standard cultural / chemical / IPM management |
| 9 | `target_spot` | `tomato_target_spot` | 1,697 | 425 | **2,122** | Standard cultural / chemical / IPM management |
| 10 | `spider_mites` | `tomato_spider_mites` | 1,612 | 404 | **2,016** | Standard cultural / chemical / IPM management |
| 11 | `leaf_blight` | `tomato_leaf_blight` | 1,004 | 251 | **1,255** | Standard cultural / chemical / IPM management |
| 12 | `powdery_mildew` | `tomato_powdery_mildew` | 810 | 203 | **1,013** | Standard cultural / chemical / IPM management |
| 13 | `brown_spot` | `tomato_brown_spot` | 609 | 153 | **762** | Standard cultural / chemical / IPM management |
| 14 | `verticulium_wilt` | `tomato_verticulium_wilt` | 571 | 143 | **714** | Standard cultural / chemical / IPM management |
| 15 | `curl` | `tomato_curl` | 369 | 93 | **462** | Standard cultural / chemical / IPM management |
| 16 | `blight_leaf` | `tomato_blight_leaf` | 287 | 72 | **359** | Standard cultural / chemical / IPM management |
| 17 | `bacterial_leaf_spot` | `tomato_bacterial_leaf_spot` | 83 | 21 | **104** | Standard cultural / chemical / IPM management |

---

### 2. **Cassava** (`cassava`) — 9 Supported Classes (37,220 Total Images)
- **Triage Support**: Healthy baseline verified (`cassava_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (43.5×)** (Min: 414 | Max: 17,995)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `mosaic` | `cassava_mosaic` | 14,395 | 3,600 | **17,995** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `cassava_healthy` | 3,736 | 934 | **4,670** | Maintain standard preventive nutrition & monitoring |
| 3 | `bacterial_blight` | `cassava_bacterial_blight` | 3,133 | 784 | **3,917** | Standard cultural / chemical / IPM management |
| 4 | `brown_streak_disease` | `cassava_brown_streak_disease` | 3,114 | 779 | **3,893** | Standard cultural / chemical / IPM management |
| 5 | `green_mottle` | `cassava_green_mottle` | 1,805 | 452 | **2,257** | Standard cultural / chemical / IPM management |
| 6 | `green_mite` | `cassava_green_mite` | 1,649 | 413 | **2,062** | Standard cultural / chemical / IPM management |
| 7 | `brown_spot` | `cassava_brown_spot` | 1,160 | 291 | **1,451** | Standard cultural / chemical / IPM management |
| 8 | `brown_leaf_spot` | `cassava_brown_leaf_spot` | 448 | 113 | **561** | Standard cultural / chemical / IPM management |
| 9 | `red_mite` | `cassava_red_mite` | 331 | 83 | **414** | Standard cultural / chemical / IPM management |

---

### 3. **Apple** (`apple`) — 17 Supported Classes (32,749 Total Images)
- **Triage Support**: Healthy baseline verified (`apple_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (46.3×)** (Min: 162 | Max: 7,499)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `apple_healthy` | 5,999 | 1,500 | **7,499** | Maintain standard preventive nutrition & monitoring |
| 2 | `rust` | `apple_rust` | 3,746 | 938 | **4,684** | Standard cultural / chemical / IPM management |
| 3 | `frog_eye_leaf_spot` | `apple_frog_eye_leaf_spot` | 2,544 | 637 | **3,181** | Standard cultural / chemical / IPM management |
| 4 | `brown_spot` | `apple_brown_spot` | 2,010 | 503 | **2,513** | Standard cultural / chemical / IPM management |
| 5 | `alternaria_blotch` | `apple_alternaria_blotch` | 1,912 | 479 | **2,391** | Standard cultural / chemical / IPM management |
| 6 | `mosaic_virus` | `apple_mosaic_virus` | 1,896 | 474 | **2,370** | Standard cultural / chemical / IPM management |
| 7 | `grey_spot` | `apple_grey_spot` | 1,826 | 457 | **2,283** | Standard cultural / chemical / IPM management |
| 8 | `marssonina_blotch` | `apple_marssonina_blotch` | 1,686 | 422 | **2,108** | Standard cultural / chemical / IPM management |
| 9 | `scab` | `apple_scab` | 1,328 | 333 | **1,661** | Standard cultural / chemical / IPM management |
| 10 | `powdery_mildew` | `apple_powdery_mildew` | 947 | 237 | **1,184** | Standard cultural / chemical / IPM management |
| 11 | `alternaria_leaf_spot` | `apple_alternaria_leaf_spot` | 644 | 161 | **805** | Standard cultural / chemical / IPM management |
| 12 | `black_rot` | `apple_black_rot` | 561 | 141 | **702** | Standard cultural / chemical / IPM management |
| 13 | `eriosoma_lanigerum` | `apple_eriosoma_lanigerum` | 292 | 74 | **366** | Standard cultural / chemical / IPM management |
| 14 | `cedar_apple_rust` | `apple_cedar_apple_rust` | 285 | 72 | **357** | Standard cultural / chemical / IPM management |
| 15 | `monillia_laxa` | `apple_monillia_laxa` | 204 | 51 | **255** | Standard cultural / chemical / IPM management |
| 16 | `venturia_inaequalis` | `apple_venturia_inaequalis` | 182 | 46 | **228** | Standard cultural / chemical / IPM management |
| 17 | `aphis_spp` | `apple_aphis_spp` | 129 | 33 | **162** | Standard cultural / chemical / IPM management |

---

### 4. **Corn** (`corn`) — 12 Supported Classes (26,630 Total Images)
- **Triage Support**: Healthy baseline verified (`corn_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (56.8×)** (Min: 126 | Max: 7,161)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `streak_virus` | `corn_streak_virus` | 5,728 | 1,433 | **7,161** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `corn_healthy` | 5,266 | 1,317 | **6,583** | Maintain standard preventive nutrition & monitoring |
| 3 | `lethal_necrosis` | `corn_lethal_necrosis` | 3,183 | 796 | **3,979** | Standard cultural / chemical / IPM management |
| 4 | `northern_leaf_blight` | `corn_northern_leaf_blight` | 2,323 | 581 | **2,904** | Standard cultural / chemical / IPM management |
| 5 | `leaf_blight` | `corn_leaf_blight` | 1,642 | 411 | **2,053** | Standard cultural / chemical / IPM management |
| 6 | `spot` | `corn_spot` | 1,239 | 311 | **1,550** | Standard cultural / chemical / IPM management |
| 7 | `rust` | `corn_rust` | 1,125 | 283 | **1,408** | Standard cultural / chemical / IPM management |
| 8 | `yellowing` | `corn_yellowing` | 242 | 61 | **303** | Standard cultural / chemical / IPM management |
| 9 | `smut` | `corn_smut` | 172 | 43 | **215** | Standard cultural / chemical / IPM management |
| 10 | `streak` | `corn_streak` | 141 | 36 | **177** | Standard cultural / chemical / IPM management |
| 11 | `brown_spot` | `corn_brown_spot` | 136 | 35 | **171** | Standard cultural / chemical / IPM management |
| 12 | `gray_leaf_spot` | `corn_gray_leaf_spot` | 100 | 26 | **126** | Standard cultural / chemical / IPM management |

---

### 5. **Paddy** (`paddy`) — 14 Supported Classes (19,063 Total Images)
- **Triage Support**: Healthy baseline verified (`paddy_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (24.8×)** (Min: 123 | Max: 3,055)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `blast` | `paddy_blast` | 2,443 | 612 | **3,055** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `paddy_healthy` | 2,248 | 563 | **2,811** | Maintain standard preventive nutrition & monitoring |
| 3 | `hispa` | `paddy_hispa` | 1,958 | 490 | **2,448** | Standard cultural / chemical / IPM management |
| 4 | `tungro` | `paddy_tungro` | 1,933 | 485 | **2,418** | Standard cultural / chemical / IPM management |
| 5 | `brown_spot` | `paddy_brown_spot` | 1,764 | 444 | **2,208** | Standard cultural / chemical / IPM management |
| 6 | `white_stem_borer` | `paddy_white_stem_borer` | 900 | 226 | **1,126** | Standard cultural / chemical / IPM management |
| 7 | `bacterial_blight` | `paddy_bacterial_blight` | 824 | 208 | **1,032** | Standard cultural / chemical / IPM management |
| 8 | `leaf_roller` | `paddy_leaf_roller` | 798 | 200 | **998** | Standard cultural / chemical / IPM management |
| 9 | `downy_mildew` | `paddy_downy_mildew` | 626 | 157 | **783** | Standard cultural / chemical / IPM management |
| 10 | `yellow_stem_borer` | `paddy_yellow_stem_borer` | 576 | 144 | **720** | Standard cultural / chemical / IPM management |
| 11 | `black_stem_borer` | `paddy_black_stem_borer` | 394 | 99 | **493** | Standard cultural / chemical / IPM management |
| 12 | `bacterial_panicle_blight` | `paddy_bacterial_panicle_blight` | 352 | 89 | **441** | Standard cultural / chemical / IPM management |
| 13 | `bacterial_leaf_streak` | `paddy_bacterial_leaf_streak` | 325 | 82 | **407** | Standard cultural / chemical / IPM management |
| 14 | `leafblast` | `paddy_leafblast` | 98 | 25 | **123** | Standard cultural / chemical / IPM management |

---

### 6. **Soybean** (`soybean`) — 7 Supported Classes (11,818 Total Images)
- **Triage Support**: Healthy baseline verified (`soybean_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (54.6×)** (Min: 108 | Max: 5,902)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `soybean_healthy` | 4,721 | 1,181 | **5,902** | Maintain standard preventive nutrition & monitoring |
| 2 | `caterpillar` | `soybean_caterpillar` | 2,550 | 638 | **3,188** | Standard cultural / chemical / IPM management |
| 3 | `diabrotica_speciosa` | `soybean_diabrotica_speciosa` | 1,758 | 440 | **2,198** | Standard cultural / chemical / IPM management |
| 4 | `frog_eye_leaf_spot` | `soybean_frog_eye_leaf_spot` | 153 | 39 | **192** | Standard cultural / chemical / IPM management |
| 5 | `downy_mildew` | `soybean_downy_mildew` | 96 | 25 | **121** | Standard cultural / chemical / IPM management |
| 6 | `mosaic` | `soybean_mosaic` | 87 | 22 | **109** | Standard cultural / chemical / IPM management |
| 7 | `rust` | `soybean_rust` | 86 | 22 | **108** | Standard cultural / chemical / IPM management |

---

### 7. **Grape** (`grape`) — 5 Supported Classes (6,457 Total Images)
- **Triage Support**: Healthy baseline verified (`grape_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (8.2×)** (Min: 278 | Max: 2,271)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `esca` | `grape_esca` | 1,816 | 455 | **2,271** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `grape_healthy` | 1,182 | 296 | **1,478** | Maintain standard preventive nutrition & monitoring |
| 3 | `black_rot` | `grape_black_rot` | 1,083 | 271 | **1,354** | Standard cultural / chemical / IPM management |
| 4 | `leaf_blight` | `grape_leaf_blight` | 860 | 216 | **1,076** | Standard cultural / chemical / IPM management |
| 5 | `downy_mildew` | `grape_downy_mildew` | 222 | 56 | **278** | Standard cultural / chemical / IPM management |

---

### 8. **Potato** (`potato`) — 3 Supported Classes (6,415 Total Images)
- **Triage Support**: Healthy baseline verified (`potato_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (2.3×)** (Min: 1,163 | Max: 2,729)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `early_blight` | `potato_early_blight` | 2,183 | 546 | **2,729** | Standard cultural / chemical / IPM management |
| 2 | `late_blight` | `potato_late_blight` | 2,018 | 505 | **2,523** | Standard cultural / chemical / IPM management |
| 3 | `healthy` | `potato_healthy` | 930 | 233 | **1,163** | Maintain standard preventive nutrition & monitoring |

---

### 9. **Sugarcane** (`sugarcane`) — 13 Supported Classes (5,148 Total Images)
- **Triage Support**: Healthy baseline verified (`sugarcane_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (9.0×)** (Min: 100 | Max: 904)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `yellowing` | `sugarcane_yellowing` | 722 | 182 | **904** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `sugarcane_healthy` | 517 | 130 | **647** | Maintain standard preventive nutrition & monitoring |
| 3 | `brown_spot` | `sugarcane_brown_spot` | 516 | 130 | **646** | Standard cultural / chemical / IPM management |
| 4 | `red_rot` | `sugarcane_red_rot` | 404 | 101 | **505** | Standard cultural / chemical / IPM management |
| 5 | `sett_rot` | `sugarcane_sett_rot` | 383 | 96 | **479** | Standard cultural / chemical / IPM management |
| 6 | `rust` | `sugarcane_rust` | 353 | 89 | **442** | Standard cultural / chemical / IPM management |
| 7 | `mosaic` | `sugarcane_mosaic` | 300 | 76 | **376** | Standard cultural / chemical / IPM management |
| 8 | `grassy_shoot` | `sugarcane_grassy_shoot` | 240 | 60 | **300** | Standard cultural / chemical / IPM management |
| 9 | `viral` | `sugarcane_viral` | 176 | 45 | **221** | Standard cultural / chemical / IPM management |
| 10 | `pokkah_boeng` | `sugarcane_pokkah_boeng` | 166 | 42 | **208** | Standard cultural / chemical / IPM management |
| 11 | `banded_chlorosis` | `sugarcane_banded_chlorosis` | 137 | 35 | **172** | Standard cultural / chemical / IPM management |
| 12 | `smut` | `sugarcane_smut` | 118 | 30 | **148** | Standard cultural / chemical / IPM management |
| 13 | `brown_rust` | `sugarcane_brown_rust` | 80 | 20 | **100** | Standard cultural / chemical / IPM management |

---

### 10. **Peach** (`peach`) — 6 Supported Classes (4,047 Total Images)
- **Triage Support**: Healthy baseline verified (`peach_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (14.5×)** (Min: 158 | Max: 2,297)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `bacterial_spot` | `peach_bacterial_spot` | 1,837 | 460 | **2,297** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `peach_healthy` | 537 | 135 | **672** | Maintain standard preventive nutrition & monitoring |
| 3 | `parthenolecanium_corni` | `peach_parthenolecanium_corni` | 340 | 86 | **426** | Standard cultural / chemical / IPM management |
| 4 | `monillia_laxa` | `peach_monillia_laxa` | 250 | 63 | **313** | Standard cultural / chemical / IPM management |
| 5 | `curl` | `peach_curl` | 144 | 37 | **181** | Standard cultural / chemical / IPM management |
| 6 | `brown_rot` | `peach_brown_rot` | 126 | 32 | **158** | Standard cultural / chemical / IPM management |

---

### 11. **Wheat** (`wheat`) — 9 Supported Classes (3,884 Total Images)
- **Triage Support**: Healthy baseline verified (`wheat_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (10.0×)** (Min: 113 | Max: 1,127)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `rust` | `wheat_rust` | 901 | 226 | **1,127** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `wheat_healthy` | 543 | 136 | **679** | Maintain standard preventive nutrition & monitoring |
| 3 | `stripe_rust` | `wheat_stripe_rust` | 496 | 125 | **621** | Standard cultural / chemical / IPM management |
| 4 | `loose_smut` | `wheat_loose_smut` | 320 | 80 | **400** | Standard cultural / chemical / IPM management |
| 5 | `head_scab` | `wheat_head_scab` | 208 | 52 | **260** | Standard cultural / chemical / IPM management |
| 6 | `powdery_mildew` | `wheat_powdery_mildew` | 200 | 51 | **251** | Standard cultural / chemical / IPM management |
| 7 | `root_rot` | `wheat_root_rot` | 197 | 50 | **247** | Standard cultural / chemical / IPM management |
| 8 | `septoria_blotch` | `wheat_septoria_blotch` | 148 | 38 | **186** | Standard cultural / chemical / IPM management |
| 9 | `bacterial_leaf_streak` | `wheat_bacterial_leaf_streak` | 90 | 23 | **113** | Standard cultural / chemical / IPM management |

---

### 12. **Coffee** (`coffee`) — 6 Supported Classes (3,861 Total Images)
- **Triage Support**: Healthy baseline verified (`coffee_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (10.4×)** (Min: 147 | Max: 1,531)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `rust` | `coffee_rust` | 1,224 | 307 | **1,531** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `coffee_healthy` | 823 | 206 | **1,029** | Maintain standard preventive nutrition & monitoring |
| 3 | `miner` | `coffee_miner` | 514 | 130 | **644** | Standard cultural / chemical / IPM management |
| 4 | `phoma` | `coffee_phoma` | 278 | 70 | **348** | Standard cultural / chemical / IPM management |
| 5 | `spider_mites` | `coffee_spider_mites` | 129 | 33 | **162** | Standard cultural / chemical / IPM management |
| 6 | `cercospora` | `coffee_cercospora` | 117 | 30 | **147** | Standard cultural / chemical / IPM management |

---

### 13. **Mango** (`mango`) — 8 Supported Classes (3,723 Total Images)
- **Triage Support**: Healthy baseline verified (`mango_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (2.3×)** (Min: 238 | Max: 536)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `mango_healthy` | 428 | 108 | **536** | Maintain standard preventive nutrition & monitoring |
| 2 | `sooty_mould` | `mango_sooty_mould` | 399 | 100 | **499** | Standard cultural / chemical / IPM management |
| 3 | `powdery_mildew` | `mango_powdery_mildew` | 397 | 100 | **497** | Standard cultural / chemical / IPM management |
| 4 | `bacterial_canker` | `mango_bacterial_canker` | 396 | 99 | **495** | Standard cultural / chemical / IPM management |
| 5 | `gall_midge` | `mango_gall_midge` | 394 | 99 | **493** | Standard cultural / chemical / IPM management |
| 6 | `die_back` | `mango_die_back` | 392 | 99 | **491** | Standard cultural / chemical / IPM management |
| 7 | `anthracnose` | `mango_anthracnose` | 379 | 95 | **474** | Standard cultural / chemical / IPM management |
| 8 | `cutting_weevil` | `mango_cutting_weevil` | 190 | 48 | **238** | Standard cultural / chemical / IPM management |

---

### 14. **Olive** (`olive`) — 3 Supported Classes (3,162 Total Images)
- **Triage Support**: Healthy baseline verified (`olive_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.7×)** (Min: 853 | Max: 1,443)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `peacock_spot` | `olive_peacock_spot` | 1,154 | 289 | **1,443** | Standard cultural / chemical / IPM management |
| 2 | `aculus_olearius` | `olive_aculus_olearius` | 692 | 174 | **866** | Standard cultural / chemical / IPM management |
| 3 | `healthy` | `olive_healthy` | 682 | 171 | **853** | Maintain standard preventive nutrition & monitoring |

---

### 15. **Peanut** (`peanut`) — 5 Supported Classes (3,056 Total Images)
- **Triage Support**: Healthy baseline verified (`peanut_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (4.1×)** (Min: 226 | Max: 928)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `peanut_healthy` | 742 | 186 | **928** | Maintain standard preventive nutrition & monitoring |
| 2 | `early_leaf_spot` | `peanut_early_leaf_spot` | 707 | 177 | **884** | Standard cultural / chemical / IPM management |
| 3 | `late_leaf_spot` | `peanut_late_leaf_spot` | 551 | 138 | **689** | Standard cultural / chemical / IPM management |
| 4 | `nutrition_deficiency` | `peanut_nutrition_deficiency` | 263 | 66 | **329** | Standard cultural / chemical / IPM management |
| 5 | `rust` | `peanut_rust` | 180 | 46 | **226** | Standard cultural / chemical / IPM management |

---

### 16. **Pepper Bell** (`pepper_bell`) — 2 Supported Classes (2,579 Total Images)
- **Triage Support**: Healthy baseline verified (`pepper_bell_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.4×)** (Min: 1,097 | Max: 1,482)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `pepper_bell_healthy` | 1,185 | 297 | **1,482** | Maintain standard preventive nutrition & monitoring |
| 2 | `bacterial_spot` | `pepper_bell_bacterial_spot` | 877 | 220 | **1,097** | Standard cultural / chemical / IPM management |

---

### 17. **Cherry** (`cherry`) — 4 Supported Classes (2,564 Total Images)
- **Triage Support**: Healthy baseline verified (`cherry_healthy`)
- **Balance Status**: ⚠️ **FLAGGED HIGH IMBALANCE (10.1×)** (Min: 107 | Max: 1,079)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `powdery_mildew` | `cherry_powdery_mildew` | 863 | 216 | **1,079** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `cherry_healthy` | 817 | 205 | **1,022** | Maintain standard preventive nutrition & monitoring |
| 3 | `aphis_spp` | `cherry_aphis_spp` | 284 | 72 | **356** | Standard cultural / chemical / IPM management |
| 4 | `spot` | `cherry_spot` | 85 | 22 | **107** | Standard cultural / chemical / IPM management |

---

### 18. **Banana** (`banana`) — 8 Supported Classes (2,518 Total Images)
- **Triage Support**: Healthy baseline verified (`banana_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (6.0×)** (Min: 135 | Max: 814)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `xamthomonas` | `banana_xamthomonas` | 651 | 163 | **814** | Standard cultural / chemical / IPM management |
| 2 | `sigatoka` | `banana_sigatoka` | 376 | 95 | **471** | Standard cultural / chemical / IPM management |
| 3 | `segatoka` | `banana_segatoka` | 256 | 64 | **320** | Standard cultural / chemical / IPM management |
| 4 | `healthy` | `banana_healthy` | 196 | 49 | **245** | Maintain standard preventive nutrition & monitoring |
| 5 | `cordana_leaf_spot` | `banana_cordana_leaf_spot` | 169 | 43 | **212** | Standard cultural / chemical / IPM management |
| 6 | `pestalotiopsis` | `banana_pestalotiopsis` | 136 | 35 | **171** | Standard cultural / chemical / IPM management |
| 7 | `black_leaf_streak` | `banana_black_leaf_streak` | 120 | 30 | **150** | Standard cultural / chemical / IPM management |
| 8 | `bunchy_top` | `banana_bunchy_top` | 108 | 27 | **135** | Standard cultural / chemical / IPM management |

---

### 19. **Cotton** (`cotton`) — 4 Supported Classes (2,480 Total Images)
- **Triage Support**: Healthy baseline verified (`cotton_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.3×)** (Min: 552 | Max: 723)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `cotton_healthy` | 578 | 145 | **723** | Maintain standard preventive nutrition & monitoring |
| 2 | `bacterial_blight` | `cotton_bacterial_blight` | 499 | 125 | **624** | Standard cultural / chemical / IPM management |
| 3 | `powdery_mildew` | `cotton_powdery_mildew` | 464 | 117 | **581** | Standard cultural / chemical / IPM management |
| 4 | `target_spot` | `cotton_target_spot` | 441 | 111 | **552** | Standard cultural / chemical / IPM management |

---

### 20. **Papaya** (`papaya`) — 5 Supported Classes (1,857 Total Images)
- **Triage Support**: Healthy baseline verified (`papaya_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (2.5×)** (Min: 197 | Max: 494)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `ring_spot` | `papaya_ring_spot` | 395 | 99 | **494** | Standard cultural / chemical / IPM management |
| 2 | `bacterial_spot` | `papaya_bacterial_spot` | 366 | 92 | **458** | Standard cultural / chemical / IPM management |
| 3 | `anthracnose` | `papaya_anthracnose` | 284 | 71 | **355** | Standard cultural / chemical / IPM management |
| 4 | `curl` | `papaya_curl` | 282 | 71 | **353** | Standard cultural / chemical / IPM management |
| 5 | `healthy` | `papaya_healthy` | 157 | 40 | **197** | Maintain standard preventive nutrition & monitoring |

---

### 21. **Strawberry** (`strawberry`) — 2 Supported Classes (1,661 Total Images)
- **Triage Support**: Healthy baseline verified (`strawberry_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (2.2×)** (Min: 517 | Max: 1,144)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `scorch` | `strawberry_scorch` | 915 | 229 | **1,144** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `strawberry_healthy` | 413 | 104 | **517** | Maintain standard preventive nutrition & monitoring |

---

### 22. **Blueberry** (`blueberry`) — 1 Supported Classes (1,607 Total Images)
- **Triage Support**: Healthy baseline verified (`blueberry_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.0×)** (Min: 1,607 | Max: 1,607)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `blueberry_healthy` | 1,285 | 322 | **1,607** | Maintain standard preventive nutrition & monitoring |

---

### 23. **Bean** (`bean`) — 4 Supported Classes (1,408 Total Images)
- **Triage Support**: Healthy baseline verified (`bean_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (3.9×)** (Min: 113 | Max: 436)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `bean_rust` | `bean_bean_rust` | 348 | 88 | **436** | Standard cultural / chemical / IPM management |
| 2 | `angular_leaf_spot` | `bean_angular_leaf_spot` | 345 | 87 | **432** | Standard cultural / chemical / IPM management |
| 3 | `healthy` | `bean_healthy` | 341 | 86 | **427** | Maintain standard preventive nutrition & monitoring |
| 4 | `rust` | `bean_rust` | 90 | 23 | **113** | Standard cultural / chemical / IPM management |

---

### 24. **Cucumber** (`cucumber`) — 7 Supported Classes (1,269 Total Images)
- **Triage Support**: Healthy baseline verified (`cucumber_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.7×)** (Min: 159 | Max: 266)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `bacterial_wilt` | `cucumber_bacterial_wilt` | 212 | 54 | **266** | Standard cultural / chemical / IPM management |
| 2 | `powdery_mildew` | `cucumber_powdery_mildew` | 147 | 37 | **184** | Standard cultural / chemical / IPM management |
| 3 | `angular_leaf_spot` | `cucumber_angular_leaf_spot` | 144 | 36 | **180** | Standard cultural / chemical / IPM management |
| 4 | `anthracnose` | `cucumber_anthracnose` | 128 | 32 | **160** | Standard cultural / chemical / IPM management |
| 5 | `gummy_stem_blight` | `cucumber_gummy_stem_blight` | 128 | 32 | **160** | Standard cultural / chemical / IPM management |
| 6 | `healthy` | `cucumber_healthy` | 128 | 32 | **160** | Maintain standard preventive nutrition & monitoring |
| 7 | `downy_mildew` | `cucumber_downy_mildew` | 127 | 32 | **159** | Standard cultural / chemical / IPM management |

---

### 25. **Palm** (`palm`) — 3 Supported Classes (1,235 Total Images)
- **Triage Support**: Healthy baseline verified (`palm_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (2.4×)** (Min: 232 | Max: 553)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `white_scale` | `palm_white_scale` | 442 | 111 | **553** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `palm_healthy` | 360 | 90 | **450** | Maintain standard preventive nutrition & monitoring |
| 3 | `brown_spot` | `palm_brown_spot` | 185 | 47 | **232** | Standard cultural / chemical / IPM management |

---

### 26. **Blackgram** (`blackgram`) — 5 Supported Classes (1,006 Total Images)
- **Triage Support**: Healthy baseline verified (`blackgram_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.5×)** (Min: 151 | Max: 230)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `anthracnose` | `blackgram_anthracnose` | 184 | 46 | **230** | Standard cultural / chemical / IPM management |
| 2 | `yellow_mosaic` | `blackgram_yellow_mosaic` | 179 | 45 | **224** | Standard cultural / chemical / IPM management |
| 3 | `healthy` | `blackgram_healthy` | 176 | 45 | **221** | Maintain standard preventive nutrition & monitoring |
| 4 | `powdery_mildew` | `blackgram_powdery_mildew` | 144 | 36 | **180** | Standard cultural / chemical / IPM management |
| 5 | `crinckle` | `blackgram_crinckle` | 120 | 31 | **151** | Standard cultural / chemical / IPM management |

---

### 27. **Rose** (`rose`) — 3 Supported Classes (914 Total Images)
- **Triage Support**: Healthy baseline verified (`rose_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (2.0×)** (Min: 199 | Max: 404)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `rose_healthy` | 323 | 81 | **404** | Maintain standard preventive nutrition & monitoring |
| 2 | `black_spot` | `rose_black_spot` | 248 | 63 | **311** | Standard cultural / chemical / IPM management |
| 3 | `downy_mildew` | `rose_downy_mildew` | 159 | 40 | **199** | Standard cultural / chemical / IPM management |

---

### 28. **Guava** (`guava`) — 3 Supported Classes (613 Total Images)
- **Triage Support**: Healthy baseline verified (`guava_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (4.0×)** (Min: 100 | Max: 399)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `guava_healthy` | 319 | 80 | **399** | Maintain standard preventive nutrition & monitoring |
| 2 | `phytophthora` | `guava_phytophthora` | 91 | 23 | **114** | Standard cultural / chemical / IPM management |
| 3 | `scab` | `guava_scab` | 80 | 20 | **100** | Standard cultural / chemical / IPM management |

---

### 29. **Raspberry** (`raspberry`) — 1 Supported Classes (411 Total Images)
- **Triage Support**: Healthy baseline verified (`raspberry_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.0×)** (Min: 411 | Max: 411)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `raspberry_healthy` | 328 | 83 | **411** | Maintain standard preventive nutrition & monitoring |

---

### 30. **Sunflower** (`sunflower`) — 3 Supported Classes (372 Total Images)
- **Triage Support**: Healthy baseline verified (`sunflower_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.4×)** (Min: 100 | Max: 139)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `leaf_scars` | `sunflower_leaf_scars` | 111 | 28 | **139** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `sunflower_healthy` | 106 | 27 | **133** | Maintain standard preventive nutrition & monitoring |
| 3 | `downy_mildew` | `sunflower_downy_mildew` | 80 | 20 | **100** | Standard cultural / chemical / IPM management |

---

### 31. **Basil** (`basil`) — 2 Supported Classes (324 Total Images)
- **Triage Support**: Healthy baseline verified (`basil_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.0×)** (Min: 161 | Max: 163)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `downy_mildew` | `basil_downy_mildew` | 130 | 33 | **163** | Standard cultural / chemical / IPM management |
| 2 | `healthy` | `basil_healthy` | 128 | 33 | **161** | Maintain standard preventive nutrition & monitoring |

---

### 32. **Coriander** (`coriander`) — 1 Supported Classes (260 Total Images)
- **Triage Support**: Healthy baseline verified (`coriander_healthy`)
- **Balance Status**: ✅ **WELL BALANCED (1.0×)** (Min: 260 | Max: 260)
- **Advisory Readiness**: 100% standard extension advisory available

| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs | Advisory Protocol |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `healthy` | `coriander_healthy` | 208 | 52 | **260** | Maintain standard preventive nutrition & monitoring |

---

## 3. Specialized Single-Condition Crops (Excluded from Healthy Triage)

These crops meet the $\ge 100$ total / $\ge 20$ test threshold for specific diseases, but lack an official `healthy` baseline in DPD. They are supported for targeted pathology diagnosis only:

### 1. **Citrus** (`citrus`) — 3 Classes (6,387 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `greening` | `citrus_greening` | 4,611 | 1,154 | **5,765** |
| 2 | `canker` | `citrus_canker` | 412 | 104 | **516** |
| 3 | `black_spot` | `citrus_black_spot` | 84 | 22 | **106** |


### 2. **Pear** (`pear`) — 3 Classes (3,116 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `slug` | `pear_slug` | 1,616 | 404 | **2,020** |
| 2 | `spot` | `pear_spot` | 704 | 177 | **881** |
| 3 | `erwinia_amylovora` | `pear_erwinia_amylovora` | 172 | 43 | **215** |


### 3. **Pumpkin** (`pumpkin`) — 1 Classes (1,835 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `powdery_mildew` | `pumpkin_powdery_mildew` | 1,468 | 367 | **1,835** |


### 4. **Cashew** (`cashew`) — 1 Classes (1,505 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `red_rust` | `cashew_red_rust` | 1,204 | 301 | **1,505** |


### 5. **Tea** (`tea`) — 5 Classes (645 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `red_leaf_spot` | `tea_red_leaf_spot` | 143 | 36 | **179** |
| 2 | `white_spot` | `tea_white_spot` | 112 | 28 | **140** |
| 3 | `algal_leaf` | `tea_algal_leaf` | 90 | 23 | **113** |
| 4 | `brown_blight` | `tea_brown_blight` | 90 | 23 | **113** |
| 5 | `anthracnose` | `tea_anthracnose` | 80 | 20 | **100** |


### 6. **Cauliflower** (`cauliflower`) — 2 Classes (309 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_spot` | `cauliflower_bacterial_spot` | 130 | 33 | **163** |
| 2 | `downy_mildew` | `cauliflower_downy_mildew` | 116 | 30 | **146** |


### 7. **Squash** (`squash`) — 1 Classes (186 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `powdery_mildew` | `squash_powdery_mildew` | 148 | 38 | **186** |


### 8. **Walnut** (`walnut`) — 1 Classes (179 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `gnomonia_leptostyla` | `walnut_gnomonia_leptostyla` | 143 | 36 | **179** |


### 9. **Zucchini** (`zucchini`) — 1 Classes (169 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `powdery_mildew` | `zucchini_powdery_mildew` | 135 | 34 | **169** |


### 10. **Apricot** (`apricot`) — 1 Classes (120 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `coryneum_blight` | `apricot_coryneum_blight` | 96 | 24 | **120** |


### 11. **Maple** (`maple`) — 1 Classes (113 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `tar_spot` | `maple_tar_spot` | 90 | 23 | **113** |


### 12. **Garlic** (`garlic`) — 1 Classes (105 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `rust` | `garlic_rust` | 84 | 21 | **105** |


### 13. **Brassica** (`brassica`) — 1 Classes (104 Images) [No Healthy Baseline]
| # | Supported Disease Class | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `black_rot` | `brassica_black_rot` | 83 | 21 | **104** |

