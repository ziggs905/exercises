from django.urls import path

from . import views

urlpatterns = [
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
]
