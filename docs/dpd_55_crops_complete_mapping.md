# DPD Benchmark: Complete 55-Crop to Disease Mapping Table

This document contains the authoritative crop-to-disease taxonomy and exact image distributions extracted from DPD's official metadata (`train.csv` + `test.csv`, 248,578 total image rows).

## Summary Statistics

- **Total Unique Crops**: 55
- **Total Unique Disease Categories**: 175
- **Total Crop-Disease Combinations (Pairs)**: 333
- **Total Ground-Truth Images in Metadata**: 248,578 images (198,711 Train / 49,867 Test)

---

## Complete 55-Crop Disease Breakdown Table

### 1. **Apple** (`apple`)
- **Disease Categories**: 17
- **Total Images**: **32,749** (Train: 26,191 | Test: 6,558)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `alternaria_blotch` | `apple_alternaria_blotch` | 1,912 | 479 | **2,391** |
| 2 | `alternaria_leaf_spot` | `apple_alternaria_leaf_spot` | 644 | 161 | **805** |
| 3 | `aphis_spp` | `apple_aphis_spp` | 129 | 33 | **162** |
| 4 | `black_rot` | `apple_black_rot` | 561 | 141 | **702** |
| 5 | `brown_spot` | `apple_brown_spot` | 2,010 | 503 | **2,513** |
| 6 | `cedar_apple_rust` | `apple_cedar_apple_rust` | 285 | 72 | **357** |
| 7 | `eriosoma_lanigerum` | `apple_eriosoma_lanigerum` | 292 | 74 | **366** |
| 8 | `frog_eye_leaf_spot` | `apple_frog_eye_leaf_spot` | 2,544 | 637 | **3,181** |
| 9 | `grey_spot` | `apple_grey_spot` | 1,826 | 457 | **2,283** |
| 10 | `healthy` | `apple_healthy` | 5,999 | 1,500 | **7,499** |
| 11 | `marssonina_blotch` | `apple_marssonina_blotch` | 1,686 | 422 | **2,108** |
| 12 | `monillia_laxa` | `apple_monillia_laxa` | 204 | 51 | **255** |
| 13 | `mosaic_virus` | `apple_mosaic_virus` | 1,896 | 474 | **2,370** |
| 14 | `powdery_mildew` | `apple_powdery_mildew` | 947 | 237 | **1,184** |
| 15 | `rust` | `apple_rust` | 3,746 | 938 | **4,684** |
| 16 | `scab` | `apple_scab` | 1,328 | 333 | **1,661** |
| 17 | `venturia_inaequalis` | `apple_venturia_inaequalis` | 182 | 46 | **228** |

---

### 2. **Apricot** (`apricot`)
- **Disease Categories**: 2
- **Total Images**: **205** (Train: 164 | Test: 41)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `coryneum_blight` | `apricot_coryneum_blight` | 96 | 24 | **120** |
| 2 | `monillia_laxa` | `apricot_monillia_laxa` | 68 | 17 | **85** |

---

### 3. **Banana** (`banana`)
- **Disease Categories**: 11
- **Total Images**: **2,702** (Train: 2,158 | Test: 544)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `banana_anthracnose` | 54 | 14 | **68** |
| 2 | `black_leaf_streak` | `banana_black_leaf_streak` | 120 | 30 | **150** |
| 3 | `bunchy_top` | `banana_bunchy_top` | 108 | 27 | **135** |
| 4 | `cigar_end_rot` | `banana_cigar_end_rot` | 44 | 11 | **55** |
| 5 | `cordana_leaf_spot` | `banana_cordana_leaf_spot` | 169 | 43 | **212** |
| 6 | `healthy` | `banana_healthy` | 196 | 49 | **245** |
| 7 | `panama_disease` | `banana_panama_disease` | 48 | 13 | **61** |
| 8 | `pestalotiopsis` | `banana_pestalotiopsis` | 136 | 35 | **171** |
| 9 | `segatoka` | `banana_segatoka` | 256 | 64 | **320** |
| 10 | `sigatoka` | `banana_sigatoka` | 376 | 95 | **471** |
| 11 | `xamthomonas` | `banana_xamthomonas` | 651 | 163 | **814** |

---

### 4. **Basil** (`basil`)
- **Disease Categories**: 3
- **Total Images**: **410** (Train: 326 | Test: 84)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `downy_mildew` | `basil_downy_mildew` | 130 | 33 | **163** |
| 2 | `fusarium_wilt` | `basil_fusarium_wilt` | 68 | 18 | **86** |
| 3 | `healthy` | `basil_healthy` | 128 | 33 | **161** |

---

### 5. **Bean** (`bean`)
- **Disease Categories**: 6
- **Total Images**: **1,521** (Train: 1,214 | Test: 307)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `angular_leaf_spot` | `bean_angular_leaf_spot` | 345 | 87 | **432** |
| 2 | `bean_rust` | `bean_bean_rust` | 348 | 88 | **436** |
| 3 | `halo_blight` | `bean_halo_blight` | 44 | 11 | **55** |
| 4 | `healthy` | `bean_healthy` | 341 | 86 | **427** |
| 5 | `mosaic_virus` | `bean_mosaic_virus` | 46 | 12 | **58** |
| 6 | `rust` | `bean_rust` | 90 | 23 | **113** |

