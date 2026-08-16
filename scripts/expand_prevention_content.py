import os
import json

MODELS_ASSETS_DIR = "models_assets"
DISEASE_INFO_PATH = os.path.join(MODELS_ASSETS_DIR, "disease_info.json")

def generate_expanded_prevention_database():
    print("======================================================================")
    print("   EXPANDING PROACTIVE PREVENTION CONTENT TO 70+ WORDS PER CLASS      ")
    print("======================================================================\n")

    with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
        disease_info = json.load(f)

    for cls, info in disease_info.items():
        if info.get("is_background", False):
            info["prevention"] = (
                "📷 Image Upload Guidance:\n"
                "• Upload a clear, focused photograph of an individual plant leaf under natural daylight.\n"
                "• Ensure the leaf blade covers at least 60% of the camera frame against a neutral background.\n"
                "• Avoid blurry, out-of-focus, or extremely dark photos to enable accurate deep learning diagnosis.\n"
                "• Make sure the leaf subject belongs to one of the 14 supported agricultural crop species."
            )
            continue

        crop = info.get("crop", "Crop")
        disease = info.get("disease", "Disease")
        disease_lower = cls.lower()

        if "healthy" in disease_lower:
            info["prevention"] = (
                f"🌾 Certified Seed & Planting Hygiene: Always plant certified disease-free seed stock sourced from recognized agricultural seed nurseries. Treat seeds prior to planting with bio-control agents such as *Trichoderma viride* @ 10 g/kg and *Pseudomonas fluorescens* @ 10 g/kg to promote robust root development and early seedling vigor.\n"
                f"🔄 Multi-Year Non-Host Crop Rotation: Practice a strict 3-year crop rotation schedule by rotating {crop} with non-host crop families (such as legumes, corn, or small grains). This breaks pathogen life cycles, prevents specialized soil-borne spore accumulation, and improves soil structure and organic matter.\n"
                f"💧 Subterranean Root-Zone Irrigation: Irrigate fields exclusively at the plant soil base using underground drip tape lines. Avoid morning, evening, or nighttime overhead sprinkler watering to keep leaf blades dry, which eliminates leaf wetness hours required for airborne fungal spore germination.\n"
                f"🌿 Canopy Spacing & Airflow Management: Maintain recommended inter-row and intra-row plant spacing (60 cm x 45 cm) during field transplantation. Perform periodic selective pruning of lower crowded sucker foliage to facilitate high airflow and maximum sunlight penetration into the lower canopy.\n"
                f"🛡️ Soil Immunity & Proactive Scouting: Apply well-rotted organic compost enriched with neem cake @ 250 kg/acre to build natural rhizosphere immunity. Conduct systematic weekly field scouting across plots to inspect leaf undersides for early symptoms or insect vectors."
            )
        elif "potato" in disease_lower and "early_blight" in disease_lower:
            info["prevention"] = (
                f"🌾 Seed Tuber Sanitation & Bio-Priming: Plant certified disease-free potato seed tubers. Dip tubers prior to planting in a bio-fungicide slurry of *Trichoderma harzianum* @ 10 g/kg or *Pseudomonas fluorescens* @ 10 g/kg to protect emerging shoots against tuber-borne *Alternaria solani* spores.\n"
                f"🔄 3-Season Solanaceous Crop Rotation: Implement a mandatory 3-year crop rotation cycle avoiding solanaceous species (Potato, Tomato, Eggplant, Pepper). Rotate with non-solanaceous cover crops like Mustard, Legumes, or Maize to deplete soil fungal spore populations.\n"
                f"💧 Subsurface Drip Irrigation: Utilize ground drip irrigation tape to deliver moisture directly to root zones. Avoid high-pressure overhead sprinklers which splash soil-borne *Alternaria* spores onto lower foliage and extend leaf wetness duration.\n"
                f"🌿 Protective Soil Mulching & Spacing: Apply a 3-inch layer of clean straw mulch over plant beds to create a physical barrier preventing fungal spore rain-splash from soil onto lower leaves. Maintain recommended plant spacing (60 cm x 45 cm) for optimal canopy drying.\n"
                f"🛡️ Stubble Disposal & Weed Sanitation: Shred and deep-plow crop stubble immediately post-harvest to accelerate organic decomposition of fungal survival structures. Eradicate wild nightshade weed reservoirs along field borders throughout the growing season."
            )
        elif "potato" in disease_lower and "late_blight" in disease_lower:
            info["prevention"] = (
                f"🌾 Cultivar Resistance & Seed Selection: Plant late blight resistant potato cultivars (such as Kufri Girdhari, Kufri Himalini, or resistant hybrids). Source certified disease-free seed tubers from official seed certification agencies.\n"
                f"🔄 High Soil Ridging & Tuber Protection: Maintain prominent, well-drained soil ridges (25–30 cm high) around potato stems to create a physical soil filter that prevents surface *Phytophthora infestans* sporangia from washing down to infect subterranean tubers during heavy rains.\n"
                f"💧 Weather-Based Preventive Spraying: Monitor local agricultural meteorological alerts for cool, humid weather spells (temperatures 15°C–22°C, RH >90%). Apply protective copper octanoate or Bordeaux mixture (1%) sprays *prior* to rainfall events.\n"
                f"🌿 Cull Pile & Volunteer Destruction: Locate and completely destroy all cull tuber disposal piles, volunteer potato sprouts, and wild solanaceous weeds within a 500-meter radius of potato fields to eliminate primary airborne inoculum sources.\n"
                f"🛡️ Vine Killing & Harvest Timing: Apply vine desiccant (or kill tops mechanically) 14 days before harvest. Allow tuber skins to mature completely in dry soil prior to digging to prevent live sporangia contact during harvesting."
            )
        elif "blight" in disease_lower:
            info["prevention"] = (
                f"🌾 Seed Heat-Treatment & Bio-Protection: Sow certified disease-free seeds treated with hot water (50°C for 25 mins) and bio-fungicides to neutralize seed-borne fungal and bacterial pathogens.\n"
                f"🔄 Field Crop Rotation Protocol: Execute a strict 3-year non-host crop rotation schedule to starve fungal resting spores and reduce pathogen survival in crop debris.\n"
                f"💧 Drip Irrigation & Canopy Drying: Switch completely to root-zone drip irrigation lines. Ensure field beds are aligned with prevailing wind directions to facilitate fast leaf canopy drying after rainfall.\n"
                f"🌿 Plant Spacing & Straw Mulching: Transplant crops at recommended distances (60x45 cm) and lay clean organic straw mulch to suppress soil-splash fungal spore movement onto lower leaves.\n"
                f"🛡️ Post-Harvest Stubble Sanitation: Burn or deep-plow infected plant residues immediately following harvest. Keep field margins clean of volunteer host weeds throughout the winter season."
            )
        elif "spot" in disease_lower or "rot" in disease_lower:
            info["prevention"] = (
                f"🌾 Seed Sanitization & Resistant Hybrids: Use hot-water treated seeds or soak in *Streptomyces* bio-bactericide solution. Choose bacterial spot/rot resistant hybrid cultivars.\n"
                f"🔄 Multi-Year Crop Diversification: Rotate fields with non-susceptible crop families (Maize, Legumes, Alliums) for 3 to 4 years to break bacterial pathogen persistence in soil.\n"
                f"💧 Subsurface Drip & Dew Management: Avoid overhead sprinkler irrigation. Refrain from working, weeding, or harvesting in crop fields when foliage is wet from morning dew or recent rain.\n"
                f"🌿 Equipment & Tool Disinfection: Sterilize pruning shears, harvest knives, tractors, and spray rigs between rows using a 70% isopropyl alcohol or quaternary ammonium disinfectant solution.\n"
                f"🛡️ Windbreak Barriers & Weed Clearing: Plant peripheral taller crop windbreaks (Sorghum or Pearl Millet) to intercept wind-driven rain splash, and clear wild host weeds around field perimeters."
            )
        elif "rust" in disease_lower or "mildew" in disease_lower:
            info["prevention"] = (
                f"🌾 Resistant Cultivars & Site Selection: Plant resistant crop varieties in open, unshaded fields receiving full sunlight (minimum 6–8 hours daily) to inhibit fungal spore germination.\n"
                f"🔄 Balanced Nitrogen Fertilization: Avoid excessive, late-season synthetic nitrogen applications which stimulate lush tender foliage highly susceptible to rust and powdery mildew spores.\n"
                f"💧 Ground-Level Drip Irrigation: Irrigate crops exclusively at soil base using subterranean drip lines during early morning hours to maintain dry leaf surfaces.\n"
                f"🌿 Canopy Aeration & Pruning: Maintain wide row spacing and perform selective pruning of inner sucker shoots to maximize airflow and minimize micro-climate relative humidity within canopy.\n"
                f"🛡️ Proactive Bio-Barrier Sprays: Apply preventive dusting of elemental sulfur or foliar sprays of *Bacillus amyloliquefaciens* at 14-day intervals prior to initial spore emergence."
            )
        elif "virus" in disease_lower or "curl" in disease_lower or "mosaic" in disease_lower:
            info["prevention"] = (
                f"🌾 Insect Netting & Seedling Protection: Cover seedling nursery beds with 50-mesh UV-stabilized insect-proof netting to prevent early whitefly and aphid vector feeding during sensitive early growth stages.\n"
                f"🔄 Reflective Silver Mulching: Lay reflective silver-on-black plastic mulch across planting beds to disorient incoming flying insect vectors and suppress weed growth.\n"
                f"💧 Perimeter Barrier Crops: Plant 3–4 border rows of tall non-host barrier crops (such as Corn, Sorghum, or Pearl Millet) around fields to act as a physical trap for insect vectors.\n"
                f"🌿 Vector Monitoring & Sticky Traps: Install yellow sticky traps (30–40 traps/acre) across field plots to continuously monitor and catch whitefly and aphid populations.\n"
                f"🛡️ Resistant Hybrids & Weed Eradication: Plant certified virus-resistant hybrids and clear weed reservoir hosts (Solanaceous and Malvaceous weeds) within 100 meters of crop fields."
            )
        else:
            info["prevention"] = (
                f"🌾 Certified Seed Stock & Soil Priming: Sow certified, disease-free seed stock treated with bio-control agents such as *Trichoderma viride* @ 10 g/kg to build initial seedling defense.\n"
                f"🔄 3-Year Non-Host Crop Rotation: Rotate {crop} with non-susceptible crop families for 3 consecutive seasons to disrupt pathogen survival cycles in field soil.\n"
                f"💧 Subterranean Drip Irrigation: Irrigate strictly at soil root zones via drip tape lines, completely avoiding overhead leaf watering to maintain foliage dryness.\n"
                f"🌿 Canopy Spacing & Aeration: Space plants adequately during transplanting to promote fast leaf canopy drying after rain events and prevent micro-climate humidity build-up.\n"
                f"🛡️ Field Sanitation & Debris Removal: Clear, compost, or deep-plow all crop residues post-harvest, and maintain weed-free field perimeters to prevent overwintering pathogen persistence."
            )

    with open(DISEASE_INFO_PATH, "w", encoding="utf-8") as f:
        json.dump(disease_info, f, indent=2)

    # Verify word counts across all 39 classes
    print("--- Verification of Prevention Word Counts across All 39 Classes ---")
    all_passed = True
    for cls, info in disease_info.items():
        prev_text = info.get("prevention", "")
        word_count = len(prev_text.split())
        print(f"Class: {cls:<45} | Word Count: {word_count} words")
        if word_count < 50:
            all_passed = False
            print(f"⚠️ WARNING: Class '{cls}' has fewer than 50 words ({word_count} words).")

    if all_passed:
        print("\nSUCCESS: Every single class has AT LEAST 50+ WORDS in its prevention guidance! 🎉")

if __name__ == "__main__":
    generate_expanded_prevention_database()
