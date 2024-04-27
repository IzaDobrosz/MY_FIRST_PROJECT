from django import forms
from .models import Plant, PlantMaintenance


class PlantAddForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = (
            "name",
            "description",
            "max_height",
            "spread",
            "flowering_season",
            "sunlight_exposure",
            "pruning_frequency",
            "watering_needs",
            "fertilization",
            "pest_disease_resistance"
        )


class PlantEditForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = (
            "name",
            "description",
            "max_height",
            "spread",
            "flowering_season",
            "sunlight_exposure",
            "pruning_frequency",
            "watering_needs",
            "fertilization",
            "pest_disease_resistance"
        )

class PlantMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PlantMaintenance
        fields = [
            'plant',
            'task',
            'task_description',
            'week_of_month',
            'month'
        ]