---

### 6. **Blackgram** (`blackgram`)
- **Disease Categories**: 5
- **Total Images**: **1,006** (Train: 803 | Test: 203)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `blackgram_anthracnose` | 184 | 46 | **230** |
| 2 | `crinckle` | `blackgram_crinckle` | 120 | 31 | **151** |
| 3 | `healthy` | `blackgram_healthy` | 176 | 45 | **221** |
| 4 | `powdery_mildew` | `blackgram_powdery_mildew` | 144 | 36 | **180** |
| 5 | `yellow_mosaic` | `blackgram_yellow_mosaic` | 179 | 45 | **224** |

---

### 7. **Blueberry** (`blueberry`)
- **Disease Categories**: 6
- **Total Images**: **1,805** (Train: 1,441 | Test: 364)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `blueberry_anthracnose` | 28 | 8 | **36** |
| 2 | `botrytis_blight` | `blueberry_botrytis_blight` | 27 | 7 | **34** |
| 3 | `healthy` | `blueberry_healthy` | 1,285 | 322 | **1,607** |
| 4 | `mummy_berry` | `blueberry_mummy_berry` | 35 | 9 | **44** |
| 5 | `rust` | `blueberry_rust` | 34 | 9 | **43** |
| 6 | `scorch` | `blueberry_scorch` | 32 | 9 | **41** |

---

### 8. **Brassica** (`brassica`)
- **Disease Categories**: 1
- **Total Images**: **104** (Train: 83 | Test: 21)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `black_rot` | `brassica_black_rot` | 83 | 21 | **104** |

---

### 9. **Broccoli** (`broccoli`)
- **Disease Categories**: 3
- **Total Images**: **93** (Train: 73 | Test: 20)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `alternaria_leaf_spot` | `broccoli_alternaria_leaf_spot` | 45 | 12 | **57** |
| 2 | `downy_mildew` | `broccoli_downy_mildew` | 23 | 6 | **29** |
| 3 | `ring_spot` | `broccoli_ring_spot` | 5 | 2 | **7** |

---

### 10. **Cabbage** (`cabbage`)
- **Disease Categories**: 3
- **Total Images**: **221** (Train: 176 | Test: 45)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `alternaria_leaf_spot` | `cabbage_alternaria_leaf_spot` | 44 | 11 | **55** |
| 2 | `black_rot` | `cabbage_black_rot` | 71 | 18 | **89** |
| 3 | `downy_mildew` | `cabbage_downy_mildew` | 61 | 16 | **77** |

---

### 11. **Carrot** (`carrot`)
- **Disease Categories**: 3
- **Total Images**: **140** (Train: 111 | Test: 29)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `alternaria_leaf_blight` | `carrot_alternaria_leaf_blight` | 42 | 11 | **53** |
| 2 | `cavity_spot` | `carrot_cavity_spot` | 57 | 15 | **72** |
| 3 | `cercospora_leaf_blight` | `carrot_cercospora_leaf_blight` | 12 | 3 | **15** |

---

### 12. **Cashew** (`cashew`)
- **Disease Categories**: 1
- **Total Images**: **1,505** (Train: 1,204 | Test: 301)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `red_rust` | `cashew_red_rust` | 1,204 | 301 | **1,505** |

---

