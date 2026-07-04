from django.test import SimpleTestCase

from nutrition import calculations


class NutritionCalculationsTests(SimpleTestCase):
    def test_bmr_formula_uses_the_expected_constants(self):
        self.assertEqual(calculations.calculate_bmr(70, 175, 30, 'M'), 10 * 70 + 6.25 * 175 - 5 * 30 + 5)
        self.assertEqual(calculations.calculate_bmr(65, 165, 28, 'F'), 10 * 65 + 6.25 * 165 - 5 * 28 - 161)

    def test_goal_calories_never_drop_below_the_floor(self):
        self.assertEqual(calculations.calculate_goal_calories(1000, 'lose'), 1200)
        self.assertEqual(calculations.calculate_goal_calories(2000, 'gain'), 2300)

    def test_macros_and_bmi_category_are_computed_as_expected(self):
        macros = calculations.calculate_macros(2400, 'maintain')
        self.assertAlmostEqual(macros['protein_g'], 180.0)
        self.assertAlmostEqual(macros['carbs_g'], 240.0)
        self.assertAlmostEqual(macros['fat_g'], 80.0)
        self.assertEqual(calculations.get_bmi_category(17.5), 'underweight')
        self.assertEqual(calculations.get_bmi_category(22.0), 'normal')
        self.assertEqual(calculations.get_bmi_category(27.0), 'overweight')
        self.assertEqual(calculations.get_bmi_category(32.0), 'obese')
