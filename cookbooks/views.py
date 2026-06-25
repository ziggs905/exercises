from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from recipes.models import Recipe

from .forms import AddToCookbookForm, CookbookForm
from .models import Cookbook


@login_required
def cookbook_list(request):
    cookbooks = Cookbook.objects.filter(owner=request.user).annotate(recipe_count=Count('recipes'))
    return render(request, 'cookbooks/cookbook_list.html', {'cookbooks': cookbooks})


@login_required
def cookbook_create(request):
    if request.method == 'POST':
        form = CookbookForm(request.POST)
        if form.is_valid():
            cookbook = form.save(commit=False)
            cookbook.owner = request.user
            cookbook.save()
            return redirect('cookbook_detail', pk=cookbook.pk)
    else:
        form = CookbookForm()
    return render(request, 'cookbooks/cookbook_form.html', {'form': form})


@login_required
def cookbook_detail(request, pk):
    cookbook = get_object_or_404(Cookbook, pk=pk, owner=request.user)
    return render(request, 'cookbooks/cookbook_detail.html', {'cookbook': cookbook})


@login_required
def cookbook_delete(request, pk):
    cookbook = get_object_or_404(Cookbook, pk=pk, owner=request.user)
    if request.method == 'POST':
        cookbook.delete()
        return redirect('cookbook_list')
    return render(request, 'cookbooks/cookbook_confirm_delete.html', {'cookbook': cookbook})


@login_required
@require_POST
def cookbook_remove_recipe(request, pk, recipe_pk):
    cookbook = get_object_or_404(Cookbook, pk=pk, owner=request.user)
    recipe = get_object_or_404(Recipe, pk=recipe_pk, owner=request.user)
    cookbook.recipes.remove(recipe)
    return redirect('cookbook_detail', pk=cookbook.pk)


@login_required
@require_POST
def add_recipe_to_cookbook(request, recipe_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk, owner=request.user)
    form = AddToCookbookForm(request.POST, user=request.user)
    if form.is_valid():
        cookbook = form.cleaned_data.get('cookbook')
        new_name = form.cleaned_data.get('new_cookbook_name', '').strip()
        if not cookbook:
            cookbook = Cookbook.objects.create(owner=request.user, name=new_name)
        cookbook.recipes.add(recipe)
    return redirect('recipe_detail', pk=recipe.pk)
