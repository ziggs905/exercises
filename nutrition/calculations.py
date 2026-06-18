"""Pure nutrition calculation functions: BMR, TDEE, goal calories, macro split, and BMI.

No Django or ORM imports here — every function takes plain numbers/strings
and returns plain numbers/dicts, independent of any model.
"""

ACTIVITY_FACTORS = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'active': 1.725,
    'very_active': 1.9,
}

GOAL_CALORIE_ADJUSTMENTS = {
    'lose': -500,
    'maintain': 0,
    'gain': 300,
}

MIN_GOAL_CALORIES = 1200

MACRO_SPLITS = {
    'lose': {'protein': 0.40, 'carbs': 0.30, 'fat': 0.30},
    'maintain': {'protein': 0.30, 'carbs': 0.40, 'fat': 0.30},
    'gain': {'protein': 0.25, 'carbs': 0.50, 'fat': 0.25},
}

PROTEIN_KCAL_PER_G = 4
CARBS_KCAL_PER_G = 4
FAT_KCAL_PER_G = 9


def calculate_bmr(weight_kg, height_cm, age, sex):
    """BMR via the Mifflin-St Jeor equation."""
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if sex == 'M' else base - 161


def calculate_tdee(bmr, activity_level):
    """TDEE: BMR scaled by activity factor."""
    return bmr * ACTIVITY_FACTORS[activity_level]


def calculate_goal_calories(tdee, goal):
    """TDEE adjusted for the goal, never below a 1200 kcal/day floor."""
    calories = tdee + GOAL_CALORIE_ADJUSTMENTS[goal]
    return max(calories, MIN_GOAL_CALORIES)


def calculate_macros(goal_calories, goal):
    """Split goal calories into protein/carbs/fat grams for the goal."""
    split = MACRO_SPLITS[goal]
    return {
        'protein_g': (goal_calories * split['protein']) / PROTEIN_KCAL_PER_G,
        'carbs_g': (goal_calories * split['carbs']) / CARBS_KCAL_PER_G,
        'fat_g': (goal_calories * split['fat']) / FAT_KCAL_PER_G,
    }


def calculate_bmi(weight_kg, height_cm):
    """Body Mass Index (kg/m^2)."""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    """Classify a BMI value into a category."""
    if bmi < 18.5:
        return 'underweight'
    if bmi < 25:
        return 'normal'
    if bmi < 30:
        return 'overweight'
    return 'obese'
