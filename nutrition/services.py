from .calculations import calculate_bmr, calculate_goal_calories, calculate_macros, calculate_tdee


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
