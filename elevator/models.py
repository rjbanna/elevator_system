from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """Contains the common fields for all the models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ElevatorSystem(BaseModel):
    """Model for elevator system which can contain multiple elevators"""
    name = models.CharField(max_length=50, default='')
    floors = models.IntegerField()

    class Meta:
        verbose_name = 'Elevator system'
        verbose_name_plural = 'Elevator systems'


class Elevator(BaseModel):
    """Model for the system elevator"""
    elevator_system = models.ForeignKey(ElevatorSystem,
                                        on_delete=models.CASCADE,
                                        related_name='elevator_system')
    current_floor = models.IntegerField(default=0)
    door_open = models.BooleanField(default=False)
    is_operational = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Elevator'
        verbose_name_plural = 'Elevators'


class ElevatorRequest(BaseModel):
    """Model to store the user requests for the elevators"""
    elevator = models.ForeignKey(Elevator,
                                 on_delete=models.CASCADE,
                                 related_name='elevator')
    current_floor = models.IntegerField()
    requested_floor = models.IntegerField()

    class Meta:
        verbose_name = 'Elevator request'
        verbose_name_plural = 'Elevator requests'
