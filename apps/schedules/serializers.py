from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'id', 'project', 'title', 'description',
            'start_datetime', 'end_datetime', 'is_all_day',
            'location', 'participants', 'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        if attrs.get('start_datetime') and attrs.get('end_datetime'):
            if attrs['start_datetime'] >= attrs['end_datetime']:
                raise serializers.ValidationError('종료 시간은 시작 시간보다 늦어야 합니다.')
        return attrs

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        validated_data['user'] = self.context['request'].user
        schedule = super().create(validated_data)
        schedule.participants.set(participants)
        return schedule

    def update(self, instance, validated_data):
        participants = validated_data.pop('participants', None)
        instance = super().update(instance, validated_data)
        if participants is not None:
            instance.participants.set(participants)
        return instance
