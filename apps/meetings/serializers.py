from rest_framework import serializers
from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = (
            'id', 'project', 'title', 'date', 'duration', 'participants',
            'summary', 'tags', 'transcript', 'ai_summary',
            'key_points', 'action_items', 'is_summarized', 'summarized_at',
            'created_at',
        )
        read_only_fields = ('id', 'ai_summary', 'is_summarized', 'summarized_at', 'created_at')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
