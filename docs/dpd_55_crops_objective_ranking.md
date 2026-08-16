# Objective Quantitative Ranking of All 55 DPD Crops

## 1. Quantitative Scoring Methodology (0 to 100 Points)

Each crop is evaluated strictly using empirical metadata metrics:

$$\text{Score} = S_{\text{vol}} + S_{\text{depth}} + S_{\text{min}} + S_{\text{bal}} + S_{\text{healthy}} + S_{\text{agri}}$$
- **Volume Score ($S_{\text{vol}}$, 0-25 pts)**: $5 \times \log_{10}(N_{\text{total}})$, rewards statistical power.
- **Category Depth ($S_{\text{depth}}$, 0-15 pts)**: $1.2 \times K_{\text{diseases}}$, rewards disease diversity.
- **Minimum Class Viability ($S_{\text{min}}$, 0-20 pts)**: $5 \times \log_{10}(N_{\min})$, penalizes extreme minority classes.
- **Class Balance Quality ($S_{\text{bal}}$, 0-15 pts)**: $15 \times \text{Entropy}$, rewards uniform image distribution across classes.
- **Healthy Baseline ($S_{\text{healthy}}$, 0 or 10 pts)**: $+10$ pts if verified `healthy` class exists.
- **Agricultural Relevance ($S_{\text{agri}}$, 4-15 pts)**: Global staple (15 pts), major commercial fruit/veg (12 pts), secondary food crop (8 pts), minor/specialty (4 pts).

---

## 2. Complete Ranked Table of All 55 Crops

