from django.contrib.auth.models import User
from django.test import TestCase

from mealplans.models import PlanEntry, WeeklyPlan
from recipes.models import Ingredient, Recipe
from shopping.services import generate_shopping_list


class ShoppingListGenerationTests(TestCase):
    def test_generate_shopping_list_aggregates_duplicate_ingredients(self):
        owner = User.objects.create_user(username='shopper', password='secret123')
        plan = WeeklyPlan.objects.create(owner=owner, name='Week 1', start_date='2026-01-01', target_calories=2000)
        recipe_one = Recipe.objects.create(
            owner=owner,
            title='Chicken Bowl',
            description='A bowl',
            meal_type='lunch',
            servings=1,
            prep_minutes=5,
            cook_minutes=10,
            calories=400,
            protein_g=30,
            carbs_g=40,
            fat_g=10,
            steps=[],
            source=Recipe.Source.MANUAL,
        )
        recipe_two = Recipe.objects.create(
            owner=owner,
            title='Salad',
            description='A salad',
            meal_type='dinner',
            servings=1,
            prep_minutes=5,
            cook_minutes=0,
            calories=300,
            protein_g=10,
            carbs_g=20,
            fat_g=10,
            steps=[],
            source=Recipe.Source.MANUAL,
        )
        Ingredient.objects.create(recipe=recipe_one, name='Chicken', quantity=200, unit='g')
        Ingredient.objects.create(recipe=recipe_one, name='Olive Oil', quantity=2, unit='tbsp')
        Ingredient.objects.create(recipe=recipe_two, name='chicken', quantity=50, unit='g')
        Ingredient.objects.create(recipe=recipe_two, name='olive oil', quantity=1, unit='tbsp')
        PlanEntry.objects.create(plan=plan, day=0, meal_slot='lunch', recipe=recipe_one)
        PlanEntry.objects.create(plan=plan, day=1, meal_slot='dinner', recipe=recipe_two)

        shopping_list = generate_shopping_list(owner, plan, 'Monday shopping')

        self.assertEqual(shopping_list.name, 'Monday shopping')
        self.assertEqual(
            {(item.name, item.quantity, item.unit) for item in shopping_list.items.all()},
            {('chicken', 250.0, 'g'), ('olive oil', 3.0, 'tbsp')},
        )
