from django.contrib.auth.models import User
from django.db import models

from recipes.models import Recipe


class Cookbook(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cookbooks')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, blank=True, related_name='cookbooks')

    def __str__(self):
        return self.name
