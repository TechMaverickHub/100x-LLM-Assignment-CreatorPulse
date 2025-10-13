from rest_framework import serializers

from app.topic.models import Topic


class TopicDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']
