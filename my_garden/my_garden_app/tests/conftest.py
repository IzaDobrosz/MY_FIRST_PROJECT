import pytest
from django.test import Client

from my_garden_app.models import Plant

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def plant():
    return Plant.objects.create(
        name='test_plant1',
        description='test_plant1 description',
        max_height=1,
        spread=2,
        flowering_season=2,
        sunlight_exposure=3,
        pruning_frequency=1,
        watering_needs=1,
        fertilization=1,
        pest_disease_resistance=1
        )


@pytest.fixture
def plants():
    return [
        Plant.objects.create(
        name=f'test_plant{i}',
        description=f'test_plant{i} description',
        max_height=1,
        spread=2,
        flowering_season=2,
        sunlight_exposure=3,
        pruning_frequency=1,
        watering_needs=1,
        fertilization=1,
        pest_disease_resistance=1
        ) for i in range(1, 4)
    ]

