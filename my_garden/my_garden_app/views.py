from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, FormView, TemplateView
from .forms import PlantAddForm, PlantEditForm, PlantMaintenanceForm, PlantToGardenAddForm, GardenAddForm, \
    PlantSearchForm, CommentForm
from .models import Plant, PlantMaintenance, PlantGarden, Garden, MONTH_CHOICES, Comments
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomePageView(TemplateView):
    """
    Landing page view.
    """

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        carousel_items = [
            {'image': 'images/azalia.jpg', 'alt': 'Azalia'},
            {'image': 'images/bez.jpg', 'alt': 'Bez'},
            {'image': 'images/budleja.jpg', 'alt': 'Budleja'},
            {'image': 'images/glicynia.jpg', 'alt': 'Glicynia'},
            {'image': 'images/magnolia.jpg', 'alt': 'Magnolia'},
        ]
        context['carousel_items'] = carousel_items
        return context


class MyGardenLoginView(LoginView):
    """Create login view using Django LoginView"""
    template_name = 'registration/login.html'


class MyGardenLogoutView(LogoutView):
    """Create logout view using Django LogoutView"""
    template_name = 'registration/logged_out.html'


"""Create view to add plant using generic Create View"""


class PlantAddView(PermissionRequiredMixin, CreateView):
    """
    A view for adding a new plant.
    """

    form_class = PlantAddForm
    template_name = 'form.html'
    success_url = '/add_maintenance/'
    permission_required = 'my_garden.add_plant'


"""Create view to edit plant with initial data using generic UpdateView"""


class PlantEditView(UpdateView):
    """
        A view for editing plant details.
    """
    model = Plant
    form_class = PlantEditForm
    template_name = 'edit_delete.html'
    pk_url_kwarg = 'plant_id'

    def form_valid(self, form):
        """
        If the form is valid, update the plant details and show success message.
        """

        response = super().form_valid(form)
        messages.success(self.request, "Dane rośliny zostały zmienione.")
        return response

    def get_success_url(self):
        """
        Get the URL to redirect after successful form submission.
        """
        return reverse_lazy('plant_details', kwargs={'plant_id': self.kwargs['plant_id']})

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Edytuj'
        context['message'] = "Edytujesz:"
        return context


"""Create view to delete plant using generic DeleteView"""


class PlantDeleteView(DeleteView):
    """
    A view for deleting a plant.
    """
    model = Plant
    template_name = 'edit_delete.html'
    success_url = '/'
    pk_url_kwarg = 'plant_id'

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Usuń'
        plant = self.get_object()
        context['message'] = f'Następująca roślina zostanie usunięta { plant.name }'
        return context


"""Create view to display list of plants using generic ListView"""


class PlantsListView(ListView):
    """
    A view for listing all plants.
    """

    template_name = 'plants_list.html'

    def get_queryset(self):
        """
        Get the queryset of all plants.
        """
        return Plant.objects.all()

        # Pagination
        paginator = Paginator(plants, 20)
        page = request.GET.get('page')

        try:
            plants = paginator.page(page)
        except PageNotAnInteger:
            # if page is not integer, deliver 1st page
            plants = paginator.page(1)
        except EmptyPage:
            # If page out of range, deliver last one
            plants = paginator.page(paginator.num_pages)


"""Create view to display details for plant using generic DetailView"""


class PlantDetailView(DetailView):
    """A base view for displaying a single object."""

    model = Plant
    template_name = 'plant_details.html'
    pk_url_kwarg = 'plant_id'

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['plant_id'] = self.kwargs.get(self.pk_url_kwarg)
        return context


"""Create view to add task to plan maintenance using generic CreateView"""