| Rank | Crop Name | Total Images | Disease Count | Min Class Imgs | Has Healthy? | Balance Entropy | Total Score (0-100) | Recommended Disease Subset |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **Tomato** | 37,701 | 18 | 63 | ✅ Yes | 0.89 | **85.2** | yellow_leaf_curl_virus, septoria_leaf_spot, healthy, late_blight (+13 more) |
| **2** | **Apple** | 32,749 | 17 | 162 | ✅ Yes | 0.86 | **83.5** | healthy, rust, frog_eye_leaf_spot, brown_spot (+13 more) |
| **3** | **Paddy** | 19,278 | 17 | 65 | ✅ Yes | 0.86 | **83.3** | blast, healthy, hispa, tungro (+10 more) |
| **4** | **Sugarcane** | 5,148 | 13 | 100 | ✅ Yes | 0.94 | **82.6** | yellowing, healthy, brown_spot, red_rot (+9 more) |
| **5** | **Cassava** | 37,285 | 10 | 65 | ✅ Yes | 0.72 | **79.8** | mosaic, healthy, bacterial_blight, brown_streak_disease (+5 more) |
| **6** | **Wheat** | 4,057 | 11 | 76 | ✅ Yes | 0.87 | **78.7** | rust, healthy, stripe_rust, loose_smut (+5 more) |
| **7** | **Potato** | 6,415 | 3 | 1,163 | ✅ Yes | 0.95 | **77.2** | early_blight, late_blight, healthy |
| **8** | **Banana** | 2,702 | 11 | 55 | ✅ Yes | 0.87 | **77.1** | xamthomonas, sigatoka, segatoka, healthy (+4 more) |
| **9** | **Corn** | 26,915 | 21 | 6 | ✅ Yes | 0.65 | **75.8** | streak_virus, healthy, lethal_necrosis, northern_leaf_blight (+8 more) |
| **10** | **Soybean** | 11,954 | 9 | 56 | ✅ Yes | 0.58 | **73.6** | healthy, caterpillar, diabrotica_speciosa, frog_eye_leaf_spot (+3 more) |
| **11** | **Cotton** | 2,633 | 6 | 65 | ✅ Yes | 0.87 | **71.4** | healthy, bacterial_blight, powdery_mildew, target_spot |
| **12** | **Mango** | 4,185 | 23 | 7 | ✅ Yes | 0.78 | **71.1** | healthy, sooty_mould, powdery_mildew, bacterial_canker (+4 more) |
| **13** | **Peanut** | 3,056 | 5 | 226 | ✅ Yes | 0.93 | **71.1** | healthy, early_leaf_spot, late_leaf_spot, nutrition_deficiency (+1 more) |
| **14** | **Grape** | 6,612 | 7 | 71 | ✅ Yes | 0.80 | **70.8** | esca, healthy, black_rot, leaf_blight (+1 more) |
| **15** | **Coffee** | 3,959 | 9 | 6 | ✅ Yes | 0.72 | **68.5** | rust, healthy, miner, phoma (+2 more) |
| **16** | **Olive** | 3,162 | 3 | 853 | ✅ Yes | 0.97 | **68.3** | peacock_spot, aculus_olearius, healthy |
| **17** | **Cucumber** | 1,269 | 7 | 159 | ✅ Yes | 0.99 | **67.8** | bacterial_wilt, powdery_mildew, angular_leaf_spot, anthracnose (+3 more) |
| **18** | **Papaya** | 1,857 | 5 | 197 | ✅ Yes | 0.97 | **66.4** | ring_spot, bacterial_spot, anthracnose, curl (+1 more) |
| **19** | **Peach** | 4,137 | 9 | 8 | ✅ Yes | 0.64 | **65.0** | bacterial_spot, healthy, parthenolecanium_corni, monillia_laxa (+2 more) |
| **20** | **Blackgram** | 1,006 | 5 | 151 | ✅ Yes | 0.99 | **64.8** | anthracnose, yellow_mosaic, healthy, powdery_mildew (+1 more) |
| **21** | **Bean** | 1,521 | 6 | 55 | ✅ Yes | 0.84 | **62.5** | bean_rust, angular_leaf_spot, healthy, rust |
| **22** | **Cherry** | 2,564 | 4 | 107 | ✅ Yes | 0.82 | **62.3** | powdery_mildew, healthy, aphis_spp, spot |
| **23** | **Tea** | 960 | 10 | 21 | ✅ Yes | 0.95 | **61.8** | red_leaf_spot, white_spot, algal_leaf, brown_blight (+1 more) |
| **24** | **Strawberry** | 1,719 | 3 | 58 | ✅ Yes | 0.68 | **60.8** | scorch, healthy |
| **25** | **Pepper Bell** | 2,727 | 5 | 23 | ✅ Yes | 0.56 | **60.4** | healthy, bacterial_spot |
| **26** | **Palm** | 1,235 | 3 | 232 | ✅ Yes | 0.95 | **59.1** | white_scale, healthy, brown_spot |
| **27** | **Rose** | 914 | 3 | 199 | ✅ Yes | 0.96 | **58.4** | healthy, black_spot, downy_mildew |
| **28** | **Pumpkin** | 1,835 | 1 | 1,835 | ❌ No | 1.00 | **56.8** | powdery_mildew |
| **29** | **Guava** | 879 | 9 | 12 | ✅ Yes | 0.77 | **56.5** | healthy, phytophthora, scab |
| **30** | **Citrus** | 6,486 | 5 | 11 | ✅ Yes | 0.27 | **56.4** | greening, canker, black_spot |
| **31** | **Chilli** | 355 | 4 | 81 | ✅ Yes | 1.00 | **56.1** | None (low counts) |
| **32** | **Sunflower** | 439 | 4 | 67 | ✅ Yes | 0.97 | **55.7** | leaf_scars, healthy, downy_mildew |
| **33** | **Basil** | 410 | 3 | 86 | ✅ Yes | 0.97 | **54.8** | downy_mildew, healthy |
| **34** | **Pear** | 3,212 | 5 | 43 | ✅ Yes | 0.59 | **54.6** | slug, spot, erwinia_amylovora |
| **35** | **Coriander** | 260 | 1 | 260 | ✅ Yes | 1.00 | **54.3** | healthy |
| **36** | **Cauliflower** | 479 | 6 | 18 | ✅ Yes | 0.85 | **53.6** | bacterial_spot, downy_mildew |
| **37** | **Blueberry** | 1,805 | 6 | 34 | ✅ Yes | 0.29 | **53.5** | healthy |
| **38** | **Cashew** | 1,505 | 1 | 1,505 | ❌ No | 1.00 | **52.0** | red_rust |
| **39** | **Raspberry** | 530 | 5 | 18 | ✅ Yes | 0.52 | **51.7** | healthy |
| **40** | **Plum** | 280 | 6 | 16 | ❌ No | 0.94 | **47.5** | None (low counts) |
| **41** | **Squash** | 186 | 1 | 186 | ❌ No | 1.00 | **46.9** | powdery_mildew |
| **42** | **Cabbage** | 221 | 3 | 55 | ❌ No | 0.98 | **46.8** | None (low counts) |
| **43** | **Eggplant** | 130 | 3 | 31 | ❌ No | 0.97 | **44.2** | None (low counts) |
| **44** | **Zucchini** | 372 | 4 | 41 | ❌ No | 0.91 | **43.3** | powdery_mildew |
| **45** | **Walnut** | 179 | 1 | 179 | ❌ No | 1.00 | **42.7** | gnomonia_leptostyla |
| **46** | **Garlic** | 195 | 2 | 90 | ❌ No | 1.00 | **42.6** | rust |
| **47** | **Apricot** | 205 | 2 | 85 | ❌ No | 0.98 | **42.3** | coryneum_blight |
| **48** | **Carrot** | 140 | 3 | 15 | ❌ No | 0.86 | **41.2** | None (low counts) |
| **49** | **Maple** | 113 | 1 | 113 | ❌ No | 1.00 | **40.7** | tar_spot |
| **50** | **Brassica** | 104 | 1 | 104 | ❌ No | 1.00 | **40.4** | black_rot |
| **51** | **Tobacco** | 167 | 4 | 16 | ❌ No | 0.94 | **40.0** | None (low counts) |
| **52** | **Lettuce** | 121 | 2 | 39 | ❌ No | 0.91 | **38.4** | None (low counts) |
| **53** | **Celery** | 64 | 2 | 29 | ❌ No | 0.99 | **37.6** | None (low counts) |
| **54** | **Broccoli** | 93 | 3 | 7 | ❌ No | 0.78 | **37.4** | None (low counts) |
| **55** | **Ginger** | 93 | 2 | 25 | ❌ No | 0.84 | **35.8** | None (low counts) |