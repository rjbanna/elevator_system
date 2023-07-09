from rest_framework import serializers

from elevator.models import ElevatorSystem, Elevator


class ElevatorSystemSerializer(serializers.ModelSerializer):
    elevators = serializers.IntegerField(min_value=1, required=True, write_only=True)
    elevator_ids = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ElevatorSystem
        fields = ('id', 'name', 'floors', 'elevators', 'elevator_ids')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_elevator_ids(self, obj):
        return Elevator.objects.filter(elevator_system=obj).values_list('id', flat=True)

    def validate(self, attrs):
        if ElevatorSystem.objects.filter(name__iexact=attrs.get('name')).exists():
            raise serializers.ValidationError('Elevator system with the given name already exists')

        return attrs


class ElevatorSerializer(serializers.ModelSerializer):
    door = serializers.CharField(required=False)
    system_id = serializers.IntegerField(min_value=0, required=False)
    elevator = serializers.IntegerField(min_value=0, required=False)
    current_floor = serializers.IntegerField(min_value=0, required=False)
    destination_floor = serializers.IntegerField(min_value=0, required=False)

    class Meta:
        model = Elevator
        fields = ('door', 'system_id', 'elevator', 'current_floor', 'destination_floor')
        extra_kwargs = {
            'door': {'required': False}
        }

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')

        if request and request.method == 'POST' and self.context.get('view_action') == 'call_elevator':
            fields['system_id'].required = True
            fields['current_floor'].required = True
            fields['destination_floor'].required = True

        return fields
