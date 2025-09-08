from django import forms
from .models import Plants, PlantTypes, HealthCheckin, Events


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plants
        fields = ['name', 'scientific_name', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'Enter plant name'
            }),
            'scientific_name': forms.Select(attrs={
                'class': 'hidden',
                'id': 'id_scientific_name'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'rows': 4,
                'placeholder': 'Add any notes about your plant...'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make scientific_name field not required for validation since we handle it via JavaScript
        self.fields['scientific_name'].required = False
        # Populate choices for the select field
        self.fields['scientific_name'].queryset = PlantTypes.objects.all()


class HealthCheckinForm(forms.ModelForm):
    class Meta:
        model = HealthCheckin
        fields = ['health_status', 'comments']
        widgets = {
            'health_status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'rows': 3,
                'placeholder': 'Optional notes about the plant\'s health...'
            }),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['event_type', 'comments']
        widgets = {
            'event_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'rows': 3,
                'placeholder': 'Optional notes about this event...'
            }),
        }