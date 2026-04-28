from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'profile_image', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')


class SocialLoginSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'kakao', 'github'])
    access_token = serializers.CharField()
