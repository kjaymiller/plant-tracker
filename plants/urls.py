from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlantListView.as_view(), name='plant-list'),
    path('<int:pk>/', views.PlantDetailView.as_view(), name='plant-detail'),
    path('create/', views.PlantCreateView.as_view(), name='plant-create'),
    path('<int:pk>/edit/', views.PlantUpdateView.as_view(), name='plant-update'),
    path('<int:pk>/delete/', views.PlantDeleteView.as_view(), name='plant-delete'),
    path('api/plant-name-autocomplete/', views.plant_name_autocomplete, name='plant-name-autocomplete'),
    path('api/create-plant-type/', views.create_plant_type, name='create-plant-type'),
]