### 13. **Cassava** (`cassava`)
- **Disease Categories**: 10
- **Total Images**: **37,285** (Train: 29,823 | Test: 7,462)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_blight` | `cassava_bacterial_blight` | 3,133 | 784 | **3,917** |
| 2 | `brown_leaf_spot` | `cassava_brown_leaf_spot` | 448 | 113 | **561** |
| 3 | `brown_spot` | `cassava_brown_spot` | 1,160 | 291 | **1,451** |
| 4 | `brown_streak_disease` | `cassava_brown_streak_disease` | 3,114 | 779 | **3,893** |
| 5 | `green_mite` | `cassava_green_mite` | 1,649 | 413 | **2,062** |
| 6 | `green_mottle` | `cassava_green_mottle` | 1,805 | 452 | **2,257** |
| 7 | `healthy` | `cassava_healthy` | 3,736 | 934 | **4,670** |
| 8 | `mosaic` | `cassava_mosaic` | 14,395 | 3,600 | **17,995** |
| 9 | `red_mite` | `cassava_red_mite` | 331 | 83 | **414** |
| 10 | `root_rot` | `cassava_root_rot` | 52 | 13 | **65** |

---

### 14. **Cauliflower** (`cauliflower`)
- **Disease Categories**: 6
- **Total Images**: **479** (Train: 380 | Test: 99)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `alternaria_leaf_spot` | `cauliflower_alternaria_leaf_spot` | 28 | 8 | **36** |
| 2 | `bacterial_soft_rot` | `cauliflower_bacterial_soft_rot` | 21 | 6 | **27** |
| 3 | `bacterial_spot` | `cauliflower_bacterial_spot` | 130 | 33 | **163** |
| 4 | `black_rot` | `cauliflower_black_rot` | 71 | 18 | **89** |
| 5 | `downy_mildew` | `cauliflower_downy_mildew` | 116 | 30 | **146** |
| 6 | `healthy` | `cauliflower_healthy` | 14 | 4 | **18** |

---

### 15. **Celery** (`celery`)
- **Disease Categories**: 2
- **Total Images**: **64** (Train: 51 | Test: 13)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `celery_anthracnose` | 23 | 6 | **29** |
| 2 | `early_blight` | `celery_early_blight` | 28 | 7 | **35** |

---

### 16. **Cherry** (`cherry`)
- **Disease Categories**: 4
- **Total Images**: **2,564** (Train: 2,049 | Test: 515)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `aphis_spp` | `cherry_aphis_spp` | 284 | 72 | **356** |
| 2 | `healthy` | `cherry_healthy` | 817 | 205 | **1,022** |
| 3 | `powdery_mildew` | `cherry_powdery_mildew` | 863 | 216 | **1,079** |
| 4 | `spot` | `cherry_spot` | 85 | 22 | **107** |

---

### 17. **Chilli** (`chilli`)
- **Disease Categories**: 4
- **Total Images**: **355** (Train: 282 | Test: 73)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `curl` | `chilli_curl` | 64 | 17 | **81** |
| 2 | `healthy` | `chilli_healthy` | 76 | 19 | **95** |
| 3 | `spot` | `chilli_spot` | 78 | 20 | **98** |
| 4 | `yellowing` | `chilli_yellowing` | 64 | 17 | **81** |

---

### 18. **Citrus** (`citrus`)
- **Disease Categories**: 5
- **Total Images**: **6,486** (Train: 5,185 | Test: 1,301)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `black_spot` | `citrus_black_spot` | 84 | 22 | **106** |
| 2 | `canker` | `citrus_canker` | 412 | 104 | **516** |
| 3 | `greening` | `citrus_greening` | 4,611 | 1,154 | **5,765** |
| 4 | `healthy` | `citrus_healthy` | 70 | 18 | **88** |
| 5 | `melanose` | `citrus_melanose` | 8 | 3 | **11** |

---

### 19. **Coffee** (`coffee`)
- **Disease Categories**: 9
- **Total Images**: **3,959** (Train: 3,161 | Test: 798)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `berry_blotch` | `coffee_berry_blotch` | 64 | 17 | **81** |
| 2 | `black_rot` | `coffee_black_rot` | 4 | 2 | **6** |
| 3 | `brown_eye_spot` | `coffee_brown_eye_spot` | 8 | 3 | **11** |
| 4 | `cercospora` | `coffee_cercospora` | 117 | 30 | **147** |
| 5 | `healthy` | `coffee_healthy` | 823 | 206 | **1,029** |
| 6 | `miner` | `coffee_miner` | 514 | 130 | **644** |
| 7 | `phoma` | `coffee_phoma` | 278 | 70 | **348** |
| 8 | `rust` | `coffee_rust` | 1,224 | 307 | **1,531** |
| 9 | `spider_mites` | `coffee_spider_mites` | 129 | 33 | **162** |

---

### 20. **Coriander** (`coriander`)
- **Disease Categories**: 1
- **Total Images**: **260** (Train: 208 | Test: 52)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `healthy` | `coriander_healthy` | 208 | 52 | **260** |

---

### 21. **Corn** (`corn`)
- **Disease Categories**: 21
- **Total Images**: **26,915** (Train: 21,520 | Test: 5,395)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `brown_spot` | `corn_brown_spot` | 136 | 35 | **171** |
| 2 | `cercospora_leaf_blight` | `corn_cercospora_leaf_blight` | 52 | 14 | **66** |
| 3 | `chlorotic_leaf_spot` | `corn_chlorotic_leaf_spot` | 20 | 6 | **26** |
| 4 | `common_rust` | `corn_common_rust` | 7 | 2 | **9** |
| 5 | `gray_leaf_spot` | `corn_gray_leaf_spot` | 100 | 26 | **126** |
| 6 | `healthy` | `corn_healthy` | 5,266 | 1,317 | **6,583** |
| 7 | `insects_damages` | `corn_insects_damages` | 13 | 4 | **17** |
| 8 | `leaf_blight` | `corn_leaf_blight` | 1,642 | 411 | **2,053** |
| 9 | `lethal_necrosis` | `corn_lethal_necrosis` | 3,183 | 796 | **3,979** |
| 10 | `mildew` | `corn_mildew` | 32 | 8 | **40** |
| 11 | `northern_leaf_blight` | `corn_northern_leaf_blight` | 2,323 | 581 | **2,904** |
| 12 | `purple_discoloration` | `corn_purple_discoloration` | 6 | 2 | **8** |
| 13 | `rust` | `corn_rust` | 1,125 | 283 | **1,408** |
| 14 | `smut` | `corn_smut` | 172 | 43 | **215** |
| 15 | `spot` | `corn_spot` | 1,239 | 311 | **1,550** |
| 16 | `streak` | `corn_streak` | 141 | 36 | **177** |
| 17 | `streak_virus` | `corn_streak_virus` | 5,728 | 1,433 | **7,161** |
| 18 | `stripe` | `corn_stripe` | 77 | 20 | **97** |
| 19 | `violet_decoloration` | `corn_violet_decoloration` | 4 | 2 | **6** |
| 20 | `yellow_spots` | `corn_yellow_spots` | 12 | 4 | **16** |
| 21 | `yellowing` | `corn_yellowing` | 242 | 61 | **303** |

---

### 22. **Cotton** (`cotton`)
- **Disease Categories**: 6
- **Total Images**: **2,633** (Train: 2,104 | Test: 529)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_blight` | `cotton_bacterial_blight` | 499 | 125 | **624** |
| 2 | `curl_virus` | `cotton_curl_virus` | 70 | 18 | **88** |
| 3 | `fusarium_wilt` | `cotton_fusarium_wilt` | 52 | 13 | **65** |
| 4 | `healthy` | `cotton_healthy` | 578 | 145 | **723** |
| 5 | `powdery_mildew` | `cotton_powdery_mildew` | 464 | 117 | **581** |
| 6 | `target_spot` | `cotton_target_spot` | 441 | 111 | **552** |

