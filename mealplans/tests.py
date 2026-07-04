from django.contrib.auth.models import User
from django.test import TestCase

from mealplans.models import PlanEntry, WeeklyPlan
from mealplans.services import EmptyRecipeLibraryError, generate_plan_entries, plan_adherence_pct, plan_slot_targets
from recipes.models import Recipe


class MealPlanGenerationTests(TestCase):
    def test_generate_plan_entries_matches_meal_types_and_slot_targets(self):
        owner = User.objects.create_user(username='planner', password='secret123')
        plan = WeeklyPlan.objects.create(
            owner=owner,
            name='Week 1',
            start_date='2026-01-01',
            target_calories=2000,
            target_protein_g=150,
            target_carbs_g=200,
            target_fat_g=70,
        )
        Recipe.objects.create(
            owner=owner,
            title='Breakfast Bowl',
            description='Good breakfast',
            meal_type='breakfast',
            servings=1,
            prep_minutes=5,
            cook_minutes=5,
            calories=400,
            protein_g=20,
            carbs_g=40,
            fat_g=10,
            steps=[],
            source=Recipe.Source.MANUAL,
        )
        Recipe.objects.create(
            owner=owner,
            title='Lunch Bowl',
            description='Good lunch',
            meal_type='lunch',
            servings=1,
            prep_minutes=5,
            cook_minutes=10,
            calories=500,
            protein_g=25,
            carbs_g=50,
            fat_g=15,
            steps=[],
            source=Recipe.Source.MANUAL,
        )
        Recipe.objects.create(
            owner=owner,
            title='Dinner Bowl',
            description='Good dinner',
            meal_type='dinner',
            servings=1,
            prep_minutes=5,
            cook_minutes=15,
            calories=700,
            protein_g=30,
            carbs_g=60,
            fat_g=20,
            steps=[],
            source=Recipe.Source.MANUAL,
        )

        generate_plan_entries(plan)

        self.assertEqual(plan.entries.count(), 21)
        self.assertFalse(plan.entries.filter(meal_slot='snack').exists())
        for entry in plan.entries.all():
            self.assertEqual(entry.recipe.meal_type, entry.meal_slot)

        targets = plan_slot_targets(plan, 'lunch')
        self.assertEqual(targets['calories'], 700)
        self.assertEqual(targets['protein_g'], 52.5)

    def test_plan_adherence_percentage_is_based_on_completed_entries(self):
        owner = User.objects.create_user(username='adherent', password='secret123')
        plan = WeeklyPlan.objects.create(owner=owner, name='Week 2', start_date='2026-01-01', target_calories=1800)
        recipe = Recipe.objects.create(
            owner=owner,
            title='Meal',
            description='A meal',
            meal_type='lunch',
            servings=1,
            prep_minutes=5,
            cook_minutes=5,
            calories=400,
            protein_g=20,
            carbs_g=40,
            fat_g=10,
            steps=[],
            source=Recipe.Source.MANUAL,
        )
        PlanEntry.objects.create(plan=plan, day=0, meal_slot='lunch', recipe=recipe)
        PlanEntry.objects.create(plan=plan, day=1, meal_slot='lunch', recipe=recipe, completed=True)

        self.assertEqual(plan_adherence_pct(plan), 50)

    def test_generate_plan_entries_requires_at_least_one_recipe(self):
        owner = User.objects.create_user(username='empty', password='secret123')
        plan = WeeklyPlan.objects.create(owner=owner, name='Week 3', start_date='2026-01-01', target_calories=1800)

        with self.assertRaises(EmptyRecipeLibraryError):
            generate_plan_entries(plan)
