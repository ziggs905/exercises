from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile
from nutrition.services import DEFAULT_MEAL_RATIOS, compute_daily_targets, profile_is_complete, slot_targets
from recipes.models import Ingredient, Recipe, Tag

from .forms import GenerateRecipeForm
from .parsing import RecipeParseError, parse_recipe
from .prompts import build_recipe_prompt
from .providers import get_provider


@login_required
def generate_recipe(request):
    profile = Profile.objects.filter(user=request.user).first()
    daily_targets = compute_daily_targets(profile) if profile_is_complete(profile) else None
    meal_targets = None
    if daily_targets:
        meal_targets = {
            meal_type: slot_targets(daily_targets, pct)
            for meal_type, pct in DEFAULT_MEAL_RATIOS.items()
        }
    error = None
    form = GenerateRecipeForm(request.POST or None)

    if request.method == 'POST' and daily_targets and form.is_valid():
        meal_type = form.cleaned_data['meal_type']
        targets = slot_targets(daily_targets, DEFAULT_MEAL_RATIOS[meal_type])
        prompt = build_recipe_prompt(profile, targets, form.cleaned_data['preferences'], meal_type=meal_type)
        raw_json = get_provider().generate_recipe(prompt)
        try:
            data = parse_recipe(raw_json)
        except RecipeParseError as exc:
            error = str(exc)
        else:
            recipe = Recipe.objects.create(
                owner=request.user,
                title=data['title'],
                description=data['description'],
                meal_type=meal_type,
                servings=data['servings'],
                prep_minutes=data['prep_minutes'],
                cook_minutes=data['cook_minutes'],
                calories=data['calories'],
                protein_g=data['protein_g'],
                carbs_g=data['carbs_g'],
                fat_g=data['fat_g'],
                steps=data['steps'],
                source=Recipe.Source.AI,
            )
            Ingredient.objects.bulk_create(
                Ingredient(recipe=recipe, **item) for item in data['ingredients']
            )
            if data['tags']:
                recipe.tags.set(Tag.objects.filter(slug__in=data['tags']))
            return redirect('recipe_detail', pk=recipe.pk)

    return render(request, 'aiengine/generate_recipe.html', {
        'form': form, 'meal_targets': meal_targets, 'error': error,
    })
