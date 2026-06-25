from django.urls import path

from . import views

urlpatterns = [
    path('cookbooks/', views.cookbook_list, name='cookbook_list'),
    path('cookbooks/new/', views.cookbook_create, name='cookbook_create'),
    path('cookbooks/<int:pk>/', views.cookbook_detail, name='cookbook_detail'),
    path('cookbooks/<int:pk>/delete/', views.cookbook_delete, name='cookbook_delete'),
    path(
        'cookbooks/<int:pk>/remove-recipe/<int:recipe_pk>/',
        views.cookbook_remove_recipe,
        name='cookbook_remove_recipe',
    ),
    path('recipes/<int:recipe_pk>/add-to-cookbook/', views.add_recipe_to_cookbook, name='recipe_add_to_cookbook'),
]
