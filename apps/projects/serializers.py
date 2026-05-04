from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Project, ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProjectMember
        fields = ('id', 'user', 'user_id', 'role', 'created_at')
        read_only_fields = ('id', 'created_at')


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    meeting_count = serializers.SerializerMethodField()
    todo_count = serializers.SerializerMethodField()
    completed_todo_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'owner',
            'start_date', 'end_date', 'status', 'tags', 'color',
            'meeting_count', 'todo_count', 'completed_todo_count',
            'created_at',
        )
        read_only_fields = ('id', 'owner', 'created_at')

    def get_meeting_count(self, obj):
        return obj.meetings.count()

    def get_todo_count(self, obj):
        return obj.todos.count()

    def get_completed_todo_count(self, obj):
        return obj.todos.filter(status='done').count()

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(owner=user, **validated_data)
        ProjectMember.objects.create(project=project, user=user, role='owner')
        return project