---

### 23. **Cucumber** (`cucumber`)
- **Disease Categories**: 7
- **Total Images**: **1,269** (Train: 1,014 | Test: 255)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `angular_leaf_spot` | `cucumber_angular_leaf_spot` | 144 | 36 | **180** |
| 2 | `anthracnose` | `cucumber_anthracnose` | 128 | 32 | **160** |
| 3 | `bacterial_wilt` | `cucumber_bacterial_wilt` | 212 | 54 | **266** |
| 4 | `downy_mildew` | `cucumber_downy_mildew` | 127 | 32 | **159** |
| 5 | `gummy_stem_blight` | `cucumber_gummy_stem_blight` | 128 | 32 | **160** |
| 6 | `healthy` | `cucumber_healthy` | 128 | 32 | **160** |
| 7 | `powdery_mildew` | `cucumber_powdery_mildew` | 147 | 37 | **184** |

---

### 24. **Eggplant** (`eggplant`)
- **Disease Categories**: 3
- **Total Images**: **130** (Train: 102 | Test: 28)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `cercospora_leaf_blight` | `eggplant_cercospora_leaf_blight` | 45 | 12 | **57** |
| 2 | `phomopsis_fruit_rot` | `eggplant_phomopsis_fruit_rot` | 33 | 9 | **42** |
| 3 | `phytophthora` | `eggplant_phytophthora` | 24 | 7 | **31** |

---

### 25. **Garlic** (`garlic`)
- **Disease Categories**: 2
- **Total Images**: **195** (Train: 156 | Test: 39)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `leaf_blight` | `garlic_leaf_blight` | 72 | 18 | **90** |
| 2 | `rust` | `garlic_rust` | 84 | 21 | **105** |

---

### 26. **Ginger** (`ginger`)
- **Disease Categories**: 2
- **Total Images**: **93** (Train: 74 | Test: 19)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `sheath_blight` | `ginger_sheath_blight` | 54 | 14 | **68** |
| 2 | `spot` | `ginger_spot` | 20 | 5 | **25** |

---

### 27. **Grape** (`grape`)
- **Disease Categories**: 7
- **Total Images**: **6,612** (Train: 5,286 | Test: 1,326)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `black_rot` | `grape_black_rot` | 1,083 | 271 | **1,354** |
| 2 | `downy_mildew` | `grape_downy_mildew` | 222 | 56 | **278** |
| 3 | `esca` | `grape_esca` | 1,816 | 455 | **2,271** |
| 4 | `healthy` | `grape_healthy` | 1,182 | 296 | **1,478** |
| 5 | `leaf_blight` | `grape_leaf_blight` | 860 | 216 | **1,076** |
| 6 | `leafroll_disease` | `grape_leafroll_disease` | 56 | 15 | **71** |
| 7 | `spot` | `grape_spot` | 67 | 17 | **84** |

---

### 28. **Guava** (`guava`)
- **Disease Categories**: 9
- **Total Images**: **879** (Train: 700 | Test: 179)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `canker` | `guava_canker` | 26 | 7 | **33** |
| 2 | `dot_leaf` | `guava_dot_leaf` | 12 | 4 | **16** |
| 3 | `healthy` | `guava_healthy` | 319 | 80 | **399** |
| 4 | `mummification_leaf` | `guava_mummification_leaf` | 9 | 3 | **12** |
| 5 | `phytophthora` | `guava_phytophthora` | 91 | 23 | **114** |
| 6 | `red_rust` | `guava_red_rust` | 69 | 18 | **87** |
| 7 | `rust` | `guava_rust` | 19 | 5 | **24** |
| 8 | `scab` | `guava_scab` | 80 | 20 | **100** |
| 9 | `stylar_end_rot` | `guava_stylar_end_rot` | 75 | 19 | **94** |

---

### 29. **Lettuce** (`lettuce`)
- **Disease Categories**: 2
- **Total Images**: **121** (Train: 96 | Test: 25)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `downy_mildew` | `lettuce_downy_mildew` | 65 | 17 | **82** |
| 2 | `mosaic_virus` | `lettuce_mosaic_virus` | 31 | 8 | **39** |

---

