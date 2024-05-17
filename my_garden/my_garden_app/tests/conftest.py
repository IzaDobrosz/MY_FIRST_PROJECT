import pytest
from django.contrib.auth.models import User
from django.test import Client

from my_garden_app.models import Plant, PlantMaintenance, Garden, PlantGarden
from my_garden_app.views import AddCommentView


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


@pytest.fixture
def maintenance_data(plant):
    return PlantMaintenance.objects.create(
        plant=plant,
        task=1,
        task_description='test_plant1 description',
        week_of_month=1,
        month=1,
    )


@pytest.fixture
def garden():
    return Garden.objects.create(name='Test Garden')


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def add_comment_view():
    return AddCommentView()


@pytest.fixture
def plant_garden(garden, plant):
    return PlantGarden.objects.create(
        garden=garden,
        plant=plant,
        start_date='2024-01-01',
        location='Test Location'
    )
