from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'id', 'project', 'title', 'description', 'type',
            'start_datetime', 'end_datetime', 'is_all_day',
            'location', 'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        if attrs.get('start_datetime') and attrs.get('end_datetime'):
            if attrs['start_datetime'] >= attrs['end_datetime']:
                raise serializers.ValidationError('종료 시간은 시작 시간보다 늦어야 합니다.')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
