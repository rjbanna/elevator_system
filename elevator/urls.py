from elevator.views import ElevatorSystemViewSet, ElevatorViewSet
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = []

router.register('elevators', ElevatorViewSet, basename='elevators')
router.register('systems', ElevatorSystemViewSet, basename='elevator_systems')

urlpatterns += router.urls