class PLantMaintenanceAddView(CreateView):
    """
    A view for adding plant maintenance tasks.
    """

    model = PlantMaintenance
    form_class = PlantMaintenanceForm
    template_name = 'form.html'
    success_url = '/add_maintenance/'

    def form_valid(self, form):
        """
        Handle form validation and add confirmation message.
        """
        # Get object from form
        plant = form.cleaned_data['plant']
        # Add confirmation
        messages.success(self.request, f"Zadania dla: { plant.name } zostały dodane.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['message'] = "Dodaj zadania dla rośliny:"
        return context


"""Create view to edit task in plant maintenance using generic UpdateView"""


class PlantMaintenanceEditView(UpdateView):
    """
    A view for editing plant maintenance tasks.
    """

    model = PlantMaintenance
    form_class = PlantMaintenanceForm
    template_name = 'edit_delete.html'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        """ Add additional data to the context.
        Returns: dict: Context data."""
        # Get the initial context data from the superclass method
        context = super().get_context_data(**kwargs)
        # Set the button text for the form
        context['button_text'] = 'Edytuj'
        # Message displayed in the template
        context['message'] = "Edytujesz:"
        # Add the plant_id to the context
        context['plant_id'] = self.object.plant_id
        return context

    def get_success_url(self):
        """
        Get the URL to redirect to after successfully updating the object.
        """
        # Get plant_id from the edited object
        plant_id = self.object.plant_id
        # Construct the URL for the maintenance list view
        return reverse_lazy('maintenance_list', kwargs={'plant_id': plant_id})


"""Create view to delete task from plant maintenance using generic DeleteView"""


class PlantMaintenanceDeleteView(DeleteView):
    """
    A view for deleting plant maintenance tasks.
    """

    model = PlantMaintenance
    template_name = 'edit_delete.html'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        """
        Add additional data to the context.
        """
        context = super().get_context_data(**kwargs)
        # Set the button text for the form
        context['button_text'] = 'Usuń'
        # Get the maintenance task name
        plant_maintenance = self.get_object()
        task_name = plant_maintenance.get_task_display()
        # Set the message to be displayed in the template
        context['message'] = f'Następujące zadanie zostanie usunięte: { task_name } dla {plant_maintenance.plant}'
        return context

    def get_success_url(self):
        """
        Get the URL to redirect to after successfully updating the object.
        """
        # Get plant_id from the edited object
        plant_id = self.object.plant_id
        # Construct the URL for the maintenance list view
        return reverse_lazy('maintenance_list', kwargs={'plant_id': plant_id})


class MaintenanceDetailView(DetailView):
    """
    A view for displaying maintenance tasks for a specific plant.
    """

    model = Plant
    template_name = 'tasks_list.html'
    pk_url_kwarg = 'plant_id'

    def get_context_data(self, **kwargs):
        """
        Add additional data to the context.
        """
        context = super().get_context_data(**kwargs)
        # # Get the plant_id from the URL
        plant_id = self.kwargs.get(self.pk_url_kwarg)
        # # Retrieve the plant object based on plant_id
        plant = get_object_or_404(Plant, pk=plant_id)

        # Filter maintenance tasks for the plant
        tasks = PlantMaintenance.objects.filter(plant_id=plant_id)

        # Condition for displaying the message in case no tasks assigned
        if not tasks:
            context['no_tasks'] = True

        context['tasks'] = tasks
        context['plant'] = plant
        context['plant_id'] = plant_id
        return context


"""Create view to creat garden using generic Create View"""


class GardenAddView(LoginRequiredMixin, CreateView):
    """
    A view for adding a new garden.
    """

    form_class = GardenAddForm
    template_name = 'garden.html'
    success_url = '/'

    def form_valid(self, form):
        """
        Check if the form is valid.
        """
        response = super().form_valid(form)
        # Associate the garden with the current user
        self.object.user.set([self.request.user])
        return response

    def get_success_url(self):
        """
        Get the URL to redirect to after successfully adding the garden.
        """
        return reverse_lazy('add_plant_to_garden', kwargs={'garden_id': self.object.pk})


class GardenEditView(UpdateView):
    """
   A view for editing an existing garden.
   """

    model = Garden
    form_class = GardenAddForm
    template_name = 'edit_delete.html'
    button_text = 'Edytuj'
    pk_url_kwarg = 'garden_id'

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        garden_id = self.kwargs.get(self.pk_url_kwarg)
        garden = get_object_or_404(Garden, pk=garden_id)

        context['button_text'] = 'Edytuj'
        context['message'] = "Edytujesz:"
        context['confirm_message'] = "Dane ogrodu zostały zmienione."
        context['garden'] = garden
        context['garden_id'] = garden_id
        return context

    def get_success_url(self):
        """
        Get the URL to redirect to after successfully editing the garden.
        """
        return reverse_lazy('garden_details', kwargs={'garden_id': self.kwargs['garden_id']})


class GardensListView(LoginRequiredMixin, ListView):
    """
    A view for listing gardens associated with the current user.
    """

    template_name = 'gardens_list.html'

    def get_queryset(self):
        """
        Get the queryset of gardens associated with the current user.
        """
        user = self.request.user
        return Garden.objects.filter(user=user)


class GardenDetailView(DetailView):
    """
    A view for displaying details of a single garden object.
    """

    model = Garden
    template_name = 'garden_details.html'
    pk_url_kwarg = 'garden_id'

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        garden_id = self.kwargs.get(self.pk_url_kwarg)
        # user = self.request.user

        # Retrieve the garden object with given ID
        garden = get_object_or_404(Garden, pk=garden_id)
        # Get all plants associated with garden
        plants = garden.plants.all()

        # Check to display message in case of "no plants associated with the garden"
        if not plants:
            context['no_plants'] = True

        context['garden'] = garden
        context['plants'] = plants
        context['garden_id'] = garden_id

        # Get the plant_garden_ids for all plants in the ga
        # dictionary with key is a tuple:plant.id, plant_garden.start_date, plant_garden.location and value is plant_garden.id
        plant_garden_ids = {}
        for plant in plants:
            # Filtering PlantGarden by garden and plant
            plant_gardens = PlantGarden.objects.filter(garden=garden, plant=plant)
            # If there are multiple entries, handle them based on start_date and location
            for plant_garden in plant_gardens:
                key = (plant.id, plant_garden.start_date, plant_garden.location)
                plant_garden_ids[key] = plant_garden.id

        context['plant_garden_ids'] = plant_garden_ids
        return context


class PlantSearchView(FormView):
    """
    A view for searching plants.
    """

    template_name = 'search_plant.html'
    form_class = PlantSearchForm
    success_url = '/plant_details/'

    def form_valid(self, form):
        """
        Process form submission with valid data.
        """
        # Get the search query from the form
        query = form.cleaned_data.get('query')
        # Filter plants by name containing the query
        plants = Plant.objects.filter(name__icontains=query)
        # Render the response with the search results
        return self.render_to_response(self.get_context_data(form=form, plants=plants))

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context


"""Create view to add plant to garden using generic CreateView"""


class PlantToGardenAddView(CreateView):
    """
    A view for adding a plant to a garden using a generic CreateView.
    """

    form_class = PlantToGardenAddForm
    template_name = 'form.html'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        # Pass additional attributes to the form
        kwargs['date_input_type'] = 'date'
        return kwargs

    def get_success_url(self):
        """
        Get the URL to redirect to after successfully adding the plant to the garden.
        """
        return reverse_lazy('garden_details', kwargs={'garden_id': self.kwargs['garden_id']})


"""Create view to edit plant in garden with initial data using generic UpdateView"""


class PlantToGardenEditView(UpdateView):
    """
    A view for editing a plant in a garden using a generic UpdateView.
    """

    model = PlantGarden
    form_class = PlantToGardenAddForm
    template_name = 'edit_delete.html'
    pk_url_kwarg = 'plant_garden_id'

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Edytuj'
        context['message'] = "Edytujesz:"
        return context

    def get_success_url(self):
        """
        Get the URL to redirect to after successfully editing the plant in the garden.
        """
        # Get_object() method retrieves PlantGarden instance
        plant_garden = self.get_object()
        # Access the garden attribute from the PlantGarden instance to get garden.id to hand over to url
        garden_id = plant_garden.garden.id
        return reverse_lazy('garden_details', kwargs={'garden_id': garden_id})


"""Create view to delete plant using generic DeleteView"""


class PlantToGardenDeleteView(LoginRequiredMixin, DeleteView):
    """
    A view for deleting a plant from a garden using a generic DeleteView.
    """
    model = PlantGarden
    template_name = 'edit_delete.html'
    pk_url_kwarg = 'plant_garden_id'

    def get_object(self, queryset=None):
        """
        Get the PlantGarden object based on the provided plant_garden_id.
        """
        plant_garden_id = self.kwargs.get(self.pk_url_kwarg)
        # Get the plant garden associated with the provided ID and the current user
        plant_garden = PlantGarden.objects.select_related('garden').get(id=plant_garden_id, garden__user=self.request.user)
        return plant_garden

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Usuń'
        # Get the PlantGarden object
        plant_garden = self.get_object()
        # Get the plant associated with PlantGarden
        plant = plant_garden.plant
        context['message'] = f'Następująca roślina zostanie usunięta: {plant.name}, posadzona: {plant_garden.start_date}'
        return context

    def get_success_url(self):
        """
        Get the URL to redirect to after successful deletion.
        """
        return reverse_lazy('garden_details', kwargs={'garden_id': self.object.garden_id})


class DisplayMonthlyTasksView(View):
    """
    A view for displaying monthly tasks related to a garden.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display monthly tasks.
        """
        garden_id = kwargs.get('garden_id')

        # Get garden or return 404 if it doesn't exist
        garden = get_object_or_404(Garden, id=garden_id)
        plants = garden.plants.all()

        month_choices = MONTH_CHOICES

        tasks = PlantMaintenance.objects.filter(plant__plantgarden__garden=garden)
        month = request.GET.get('month')
        if month:
            tasks = tasks.filter(month=month)

    # Pagination
        paginator = Paginator(tasks, 10)
        page = request.GET.get('page')

        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # if page is not integer, deliver 1st page
            tasks = paginator.page(1)
        except EmptyPage:
            # If page out of range, deliver last one
            tasks = paginator.page(paginator.num_pages)

        context = {
            'garden': garden,
            'plants': plants,
            'month_choices': month_choices,
            'selected_month': int(month) if month else None,
            'tasks': tasks,
        }
        return render(request, 'monthly_tasks.html', context)


class AddCommentView(LoginRequiredMixin, View):
    """
    A view for adding comments to a plant.
    """

    def get(self, request, plant_id):
        """
        Handle GET requests to display the comment form.
        """
        form = CommentForm()
        plant = Plant.objects.get(pk=plant_id)
        return render(request, 'add_comment.html', {'form': form, 'plant': plant})

    def post(self, request, plant_id):
        """
        Handle POST requests to submit a new comment.
        """
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.plant_id = plant_id
            comment.user = request.user
            comment.save()
        return redirect('plant_details', plant_id=plant_id)


class CommentsListView(ListView):
    """
    A view for listing comments related to a plant.
    """

    template_name = 'comments_list.html'

    def get_queryset(self):
        """
        Get the queryset of comments for the specified plant.
        """
        # Get the plant ID from the URL parameters
        plant_id = self.kwargs['plant_id']
        # Filter comments for the selected plant
        queryset = Comments.objects.filter(plant_id=plant_id)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        # Get the plant object
        plant = get_object_or_404(Plant, pk=self.kwargs['plant_id'])
        # Add the plant name to the template context
        context['plant'] = plant

        return context
