import os
import json
import shutil

DATASET_DIR = r"d:\Projects\AI-ML Portfolio\Potato_disease\Dataset\Plant_leave_diseases_dataset_without_augmentation"
POTATO_HEALTHY_EXTRA_DIR = r"d:\Projects\AI-ML Portfolio\Potato_disease\Potato_disease_dataset\Potato___healthy"
MODELS_ASSETS_DIR = "models_assets"

os.makedirs(MODELS_ASSETS_DIR, exist_ok=True)

def supplement_potato_healthy():
    print("--- Step 1.1: Supplementing Potato___healthy Class ---")
    target_potato_dir = os.path.join(DATASET_DIR, "Potato___healthy")
    os.makedirs(target_potato_dir, exist_ok=True)

    if os.path.exists(POTATO_HEALTHY_EXTRA_DIR):
        extra_files = os.listdir(POTATO_HEALTHY_EXTRA_DIR)
        copied_count = 0
        for f in extra_files:
            src_file = os.path.join(POTATO_HEALTHY_EXTRA_DIR, f)
            dst_file = os.path.join(target_potato_dir, f)
            if os.path.isfile(src_file) and not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_file)
                copied_count += 1
        print(f"Copied {copied_count} extra healthy potato images. Total now: {len(os.listdir(target_potato_dir))}")

