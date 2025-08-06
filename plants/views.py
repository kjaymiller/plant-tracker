from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Plants, PlantTypes
from .forms import PlantForm


def home(request):
    plant_count = Plants.objects.count()
    return render(request, 'plants/home.html', {'plant_count': plant_count})


class PlantListView(ListView):
    model = Plants
    template_name = 'plants/plant_list.html'
    context_object_name = 'plants'
    paginate_by = 20

    def get_queryset(self):
        return Plants.objects.select_related('scientific_name').all()


class PlantDetailView(DetailView):
    model = Plants
    template_name = 'plants/plant_detail.html'
    context_object_name = 'plant'

    def get_queryset(self):
        return Plants.objects.select_related('scientific_name').all()


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
