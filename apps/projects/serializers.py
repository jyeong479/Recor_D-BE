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
    members = ProjectMemberSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'owner', 'members',
            'member_count', 'start_date', 'end_date', 'is_active', 'created_at',
        )
        read_only_fields = ('id', 'owner', 'created_at')

    def get_member_count(self, obj):
        return len(obj.members.all())

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(owner=user, **validated_data)
        ProjectMember.objects.create(project=project, user=user, role='owner')
        return project
