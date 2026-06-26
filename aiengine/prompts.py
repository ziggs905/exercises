def build_recipe_prompt(profile, targets, preferences='', meal_type=None):
    dietary_tags = ', '.join(profile.dietary_tags.values_list('slug', flat=True)) or 'none'
    allergies = profile.allergies.strip() or 'none'

    lines = ['You are a recipe generator for a nutrition app.']
    if meal_type:
        lines.append(f'This recipe is for: {meal_type}')
    lines += [
        f"Target calories per serving: {targets['calories']}",
        f"Target protein per serving: {targets['protein_g']}g",
        f"Target carbs per serving: {targets['carbs_g']}g",
        f"Target fat per serving: {targets['fat_g']}g",
        f'Dietary preferences: {dietary_tags}',
        f'Allergies to avoid: {allergies}',
    ]
    if preferences.strip():
        lines.append(f'Additional preferences: {preferences.strip()}')
    lines.append(
        'Respond with only a JSON object with keys: title, description, servings, '
        'prep_minutes, cook_minutes, calories, protein_g, carbs_g, fat_g, ingredients '
        '(list of objects with name, quantity, unit), steps (list of strings), '
        'tags (list of slugs). No text outside the JSON object.'
    )
    return '\n'.join(lines)
