from rest_framework import serializers

from app.source.models import Source, SourceType


class SourceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a source"""

    class Meta:
        model = Source
        fields = ["name", "url", "source_type", "description", "user"]

class SourceTypeDisplaySerializer(serializers.ModelSerializer):
    """Serializer for displaying a source type"""

    class Meta:
        model = SourceType
        fields = ["name"]

class SourceDisplaySerializer(serializers.ModelSerializer):
    """Serializer for displaying a source"""

    source_type = SourceTypeDisplaySerializer()
    class Meta:
        model = Source
        fields = ["pk", "name", "url", "source_type", "description"]

class SourceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating the source"""

    class Meta:
        model = Source
        fields = ["name", "url", "source_type", "description"]

class SourceListFilterDisplaySerializer(serializers.ModelSerializer):
    """Serializer for Source List Filter"""

    source_type = SourceTypeDisplaySerializer()
    class Meta:
        model = Source
        fields = ["pk", "name", "url", "source_type", "description"]
