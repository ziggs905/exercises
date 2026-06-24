import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import IngredientFormSet, NotesForm, RecipeForm, RecipeSearchForm
from .models import Recipe


@login_required
def recipe_list(request):
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.filter(owner=request.user)
    sort = '-created_at'

    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            recipes = recipes.filter(
                Q(title__icontains=q) | Q(ingredients__name__icontains=q)
            ).distinct()

        tags = form.cleaned_data.get('tags')
        if tags:
            recipes = recipes.filter(tags__in=tags).distinct()

        max_calories = form.cleaned_data.get('max_calories')
        if max_calories is not None:
            recipes = recipes.filter(calories__lte=max_calories)

        min_protein = form.cleaned_data.get('min_protein')
        if min_protein is not None:
            recipes = recipes.filter(protein_g__gte=min_protein)

        if form.cleaned_data.get('favorites_only'):
            recipes = recipes.filter(is_favorite=True)

        sort = form.cleaned_data.get('sort') or sort

    recipes = recipes.order_by(sort)

    return render(request, 'recipes/recipe_list.html', {'form': form, 'recipes': recipes})


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    notes_form = NotesForm(instance=recipe)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'notes_form': notes_form})


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = IngredientFormSet(request.POST, instance=Recipe())
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.source = Recipe.Source.MANUAL
            recipe.save()
            form.save_m2m()
            formset.instance = recipe
            formset.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = IngredientFormSet(instance=Recipe())
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset, 'recipe': recipe})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


@login_required
def recipe_update_notes(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
    return redirect('recipe_detail', pk=recipe.pk)


@login_required
@require_POST
def recipe_toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    recipe.is_favorite = not recipe.is_favorite
    recipe.save(update_fields=['is_favorite'])
    return JsonResponse({'is_favorite': recipe.is_favorite})


@login_required
@require_POST
def recipe_set_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    try:
        rating = int(json.loads(request.body).get('rating'))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid rating'}, status=400)
    if rating not in range(1, 6):
        return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
    recipe.rating = rating
    recipe.save(update_fields=['rating'])
    return JsonResponse({'rating': recipe.rating})
