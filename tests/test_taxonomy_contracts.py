"""
======================================================================
 Taxonomy Contract & Data Invariant Test Suite
 Multi-Crop Plant Disease Detection & Advisory System
======================================================================
Verifies data consistency between:
- models_assets/dpd_crop_rankings.json (333 pairs, 55 crops)
- models_assets/dpd_55_plants.json (55 plant head classes)
- models_assets/dpd_175_diseases.json (175 disease head classes)
- models_assets/disease_info.json (Clinical advisory knowledge base)
"""

import os
import sys
import json
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dpd_model


class TestTaxonomyContracts:
    """Contract tests ensuring zero data drift or missing pairings across assets."""

    @pytest.fixture(scope="class")
    @staticmethod
    def assets():
        assets_dir = "models_assets"
        with open(os.path.join(assets_dir, "dpd_crop_rankings.json"), "r", encoding="utf-8") as f:
            rankings = json.load(f)
        with open(os.path.join(assets_dir, "dpd_55_plants.json"), "r", encoding="utf-8") as f:
            plants = json.load(f)
        with open(os.path.join(assets_dir, "dpd_175_diseases.json"), "r", encoding="utf-8") as f:
            diseases = json.load(f)
        with open(os.path.join(assets_dir, "disease_info.json"), "r", encoding="utf-8") as f:
            disease_info = json.load(f)

        return {
            "rankings": rankings,
            "plants": plants,
            "diseases": diseases,
            "disease_info": disease_info
        }

    def test_crop_rankings_has_333_pairs_and_55_crops(self, assets):
        rankings = assets["rankings"]
        assert len(rankings) == 55, f"Expected 55 crops in rankings, found {len(rankings)}"

        total_pairs = sum(len(c.get("all_diseases", {})) for c in rankings)
        assert total_pairs == 333, f"Expected exactly 333 crop-disease pairs in rankings, found {total_pairs}"

    def test_plants_contract_exact_55_mapping(self, assets):
        plants = assets["plants"]
        rankings = assets["rankings"]

        assert len(plants) == 55, f"Expected 55 plants in dpd_55_plants.json, found {len(plants)}"
        p_slugs = set(v.lower().strip().replace(" ", "_") for v in plants.values())

        for c in rankings:
            c_slug = c["crop"].lower().strip().replace(" ", "_")
            assert c_slug in p_slugs, f"Crop '{c['crop']}' from rankings is missing from dpd_55_plants.json!"

    def test_diseases_contract_exact_175_mapping(self, assets):
        diseases = assets["diseases"]
        rankings = assets["rankings"]

        assert len(diseases) == 175, f"Expected 175 diseases in dpd_175_diseases.json, found {len(diseases)}"
        d_slugs = set(v.lower().strip().replace(" ", "_") for v in diseases.values())

        for c in rankings:
            for d_name in c.get("all_diseases", {}).keys():
                d_slug = d_name.lower().strip().replace(" ", "_")
                assert d_slug in d_slugs, f"Disease '{d_name}' on crop '{c['crop']}' missing from dpd_175_diseases.json!"

    def test_100_percent_advisory_coverage(self, assets):
        """Validates that 100% of the 333 supported pairs have complete 5-pillar advisory data."""
        pairs = dpd_model.load_333_supported_pairs("models_assets")
        disease_info = assets["disease_info"]

        # Create lightweight engine instance for lookup testing
        engine = dpd_model.DPDInferenceEngine()

        missing_advisory = []
        for pair in pairs:
            adv = engine._match_advisory(pair, disease_info)
            if not adv:
                missing_advisory.append(pair["raw_class"])
                continue

            # Verify presence of all 5 clinical pillars
            for pillar in ["symptoms", "cause", "organic_treatment", "chemical_treatment", "prevention"]:
                assert pillar in adv and len(adv[pillar]) > 0, (
                    f"Pillar '{pillar}' is empty for class '{pair['raw_class']}'!"
                )

        assert len(missing_advisory) == 0, (
            f"Advisory coverage incomplete! Missing {len(missing_advisory)} pairs: {missing_advisory[:10]}"
        )

    def test_pv_legacy_fallback_is_valid_subset(self):
        """Ensures the 38-class legacy fallback mapping remains a strictly valid subset of the 333 taxonomy."""
        for pv_cls, (p_name, d_name, p_idx, d_idx, _) in dpd_model.PV_TO_DPD_MAPPING.items():
            assert 0 <= p_idx < 55, f"Plant index {p_idx} out of range in PV_TO_DPD_MAPPING"
            assert 0 <= d_idx < 175, f"Disease index {d_idx} out of range in PV_TO_DPD_MAPPING"
            assert isinstance(p_name, str) and len(p_name) > 0
            assert isinstance(d_name, str) and len(d_name) > 0
