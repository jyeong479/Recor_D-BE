from rest_framework import serializers
from .models import Portfolio, StarEntry


class StarEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StarEntry
        fields = (
            'id', 'situation', 'task', 'action', 'result',
            'ai_summary', 'is_summarized', 'summarized_at', 'created_at',
        )
        read_only_fields = ('id', 'ai_summary', 'is_summarized', 'summarized_at', 'created_at')


class PortfolioSerializer(serializers.ModelSerializer):
    star_entries = StarEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = (
            'id', 'project', 'title', 'description', 'tech_stack',
            'github_url', 'deploy_url', 'thumbnail_url',
            'is_public', 'star_entries', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
