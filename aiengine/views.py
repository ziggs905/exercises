from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile
from nutrition.services import compute_daily_targets, profile_is_complete
from recipes.models import Ingredient, Recipe, Tag

from .forms import GenerateRecipeForm
from .parsing import RecipeParseError, parse_recipe
from .prompts import build_recipe_prompt
from .providers import get_provider


@login_required
def generate_recipe(request):
    profile = Profile.objects.filter(user=request.user).first()
    targets = compute_daily_targets(profile) if profile_is_complete(profile) else None
    error = None
    form = GenerateRecipeForm(request.POST or None)

    if request.method == 'POST' and targets and form.is_valid():
        prompt = build_recipe_prompt(profile, targets, form.cleaned_data['preferences'])
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
        'form': form, 'targets': targets, 'error': error,
    })
