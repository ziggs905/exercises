from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    class ActivityLevel(models.TextChoices):
        SEDENTARY = 'sedentary', 'Sedentary'
        LIGHT = 'light', 'Light'
        MODERATE = 'moderate', 'Moderate'
        ACTIVE = 'active', 'Active'
        VERY_ACTIVE = 'very_active', 'Very active'

    class Goal(models.TextChoices):
        LOSE = 'lose', 'Lose weight'
        MAINTAIN = 'maintain', 'Maintain weight'
        GAIN = 'gain', 'Gain weight'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight_kg = models.FloatField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True)
    activity_level = models.CharField(max_length=20, choices=ActivityLevel.choices, blank=True)
    goal = models.CharField(max_length=10, choices=Goal.choices, blank=True)
    allergies = models.TextField(blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
