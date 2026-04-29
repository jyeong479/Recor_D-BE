from rest_framework import serializers
from .models import Meeting, MeetingNote


class MeetingNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingNote
        fields = ('id', 'content', 'ai_summary', 'is_summarized', 'summarized_at', 'updated_at')
        read_only_fields = ('id', 'ai_summary', 'is_summarized', 'summarized_at', 'updated_at')


class MeetingSerializer(serializers.ModelSerializer):
    note = MeetingNoteSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'project', 'title', 'held_at', 'location',
            'participants', 'note', 'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        validated_data['created_by'] = self.context['request'].user
        meeting = super().create(validated_data)
        meeting.participants.set(participants)
        return meeting

    def update(self, instance, validated_data):
        participants = validated_data.pop('participants', None)
        instance = super().update(instance, validated_data)
        if participants is not None:
            instance.participants.set(participants)
        return instance
