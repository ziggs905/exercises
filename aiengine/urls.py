from django.urls import path

from . import views

urlpatterns = [
    path('generate-recipe/', views.generate_recipe, name='generate_recipe'),
]
