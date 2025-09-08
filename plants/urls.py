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
    path('<int:plant_id>/health-checkin/', views.create_health_checkin, name='create-health-checkin'),
    path('<int:plant_id>/event/', views.create_event, name='create-event'),
    path('<int:plant_id>/quick-health/', views.quick_health_update, name='quick-health-update'),
]