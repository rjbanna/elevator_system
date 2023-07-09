from django.contrib import admin
from elevator.models import *

# Register your models here.
admin.site.register(ElevatorSystem)


class ElevatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'elevator_system', 'current_floor', 'door_open', 'is_operational']


admin.site.register(Elevator, ElevatorAdmin)
admin.site.register(ElevatorRequest)
