from recipes.models import Recipe

from .models import PlanEntry

SLOT_SPLIT = {
    'breakfast': 0.25,
    'lunch': 0.35,
    'dinner': 0.30,
    'snack': 0.10,
}

DAYS = range(7)


class EmptyRecipeLibraryError(Exception):
    pass


def generate_plan_entries(plan):
    """Greedily fill a WeeklyPlan's 7x4 grid from the owner's recipe library."""
    recipes = list(Recipe.objects.filter(owner=plan.owner))
    if not recipes:
        raise EmptyRecipeLibraryError('Generate some recipes first, then create a plan.')

    entries = []
    for day in DAYS:
        used_today = set()
        for slot, fraction in SLOT_SPLIT.items():
            slot_target = plan.target_calories * fraction
            candidates = [r for r in recipes if r.pk not in used_today] or recipes
            recipe = min(candidates, key=lambda r: abs(r.calories - slot_target))
            used_today.add(recipe.pk)
            entries.append(PlanEntry(plan=plan, day=day, meal_slot=slot, recipe=recipe))

    PlanEntry.objects.bulk_create(entries)
