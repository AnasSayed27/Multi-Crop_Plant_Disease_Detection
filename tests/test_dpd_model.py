"""
======================================================================
 Unit Test Suite: DPD Dual-Head Vision Transformer Model Module
 Multi-Crop Plant Disease Detection & Advisory System
======================================================================
"""

import os
import sys
import pytest
import torch
from PIL import Image
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dpd_model


class TestDPDModelTaxonomyAndArchitecture:
    """Validates the mathematical architecture and 333-pair taxonomy of DPD ViT-Base."""

    def test_load_333_supported_pairs_count_and_uniqueness(self):
        pairs = dpd_model.load_333_supported_pairs("models_assets")
        assert len(pairs) == 333, f"Expected 333 pairs, but got {len(pairs)}"

        # Verify uniqueness of (plant_idx, disease_idx)
        unique_indices = set((p["plant_idx"], p["disease_idx"]) for p in pairs)
        assert len(unique_indices) == 333, "Duplicate plant-disease index pairs found!"

        # Verify plant head index bounds [0, 54] and disease head bounds [0, 174]
        for p in pairs:
            assert 0 <= p["plant_idx"] < 55, f"Plant index {p['plant_idx']} out of bounds [0, 54]"
            assert 0 <= p["disease_idx"] < 175, f"Disease index {p['disease_idx']} out of bounds [0, 174]"
            assert "crop" in p and len(p["crop"]) > 0
            assert "disease" in p and len(p["disease"]) > 0
            assert "crop_slug" in p
            assert "disease_slug" in p

    def test_dual_head_architecture_dimensions(self):
        model = dpd_model.DPDViTDualHead(num_plants=55, num_diseases=175)
        assert model.linear_plant.in_features == 768
        assert model.linear_plant.out_features == 55
        assert model.linear_disease.in_features == 768
        assert model.linear_disease.out_features == 175

    def test_model_forward_pass_tensor_shapes(self):
        model = dpd_model.DPDViTDualHead(num_plants=55, num_diseases=175)
        model.eval()

        dummy_tensor = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            p_out, d_out = model(dummy_tensor)

        assert p_out.shape == (1, 55), f"Expected (1, 55) plant logits, got {p_out.shape}"
        assert d_out.shape == (1, 175), f"Expected (1, 175) disease logits, got {d_out.shape}"

    def test_non_plantvillage_crops_present(self):
        """Ensures the bug that restricted DPD to only 38 PlantVillage classes never regresses."""
        pairs = dpd_model.load_333_supported_pairs("models_assets")
        crops_present = set(p["crop"].lower() for p in pairs)

        # Critical non-PlantVillage crops that must be present in 55-crop taxonomy
        required_crops = ["cassava", "coffee", "wheat", "banana", "cotton", "paddy", "sugarcane"]
        for crop in required_crops:
            assert any(crop in c for c in crops_present), f"Required crop '{crop}' missing from supported pairs!"


class TestDPDInferenceEngine:
    """Validates runtime behavior, confidence monotonicity, and output structure."""

    @pytest.fixture(scope="class")
    @staticmethod
    def engine():
        eng = dpd_model.get_inference_engine(assets_dir="models_assets")
        return eng

    def test_engine_initialization(self, engine):
        assert engine is not None
        assert len(engine.supported_pairs) == 333
        assert engine.loaded is True, "Engine failed to load checkpoint weights"

    def test_prediction_output_schema_and_monotonic_confidence(self, engine):
        # Create a synthetic image for inference
        img = Image.new("RGB", (224, 224), color=(34, 139, 34))

        import json
        with open("models_assets/disease_info.json", "r", encoding="utf-8") as f:
            disease_info = json.load(f)

        result = engine.predict(img, disease_info=disease_info)

        assert result["success"] is True
        assert "crop" in result and isinstance(result["crop"], str)
        assert "disease" in result and isinstance(result["disease"], str)
        assert "confidence" in result and 0.0 <= result["confidence"] <= 100.0
        assert "is_healthy" in result and isinstance(result["is_healthy"], bool)
        assert "top_3_predictions" in result and len(result["top_3_predictions"]) == 3

        # Critical Check: Strict Monotonic Confidence (Conf1 >= Conf2 >= Conf3)
        top3 = result["top_3_predictions"]
        conf1 = top3[0]["confidence"]
        conf2 = top3[1]["confidence"]
        conf3 = top3[2]["confidence"]

        assert conf1 >= conf2, f"Top 1 confidence ({conf1}%) is less than Top 2 ({conf2}%)!"
        assert conf2 >= conf3, f"Top 2 confidence ({conf2}%) is less than Top 3 ({conf3}%)!"
        assert result["confidence"] == conf1, "Top-level confidence does not match Top 1 prediction!"

        # Advisory 5-pillar structure check
        advisory = result["advisory"]
        assert "symptoms" in advisory and len(advisory["symptoms"]) > 0
        assert "cause" in advisory and len(advisory["cause"]) > 0
        assert "organic_treatment" in advisory and len(advisory["organic_treatment"]) > 0
        assert "chemical_treatment" in advisory and len(advisory["chemical_treatment"]) > 0
        assert "prevention" in advisory and len(advisory["prevention"]) > 0

    def test_prediction_with_real_leaf_image(self, engine):
        real_img_path = "test_real_images/Potato_Early-Blight-1.jpg"
        if not os.path.exists(real_img_path):
            pytest.skip(f"Test image '{real_img_path}' not found.")

        img = Image.open(real_img_path)
        import json
        with open("models_assets/disease_info.json", "r", encoding="utf-8") as f:
            disease_info = json.load(f)

        result = engine.predict(img, disease_info=disease_info)

        assert result["success"] is True
        assert "potato" in result["crop"].lower()
        assert "early blight" in result["disease"].lower()
        assert result["confidence"] > 70.0, f"Expected >70% confidence on clear potato leaf, got {result['confidence']}%"
        assert result["is_healthy"] is False
