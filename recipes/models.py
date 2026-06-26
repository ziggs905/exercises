from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Tag(models.Model):
    class Category(models.TextChoices):
        DIETARY = 'dietary', 'Dietary'
        PRACTICAL = 'practical', 'Practical'
        NUTRITIONAL = 'nutritional', 'Nutritional'

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    class Source(models.TextChoices):
        AI = 'ai', 'AI-generated'
        MANUAL = 'manual', 'Manual'

    class MealType(models.TextChoices):
        BREAKFAST = 'breakfast', 'Breakfast'
        LUNCH = 'lunch', 'Lunch'
        DINNER = 'dinner', 'Dinner'
        SNACK = 'snack', 'Snack'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    meal_type = models.CharField(max_length=10, choices=MealType.choices, default=MealType.LUNCH)
    servings = models.PositiveIntegerField()
    prep_minutes = models.PositiveIntegerField()
    cook_minutes = models.PositiveIntegerField()
    calories = models.PositiveIntegerField()
    protein_g = models.FloatField()
    carbs_g = models.FloatField()
    fat_g = models.FloatField()
    steps = models.JSONField(default=list)
    source = models.CharField(max_length=10, choices=Source.choices)
    is_favorite = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    notes = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    class Unit(models.TextChoices):
        GRAM = 'g', 'g'
        MILLILITER = 'ml', 'ml'
        PIECE = 'pcs', 'pcs'
        TABLESPOON = 'tbsp', 'tbsp'
        TEASPOON = 'tsp', 'tsp'

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=Unit.choices)

    def __str__(self):
        return f'{self.quantity} {self.unit} {self.name}'
