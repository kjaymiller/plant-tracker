from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from pathlib import Path
import shutil
import uuid
from datetime import datetime
from .models import Plants, PlantTypes, HealthCheckin, Events, Images
from .forms import PlantForm, HealthCheckinForm, EventForm, ImageForm


def home(request):
    plant_count = Plants.objects.count()
    
    # Get recent activities
    recent_images = Images.objects.select_related('plant').all()[:10]
    recent_health_checks = HealthCheckin.objects.select_related('plant').all()[:10]
    recent_events = Events.objects.select_related('plant').all()[:10]
    
    # Combine all activities into a single list with type info
    activities = []
    
    for image in recent_images:
        activities.append({
            'type': 'image',
            'datetime': image.uploaded_at,
            'plant': image.plant,
            'data': image,
            'icon': 'camera',
            'title': f'Image added for {image.plant.name}',
            'description': image.caption or 'New image uploaded'
        })
    
    for health_check in recent_health_checks:
        activities.append({
            'type': 'health_check',
            'datetime': health_check.datetime,
            'plant': health_check.plant,
            'data': health_check,
            'icon': 'heart',
            'title': f'Health check for {health_check.plant.name}',
            'description': f'Status: {health_check.get_health_status_display()}'
        })
    
    for event in recent_events:
        activities.append({
            'type': 'event',
            'datetime': event.datetime,
            'plant': event.plant,
            'data': event,
            'icon': 'calendar',
            'title': f'{event.get_event_type_display().title()} for {event.plant.name}',
            'description': event.comments or f'{event.get_event_type_display().title()} event'
        })
    
    # Sort activities by datetime (most recent first)
    activities.sort(key=lambda x: x['datetime'], reverse=True)
    
    # Take only the most recent 15 activities
    recent_activities = activities[:15]
    
    return render(request, 'plants/home.html', {
        'plant_count': plant_count,
        'recent_activities': recent_activities
    })


class PlantListView(ListView):
    model = Plants
    template_name = 'plants/plant_list.html'
    context_object_name = 'plants'
    paginate_by = 20

    def get_queryset(self):
        return Plants.objects.select_related('scientific_name').prefetch_related('images', 'health_checkins', 'events').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add latest image, health status, and recent events for each plant
        plants = context.get('plants', [])
        for plant in plants:
            plant.latest_image = plant.images.first()
            plant.latest_health = plant.health_checkins.first()
            plant.recent_events = list(plant.events.all()[:3])  # Get last 3 events
        return context


class PlantDetailView(DetailView):
    model = Plants
    template_name = 'plants/plant_detail.html'
    context_object_name = 'plant'

    def get_queryset(self):
        return Plants.objects.select_related('scientific_name').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.get_object()
        context['latest_health_status'] = plant.health_checkins.first()
        context['recent_events'] = plant.events.all()[:5]
        context['images'] = plant.images.all()[:10]
        context['health_form'] = HealthCheckinForm()
        context['event_form'] = EventForm()
        context['image_form'] = ImageForm()
        return context


