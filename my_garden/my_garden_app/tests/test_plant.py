import pytest
from django.test import RequestFactory
from django.urls import reverse
from my_garden_app.models import Plant
from my_garden_app.views import (
    MyGardenLoginView,
    PlantAddView,
    PlantEditView,
    PlantDeleteView,
    PlantsListView,
    PlantDetailView,
)

@pytest.mark.django_db
def test_plant_add_view_get(client):
    """Ensure plant add view loads and displays the form template when accessed via GET request."""
    url = reverse('add_plant')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_plant_add_view_post(client, plant):
    """Verify that new plant can be added to the database when form data is submitted via POST request to the plant add view."""
    url = reverse('add_plant')
    response = client.post(url)
    assert response.status_code == 302
    assert Plant.objects.count() == 1

@pytest.mark.django_db
def test_plant_edit_view_get(client, plant):
    """Ensure plant edit view loads and displays the edit plant template when accessed via GET request."""
    url = reverse('edit_plant', kwargs={'pk': plant.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_plant_edit_view_post(client, plant):
    """Verify existing plant can be updated in the database when form data is submitted via POST request to the plant edit view."""
    url = reverse('edit_plant', kwargs={'pk': plant.pk})
    data = {
       'name': 'Updated Plant Name',
       'description': 'Updated Plant Description',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Plant.objects.get(pk=plant.pk).name == 'Updated Plant Name'
    assert Plant.objects.get(pk=plant.pk).description == 'Updated Plant Description'
    # assert str(messages[0]) == "Zmiany zostaly zapisane."
@pytest.mark.django_db
def test_plant_delete_view(client, plant):
    """Ensure plant object can be deleted from the database when a POST request is made to the plant delete view."""
    url = reverse('delete_plant', kwargs={'plant_id': plant.id})
    response = client.post(url)
    assert response.status_code == 302
    assert not Plant.objects.filter(pk=plant.id).exists()

@pytest.mark.django_db
def test_plants_list_view(client, plants):
    """Verify plants list view loads, renders the plants list template, and displays the correct number of plant objects retrieved from the database."""
    url = reverse('plants_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['object_list']) == 3

@pytest.mark.django_db
def test_plant_detail_view(client, plant):
    """Ensure plant detail view loads, renders the plant details template, and displays details of the specified plant object retrieved from the database."""
    url = reverse('plant_details', kwargs={'plant_id': plant.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object'] == plant


