from django.contrib import admin

from .models import PlantTypes, Plants


@admin.register(PlantTypes)
class PlantTypesAdmin(admin.ModelAdmin):
    list_display = ["id", "scientific_name"]
    search_fields = ["scientific_name"]


@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "scientific_name"]
    search_fields = ["name"]
    list_filter = ["scientific_name"]
