from django import forms
from .models import Plant, PlantMaintenance, PlantGarden, Garden, Comments


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


class GardenAddForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = [
            'name',
            # 'plants',
            # 'user',
        ]


class PlantSearchForm(forms.Form):
    query = forms.CharField(label='Wyszukaj roślinę', max_length=100)


class PlantToGardenAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Fetching the passed attributes
        date_input_type = kwargs.pop('date_input_type', None)
        super().__init__(*args, **kwargs)
        # Nonstandatd widget for date fiels
        if date_input_type:
            self.fields['start_date'].widget.input_type = date_input_type

    class Meta:
        model = PlantGarden
        fields = ['garden', 'plant', 'start_date', 'location']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