### 30. **Mango** (`mango`)
- **Disease Categories**: 23
- **Total Images**: **4,185** (Train: 3,337 | Test: 848)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `mango_anthracnose` | 379 | 95 | **474** |
| 2 | `apoderus_javanicus` | `mango_apoderus_javanicus` | 50 | 13 | **63** |
| 3 | `aulacaspis_tubercularis` | `mango_aulacaspis_tubercularis` | 10 | 3 | **13** |
| 4 | `bacterial_canker` | `mango_bacterial_canker` | 396 | 99 | **495** |
| 5 | `ceroplastes_rubens` | `mango_ceroplastes_rubens` | 8 | 3 | **11** |
| 6 | `cisaberoptus_kenyae` | `mango_cisaberoptus_kenyae` | 12 | 4 | **16** |
| 7 | `cutting_weevil` | `mango_cutting_weevil` | 190 | 48 | **238** |
| 8 | `dappula_tertia` | `mango_dappula_tertia` | 30 | 8 | **38** |
| 9 | `dialeuropora_decempuncta` | `mango_dialeuropora_decempuncta` | 18 | 5 | **23** |
| 10 | `die_back` | `mango_die_back` | 392 | 99 | **491** |
| 11 | `erosomyia_sp` | `mango_erosomyia_sp` | 10 | 3 | **13** |
| 12 | `gall_midge` | `mango_gall_midge` | 394 | 99 | **493** |
| 13 | `healthy` | `mango_healthy` | 428 | 108 | **536** |
| 14 | `icerya_seychellarum` | `mango_icerya_seychellarum` | 21 | 6 | **27** |
| 15 | `ischnaspis_longirostris` | `mango_ischnaspis_longirostris` | 5 | 2 | **7** |
| 16 | `mictis_longicornis` | `mango_mictis_longicornis` | 68 | 17 | **85** |
| 17 | `neomelicharia_sparsa` | `mango_neomelicharia_sparsa` | 28 | 8 | **36** |
| 18 | `orthaga_euadrusalis` | `mango_orthaga_euadrusalis` | 17 | 5 | **22** |
| 19 | `powdery_mildew` | `mango_powdery_mildew` | 397 | 100 | **497** |
| 20 | `procontarinia_matteiana` | `mango_procontarinia_matteiana` | 21 | 6 | **27** |
| 21 | `procontarinia_rubus` | `mango_procontarinia_rubus` | 20 | 5 | **25** |
| 22 | `sooty_mould` | `mango_sooty_mould` | 399 | 100 | **499** |
| 23 | `valanga_nigricornis` | `mango_valanga_nigricornis` | 44 | 12 | **56** |

---

### 31. **Maple** (`maple`)
- **Disease Categories**: 1
- **Total Images**: **113** (Train: 90 | Test: 23)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `tar_spot` | `maple_tar_spot` | 90 | 23 | **113** |

---

### 32. **Olive** (`olive`)
- **Disease Categories**: 3
- **Total Images**: **3,162** (Train: 2,528 | Test: 634)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `aculus_olearius` | `olive_aculus_olearius` | 692 | 174 | **866** |
| 2 | `healthy` | `olive_healthy` | 682 | 171 | **853** |
| 3 | `peacock_spot` | `olive_peacock_spot` | 1,154 | 289 | **1,443** |

---

