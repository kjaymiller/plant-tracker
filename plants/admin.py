from django.contrib import admin

from .models import PlantTypes, Devices, Plants, MoistureLogs, PlantDeviceRegistration


@admin.register(PlantTypes)
class PlantTypesAdmin(admin.ModelAdmin):
    list_display = ["id", "scientific_name"]
    search_fields = ["scientific_name"]


@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    list_display = ["id", "hostname", "location"]
    search_fields = ["hostname", "location"]


@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "scientific_name"]
    search_fields = ["name"]
    list_filter = ["scientific_name"]


@admin.register(MoistureLogs)
class MoistureLogsAdmin(admin.ModelAdmin):
    list_display = ["id", "datetime", "moisture_data"]
    list_filter = ["datetime"]
    ordering = ["-datetime"]


@admin.register(PlantDeviceRegistration)
class PlantDeviceRegistrationAdmin(admin.ModelAdmin):
    list_display = ["id", "plant", "device", "registered_at", "is_active"]
    list_filter = ["is_active", "registered_at"]
    search_fields = ["plant__name", "device__hostname"]
