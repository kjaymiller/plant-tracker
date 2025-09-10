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
    path('<int:plant_id>/upload-image/', views.upload_plant_image, name='upload-plant-image'),
    path('image/<int:pk>/edit/', views.ImageUpdateView.as_view(), name='image-update'),
    path('image/<int:pk>/delete/', views.ImageDeleteView.as_view(), name='image-delete'),
    path('image/<int:image_id>/update-caption/', views.update_image_caption, name='update-image-caption'),
    path('health-checkin/<int:pk>/delete/', views.HealthCheckinDeleteView.as_view(), name='health-checkin-delete'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('health-checkin/<int:checkin_id>/quick-delete/', views.delete_health_checkin, name='quick-delete-health-checkin'),
    path('event/<int:event_id>/quick-delete/', views.delete_event, name='quick-delete-event'),
]