### 33. **Paddy** (`paddy`)
- **Disease Categories**: 17
- **Total Images**: **19,278** (Train: 15,411 | Test: 3,867)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_blight` | `paddy_bacterial_blight` | 824 | 208 | **1,032** |
| 2 | `bacterial_leaf_streak` | `paddy_bacterial_leaf_streak` | 325 | 82 | **407** |
| 3 | `bacterial_panicle_blight` | `paddy_bacterial_panicle_blight` | 352 | 89 | **441** |
| 4 | `black_stem_borer` | `paddy_black_stem_borer` | 394 | 99 | **493** |
| 5 | `blast` | `paddy_blast` | 2,443 | 612 | **3,055** |
| 6 | `brown_spot` | `paddy_brown_spot` | 1,764 | 444 | **2,208** |
| 7 | `downy_mildew` | `paddy_downy_mildew` | 626 | 157 | **783** |
| 8 | `healthy` | `paddy_healthy` | 2,248 | 563 | **2,811** |
| 9 | `hispa` | `paddy_hispa` | 1,958 | 490 | **2,448** |
| 10 | `leaf_blight` | `paddy_leaf_blight` | 64 | 16 | **80** |
| 11 | `leaf_roller` | `paddy_leaf_roller` | 798 | 200 | **998** |
| 12 | `leafblast` | `paddy_leafblast` | 98 | 25 | **123** |
| 13 | `sheath_blight` | `paddy_sheath_blight` | 52 | 13 | **65** |
| 14 | `smut` | `paddy_smut` | 56 | 14 | **70** |
| 15 | `tungro` | `paddy_tungro` | 1,933 | 485 | **2,418** |
| 16 | `white_stem_borer` | `paddy_white_stem_borer` | 900 | 226 | **1,126** |
| 17 | `yellow_stem_borer` | `paddy_yellow_stem_borer` | 576 | 144 | **720** |

---

### 34. **Palm** (`palm`)
- **Disease Categories**: 3
- **Total Images**: **1,235** (Train: 987 | Test: 248)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `brown_spot` | `palm_brown_spot` | 185 | 47 | **232** |
| 2 | `healthy` | `palm_healthy` | 360 | 90 | **450** |
| 3 | `white_scale` | `palm_white_scale` | 442 | 111 | **553** |

---

### 35. **Papaya** (`papaya`)
- **Disease Categories**: 5
- **Total Images**: **1,857** (Train: 1,484 | Test: 373)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `papaya_anthracnose` | 284 | 71 | **355** |
| 2 | `bacterial_spot` | `papaya_bacterial_spot` | 366 | 92 | **458** |
| 3 | `curl` | `papaya_curl` | 282 | 71 | **353** |
| 4 | `healthy` | `papaya_healthy` | 157 | 40 | **197** |
| 5 | `ring_spot` | `papaya_ring_spot` | 395 | 99 | **494** |

---

### 36. **Peach** (`peach`)
- **Disease Categories**: 9
- **Total Images**: **4,137** (Train: 3,305 | Test: 832)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `peach_anthracnose` | 9 | 3 | **12** |
| 2 | `bacterial_spot` | `peach_bacterial_spot` | 1,837 | 460 | **2,297** |
| 3 | `brown_rot` | `peach_brown_rot` | 126 | 32 | **158** |
| 4 | `curl` | `peach_curl` | 144 | 37 | **181** |
| 5 | `healthy` | `peach_healthy` | 537 | 135 | **672** |
| 6 | `monillia_laxa` | `peach_monillia_laxa` | 250 | 63 | **313** |
| 7 | `parthenolecanium_corni` | `peach_parthenolecanium_corni` | 340 | 86 | **426** |
| 8 | `rust` | `peach_rust` | 6 | 2 | **8** |
| 9 | `scab` | `peach_scab` | 56 | 14 | **70** |

---

### 37. **Peanut** (`peanut`)
- **Disease Categories**: 5
- **Total Images**: **3,056** (Train: 2,443 | Test: 613)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `early_leaf_spot` | `peanut_early_leaf_spot` | 707 | 177 | **884** |
| 2 | `healthy` | `peanut_healthy` | 742 | 186 | **928** |
| 3 | `late_leaf_spot` | `peanut_late_leaf_spot` | 551 | 138 | **689** |
| 4 | `nutrition_deficiency` | `peanut_nutrition_deficiency` | 263 | 66 | **329** |
| 5 | `rust` | `peanut_rust` | 180 | 46 | **226** |

---

### 38. **Pear** (`pear`)
- **Disease Categories**: 5
- **Total Images**: **3,212** (Train: 2,568 | Test: 644)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `curl` | `pear_curl` | 42 | 11 | **53** |
| 2 | `erwinia_amylovora` | `pear_erwinia_amylovora` | 172 | 43 | **215** |
| 3 | `healthy` | `pear_healthy` | 34 | 9 | **43** |
| 4 | `slug` | `pear_slug` | 1,616 | 404 | **2,020** |
| 5 | `spot` | `pear_spot` | 704 | 177 | **881** |

---

### 39. **Pepper Bell** (`pepper_bell`)
- **Disease Categories**: 5
- **Total Images**: **2,727** (Train: 2,179 | Test: 548)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_spot` | `pepper_bell_bacterial_spot` | 877 | 220 | **1,097** |
| 2 | `blossom_end_rot` | `pepper_bell_blossom_end_rot` | 78 | 20 | **98** |
| 3 | `frogeye_leaf_spot` | `pepper_bell_frogeye_leaf_spot` | 21 | 6 | **27** |
| 4 | `healthy` | `pepper_bell_healthy` | 1,185 | 297 | **1,482** |
| 5 | `powdery_mildew` | `pepper_bell_powdery_mildew` | 18 | 5 | **23** |

---

### 40. **Plum** (`plum`)
- **Disease Categories**: 6
- **Total Images**: **280** (Train: 221 | Test: 59)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `aphis_spp` | `plum_aphis_spp` | 56 | 14 | **70** |
| 2 | `bacterial_spot` | `plum_bacterial_spot` | 12 | 4 | **16** |
| 3 | `brown_rot` | `plum_brown_rot` | 57 | 15 | **72** |
| 4 | `pocket_disease` | `plum_pocket_disease` | 45 | 12 | **57** |
| 5 | `pox_virus` | `plum_pox_virus` | 25 | 7 | **32** |
| 6 | `rust` | `plum_rust` | 26 | 7 | **33** |

---

### 41. **Potato** (`potato`)
- **Disease Categories**: 3
- **Total Images**: **6,415** (Train: 5,131 | Test: 1,284)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `early_blight` | `potato_early_blight` | 2,183 | 546 | **2,729** |
| 2 | `healthy` | `potato_healthy` | 930 | 233 | **1,163** |
| 3 | `late_blight` | `potato_late_blight` | 2,018 | 505 | **2,523** |

---

### 42. **Pumpkin** (`pumpkin`)
- **Disease Categories**: 1
- **Total Images**: **1,835** (Train: 1,468 | Test: 367)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `powdery_mildew` | `pumpkin_powdery_mildew` | 1,468 | 367 | **1,835** |

---

