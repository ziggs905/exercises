from django.urls import path

from . import views

urlpatterns = [
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/new/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipes/<int:pk>/favorite/', views.recipe_toggle_favorite, name='recipe_toggle_favorite'),
    path('recipes/<int:pk>/rate/', views.recipe_set_rating, name='recipe_set_rating'),
    path('recipes/<int:pk>/notes/', views.recipe_update_notes, name='recipe_update_notes'),
]
