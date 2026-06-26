from .calculations import calculate_bmr, calculate_goal_calories, calculate_macros, calculate_tdee

DEFAULT_MEAL_RATIOS = {
    'breakfast': 25,
    'lunch': 35,
    'dinner': 30,
    'snack': 10,
}


def slot_targets(daily_targets, pct):
    """Scale daily calorie/macro targets down to one meal slot's share."""
    fraction = pct / 100
    return {
        'calories': round(daily_targets['calories'] * fraction),
        'protein_g': round(daily_targets['protein_g'] * fraction, 1),
        'carbs_g': round(daily_targets['carbs_g'] * fraction, 1),
        'fat_g': round(daily_targets['fat_g'] * fraction, 1),
    }


def profile_is_complete(profile):
    """Whether a Profile has all the fields nutrition calculations need."""
    return bool(
        profile and profile.weight_kg and profile.height_cm and profile.age
        and profile.sex and profile.activity_level and profile.goal
    )


def compute_daily_targets(profile):
    """Goal calories and macro grams for a Profile with metrics set."""
    bmr = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.sex)
    tdee = calculate_tdee(bmr, profile.activity_level)
    goal_calories = calculate_goal_calories(tdee, profile.goal)
    macros = calculate_macros(goal_calories, profile.goal)
    return {
        'calories': round(goal_calories),
        'protein_g': round(macros['protein_g'], 1),
        'carbs_g': round(macros['carbs_g'], 1),
        'fat_g': round(macros['fat_g'], 1),
    }
