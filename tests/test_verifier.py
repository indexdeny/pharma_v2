import unittest
from verification_agent import agent_2_verifier

class TestVerifier(unittest.TestCase):
    def test_positive_valid(self):
        # Fully valid passport
        data = {
            "product_name": "Atomoxetine",
            "active_ingredient": "Atomoxetine HCl",
            "branding": {
                "palette": {
                    "primary": "#005A9C",
                    "background": "#FFFFFF"
                }
            },
            "label_content": {
                "dosage_display": "40 mg",
                "unit_count_display": "30 Pills"
            },
            "brand_color_verified": True
        }
        res = agent_2_verifier(data)
        self.assertTrue(res["verified"])
        self.assertEqual(res["confidence"], 1.0)
        self.assertEqual(len(res["warnings"]), 0)

    def test_penalty_active_ingredient_equals_product_name(self):
        # active_ingredient == product_name -> penalty -0.15
        data = {
            "product_name": "Atomoxetine",
            "active_ingredient": "Atomoxetine",
            "branding": {
                "palette": {
                    "primary": "#005A9C",
                    "background": "#FFFFFF"
                }
            },
            "label_content": {
                "dosage_display": "40 mg",
                "unit_count_display": "30 Pills"
            },
            "brand_color_verified": True
        }
        res = agent_2_verifier(data)
        # confidence = 1.0 - 0.15 (ai==pn) = 0.85. Threshold is >= 0.70 so verified=True
        self.assertEqual(res["confidence"], 0.85)
        self.assertTrue(res["verified"])
        self.assertIn("active_ingredient identical to product_name", res["warnings"][0])

    def test_penalty_no_numeric_dosage(self):
        # dosage_display = "N/A" -> penalty -0.20
        data = {
            "product_name": "Atomoxetine",
            "active_ingredient": "Atomoxetine HCl",
            "branding": {
                "palette": {
                    "primary": "#005A9C",
                    "background": "#FFFFFF"
                }
            },
            "label_content": {
                "dosage_display": "N/A",
                "unit_count_display": "30 Pills"
            },
            "brand_color_verified": True
        }
        res = agent_2_verifier(data)
        self.assertEqual(res["confidence"], 0.80)
        self.assertTrue(res["verified"])

    def test_penalty_primary_equals_background_white(self):
        # primary = #FFFFFF, background = #FFFFFF -> penalty -0.30
        data = {
            "product_name": "Atomoxetine",
            "active_ingredient": "Atomoxetine HCl",
            "branding": {
                "palette": {
                    "primary": "#FFFFFF",
                    "background": "#FFFFFF"
                }
            },
            "label_content": {
                "dosage_display": "40 mg",
                "unit_count_display": "30 Pills"
            },
            "brand_color_verified": True
        }
        res = agent_2_verifier(data)
        self.assertEqual(res["confidence"], 0.70)
        # Threshold is 0.75 (raised in v2.2) — 0.70 is below threshold, not verified
        self.assertFalse(res["verified"])

    def test_penalty_background_not_white(self):
        # background = #0077CC -> penalty -0.30
        data = {
            "product_name": "Atomoxetine",
            "active_ingredient": "Atomoxetine HCl",
            "branding": {
                "palette": {
                    "primary": "#005A9C",
                    "background": "#0077CC"
                }
            },
            "label_content": {
                "dosage_display": "40 mg",
                "unit_count_display": "30 Pills"
            },
            "brand_color_verified": True
        }
        res = agent_2_verifier(data)
        self.assertEqual(res["confidence"], 0.70)
        self.assertFalse(res["verified"])
        self.assertIn("CHECK 3: background color #0077CC is not white", res["warnings"][0])

    def test_penalty_all_empty(self):
        # All empty fields -> confidence = 0.0
        data = {
            "product_name": "",
            "active_ingredient": "",
            "branding": {
                "palette": {
                    "primary": "#FFFFFF",
                    "background": "#FFFFFF"
                }
            },
            "label_content": {
                "dosage_display": "",
                "unit_count_display": ""
            },
            "brand_color_verified": False
        }
        res = agent_2_verifier(data)
        self.assertEqual(res["confidence"], 0.0)
        self.assertFalse(res["verified"])

    def test_check10_vertical_correct_scene_no_penalty(self):
        """CHECK 10: vertical vial SKU with correct vial scene → no penalty (P8.0 fix)."""
        data = {
            "sku_id": "414-min.jpg",  # vials pkg_type in SKU.csv
            "product_name": "Nandrolone Phenylpropionate",
            "active_ingredient": "Nandrolone",
            "packaging_geometry": "VIAL",
            "render_config": {
                "primary_render_target": "carton_box",
                "future_dual_shot_enabled": False,
                "scene_archetype": "vial_tray_carton",  # correct scene for vials
            },
            "branding": {
                "palette": {
                    "primary": "#003366",
                    "background": "#FFFFFF",
                }
            },
            "label_content": {
                "dosage_display": "100 mg/ml",
                "unit_count_display": "10 Vials",
            },
        }
        res = agent_2_verifier(data)
        # CHECK 10 should NOT fire — vial scene is correct for vertical product
        check10_warnings = [w for w in res["warnings"] if "CHECK 10" in w]
        self.assertEqual(len(check10_warnings), 0, f"CHECK 10 should not fire: {check10_warnings}")

    def test_check10_vertical_blister_scene_fires(self):
        """CHECK 10: vertical vial SKU with blister scene → routing mismatch penalty -0.15."""
        data = {
            "sku_id": "414-min.jpg",  # vials in SKU.csv
            "product_name": "Nandrolone Phenylpropionate",
            "active_ingredient": "Nandrolone",
            "packaging_geometry": "VIAL",
            "render_config": {
                "primary_render_target": "carton_box",
                "future_dual_shot_enabled": False,
                "scene_archetype": "slim_blister_carton",  # WRONG for vials
            },
            "branding": {
                "palette": {
                    "primary": "#003366",
                    "background": "#FFFFFF",
                }
            },
            "label_content": {
                "dosage_display": "100 mg/ml",
                "unit_count_display": "10 Vials",
            },
        }
        res = agent_2_verifier(data)
        check10_warnings = [w for w in res["warnings"] if "CHECK 10" in w]
        self.assertEqual(len(check10_warnings), 1, "CHECK 10 should fire for blister scene on vial")
        self.assertIn("routing mismatch", res["warnings"][0] if check10_warnings else "")

    def test_check10_pill_blister_scene_no_penalty(self):
        """CHECK 10: standard pill SKU with blister scene → no penalty (not vertical product)."""
        data = {
            "sku_id": "1-min.jpg",  # pills in SKU.csv
            "product_name": "Atomoxetine",
            "active_ingredient": "Atomoxetine HCl",
            "packaging_geometry": "BLISTER",
            "render_config": {
                "primary_render_target": "carton_box",
                "scene_archetype": "thick_blister_carton",  # correct for pills
            },
            "branding": {
                "palette": {
                    "primary": "#005A9C",
                    "background": "#FFFFFF",
                }
            },
            "label_content": {
                "dosage_display": "40 mg",
                "unit_count_display": "10 Pills",
            },
        }
        res = agent_2_verifier(data)
        check10_warnings = [w for w in res["warnings"] if "CHECK 10" in w]
        self.assertEqual(len(check10_warnings), 0, f"CHECK 10 should not fire for pills: {check10_warnings}")


if __name__ == "__main__":
    unittest.main()
