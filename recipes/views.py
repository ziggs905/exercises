from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Recipe


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
