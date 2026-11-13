"""Regression checks for previously accepted uncarried chain numbers."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("validator", Path(__file__).with_name("validate.py"))
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class NumericEvidenceTests(unittest.TestCase):
    def test_coreweave_prepayment_cannot_match_alphabet_cash_flow(self):
        self.assertFalse(validator.supported(9, [46.9, 5, 9.07]))

    def test_missing_inflation_measures_cannot_match_unrelated_two(self):
        self.assertFalse(validator.supported(1.9, [2]))
        self.assertFalse(validator.supported(1.8, [2]))

    def test_exact_source_value_is_allowed(self):
        self.assertTrue(validator.supported(9.07, [9.07]))
        self.assertTrue(validator.supported(9, [9]))

    def test_demonstrable_decimal_rounding_is_allowed(self):
        self.assertTrue(validator.supported(27.1, [27.08]))
        self.assertTrue(validator.supported(10507, [10506.67]))

    def test_nearby_values_are_not_arbitrary_ten_percent_evidence(self):
        self.assertFalse(validator.supported(10.5, [10]))
        self.assertFalse(validator.supported(100, [105]))

    def test_years_require_exact_support(self):
        self.assertFalse(validator.supported(2026, [2025.9]))
        self.assertTrue(validator.supported(2026, [2026]))


if __name__ == "__main__":
    unittest.main()
