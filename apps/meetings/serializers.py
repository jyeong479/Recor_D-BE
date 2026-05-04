from rest_framework import serializers
from apps.projects.models import ProjectMember
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

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        project = attrs.get('project') or getattr(self.instance, 'project', None)

        if user and project:
            is_member = ProjectMember.objects.filter(project=project, user=user).exists()
            if not is_member:
                raise serializers.ValidationError({
                    'project': 'You are not a member of this project.'
                })

        participants = attrs.get('participants')
        if participants is None and self.instance is not None and 'project' in attrs:
            participants = self.instance.participants.all()

        if project and participants is not None:
            participant_ids = {participant.id for participant in participants}
            member_ids = set(ProjectMember.objects.filter(
                project=project,
                user_id__in=participant_ids,
            ).values_list('user_id', flat=True))
            if participant_ids - member_ids:
                raise serializers.ValidationError({
                    'participants': 'All participants must be project members.'
                })

        return attrs

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        validated_data['created_by'] = self.context['request'].user
        meeting = super().create(validated_data)
        meeting.participants.set(participants)
        return meeting
