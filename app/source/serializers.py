from rest_framework import serializers

from app.source.models import Source


class SourceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a source"""

    class Meta:
        model = Source
        fields = ["name", "url", "source_type", "description", "user"]