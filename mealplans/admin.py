from django.contrib import admin

from .models import PlanEntry, WeeklyPlan


class PlanEntryInline(admin.TabularInline):
    model = PlanEntry
    extra = 0


@admin.register(WeeklyPlan)
class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'start_date', 'target_calories', 'created_at']
    inlines = [PlanEntryInline]


@admin.register(PlanEntry)
class PlanEntryAdmin(admin.ModelAdmin):
    list_display = ['plan', 'day', 'meal_slot', 'recipe', 'completed']
