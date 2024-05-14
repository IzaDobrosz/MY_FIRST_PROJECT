from django.contrib import admin

# Register your models here.
from .models import Plant, Garden, PlantGarden, PlantMaintenance, MaintenanceMonthlySchedule, Comments


# def my_field(obj):
#     return f' klasa ucznia to {obj.get_school_class_display()}'


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    pass


@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
    pass


@admin.register(PlantGarden)
class PlantGardenAdmin(admin.ModelAdmin):
    pass


@admin.register(PlantMaintenance)
class PlantMaintenanceAdmin(admin.ModelAdmin):
    pass


@admin.register(MaintenanceMonthlySchedule)
class MaintenanceMonthlyScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['comment', 'created_on', 'user', 'plant']
