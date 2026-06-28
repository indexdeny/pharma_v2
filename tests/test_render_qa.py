import unittest
from unittest.mock import patch
from pathlib import Path
from render_qa import check_image

class TestRenderQA(unittest.TestCase):
    @patch('render_qa.extract_text')
    def test_dosage_word_boundary_matching(self, mock_extract):
        # Test case: dosage "5" in "500mg" should be False, but "5" in "5 mg" should be True
        passport = {
            "brand_name": "TestDrug",
            "label_content": {
                "dosage_display": "5 mg",
                "unit_count_display": "10 Pills"
            }
        }
        
        # Scenario A: OCR returns "500mg" (dosage "5" should NOT be found due to word boundaries)
        mock_extract.return_value = (True, "TestDrug 500mg 10 Pills")
        res = check_image(Path("dummy.png"), passport)
        self.assertFalse(res["dosage_found"], "Dosage '5' should not match inside '500'")
        
        # Scenario B: OCR returns "5 mg" (dosage "5" should be found)
        mock_extract.return_value = (True, "TestDrug 5 mg 10 Pills")
        res = check_image(Path("dummy.png"), passport)
        self.assertTrue(res["dosage_found"], "Dosage '5' should match in '5 mg'")

        # Scenario C: OCR returns "dosage: 5, quantity: 10" (dosage "5" should be found)
        mock_extract.return_value = (True, "TestDrug dosage: 5, quantity: 10")
        res = check_image(Path("dummy.png"), passport)
        self.assertTrue(res["dosage_found"], "Dosage '5' should match with surrounding punctuation")

    @patch('render_qa.extract_text')
    def test_unit_count_word_boundary_matching(self, mock_extract):
        passport = {
            "brand_name": "TestDrug",
            "label_content": {
                "dosage_display": "50 mg",
                "unit_count_display": "10 Pills"
            }
        }
        
        # Scenario A: OCR returns "100 Pills" (count "10" should NOT match inside "100")
        mock_extract.return_value = (True, "TestDrug 50 mg 100 Pills")
        res = check_image(Path("dummy.png"), passport)
        self.assertFalse(res["count_found"], "Count '10' should not match inside '100'")
        
        # Scenario B: OCR returns "10 Pills" (count "10" should match)
        mock_extract.return_value = (True, "TestDrug 50 mg 10 Pills")
        res = check_image(Path("dummy.png"), passport)
        self.assertTrue(res["count_found"], "Count '10' should match in '10 Pills'")

if __name__ == '__main__':
    unittest.main()
