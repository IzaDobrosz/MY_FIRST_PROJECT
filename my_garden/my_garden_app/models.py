from django.db import models

class Plant(models.Model):
    SUNLIGHT_EXPOSURE_CHOICES = [
        (1, 'Pełne słońce'),
        (2, 'Częściowy cień'),
        (3, 'Cień')
    ]

    PRUNING_FREQUENCY_CHOICES = [
        (1, 'Regularne'),
        (2, 'Okazjonalne')
    ]

    WATERING_NEEDS_CHOICES = [
        (1, 'Niskie'),
        (2, 'Umiarkowane'),
        (3, 'Wysokie')
    ]

    FERTILIZATION_CHOICES = [
        (1, 'Regularne'),
        (2, 'Okazjonalne')
    ]

    PEST_DISEASE_RESISTANCE_CHOICES = [
        (1, 'Odporny'),
        (2, 'Podatny')
    ]

    MAXIMUM_HEIGHT_CHOICES = [
        (1, 'Wysoka'),
        (2, 'Średnia'),
        (3, 'Niska')
    ]

    SPREAD_CHOICES = [
        (1, 'Szeroka'),
        (2, 'Średnia'),
        (3, 'Kompaktowa')
    ]

    FLOWERING_SEASON_CHOICES = [
        (1, 'Wiosna'),
        (2, 'Lato'),
        (3, 'Jesień'),
        (4, 'Brak')
    ]

    name = models.CharField(max_length=100, verbose_name="Nazwa")
    description = models.TextField(verbose_name="Opis")
    max_height = models.IntegerField(choices=MAXIMUM_HEIGHT_CHOICES, verbose_name="Wysokość_max")
    spread = models.IntegerField(choices=SPREAD_CHOICES, verbose_name="Rozpiętość")
    flowering_season = models.IntegerField(choices=FLOWERING_SEASON_CHOICES, verbose_name="Sezon kwitnienia")
    sunlight_exposure = models.IntegerField(choices=SUNLIGHT_EXPOSURE_CHOICES, verbose_name="Nasłonecznienie")
    pruning_frequency = models.IntegerField(choices=PRUNING_FREQUENCY_CHOICES, verbose_name="Częstotliwość przycinania")
    watering_needs = models.IntegerField(choices=WATERING_NEEDS_CHOICES, verbose_name="Potrzeba podlewania")
    fertilization = models.IntegerField(choices=FERTILIZATION_CHOICES, verbose_name="Nawożenie")
    pest_disease_resistance = models.IntegerField(choices=PEST_DISEASE_RESISTANCE_CHOICES, verbose_name="Odporność na szkodniki i choroby")

    def __str__(self):
        return self.name


class PlantMaintenance(models.Model):
    TASK_CHOICES = [
        (1, 'Przycinanie'),
        (2, 'Nawożenie'),
    ]

    WEEK_OF_MONTH_CHOICES = [
        (1, 'Pierwszy'),
        (2, 'Drugi'),
        (3, 'Trzeci'),
        (4, 'Czwarty'),
        (5, 'Ostatni')
    ]

    MONTH_CHOICES = [
        (1, 'Styczeń'),
        (2, 'Luty'),
        (3, 'Marzec'),
        (4, 'Kwiecień'),
        (5, 'Maj'),
        (6, 'Czerwiec'),
        (7, 'Lipiec'),
        (8, 'Sierpień'),
        (9, 'Wrzesień'),
        (10, 'Październik'),
        (11, 'Listopad'),
        (12, 'Grudzień')
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="Nazwa")
    task = models.IntegerField(choices=TASK_CHOICES, verbose_name="Zadanie")
    task_description = models.TextField(verbose_name="Opis")
    week_of_month = models.IntegerField(choices=WEEK_OF_MONTH_CHOICES, verbose_name="Tydzień")
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name="Miesiąc")

    def __str__(self):
        task_name = dict(self.TASK_CHOICES).get(self.task)
        return f"{task_name} - {self.plant.name}"

