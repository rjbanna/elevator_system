from django.shortcuts import get_object_or_404
from elevator.models import ElevatorSystem, Elevator, ElevatorRequest
from elevator.serializers import ElevatorSystemSerializer, ElevatorSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ElevatorSystemViewSet(viewsets.ViewSet):
    serializer_class = ElevatorSystemSerializer
    res_status, data, message, status_code = False, {}, 'Invalid request', status.HTTP_500_INTERNAL_SERVER_ERROR

    # API to create the elevator system
    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                request_payload = dict(serializer.validated_data)

                elevator_system = ElevatorSystem.objects.create(name=request_payload['name'],
                                                                floors=request_payload['floors'])

                [Elevator.objects.create(elevator_system=elevator_system) for _ in range(request_payload['elevators'])]

                self.message = 'New elevator system initialized'
                self.res_status = True
                self.status_code = status.HTTP_201_CREATED
            else:
                self.status_code = status.HTTP_400_BAD_REQUEST
                self.message = serializer.errors
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})

    # API to list all the elevator systems
    def list(self, request, *args, **kwargs):
        try:
            queryset = ElevatorSystem.objects.all()

            serializer = self.serializer_class(queryset, many=True)

            self.data = serializer.data
            self.message = 'Elevator systems fetched successfully'
            self.res_status = True
            self.status_code = status.HTTP_200_OK
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})


class ElevatorViewSet(viewsets.ViewSet):
    serializer_class = ElevatorSerializer
    res_status, data, message, status_code = False, {}, 'Invalid request', status.HTTP_500_INTERNAL_SERVER_ERROR

    # API to close the elevator door
    @action(detail=True, methods=['get'], url_path='door/close')
    def close_door(self, request, pk=None):
        try:
            elevator_obj = get_object_or_404(Elevator, pk=pk)
            elevator_obj.door_open = False
            elevator_obj.save()

            self.message = 'Elevator door closed successfully'
            self.res_status = True
            self.status_code = status.HTTP_200_OK
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})

    # API to open the elevator door
    @action(detail=True, methods=['get'], url_path='door/open')
    def open_door(self, request, pk=None):
        try:
            elevator_obj = get_object_or_404(Elevator, pk=pk)
            elevator_obj.door_open = True
            elevator_obj.save()

            self.message = 'Elevator door opened successfully'
            self.res_status = True
            self.status_code = status.HTTP_200_OK
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})

    # API to mark the elevator as not operational
    @action(detail=True, methods=['get'], url_path='maintenance/start')
    def maintenance_start(self, request, pk=None):
        try:
            elevator_obj = get_object_or_404(Elevator, pk=pk)
            elevator_obj.is_operational = False
            elevator_obj.save()

            self.message = 'Elevator maintenance started successfully'
            self.res_status = True
            self.status_code = status.HTTP_200_OK
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})

    # API to mark the elevator as operational
    @action(detail=True, methods=['get'], url_path='maintenance/stop')
    def maintenance_stop(self, request, pk=None):
        try:
            elevator_obj = get_object_or_404(Elevator, pk=pk)
            elevator_obj.is_operational = True
            elevator_obj.save()

            self.message = 'Elevator maintenance stopped successfully'
            self.res_status = True
            self.status_code = status.HTTP_200_OK
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})

    # API to call the elevator at given floor
    @action(detail=False, methods=['post'], url_path='call')
    def call_elevator(self, request):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request,
                                                        'view_action': 'call_elevator'})
            if serializer.is_valid():
                request_payload = dict(serializer.validated_data)

                system_id = request_payload['system_id']
                current_floor = request_payload['current_floor']
                destination_floor = request_payload['destination_floor']

                elevator_system_filter = ElevatorSystem.objects.filter(id=system_id)
                if elevator_system_filter.exists():
                    elevator_system_obj = elevator_system_filter.first()
                    system_floors = elevator_system_obj.floors

                    if (current_floor > system_floors) or (destination_floor > system_floors):
                        self.message = f"""Floor value should be less than or equal to the system floors ({system_floors})"""
                        self.status_code = status.HTTP_400_BAD_REQUEST
                    else:
                        nearest_elevator_id = 0
                        nearest_floor_with_elevator = float('inf')
                        for elevator in Elevator.objects.filter(elevator_system__id=system_id,
                                                                door_open=False,
                                                                is_operational=True):
                            if nearest_floor_with_elevator > abs(elevator.current_floor - current_floor):
                                nearest_floor_with_elevator = elevator.current_floor
                                nearest_elevator_id = elevator.id

                        if nearest_elevator_id:
                            elevator_obj = get_object_or_404(Elevator, pk=nearest_elevator_id)
                            elevator_obj.current_floor = destination_floor
                            elevator_obj.save()

                            ElevatorRequest.objects.create(elevator=elevator_obj,
                                                           current_floor=current_floor,
                                                           requested_floor=destination_floor)

                            self.message = 'Elevator requested successfully'
                            self.data = {'elevator': nearest_elevator_id}
                            self.status_code = status.HTTP_200_OK
                        else:
                            self.message = 'No elevators found'
                            self.status_code = status.HTTP_404_NOT_FOUND
                        self.res_status = True
                else:
                    self.message = 'Elevator system not found'
                    self.status_code = status.HTTP_404_NOT_FOUND
            else:
                self.message = serializer.errors
                self.status_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})

    # API to fetch the user requests for the elevator
    @action(detail=True, methods=['get'], url_path='requests')
    def elevator_requests_list(self, request, pk=None):
        try:
            request_list = []
            for elevator_request in ElevatorRequest.objects.filter(elevator__id=pk):
                request_list.append({
                    'requested_from_floor': elevator_request.current_floor,
                    'requested_upto_floor': elevator_request.requested_floor,
                    'requested_at': elevator_request.created_at
                })

            self.data = request_list
            self.message = 'Elevator request list fetched successfully'
            self.res_status = True
            self.status_code = status.HTTP_200_OK
        except Exception as e:
            self.message = str(e)

        return Response({'status': self.res_status,
                         'code': self.status_code,
                         'message': self.message,
                         'data': self.data})