### 43. **Raspberry** (`raspberry`)
- **Disease Categories**: 5
- **Total Images**: **530** (Train: 422 | Test: 108)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `fire_blight` | `raspberry_fire_blight` | 23 | 6 | **29** |
| 2 | `gray_mold` | `raspberry_gray_mold` | 29 | 8 | **37** |
| 3 | `healthy` | `raspberry_healthy` | 328 | 83 | **411** |
| 4 | `spot` | `raspberry_spot` | 14 | 4 | **18** |
| 5 | `yellow_rust` | `raspberry_yellow_rust` | 28 | 7 | **35** |

---

### 44. **Rose** (`rose`)
- **Disease Categories**: 3
- **Total Images**: **914** (Train: 730 | Test: 184)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `black_spot` | `rose_black_spot` | 248 | 63 | **311** |
| 2 | `downy_mildew` | `rose_downy_mildew` | 159 | 40 | **199** |
| 3 | `healthy` | `rose_healthy` | 323 | 81 | **404** |

---

### 45. **Soybean** (`soybean`)
- **Disease Categories**: 9
- **Total Images**: **11,954** (Train: 9,559 | Test: 2,395)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_blight` | `soybean_bacterial_blight` | 64 | 16 | **80** |
| 2 | `brown_spot` | `soybean_brown_spot` | 44 | 12 | **56** |
| 3 | `caterpillar` | `soybean_caterpillar` | 2,550 | 638 | **3,188** |
| 4 | `diabrotica_speciosa` | `soybean_diabrotica_speciosa` | 1,758 | 440 | **2,198** |
| 5 | `downy_mildew` | `soybean_downy_mildew` | 96 | 25 | **121** |
| 6 | `frog_eye_leaf_spot` | `soybean_frog_eye_leaf_spot` | 153 | 39 | **192** |
| 7 | `healthy` | `soybean_healthy` | 4,721 | 1,181 | **5,902** |
| 8 | `mosaic` | `soybean_mosaic` | 87 | 22 | **109** |
| 9 | `rust` | `soybean_rust` | 86 | 22 | **108** |

---

### 46. **Squash** (`squash`)
- **Disease Categories**: 1
- **Total Images**: **186** (Train: 148 | Test: 38)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `powdery_mildew` | `squash_powdery_mildew` | 148 | 38 | **186** |

---

### 47. **Strawberry** (`strawberry`)
- **Disease Categories**: 3
- **Total Images**: **1,719** (Train: 1,374 | Test: 345)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `anthracnose` | `strawberry_anthracnose` | 46 | 12 | **58** |
| 2 | `healthy` | `strawberry_healthy` | 413 | 104 | **517** |
| 3 | `scorch` | `strawberry_scorch` | 915 | 229 | **1,144** |

---

### 48. **Sugarcane** (`sugarcane`)
- **Disease Categories**: 13
- **Total Images**: **5,148** (Train: 4,112 | Test: 1,036)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `banded_chlorosis` | `sugarcane_banded_chlorosis` | 137 | 35 | **172** |
| 2 | `brown_rust` | `sugarcane_brown_rust` | 80 | 20 | **100** |
| 3 | `brown_spot` | `sugarcane_brown_spot` | 516 | 130 | **646** |
| 4 | `grassy_shoot` | `sugarcane_grassy_shoot` | 240 | 60 | **300** |
| 5 | `healthy` | `sugarcane_healthy` | 517 | 130 | **647** |
| 6 | `mosaic` | `sugarcane_mosaic` | 300 | 76 | **376** |
| 7 | `pokkah_boeng` | `sugarcane_pokkah_boeng` | 166 | 42 | **208** |
| 8 | `red_rot` | `sugarcane_red_rot` | 404 | 101 | **505** |
| 9 | `rust` | `sugarcane_rust` | 353 | 89 | **442** |
| 10 | `sett_rot` | `sugarcane_sett_rot` | 383 | 96 | **479** |
| 11 | `smut` | `sugarcane_smut` | 118 | 30 | **148** |
| 12 | `viral` | `sugarcane_viral` | 176 | 45 | **221** |
| 13 | `yellowing` | `sugarcane_yellowing` | 722 | 182 | **904** |

---

### 49. **Sunflower** (`sunflower`)
- **Disease Categories**: 4
- **Total Images**: **439** (Train: 350 | Test: 89)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `downy_mildew` | `sunflower_downy_mildew` | 80 | 20 | **100** |
| 2 | `gray_mold` | `sunflower_gray_mold` | 53 | 14 | **67** |
| 3 | `healthy` | `sunflower_healthy` | 106 | 27 | **133** |
| 4 | `leaf_scars` | `sunflower_leaf_scars` | 111 | 28 | **139** |

---

### 50. **Tea** (`tea`)
- **Disease Categories**: 10
- **Total Images**: **960** (Train: 765 | Test: 195)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `algal_leaf` | `tea_algal_leaf` | 90 | 23 | **113** |
| 2 | `anthracnose` | `tea_anthracnose` | 80 | 20 | **100** |
| 3 | `bird_eye_spot` | `tea_bird_eye_spot` | 79 | 20 | **99** |
| 4 | `brown_blight` | `tea_brown_blight` | 90 | 23 | **113** |
| 5 | `gray_light` | `tea_gray_light` | 77 | 20 | **97** |
| 6 | `healthy` | `tea_healthy` | 47 | 12 | **59** |
| 7 | `leaf_blight` | `tea_leaf_blight` | 31 | 8 | **39** |
| 8 | `red_leaf_spot` | `tea_red_leaf_spot` | 143 | 36 | **179** |
| 9 | `red_scab` | `tea_red_scab` | 16 | 5 | **21** |
| 10 | `white_spot` | `tea_white_spot` | 112 | 28 | **140** |

---

### 51. **Tobacco** (`tobacco`)
- **Disease Categories**: 4
- **Total Images**: **167** (Train: 131 | Test: 36)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `blue_mold` | `tobacco_blue_mold` | 41 | 11 | **52** |
| 2 | `brown_spot` | `tobacco_brown_spot` | 46 | 12 | **58** |
| 3 | `frogeye_leaf_spot` | `tobacco_frogeye_leaf_spot` | 12 | 4 | **16** |
| 4 | `mosaic_virus` | `tobacco_mosaic_virus` | 32 | 9 | **41** |

---

### 52. **Tomato** (`tomato`)
- **Disease Categories**: 18
- **Total Images**: **37,701** (Train: 30,154 | Test: 7,547)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_leaf_spot` | `tomato_bacterial_leaf_spot` | 83 | 21 | **104** |
| 2 | `bacterial_spot` | `tomato_bacterial_spot` | 2,511 | 628 | **3,139** |
| 3 | `blight_leaf` | `tomato_blight_leaf` | 287 | 72 | **359** |
| 4 | `brown_spot` | `tomato_brown_spot` | 609 | 153 | **762** |
| 5 | `curl` | `tomato_curl` | 369 | 93 | **462** |
| 6 | `early_blight` | `tomato_early_blight` | 1,884 | 472 | **2,356** |
| 7 | `healthy` | `tomato_healthy` | 2,868 | 718 | **3,586** |
| 8 | `late_blight` | `tomato_late_blight` | 2,644 | 661 | **3,305** |
| 9 | `leaf_blight` | `tomato_leaf_blight` | 1,004 | 251 | **1,255** |
| 10 | `leaf_mold` | `tomato_leaf_mold` | 2,047 | 512 | **2,559** |
| 11 | `leaf_yellow_virus` | `tomato_leaf_yellow_virus` | 50 | 13 | **63** |
| 12 | `mosaic_virus` | `tomato_mosaic_virus` | 2,188 | 548 | **2,736** |
| 13 | `powdery_mildew` | `tomato_powdery_mildew` | 810 | 203 | **1,013** |
| 14 | `septoria_leaf_spot` | `tomato_septoria_leaf_spot` | 4,456 | 1,114 | **5,570** |
| 15 | `spider_mites` | `tomato_spider_mites` | 1,612 | 404 | **2,016** |
| 16 | `target_spot` | `tomato_target_spot` | 1,697 | 425 | **2,122** |
| 17 | `verticulium_wilt` | `tomato_verticulium_wilt` | 571 | 143 | **714** |
| 18 | `yellow_leaf_curl_virus` | `tomato_yellow_leaf_curl_virus` | 4,464 | 1,116 | **5,580** |