class PlantCreateView(CreateView):
    model = Plants
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    success_url = reverse_lazy('plant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Plant'
        return context


class PlantUpdateView(UpdateView):
    model = Plants
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    success_url = reverse_lazy('plant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Plant'
        return context


class PlantDeleteView(DeleteView):
    model = Plants
    template_name = 'plants/plant_confirm_delete.html'
    success_url = reverse_lazy('plant-list')
    context_object_name = 'plant'


def plant_name_autocomplete(request):
    query = request.GET.get('plant_name_search', '')
    if len(query) < 2:
        return render(request, 'plants/autocomplete_results.html', {'results': []})
    
    # Search in PlantTypes scientific names
    plant_types = PlantTypes.objects.filter(
        scientific_name__icontains=query
    ).distinct()[:10]
    
    results = []
    for plant_type in plant_types:
        results.append({
            'id': plant_type.id,
            'name': plant_type.scientific_name,
            'type': 'existing'
        })
    
    # If less than 10 results and query is substantial, offer to create new
    if len(results) < 10 and len(query) >= 3:
        results.append({
            'id': 'create_new',
            'name': f'Create new: "{query}"',
            'type': 'create',
            'value': query
        })
    
    return render(request, 'plants/autocomplete_results.html', {'results': results, 'query': query})


@require_POST
def create_plant_type(request):
    scientific_name = request.POST.get('scientific_name', '').strip()
    
    if not scientific_name:
        return JsonResponse({'error': 'Scientific name is required'}, status=400)
    
    # Check if plant type already exists
    existing_plant_type = PlantTypes.objects.filter(scientific_name__iexact=scientific_name).first()
    if existing_plant_type:
        return JsonResponse({
            'success': True,
            'plant_type': {
                'id': existing_plant_type.id,
                'scientific_name': existing_plant_type.scientific_name
            },
            'message': 'Plant type already exists'
        })
    
    # Create new plant type
    try:
        new_plant_type = PlantTypes.objects.create(scientific_name=scientific_name)
        return JsonResponse({
            'success': True,
            'plant_type': {
                'id': new_plant_type.id,
                'scientific_name': new_plant_type.scientific_name
            },
            'message': 'Plant type created successfully'
        })
    except Exception as e:
        return JsonResponse({'error': f'Failed to create plant type: {str(e)}'}, status=500)


@require_POST
def create_health_checkin(request, plant_id):
    plant = get_object_or_404(Plants, pk=plant_id)
    form = HealthCheckinForm(request.POST)
    
    if form.is_valid():
        health_checkin = form.save(commit=False)
        health_checkin.plant = plant
        health_checkin.save()
        return JsonResponse({
            'success': True,
            'message': 'Health check-in recorded successfully',
            'health_status': health_checkin.get_health_status_display(),
            'datetime': health_checkin.datetime.strftime('%B %d, %Y at %I:%M %p')
        })
    else:
        return JsonResponse({'error': 'Invalid form data', 'errors': form.errors}, status=400)


@require_POST
def create_event(request, plant_id):
    plant = get_object_or_404(Plants, pk=plant_id)
    form = EventForm(request.POST)
    
    if form.is_valid():
        event = form.save(commit=False)
        event.plant = plant
        event.save()
        return JsonResponse({
            'success': True,
            'message': 'Event logged successfully',
            'event_type': event.get_event_type_display(),
            'datetime': event.datetime.strftime('%B %d, %Y at %I:%M %p')
        })
    else:
        return JsonResponse({'error': 'Invalid form data', 'errors': form.errors}, status=400)


@require_POST
def quick_health_update(request, plant_id):
    plant = get_object_or_404(Plants, pk=plant_id)
    health_status = request.POST.get('health_status')
    
    if health_status and health_status in [choice[0] for choice in HealthCheckin.HealthStatus.choices]:
        health_checkin = HealthCheckin.objects.create(
            plant=plant,
            health_status=health_status
        )
        return JsonResponse({
            'success': True,
            'message': 'Health status updated successfully',
            'health_status': health_checkin.get_health_status_display()
        })
    else:
        return JsonResponse({'error': 'Invalid health status'}, status=400)


@require_POST
def upload_plant_image(request, plant_id):
    plant = get_object_or_404(Plants, pk=plant_id)
    form = ImageForm(request.POST, request.FILES)
    
    if form.is_valid() and 'image_file' in request.FILES:
        image_file = request.FILES['image_file']
        
        # Create media directory using pathlib
        media_root = Path(settings.MEDIA_ROOT)
        plant_dir = media_root / 'plants' / str(plant_id)
        plant_dir.mkdir(parents=True, exist_ok=True)
        
        # Save the file with a unique name using pathlib
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = Path(image_file.name).suffix
        filename = f"{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"
        file_path = plant_dir / filename
        
        # Save the file using shutil
        with file_path.open('wb') as destination:
            shutil.copyfileobj(image_file, destination)
        
        # Create database record with relative path
        relative_path = Path('plants') / str(plant_id) / filename
        image = form.save(commit=False)
        image.plant = plant
        image.image_path = str(relative_path)
        image.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Image uploaded successfully',
            'image_url': f"{settings.MEDIA_URL}{relative_path}",
            'image_id': image.id
        })
    else:
        return JsonResponse({'error': 'Invalid form data or no image file', 'errors': form.errors}, status=400)


class ImageUpdateView(UpdateView):
    model = Images
    form_class = ImageForm
    template_name = 'plants/image_form.html'
    context_object_name = 'image'

    def get_success_url(self):
        return reverse_lazy('plant-detail', kwargs={'pk': self.object.plant.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Image'
        context['plant'] = self.object.plant
        return context


class ImageDeleteView(DeleteView):
    model = Images
    template_name = 'plants/image_confirm_delete.html'
    context_object_name = 'image'

    def get_success_url(self):
        return reverse_lazy('plant-detail', kwargs={'pk': self.object.plant.pk})

    def delete(self, request, *args, **kwargs):
        image = self.get_object()
        
        # Delete the physical file
        media_root = Path(settings.MEDIA_ROOT)
        file_path = media_root / image.image_path
        if file_path.exists():
            file_path.unlink()
        
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plant'] = self.object.plant
        return context


@require_POST
def update_image_caption(request, image_id):
    image = get_object_or_404(Images, pk=image_id)
    caption = request.POST.get('caption', '').strip()
    
    image.caption = caption
    image.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Caption updated successfully',
        'caption': image.caption
    })