def export_class_names_and_disease_info():
    print("\n--- Step 1.2: Exporting Expanded Advisory Metadata (disease_info.json) ---")
    class_folders = sorted([
        d for d in os.listdir(DATASET_DIR)
        if os.path.isdir(os.path.join(DATASET_DIR, d))
    ])

    # Save class_names.json
    class_names_path = os.path.join(MODELS_ASSETS_DIR, "class_names.json")
    with open(class_names_path, "w", encoding="utf-8") as f:
        json.dump(class_folders, f, indent=2)

    # Generate expanded disease_info.json
    disease_info = {}
    for cls in class_folders:
        if cls == "Background_without_leaves":
            disease_info[cls] = {
                "crop": "Non-Crop / Background",
                "disease": "No Plant Leaf Detected",
                "status": "Non-Leaf",
                "is_background": True,
                "symptoms": "• Image does not contain a recognized crop leaf.\n• Subject appears to be background or unhandled material.",
                "cause": "• Non-agricultural photo upload.\n• Subject is outside trained 38 plant species scope.",
                "organic_treatment": "• N/A — No crop treatment required.",
                "chemical_treatment": "• N/A — No chemical intervention needed.",
                "prevention": "• Please upload a clear, focused photograph of a plant leaf for accurate diagnostic analysis."
            }
            continue

        parts = cls.replace("___", " - ").replace("_", " ").title().split(" - ")
        crop_name = parts[0].strip()
        disease_name = parts[1].strip() if len(parts) > 1 else "Healthy"

        if "healthy" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Healthy (No Disease Detected)",
                "status": "Healthy",
                "is_background": False,
                "symptoms": f"• Vibrant, uniform green pigmentation across all leaf veins and blade surface.\n• Turgid leaf margins with zero spots, necrotic lesions, or fungal pustules.\n• Normal vigor and physiological leaf architecture.",
                "cause": f"• Balanced plant nutrition (N-P-K) and optimal soil pH.\n• Favorable environmental temperature and moisture conditions.\n• Absence of bacterial, fungal, or viral pathogen infection.",
                "organic_treatment": f"• Apply well-composted organic mulch around crop drip line.\n• Spray foliar bio-stimulants or neem oil solution periodically for protection.",
                "chemical_treatment": f"• No chemical treatment required.\n• Continue regular field monitoring and leaf sampling every 7–10 days.",
                "prevention": (
                    f"🌾 Soil & Seed Hygiene: Plant certified, disease-free seed stock. Solarize soil beds in summer prior to planting.\n"
                    f"🔄 Crop Rotation: Practice a strict 3-year crop rotation cycle with non-host crops to prevent soil-borne inoculum buildup.\n"
                    f"💧 Irrigation Management: Irrigate exclusively via subterranean drip lines at soil level. Avoid morning/evening overhead sprinkling.\n"
                    f"🌿 Field Sanitation: Maintain wider row spacing to enable optimal canopy aeration. Remove all weeds and volunteer host plants around field boundaries.\n"
                    f"🛡️ Proactive Immunity: Apply neem cake @ 250 kg/acre and enrich soil with *Trichoderma viride* to build natural rhizosphere immunity."
                )
            }
        elif "early_blight" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Early Blight",
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• Dark brown to black lesions featuring concentric target-like rings.\n• Yellow chlorotic halos surrounding mature lower leaf spots.\n• Premature leaf senescence and defoliation progressing upward.",
                "cause": f"• Fungal pathogen *Alternaria solani* / *Alternaria grandis*.\n• Favored by warm temperatures (24°C–29°C) and frequent leaf wetness.\n• Survival in infected crop debris and volunteer solanaceous hosts.",
                "organic_treatment": f"• Prune and burn infected lower leaves immediately upon detection.\n• Spray Liquid Copper Fungicide or *Bacillus subtilis* bio-control solution.\n• Mulch soil surface to prevent fungal spore splash-back during rain.",
                "chemical_treatment": f"• Apply Chlorothalonil 75% WP @ 2.0 g/L or Mancozeb 75% WP @ 2.5 g/L.\n• Alternate with Difenoconazole 25% EC @ 0.5 mL/L for resistance management.\n• Spray at 7–10 day intervals during high risk periods.",
                "prevention": (
                    f"🌾 Seed & Tuber Certification: Use certified, disease-free seed stock treated with *Trichoderma harzianum* @ 10 g/kg.\n"
                    f"🔄 Strict Crop Rotation: Rotate out of solanaceous crops (Potato, Tomato, Eggplant, Pepper) for a minimum of 3 full seasons.\n"
                    f"💧 Moisture Control: Install subsurface drip lines. Avoid night overhead irrigation to maintain dry leaf canopies.\n"
                    f"🌿 Canopy Aeration & Mulching: Space plants at recommended distances (60x45 cm). Apply 3-inch straw mulch to suppress spore splash from soil.\n"
                    f"🛡️ Post-Harvest Sanitation: Deep plow or burn crop stubble immediately following harvest. Clear nightshade weed hosts along field perimeters."
                )
            }
        elif "late_blight" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Late Blight",
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• Irregular, water-soaked dark green to brownish lesions on leaf margins.\n• Delicate white cottony mold growth on lower leaf surface under high humidity.\n• Rapid leaf collapse, wilting, and characteristic foul odor in fields.",
                "cause": f"• Oomycete pathogen *Phytophthora infestans*.\n• Extremely destructive under cool, moist weather (15°C–22°C, RH >90%).\n• Airborne sporangia spreading across multi-kilometer distances in wind.",
                "organic_treatment": f"• Remove and destroy entire severely infected plants immediately.\n• Apply Copper Octanoate or Bordeaux mixture (1%) as protective spray.\n• Apply bio-fungicide containing *Trichoderma viride* to soil base.",
                "chemical_treatment": f"• Apply systemic fungicide Metalaxyl + Mancozeb (Ridomil Gold) @ 2.5 g/L.\n• Alternate with Cymoxanil + Mancozeb @ 2.0 g/L or Dimethomorph @ 1.0 g/L.\n• Repeat spray every 5–7 days while wet cool conditions persist.",
                "prevention": (
                    f"🌾 Resistant Varieties: Select late-blight resistant cultivars (e.g. Kufri Girdhari / Kufri Himalini / resistant hybrids).\n"
                    f"🔄 Soil & Drainage Ridging: Build high, well-drained soil ridges around plant bases to prevent sporangia from washing down into tubers/roots.\n"
                    f"💧 Micro-Climate Warning: Monitor local weather forecasts; apply protective copper contact sprays *prior* to wet overcast weather spells.\n"
                    f"🌿 Destruction of Cull Piles: Destroy cull tuber piles, volunteer plants, and wild solanaceous weeds within a 500-meter radius.\n"
                    f"🛡️ Harvest Management: Kill vine canopy with desiccant 14 days before harvest to prevent spore transfer to tubers during digging."
                )
            }
        elif "bacterial_spot" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Bacterial Spot",
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• Small (2–3 mm), dark, water-soaked angular spots on leaves.\n• Lesions dry out, forming translucent parchment-like centers.\n• Leaves turn yellow and drop prematurely, exposing fruit to sunscald.",
                "cause": f"• Bacterial pathogen *Xanthomonas vesicatoria* species complex.\n• Transmitted via infected seed, wind-driven rain splashes, and tools.\n• Thrives in high humidity and warm temperatures (25°C–30°C).",
                "organic_treatment": f"• Apply Copper Hydroxide spray mixed with Organic Neem Extract.\n• Remove and destroy infected foliage during dry weather.\n• Sterilize pruning shears between plants using 70% isopropyl alcohol.",
                "chemical_treatment": f"• Apply Copper Oxychloride 50% WP @ 3.0 g/L + Streptocycline @ 60 ppm.\n• Apply Kasugamycin 3% SL @ 2.0 mL/L at first sign of disease.\n• Re-apply after heavy rain events.",
                "prevention": (
                    f"🌾 Hot-Water Seed Treatment: Soak seeds in 50°C water for 25 minutes prior to planting to eradicate seed-borne *Xanthomonas*.\n"
                    f"🔄 Field Work Discipline: Avoid entering, weeding, or pruning in fields when foliage is wet from rain or morning dew.\n"
                    f"💧 Overhead Water Avoidance: Switch completely to surface or drip irrigation. Use plastic mulch to eliminate soil splash.\n"
                    f"🌿 Equipment Decontamination: Disinfect tractors, sprayers, tools, and harvest crates with a 10% bleach or quaternary ammonium solution.\n"
                    f"🛡️ Windbreak Barriers: Plant peripheral windbreak hedges to reduce wind-driven rain particle dissemination across plots."
                )
            }
        elif "black_rot" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Black Rot",
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• Characteristic V-shaped chlorotic yellow lesions at leaf margins pointing toward stem.\n• Darkening of leaf veins turning black, forming a prominent net-like pattern.\n• Stems show internal vascular blackening and dwarfed head development.",
                "cause": f"• Bacterial pathogen *Xanthomonas campestris* pv. *campestris*.\n• Enters leaves through hydathodes at leaf edges or mechanical wounds.\n• Favored by warm moist conditions (24°C–30°C) and heavy rain.",
                "organic_treatment": f"• Prune infected leaves and destroy plant debris by deep burial.\n• Spray bio-bactericide *Pseudomonas fluorescens* @ 5 g/L foliar spray.\n• Incorporate mustard green manure into soil prior to planting.",
                "chemical_treatment": f"• Soak seeds in Streptomycin Sulfate solution (100 ppm) for 30 mins.\n• Apply Copper Hydroxide @ 2.0 g/L mixed with Mancozeb @ 2.0 g/L.\n• Repeat spraying at 10-day intervals during wet periods.",
                "prevention": (
                    f"🌾 Seed Sanitation & Nursery Netting: Plant heat-treated, certified brassica seeds. Use 40-mesh netting over seedling beds.\n"
                    f"🔄 4-Year Crop Rotation: Rotate with non-cruciferous crops (Corn, Beans, Small Grains, Alliums) for 3–4 consecutive years.\n"
                    f"💧 Raised Bed Soil Aeration: Plant on raised ridges to maintain rapid surface soil drying and reduce hydathode guttation moisture.\n"
                    f"🌿 Cruciferous Weed Control: Eradicate wild mustard, shepherd's purse, radish weeds, and volunteer crucifers near plots.\n"
                    f"🛡️ Post-Harvest Bio-Fumigation: Incorporate bio-fumigant green manure crops into soil immediately after crop harvest."
                )
            }
        elif "rust" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Rust Disease",
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• Numerous raised, powdery orange-red to rust-brown pustules on lower leaf surface.\n• Corresponding yellow chlorotic spots appearing on upper leaf canopy.\n• Severe infection leads to leaf curling, drying, and early leaf drop.",
                "cause": f"• Fungal rust pathogens (*Puccinia* / *Uromyces* species).\n• Spores (urediniospores) carried efficiently over long distances by wind.\n• Requires high relative humidity (>90%) and mild temperatures (18°C–25°C).",
                "organic_treatment": f"• Prune severely rusted leaves and burn away from field area.\n• Apply Wettable Sulfur 80% WP @ 3.0 g/L or 0.5% Neem Oil emulsion.\n• Spray bio-agent *Verticillium lecanii* @ 5 g/L to parasitise rust spores.",
                "chemical_treatment": f"• Apply systemic Triazole fungicide Tebuconazole 25.9% EC @ 1.0 mL/L.\n• Alternate with Propiconazole 25% EC @ 1.0 mL/L or Hexaconazole @ 1.0 mL/L.\n• Apply at onset of initial pustule formation.",
                "prevention": (
                    f"🌾 Genetic Resistance & Hybrid Selection: Sow rust-resistant crop varieties recommended by regional agricultural universities.\n"
                    f"🔄 Nitrogen Balance Control: Avoid excessive, late-season synthetic nitrogen applications that promote soft, highly susceptible foliage.\n"
                    f"💧 Airflow Canopy Management: Maintain wider row spacing aligned with dominant prevailing wind directions to facilitate fast leaf drying.\n"
                    f"🌿 Destruction of Alternate Hosts: Eradicate woody alternate host shrubs (e.g. Barberry, Buckthorn) located near field boundaries.\n"
                    f"🛡️ Proactive Sulfur Barrier: Apply protective dustings of elemental sulfur early in the growing season prior to spore arrival."
                )
            }
        elif "powdery_mildew" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Powdery Mildew",
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• White to grayish talcum powder-like fungal patches on upper leaf blades.\n• Patches expand to cover entire leaf surfaces, stems, and shoots.\n• Infected leaves curl upward, turn brown, dry out, and drop off.",
                "cause": f"• Obligate biotrophic fungal pathogens (*Erysiphe* / *Podosphaera* species).\n• Favored by dry atmospheric conditions combined with high ambient humidity.\n• Thrives in shaded, low-airflow environments.",
                "organic_treatment": f"• Spray Potassium Bicarbonate (5 g/L) + Horticultural Oil solution.\n• Apply Neem Oil 1% spray every 7 days onto leaf surfaces.\n• Spray fresh diluted cow milk emulsion (1:9 ratio with water) in sunshine.",
                "chemical_treatment": f"• Apply Myclobutanil 10% WP @ 1.0 g/L or Penconazole 10% EC @ 0.5 mL/L.\n• Apply Azoxystrobin 23% SC @ 1.0 mL/L for systemic dual protection.\n• Spray early when first white dusting spots emerge.",
                "prevention": (
                    f"🌾 Site Selection & Sunlight Exposure: Plant in open, sunny locations receiving full sunlight (minimum 6–8 hours daily).\n"
                    f"🔄 Canopy Pruning & Spacing: Prune inner sucker shoots and lower foliage to eliminate humid micro-climates within plant canopy.\n"
                    f"💧 Soil-Base Drip Watering: Water at soil level during morning hours. Avoid evening foliage spraying.\n"
                    f"🌿 Organic Bio-Fungicide Barrier: Apply prophylactic foliar sprays of *Bacillus amyloliquefaciens* at 14-day intervals.\n"
                    f"🛡️ Crop Residue Management: Remove and compost or burn all fallen infected leaves at the end of the crop season."
                )
            }
        elif "yellow_leaf_curl" in cls.lower():
            disease_info[cls] = {
                "crop": crop_name,
                "disease": "Yellow Leaf Curl Virus",
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• Severe upward cupping and wrinkling of young terminal leaves.\n• Pronounced yellow chlorosis along leaf margins and interveinal tissue.\n• Stunted bush-like plant growth with severe flower drop and zero fruit set.",
                "cause": f"• Begomovirus (*Tomato Yellow Leaf Curl Virus* - TYLCV).\n• Transmitted exclusively by insect vector Silverleaf Whitefly (*Bemisia tabaci*).\n• Rapid vector multiplication during warm dry weather.",
                "organic_treatment": f"• Install yellow sticky traps (30–40 traps/acre) to monitor/catch whiteflies.\n• Spray Insecticidal Soap or 2% Neem Seed Kernel Extract (NSKE).\n• Apply *Beauveria bassiana* bio-insecticide @ 5 g/L to control whiteflies.",
                "chemical_treatment": f"• Apply systemic insecticide Imidacloprid 17.8% SL @ 0.5 mL/L.\n• Alternate with Thiamethoxam 25% WG @ 0.3 g/L or Spiromesifen @ 1.0 mL/L.\n• Target under-surface of foliage where whitefly nymphs congregate.",
                "prevention": (
                    f"🌾 Nursery Netting Protection: Cover seedling nursery beds with 50-mesh UV-stabilized insect netting to prevent early whitefly vector feeding.\n"
                    f"🔄 Vector Barrier Crops: Surround susceptible plots with border rows of tall non-host barrier crops (e.g. Corn, Sorghum, Pearl Millet).\n"
                    f"💧 Reflective Silver Mulching: Lay silver/black reflective plastic mulch across planting beds to disorient incoming flying whiteflies.\n"
                    f"🌿 Weed Reservoir Eradication: Remove nightshade, mallow, and bindweed weeds from surrounding field perimeters.\n"
                    f"🛡️ Resistant Hybrids: Plant certified TYLCV-resistant hybrids (e.g. Ty-1 / Ty-3 gene carrying cultivars)."
                )
            }
        else:
            disease_info[cls] = {
                "crop": crop_name,
                "disease": disease_name,
                "status": "Diseased",
                "is_background": False,
                "symptoms": f"• Pathological leaf spots, necrotic lesions, or chlorotic yellowing on {crop_name} foliage.\n• Irregular brown leaf margins and wilting of affected leaf canopy.\n• Stunted shoot development under severe disease pressure.",
                "cause": f"• Pathogenic fungal/bacterial micro-organism affecting {crop_name}.\n• Favored by warm temperatures, high humidity, and prolonged foliage wetness.\n• Spreads via wind, water splash, infected soil, or insect vectors.",
                "organic_treatment": f"• Prune infected foliage and remove severely diseased plant tissue.\n• Spray Copper Octanoate or Neem Extract (1%) bio-fungicide.\n• Improve soil health with Trichoderma-enriched organic bio-fertilizer.",
                "chemical_treatment": f"• Apply broad-spectrum protective fungicide Mancozeb 75% WP @ 2.5 g/L.\n• Alternate with Carbendazim 50% WP @ 1.0 g/L if fungal origin is suspected.\n• Consult local agricultural extension for precise local chemical guidelines.",
                "prevention": (
                    f"🌾 Certified Seed Stock: Sourced certified disease-free seeds/seedlings treated with bio-agents prior to sowing.\n"
                    f"🔄 3-Year Crop Rotation: Rotate out of host plant families for 3 consecutive seasons to break soil-borne pathogen cycles.\n"
                    f"💧 Subsurface Drip Irrigation: Irrigate at plant roots using drip tape; avoid high-pressure foliage wetting.\n"
                    f"🌿 Field Canopy Ventilation: Space plants at recommended row distances to promote fast leaf drying after rainfall.\n"
                    f"🛡️ Post-Harvest Sanitation: Remove and burn crop residue after harvest. Deep plow soil beds to bury overwintering inoculum."
                )
            }

    disease_info_path = os.path.join(MODELS_ASSETS_DIR, "disease_info.json")
    with open(disease_info_path, "w", encoding="utf-8") as f:
        json.dump(disease_info, f, indent=2)
    print(f"Saved expanded disease advisory metadata to '{disease_info_path}'")

if __name__ == "__main__":
    supplement_potato_healthy()
    export_class_names_and_disease_info()
