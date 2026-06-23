import json

from recipes.models import Tag

REQUIRED_STRING_FIELDS = ['title', 'description']
REQUIRED_NUMERIC_FIELDS = [
    'servings', 'prep_minutes', 'cook_minutes', 'calories', 'protein_g', 'carbs_g', 'fat_g',
]
ALLOWED_UNITS = {'g', 'ml', 'pcs', 'tbsp', 'tsp'}


class RecipeParseError(Exception):
    pass


def parse_recipe(raw_json):
    """Parse and validate raw AI provider JSON text against the recipe schema."""
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise RecipeParseError(f'Invalid JSON: {exc}') from exc

    if not isinstance(data, dict):
        raise RecipeParseError('Recipe JSON must be an object.')

    for field in REQUIRED_STRING_FIELDS:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise RecipeParseError(f'Missing or invalid field: {field}')

    for field in REQUIRED_NUMERIC_FIELDS:
        value = data.get(field)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise RecipeParseError(f'Missing or invalid field: {field}')

    ingredients = data.get('ingredients')
    if not isinstance(ingredients, list) or not ingredients:
        raise RecipeParseError('Missing or invalid field: ingredients')

    clean_ingredients = []
    for item in ingredients:
        if not isinstance(item, dict):
            raise RecipeParseError('Each ingredient must be an object.')
        name = item.get('name')
        quantity = item.get('quantity')
        unit = item.get('unit')
        if not isinstance(name, str) or not name.strip():
            raise RecipeParseError('Ingredient is missing a valid name.')
        if not isinstance(quantity, (int, float)) or isinstance(quantity, bool):
            raise RecipeParseError('Ingredient is missing a valid quantity.')
        if unit not in ALLOWED_UNITS:
            raise RecipeParseError(f'Ingredient has an invalid unit: {unit!r}')
        clean_ingredients.append({'name': name.strip(), 'quantity': quantity, 'unit': unit})

    steps = data.get('steps')
    if not isinstance(steps, list) or not steps or not all(
        isinstance(step, str) and step.strip() for step in steps
    ):
        raise RecipeParseError('Missing or invalid field: steps')

    raw_tags = data.get('tags', [])
    if not isinstance(raw_tags, list):
        raise RecipeParseError('Field "tags" must be a list.')
    known_slugs = set(Tag.objects.values_list('slug', flat=True))
    clean_tags = [slug for slug in raw_tags if slug in known_slugs]

    return {
        'title': data['title'].strip(),
        'description': data['description'].strip(),
        'servings': int(data['servings']),
        'prep_minutes': int(data['prep_minutes']),
        'cook_minutes': int(data['cook_minutes']),
        'calories': int(data['calories']),
        'protein_g': float(data['protein_g']),
        'carbs_g': float(data['carbs_g']),
        'fat_g': float(data['fat_g']),
        'ingredients': clean_ingredients,
        'steps': [step.strip() for step in steps],
        'tags': clean_tags,
    }
