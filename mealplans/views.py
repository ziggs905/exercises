from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from nutrition.services import compute_daily_targets, profile_is_complete

from .forms import SwapRecipeForm, WeeklyPlanForm
from .models import WeeklyPlan
from .services import EmptyRecipeLibraryError, generate_plan_entries

DAYS = range(7)
DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MEAL_SLOTS = ['breakfast', 'lunch', 'dinner', 'snack']


@login_required
def plan_list(request):
    plans = WeeklyPlan.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'mealplans/plan_list.html', {'plans': plans})


@login_required
def plan_create(request):
    profile = Profile.objects.filter(user=request.user).first()
    error = None

    if not profile_is_complete(profile):
        error = 'Complete your profile before creating a meal plan.'
        form = WeeklyPlanForm()
    elif request.method == 'POST':
        form = WeeklyPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.owner = request.user
            plan.target_calories = compute_daily_targets(profile)['calories']
            plan.save()
            try:
                generate_plan_entries(plan)
            except EmptyRecipeLibraryError as exc:
                plan.delete()
                error = str(exc)
            else:
                return redirect('plan_detail', pk=plan.pk)
    else:
        form = WeeklyPlanForm()

    return render(request, 'mealplans/plan_form.html', {'form': form, 'error': error})


@login_required
def plan_detail(request, pk):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    entries = list(plan.entries.select_related('recipe'))
    for entry in entries:
        entry.swap_form = SwapRecipeForm(instance=entry, owner=request.user)

    grid = {day: {} for day in DAYS}
    day_totals = {day: 0 for day in DAYS}
    for entry in entries:
        grid[entry.day][entry.meal_slot] = entry
        day_totals[entry.day] += entry.recipe.calories

    days = [
        {
            'name': DAY_NAMES[day],
            'slots': [grid[day].get(slot) for slot in MEAL_SLOTS],
            'total': day_totals[day],
        }
        for day in DAYS
    ]

    return render(request, 'mealplans/plan_detail.html', {
        'plan': plan, 'days': days, 'meal_slots': MEAL_SLOTS,
    })


@login_required
def plan_delete(request, pk):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    if request.method == 'POST':
        plan.delete()
        return redirect('plan_list')
    return render(request, 'mealplans/plan_confirm_delete.html', {'plan': plan})


@login_required
def plan_entry_swap(request, pk, entry_pk):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    entry = get_object_or_404(plan.entries, pk=entry_pk)
    if request.method == 'POST':
        form = SwapRecipeForm(request.POST, instance=entry, owner=request.user)
        if form.is_valid():
            form.save()
    return redirect('plan_detail', pk=plan.pk)
