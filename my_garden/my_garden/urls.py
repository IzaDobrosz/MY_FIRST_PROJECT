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
                                 )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyGardenLoginView.as_view(), name='login'),
    path('logout/', MyGardenLogoutView.as_view(), name='logout'),
    path('add_plant/', PlantAddView.as_view(), name='add_plant'),
    path('edit_plant/<int:pk>/', PlantEditView.as_view(), name='edit_plant'),
    path('delete_plant/<int:plant_id>/', PlantDeleteView.as_view(), name='delete_plant'),
    path('plants_list/', PlantsListView.as_view(), name='plants_list'),
    path('plant_details/<int:plant_id>/', PlantDetailView.as_view(), name='plant_details'),
    path('add_maintenance/', PLantMaintenanceAddView.as_view(), name='add_maintenance'),
    path('delete_maintenance/<int:task_id>/', PlantMaintenanceDeleteView.as_view(), name='delete_maintenance'),
]
