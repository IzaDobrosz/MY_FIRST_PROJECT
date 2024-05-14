"""
URL configuration for my_garden project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_garden_app.views import (MyGardenLoginView,
                                 PlantAddView,
                                 PlantEditView,
                                 PlantDeleteView,
                                 PlantsListView,
                                 PlantDetailView,
                                 MyGardenLogoutView,
                                 PLantMaintenanceAddView,
                                 PlantMaintenanceDeleteView,
                                 PlantMaintenanceEditView,
                                 GardenAddView,
                                 PlantSearchView,
                                 PlantToGardenAddView,
                                 PlantToGardenEditView,
                                 PlantToGardenDeleteView,
                                 DisplayMonthlyTasksView,
                                 AddCommentView,
                                 HomePageView,
                                 MaintenanceDetailView,
                                 GardensListView,
                                 GardenDetailView,
                                 GardenEditView,
                                 CommentsListView,
                                 )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('login/', MyGardenLoginView.as_view(), name='login'),
    path('logout/', MyGardenLogoutView.as_view(), name='logout'),
    path('add_plant/', PlantAddView.as_view(), name='add_plant'),
    path('edit_plant/<int:plant_id>/', PlantEditView.as_view(), name='edit_plant'),
    path('delete_plant/<int:plant_id>/', PlantDeleteView.as_view(), name='delete_plant'),
    path('plants_list/', PlantsListView.as_view(), name='plants_list'),
    path('plant_details/<int:plant_id>/', PlantDetailView.as_view(), name='plant_details'),
    path('add_maintenance/', PLantMaintenanceAddView.as_view(), name='add_maintenance'),
    path('edit_maintenance/<int:task_id>/', PlantMaintenanceEditView.as_view(), name='edit_maintenance'),
    path('delete_maintenance/<int:task_id>/', PlantMaintenanceDeleteView.as_view(), name='delete_maintenance'),
    path('maintenance_list/<int:plant_id>/', MaintenanceDetailView.as_view(), name='maintenance_list'),
    path('add_garden/', GardenAddView.as_view(), name='add_garden'),
    path('edit_garden/<int:garden_id>/', GardenEditView.as_view(), name='edit_garden'),
    path('gardens_list/', GardensListView.as_view(), name='gardens_list'),
    path('garden_details/<int:garden_id>/', GardenDetailView.as_view(), name='garden_details'),
    path('plant_search/', PlantSearchView.as_view(), name='plant_search'),
    path('add_plant_to_garden/<int:garden_id>/', PlantToGardenAddView.as_view(), name='add_plant_to_garden'),
    path('edit_plant_in_garden/<int:plant_garden_id>/', PlantToGardenEditView.as_view(), name='edit_plant_in_garden'),
    path('delete_plant_from_garden/<int:plant_garden_id>/', PlantToGardenDeleteView.as_view(), name='delete_plant_from_garden'),
    path('monthly_tasks/<int:garden_id>/', DisplayMonthlyTasksView.as_view(), name='monthly_tasks'),
    path('plant/<int:plant_id>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('comments_list/<int:plant_id>/', CommentsListView.as_view(), name='comments_list'),
]
