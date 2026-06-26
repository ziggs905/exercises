from django.urls import path

from . import views

urlpatterns = [
    path('mealplans/', views.plan_list, name='plan_list'),
    path('mealplans/new/', views.plan_create, name='plan_create'),
    path('mealplans/<int:pk>/', views.plan_detail, name='plan_detail'),
    path('mealplans/<int:pk>/delete/', views.plan_delete, name='plan_delete'),
    path('mealplans/<int:pk>/entries/<int:entry_pk>/swap/', views.plan_entry_swap, name='plan_entry_swap'),
]
