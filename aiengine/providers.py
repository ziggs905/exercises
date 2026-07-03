import itertools
import json
import re
from typing import Protocol

from django.conf import settings
from google import genai
from google.genai import types
from google.genai._gaos.lib import compat_errors as genai_errors


class RecipeProvider(Protocol):
    def generate_recipe(self, prompt: str) -> str:
        ...


class ProviderError(Exception):
    pass


CANNED_RECIPES = [
    {
        "title": "Grilled Chicken and Rice Bowl",
        "description": "A balanced bowl of grilled chicken breast, rice, and steamed broccoli.",
        "servings": 1,
        "prep_minutes": 10,
        "cook_minutes": 20,
        "calories": 550,
        "protein_g": 40.0,
        "carbs_g": 45.0,
        "fat_g": 20.0,
        "ingredients": [
            {"name": "chicken breast", "quantity": 200, "unit": "g"},
            {"name": "cooked rice", "quantity": 150, "unit": "g"},
            {"name": "broccoli", "quantity": 100, "unit": "g"},
            {"name": "olive oil", "quantity": 1, "unit": "tbsp"},
        ],
        "steps": [
            "Season the chicken breast with salt and pepper.",
            "Grill the chicken for 8-10 minutes per side until cooked through.",
            "Steam the broccoli for 5 minutes.",
            "Serve the chicken and broccoli over rice, drizzled with olive oil.",
        ],
        "tags": ["high-protein", "quick-meals"],
    },
    {
        "title": "Veggie Lentil Stew",
        "description": "A hearty vegan stew of lentils, carrots, and tomatoes.",
        "servings": 2,
        "prep_minutes": 10,
        "cook_minutes": 30,
        "calories": 420,
        "protein_g": 22.0,
        "carbs_g": 60.0,
        "fat_g": 10.0,
        "ingredients": [
            {"name": "red lentils", "quantity": 150, "unit": "g"},
            {"name": "carrot", "quantity": 2, "unit": "pcs"},
            {"name": "canned tomatoes", "quantity": 400, "unit": "g"},
            {"name": "vegetable stock", "quantity": 500, "unit": "ml"},
        ],
        "steps": [
            "Saute the chopped carrot for 5 minutes.",
            "Add the lentils, tomatoes, and stock.",
            "Simmer for 25 minutes until the lentils are soft.",
            "Season to taste and serve.",
        ],
        "tags": ["vegan", "budget-friendly", "high-fiber"],
    },
    {
        "title": "Greek Yogurt Protein Parfait",
        "description": "A quick high-protein parfait with yogurt, berries, and almonds.",
        "servings": 1,
        "prep_minutes": 5,
        "cook_minutes": 0,
        "calories": 320,
        "protein_g": 28.0,
        "carbs_g": 30.0,
        "fat_g": 10.0,
        "ingredients": [
            {"name": "greek yogurt", "quantity": 250, "unit": "g"},
            {"name": "mixed berries", "quantity": 80, "unit": "g"},
            {"name": "almonds", "quantity": 15, "unit": "g"},
            {"name": "honey", "quantity": 1, "unit": "tbsp"},
        ],
        "steps": [
            "Spoon half the yogurt into a glass.",
            "Add a layer of berries and almonds.",
            "Repeat with the remaining yogurt, berries, and almonds.",
            "Drizzle with honey and serve.",
        ],
        "tags": ["high-protein", "vegetarian", "quick-meals"],
    },
    {
        "title": "Keto Salmon and Asparagus",
        "description": "Pan-seared salmon with butter-roasted asparagus.",
        "servings": 1,
        "prep_minutes": 10,
        "cook_minutes": 15,
        "calories": 610,
        "protein_g": 38.0,
        "carbs_g": 8.0,
        "fat_g": 45.0,
        "ingredients": [
            {"name": "salmon fillet", "quantity": 200, "unit": "g"},
            {"name": "asparagus", "quantity": 150, "unit": "g"},
            {"name": "butter", "quantity": 1, "unit": "tbsp"},
            {"name": "lemon", "quantity": 1, "unit": "pcs"},
        ],
        "steps": [
            "Pan-sear the salmon skin-side down for 5 minutes, then flip and cook 3 more minutes.",
            "Roast the asparagus in butter for 8-10 minutes.",
            "Squeeze lemon over both before serving.",
        ],
        "tags": ["keto", "gluten-free", "high-protein"],
    },
]

_rotation = itertools.count()


def _extract_target_calories(prompt: str) -> float | None:
    match = re.search(r'[Tt]arget calories[^\d]*(\d+)', prompt)
    return float(match.group(1)) if match else None


class MockProvider:
    def generate_recipe(self, prompt: str) -> str:
        recipe = dict(CANNED_RECIPES[next(_rotation) % len(CANNED_RECIPES)])
        target_calories = _extract_target_calories(prompt)
        if target_calories:
            scale = target_calories / recipe['calories']
            recipe['calories'] = round(recipe['calories'] * scale)
            recipe['protein_g'] = round(recipe['protein_g'] * scale, 1)
            recipe['carbs_g'] = round(recipe['carbs_g'] * scale, 1)
            recipe['fat_g'] = round(recipe['fat_g'] * scale, 1)
        return json.dumps(recipe)


class ClaudeProvider:
    def generate_recipe(self, prompt: str) -> str:
        raise NotImplementedError


_CODE_FENCE_RE = re.compile(r'^```(?:json)?\s*\n(.*)\n```\s*$', re.DOTALL)


class GeminiProvider:
    def generate_recipe(self, prompt: str) -> str:
        try:
            # Default SDK behavior retries a failing call several times with backoff,
            # which turns one bad request into a handful of billed API calls. Since
            # generate_and_save_recipe already surfaces failures to the user directly,
            # fail fast instead: one attempt, no retries.
            client = genai.Client(
                http_options=types.HttpOptions(
                    timeout=20000,
                    retry_options=types.HttpRetryOptions(attempts=1),
                )
            )
        except ValueError as exc:
            raise ProviderError('Gemini is not configured correctly: missing or invalid API key.') from exc

        try:
            response = client.interactions.create(model=settings.GEMINI_MODEL, input=prompt)
        # client.interactions raises from the private _gaos.lib.compat_errors module, not
        # the public google.genai.errors module - confirmed by triggering a real API error.
        except (genai_errors.APIError, genai_errors.NoResponseError) as exc:
            raise ProviderError(f'Gemini request failed: {exc}') from exc

        if not response.output_text:
            raise ProviderError('Gemini returned an empty response.')

        # Gemini wraps JSON in a markdown code fence despite the "only JSON" instruction.
        fence_match = _CODE_FENCE_RE.match(response.output_text.strip())
        return fence_match.group(1) if fence_match else response.output_text


def get_provider() -> RecipeProvider:
    if settings.AI_PROVIDER == 'gemini':
        return GeminiProvider()
    if settings.AI_PROVIDER == 'claude':
        return ClaudeProvider()
    return MockProvider()
