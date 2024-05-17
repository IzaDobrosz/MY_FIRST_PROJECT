from django.contrib.auth.models import User, Permission
from django.utils import timezone
import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from my_garden_app.forms import PlantMaintenanceForm, GardenAddForm
from my_garden_app.models import Plant, PlantMaintenance, Comments, Garden, PlantGarden


# Test for Homepage, login and logout
@pytest.mark.django_db
def test_home_page_view(client):
    """
    Test the HomePageView if it displays the correct template and data.
    """
    # Make a GET request to the home page
    response = client.get(reverse('home'))

    # Assert that the response is successful
    assert response.status_code == 200

    # Assert that the correct template is used
    assert 'home.html' in response.template_name

    # Assert that carousel items are present in the context
    assert 'carousel_items' in response.context

    # Assert that the carousel items contain the expected data
    expected_items = [
        {'image': 'images/azalia.jpg', 'alt': 'Azalia'},
        {'image': 'images/bez.jpg', 'alt': 'Bez'},
        {'image': 'images/budleja.jpg', 'alt': 'Budleja'},
        {'image': 'images/glicynia.jpg', 'alt': 'Glicynia'},
        {'image': 'images/magnolia.jpg', 'alt': 'Magnolia'},
    ]
    assert response.context['carousel_items'] == expected_items


@pytest.mark.django_db
def test_my_garden_login_view_get(client):
    """
    Verify that the MyGardenLoginView renders the login template correctly and that response is successful.
    """
    # Make a GET request to the login page
    response = client.get(reverse('login'))

    # Assert that the response is successful
    assert response.status_code == 200

    # Assert that the correct template is used
    assert 'registration/login.html' in response.template_name


@pytest.mark.django_db
def test_my_garden_login_view_post(client):
    """
    Test MyGardenLoginView POST request whether after successful login it redirects to the homepage.
    """
    # Define and create test user
    username = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)

    # Make a POST request to the login page with correct user data
    response = client.post(reverse('login'), {'username': username, 'password': password})

    # Assert that the response is a redirect
    assert response.status_code == 302

    # Assert that the redirect is the home page
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_my_garden_logout_view_get(client):
    """
    Test the MyGardenLogoutView GET request checking if it renders the logout template correctly and that response is successful.
    """
    # Make a GET request to the logout page
    response = client.get(reverse('logout'))

    # Assert that the response is successful
    assert response.status_code == 200

    # Assert that the correct template is used
    assert 'registration/logged_out.html' in response.template_name

    @pytest.mark.django_db
    def test_my_garden_logout_view_post(client):
        """
        Test the MyGardenLogoutView POST request if it redirects to the login page.
        """
        # Make a POST request to the logout page
        response = client.post(reverse('logout'))

        # Assert that the response is a redirect
        assert response.status_code == 302

        # Assert that the redirect is the login page
        assert response.url == reverse('login')


#  tests for Plant

@pytest.mark.django_db
def test_plant_add_view_no_permission(client):
    """
    Test that user without the required permission receives 403 Forbidden response.
    """
    # Create user without the required permission
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Attempt to access the PlantAddView
    response = client.get(reverse('add_plant'))

    # Assert that the response is 403 Forbidden
    assert response.status_code == 403


@pytest.mark.django_db
def test_plant_add_view_with_permission(client):
    """
    Test that a user with the required permission can access the PlantAddView and submit the form.
    """
    # Create a superuser with the required permission
    superuser = User.objects.create_superuser(username='testuser', password='testpassword')
    permission = Permission.objects.get(codename='add_plant')
    superuser.user_permissions.add(permission)
    client.login(username='testuser', password='testpassword')

    # Attempt to access the PlantAddView
    response = client.get(reverse('add_plant'))

    # Assert that the response is 200 OK
    assert response.status_code == 200

    # Submit the form
    form_data = {
        'name': 'Test Plant',
        'description': 'Test Plant description',
        'max_height': 1,
        'spread': 1,
        'flowering_season': 1,
        'sunlight_exposure': 1,
        'pruning_frequency': 1,
        'watering_needs': 1,
        'fertilization': 1,
        'pest_disease_resistance': 1,
    }
    response = client.post(reverse('add_plant'), data=form_data)

    # Assert that the response is a redirect to the success URL
    assert response.status_code == 302
    assert response.url == '/add_maintenance/'

    # Verify that the plant was added to the database
    assert Plant.objects.filter(name='Test Plant').exists()
    assert Plant.objects.count() == 1


