import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile
from aiengine.parsing import RecipeParseError, parse_recipe
from aiengine.services import generate_and_save_recipe
from recipes.models import Tag


class ParseRecipeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='High Protein', slug='high-protein', category=Tag.Category.NUTRITIONAL)
        Tag.objects.create(name='Quick Meals', slug='quick-meals', category=Tag.Category.PRACTICAL)

    def test_parse_recipe_normalizes_valid_payload_and_drops_unknown_tags(self):
        raw_json = json.dumps({
            'title': 'Chicken Bowl',
            'description': 'Great lunch bowl.',
            'servings': 2,
            'prep_minutes': 10,
            'cook_minutes': 20,
            'calories': 550,
            'protein_g': 40.0,
            'carbs_g': 45.0,
            'fat_g': 20.0,
            'ingredients': [{'name': ' chicken breast ', 'quantity': 300, 'unit': 'g'}],
            'steps': ['Cook the chicken', 'Serve it warm'],
            'tags': ['high-protein', 'unknown-tag'],
        })

        payload = parse_recipe(raw_json)

        self.assertEqual(payload['title'], 'Chicken Bowl')
        self.assertEqual(payload['ingredients'][0]['name'], 'chicken breast')
        self.assertEqual(payload['tags'], ['high-protein'])

    def test_parse_recipe_rejects_invalid_payloads(self):
        with self.assertRaises(RecipeParseError):
            parse_recipe(json.dumps({'title': 'Bad', 'description': 'Recipe', 'ingredients': [], 'steps': []}))


class GenerateAndSaveRecipeTests(TestCase):
    def test_generate_and_save_recipe_creates_recipe_from_mocked_provider(self):
        user = User.objects.create_user(username='chef', password='secret123')
        profile = Profile.objects.create(user=user)
        tag = Tag.objects.create(name='High Protein', slug='high-protein', category=Tag.Category.NUTRITIONAL)
        profile.dietary_tags.add(tag)

        fake_response = json.dumps({
            'title': 'Mocked Dinner',
            'description': 'A nice dinner.',
            'servings': 1,
            'prep_minutes': 5,
            'cook_minutes': 10,
            'calories': 450,
            'protein_g': 30.0,
            'carbs_g': 35.0,
            'fat_g': 15.0,
            'ingredients': [{'name': 'salmon', 'quantity': 200, 'unit': 'g'}],
            'steps': ['Cook the salmon'],
            'tags': ['high-protein'],
        })

        with patch('aiengine.services.get_provider', return_value=type('StubProvider', (), {'generate_recipe': lambda self, prompt: fake_response})()):
            recipe, error = generate_and_save_recipe(user, profile, {'calories': 500, 'protein_g': 35, 'carbs_g': 40, 'fat_g': 15}, 'dinner')

        self.assertIsNone(error)
        self.assertEqual(recipe.title, 'Mocked Dinner')
        self.assertEqual(recipe.meal_type, 'dinner')
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(list(recipe.tags.values_list('slug', flat=True)), ['high-protein'])