---

### 53. **Walnut** (`walnut`)
- **Disease Categories**: 1
- **Total Images**: **179** (Train: 143 | Test: 36)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `gnomonia_leptostyla` | `walnut_gnomonia_leptostyla` | 143 | 36 | **179** |

---

### 54. **Wheat** (`wheat`)
- **Disease Categories**: 11
- **Total Images**: **4,057** (Train: 3,240 | Test: 817)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_leaf_streak` | `wheat_bacterial_leaf_streak` | 90 | 23 | **113** |
| 2 | `head_scab` | `wheat_head_scab` | 208 | 52 | **260** |
| 3 | `healthy` | `wheat_healthy` | 543 | 136 | **679** |
| 4 | `loose_smut` | `wheat_loose_smut` | 320 | 80 | **400** |
| 5 | `powdery_mildew` | `wheat_powdery_mildew` | 200 | 51 | **251** |
| 6 | `root_rot` | `wheat_root_rot` | 197 | 50 | **247** |
| 7 | `rust` | `wheat_rust` | 901 | 226 | **1,127** |
| 8 | `septoria` | `wheat_septoria` | 60 | 16 | **76** |
| 9 | `septoria_blotch` | `wheat_septoria_blotch` | 148 | 38 | **186** |
| 10 | `septoria_leaf_spot` | `wheat_septoria_leaf_spot` | 77 | 20 | **97** |
| 11 | `stripe_rust` | `wheat_stripe_rust` | 496 | 125 | **621** |

---

### 55. **Zucchini** (`zucchini`)
- **Disease Categories**: 4
- **Total Images**: **372** (Train: 296 | Test: 76)

| # | Disease Name (Label) | Full DPD Pair Key | Train Imgs | Test Imgs | Total Imgs |
|:---:|---|---|:---:|:---:|:---:|
| 1 | `bacterial_wilt` | `zucchini_bacterial_wilt` | 53 | 14 | **67** |
| 2 | `downy_mildew` | `zucchini_downy_mildew` | 32 | 9 | **41** |
| 3 | `powdery_mildew` | `zucchini_powdery_mildew` | 135 | 34 | **169** |
| 4 | `yellow_mosaic_virus` | `zucchini_yellow_mosaic_virus` | 76 | 19 | **95** |

---
