from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.models import Recipe


class WeeklyPlan(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_plans')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    target_calories = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PlanEntry(models.Model):
    class MealSlot(models.TextChoices):
        BREAKFAST = 'breakfast', 'Breakfast'
        LUNCH = 'lunch', 'Lunch'
        DINNER = 'dinner', 'Dinner'
        SNACK = 'snack', 'Snack'

    plan = models.ForeignKey(WeeklyPlan, on_delete=models.CASCADE, related_name='entries')
    day = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])
    meal_slot = models.CharField(max_length=10, choices=MealSlot.choices)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.plan.name} — day {self.day} {self.meal_slot}: {self.recipe.title}'
