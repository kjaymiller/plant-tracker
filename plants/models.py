# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import gettext_lazy as _


class PlantTypes(models.Model):
    scientific_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "plant_types"
        verbose_name_plural = "Plant Types"


class Plants(models.Model):
    name = models.TextField(blank=True, null=True)
    scientific_name = models.ForeignKey(
        PlantTypes,
        models.DO_NOTHING,
        db_column="scientific_name",
        blank=True,
        null=True,
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "plants"


class Events(models.Model):

    class EventType(models.TextChoices):
        WATERING = "watering", _("watering")
        REPOT = "repot", _("repot")
        ENVIRONMENT_CHANGE = "environment change", _("environment change")
        CUTTINGS = "cuttings", _("cuttings")

    plant = models.ForeignKey("Plants", models.CASCADE, related_name="events")
    datetime = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20, choices=EventType)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "events"
        ordering = ["-datetime"]


class HealthCheckin(models.Model):

    class HealthStatus(models.TextChoices):
        DEAD = "dead", _("dead")
        WORSENING = "worsening", _("worsening")
        BAD = "bad", _("bad")
        IMPROVING = "improving", _("improving")
        HEALTHY = "healthy", _("healthy")
        THRIVING = "thriving", _("thriving")

    plant = models.ForeignKey("Plants", models.CASCADE, related_name="health_checkins")
    datetime = models.DateTimeField(auto_now_add=True)
    health_status = models.CharField(
        max_length=10, choices=HealthStatus, default=HealthStatus.HEALTHY
    )
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "health_checkin"
        ordering = ["-datetime"]
        verbose_name_plural = "Health Check-ins"


class Images(models.Model):
    plant = models.ForeignKey(
        "Plants", models.CASCADE, related_name="images", db_column="plant"
    )
    image_path = models.CharField(max_length=255, db_column="filename")
    caption = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_column="datetime")

    class Meta:
        managed = False
        db_table = "images"
        ordering = ["-uploaded_at"]