@pytest.mark.django_db
def test_plant_edit_view_get(client, plant):
    """
    Ensure plant edit view loads and displays the edit plant template  via GET request.
    """
    url = reverse('edit_plant', kwargs={'plant_id': plant.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_plant_edit_view_post(client, plant):
    """
    Verify existing plant can be updated in database when form data is submitted via POST.
    """
    url = reverse('edit_plant', kwargs={'plant_id': plant.pk})
    data = {
        'name': 'Updated Plant Name',
        'description': 'Updated Plant Description',
        'max_height': 1,
        'spread': 1,
        'flowering_season': 2,
        'sunlight_exposure': 1,
        'pruning_frequency': 1,
        'watering_needs': 1,
        'fertilization': 1,
        'pest_disease_resistance': 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    updated_plant = Plant.objects.get(pk=plant.pk)
    assert updated_plant.name == 'Updated Plant Name'
    assert updated_plant.description == 'Updated Plant Description'
    assert updated_plant.flowering_season == 2


@pytest.mark.django_db
def test_plant_delete_view(client, plant):
    """
    Ensure plant object can be deleted from the database when a POST request.
    """
    url = reverse('delete_plant', kwargs={'plant_id': plant.id})
    response = client.post(url)
    assert response.status_code == 302
    assert not Plant.objects.filter(pk=plant.id).exists()


@pytest.mark.django_db
def test_plants_list_view(client, plants):
    """
    Verify plants list view loads, renders the plants list template, and displays the correct number of plant objects.
    """
    url = reverse('plants_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['object_list']) == 3


@pytest.mark.django_db
def test_plant_detail_view(client, plant):
    """
    Ensure plant detail view loads, renders the plant details template, and displays details for correct plant object.
    """
    url = reverse('plant_details', kwargs={'plant_id': plant.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object'] == plant


#     tests for PlantMaintenance

@pytest.mark.django_db
def test_plant_maintenance_add_view(client):
    """
    Test if the PlantMaintenanceAddView renders the correct template and form.
    """
    response = client.get(reverse('add_maintenance'))
    assert response.status_code == 200
    assert 'form.html' in response.template_name
    assert isinstance(response.context['form'], PlantMaintenanceForm)


@pytest.mark.django_db
def test_plant_maintenance_add_view_post(client, plant):
    """
    Test if the form submission in PlantMaintenanceAddView is valid.
    """
    form_data = {
        'plant': plant.id,
        'task': 2,
        'task_description': 'Test description',
        'week_of_month': 2,
        'month': 2
    }
    response = client.post(reverse('add_maintenance'), data=form_data)
    assert response.status_code == 302
    assert response.url == '/add_maintenance/'
    assert PlantMaintenance.objects.filter(plant=plant).exists()
    storage = get_messages(response.wsgi_request)
    assert any(message.message == f"Zadania dla: { plant.name } zostały dodane." for message in storage)


@pytest.mark.django_db
def test_plant_maintenance_edit_view_get(client, maintenance_data):
    """
    Test if the PlantMaintenanceEditView renders the correct template and form on GET request.
    """
    response = client.get(reverse('edit_maintenance', kwargs={'task_id': maintenance_data.pk}))
    assert response.status_code == 200
    assert 'edit_delete.html' in response.template_name
    assert isinstance(response.context['form'], PlantMaintenanceForm)
    assert response.context['button_text'] == 'Edytuj'
    assert response.context['message'] == 'Edytujesz:'
    assert response.context['plant_id'] == maintenance_data.plant_id


@pytest.mark.django_db
def test_plant_maintenance_edit_view_post(client, plant, maintenance_data):
    """
    Test if the PlantMaintenanceEditView updates the object correctly on POST request.
    """
    url = reverse('edit_maintenance', kwargs={'task_id': maintenance_data.pk})
    data = {
        'plant': plant.id,
        'task': 2,
        'task_description': 'Updated task description',
        'week_of_month': 2,
        'month': 2
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('maintenance_list', kwargs={'plant_id': data['plant']})
    updated_task = PlantMaintenance.objects.get(pk=maintenance_data.pk)
    assert updated_task.plant_id == data['plant']
    assert updated_task.task == data['task']
    assert updated_task.task_description == data['task_description']
    assert updated_task.week_of_month == data['week_of_month']
    assert updated_task.month == data['month']


@pytest.mark.django_db
def test_plant_maintenance_delete_view(client, maintenance_data):
    """
    Test if the PlantMaintenanceDeleteView deletes the object correctly and redirects to the correct URL afterwords.
    """
    url = reverse('delete_maintenance', kwargs={'task_id': maintenance_data.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('maintenance_list', kwargs={'plant_id': maintenance_data.plant_id})
    assert not PlantMaintenance.objects.filter(pk=maintenance_data.pk).exists()


@pytest.mark.django_db
def test_plant_maintenance_view_context(client, maintenance_data):
    """
    Test if the PlantMaintenanceDeleteView context contains the correct data.
    """
    url = reverse('delete_maintenance', kwargs={'task_id': maintenance_data.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'message' in response.context
    assert 'Następujące zadanie zostanie usunięte' in response.context['message']
    assert 'button_text' in response.context
    assert response.context['button_text'] == 'Usuń'


@pytest.mark.django_db
def test_maintenance_detail_view_with_tasks(client, plant, maintenance_data):
    """
    Test if the MaintenanceDetailView displays maintenance tasks for a specific plant when tasks are available.
    """
    # Access the MaintenanceDetailView for the created plant
    response = client.get(reverse('maintenance_list', kwargs={'plant_id': plant.id}))

    # Assert that the response is successful
    assert response.status_code == 200

    # Assert that the plant name and maintenance task are present in the response content
    assert 'test_plant1' in response.content.decode()
    assert 'test_plant1 description' in response.content.decode()


@pytest.mark.django_db
def test_maintenance_detail_view_without_tasks(client, plant):
    """
    Test if MaintenanceDetailView correctly handles the case for "no tasks" scenario.
    """
    url = reverse('maintenance_list', kwargs={'plant_id': plant.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert plant.name in response.content.decode()
    assert 'Wybrana roślina nie ma przypisanych żadnych zadań.' in response.content.decode()


# Test for Garden
@pytest.mark.django_db
def test_garden_add_view_get(client, user):
    """
    Test if the GardenAddView renders the correct template and form on GET request.
    """
    client.force_login(user)
    response = client.get(reverse('add_garden'))
    assert response.status_code == 200
    assert 'garden.html' in response.template_name
    assert isinstance(response.context['form'], GardenAddForm)


@pytest.mark.django_db
def test_garden_add_view_post(client, user):
    """
    Test if the GardenAddView adds a new garden to the database on POST request.
    """
    client.force_login(user)
    url = reverse('add_garden')
    data = {
        'name': 'Test Garden',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('add_plant_to_garden', kwargs={'garden_id': Garden.objects.latest('id').pk})
    assert Garden.objects.filter(name='Test Garden', user=user).exists()


@pytest.mark.django_db
def test_garden_edit_view(client, garden, user):
    """
    Test if the GardenEditView edits an existing garden.
    """
    client.force_login(user)
    url = reverse('edit_garden', kwargs={'garden_id': garden.id})
    response = client.get(url)
    assert response.status_code == 200
    # assert 'form' in response.context
    # assert 'button_text' in response.context
    # assert 'message' in response.context
    # assert 'confirm_message' in response.context
    # assert 'garden' in response.context
    # assert 'garden_id' in response.context
    assert all(
        key in response.context for key in
        ['form', 'button_text', 'message', 'confirm_message', 'garden', 'garden_id']
    )


@pytest.mark.django_db
def test_garden_edit_view_post(client, garden, user):
    """
    Test if the form submission in GardenEditView is valid.
    """
    client.force_login(user)
    url = reverse('edit_garden', kwargs={'garden_id': garden.id})
    form_data = {
        'name': 'Test Garden1'
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    assert response.url == reverse('garden_details', kwargs={'garden_id': garden.id})
    assert Garden.objects.filter(id=garden.id, name='Test Garden1').exists()


@pytest.mark.django_db
def test_garden_edit_view_post_invalid(client, garden, user):
    """
    Test if the form submission in GardenEditView with invalid data.
    """
    client.force_login(user)
    url = reverse('edit_garden', kwargs={'garden_id': garden.id})
    form_data = {
        'name': ''
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_gardens_list_view_no_gardens(client, user):
    """
    Test if the GardensListView handles the case when the user has no gardens.
    """
    client.force_login(user)
    url = reverse('gardens_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['object_list']) == 0


@pytest.mark.django_db
def test_gardens_list_view_redirect_unauthenticated(client):
    """
    Test if unauthenticated users are redirected to the login page.
    """
    url = reverse('gardens_list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login')) or response.url.startswith('/login?next=' + reverse('gardens_list'))


@pytest.mark.django_db
def test_garden_detail_view_with_plants(client, garden, plant_garden):
    """
    Test if GardenDetailView correctly displays details of garden with added plants.
    """
    url = reverse('garden_details', kwargs={'garden_id': garden.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert garden.name in response.content.decode()
    assert plant_garden.plant.name in response.content.decode()
    assert plant_garden.location in response.content.decode()


@pytest.mark.django_db
def test_garden_detail_view_without_plants(client, garden):
    """
    Test if GardenDetailView correctly handles the case of "no plants in the garden" scenario.
    """
    url = reverse('garden_details', kwargs={'garden_id': garden.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert garden.name in response.content.decode()
    assert 'W Twoim ogrodzie nie ma żadnych roślin' in response.content.decode()


@pytest.mark.django_db
def test_plant_search_view(client, plants):
    """
    Test if the PlantSearchView correctly searches for plants.
    """
    # Define the search query
    search_query = "test_plant"

    # Access the search view
    url = reverse('plant_search')
    response = client.post(url, {'query': search_query})

    # Check response status code
    assert response.status_code == 200

    # Check if form is in the context
    assert 'form' in response.context

    # Check if plants containing the search query are in the context
    assert 'plants' in response.context
    assert len(response.context['plants']) == 3
    assert response.context['plants'][0].name == "test_plant1"


@pytest.mark.django_db
def test_plant_to_garden_add_view(client, garden):
    """
    Test if PlantToGardenAddView correctly adds a plant to the garden.
    """
    # Access the add plant to garden view
    url = reverse('add_plant_to_garden', kwargs={'garden_id': garden.id})
    response = client.get(url)
    assert response.status_code == 200

    # Check if the correct form class is used
    assert response.context['form'].__class__.__name__ == 'PlantToGardenAddForm'


@pytest.mark.django_db
def test_plant_deletion_success(client, user):
    """
    Tests if deletion of plant from the garden works properly"
    """
    # Create plant
    plant = Plant.objects.create(
        name='Test Plant',
        description='Test Plant Description',
        max_height=1,
        spread=2,
        flowering_season=2,
        sunlight_exposure=3,
        pruning_frequency=1,
        watering_needs=1,
        fertilization=1,
        pest_disease_resistance=1
    )
    # Create garden with user
    garden = Garden.objects.create(name='Test Garden')
    garden.user.add(user)

    # Add plant to garden
    plant_garden = PlantGarden.objects.create(
        garden=garden,
        plant=plant,
        start_date='2024-01-01',
        location='Test Location'
    )

    # Log in user
    client.login(username='testuser', password='testpassword')

    # Check if PlantGarden exists before deletion
    assert PlantGarden.objects.filter(id=plant_garden.id).exists()

    delete_url = reverse('delete_plant_from_garden', kwargs={'plant_garden_id': plant_garden.id})
    # Send POST request deleting plant from the garden
    response = client.post(delete_url)

    # Check response status
    assert response.status_code == 302
    # Check if PlantGarden does not exist
    assert not PlantGarden.objects.filter(id=plant_garden.id).exists()
    # Check redirection
    assert response.url == reverse('garden_details', kwargs={'garden_id': garden.id})


@pytest.mark.django_db
def test_display_monthly_tasks_view(client, garden, maintenance_data, user):
    """
    Test if the DisplayMonthlyTasksView displays monthly tasks correctly.
    """
    client.force_login(user)
    url = reverse('monthly_tasks', kwargs={'garden_id': garden.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'garden' in response.context
    assert 'plants' in response.context
    assert 'month_choices' in response.context
    assert 'selected_month' in response.context
    assert 'tasks' in response.context


# Tests for Comments
@pytest.mark.django_db
def test_add_comment_view_get(client, user, plant):
    """
    Ensure comment add view loads and displays the form template via GET request.
    """
    client.force_login(user)
    url = reverse('add_comment', kwargs={'plant_id': plant.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'add_comment.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_add_comment_view_permissions(client, user, plant):
    """
    Ensure that the comment add view is restricted to authenticated users only.
    """
    # Set up
    url = reverse('add_comment', kwargs={'plant_id': plant.id})

    # Execute without logging in
    response = client.get(url)

    # Verify
    assert response.status_code == 302
    assert 'login' in response.url

    # Log in as a user
    client.login(username='testuser', password='testpassword')

    # Execute after logging in
    response = client.get(url)

    # Verify
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_comment_view_post_valid_form(client, user, plant):
    """
    Ensure that comment is successfully added when valid form data is submitted.
    """
    # Set up
    url = reverse('add_comment', kwargs={'plant_id': plant.id})
    client.login(username='testuser', password='testpassword')
    comment_text = 'Test comment'

    # Execute
    response = client.post(url, {'comment': comment_text})

    # Verify
    assert response.status_code == 302
    assert response.url == reverse('plant_details', kwargs={'plant_id': plant.id})
    assert plant.comments_set.filter(comment=comment_text).exists()


@pytest.mark.django_db
def test_comments_list_view(client, user, plant):
    """
    Test that the comments list view returns the correct comments for a plant.
    """
    # Create comments for the plant
    comment1 = Comments.objects.create(comment="Comment 1", created_on=timezone.now(), plant=plant, user=user)
    comment2 = Comments.objects.create(comment="Comment 2", created_on=timezone.now(), plant=plant, user=user)

    url = reverse('comments_list', kwargs={'plant_id': plant.id})
    response = client.get(url)
    assert response.status_code == 200

    # Check if the comments are in the context as 'object_list'
    assert comment1 in response.context['object_list']
    assert comment2 in response.context['object_list']

    # Check if the plant is in the context
    assert response.context['plant'] == plant


@pytest.mark.django_db
def test_comments_list_view_no_comments(client, user, plant):
    """
    Test that the comments list view returns no comments for a plant with no comments.
    """
    url = reverse('comments_list', kwargs={'plant_id': plant.id})
    response = client.get(url)
    assert response.status_code == 200

    # Check if there are no comments in the context
    assert 'comments' not in response.context

    # Check if the plant is in the context
    assert response.context['plant'] == plant
    # Check if the correct message is displayed ->decode method to convert bytes into a string
    assert 'Brak komentarzy dla tej rośliny.' in response.content.decode()
