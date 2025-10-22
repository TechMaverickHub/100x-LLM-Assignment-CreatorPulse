from rest_framework import serializers

from app.topic.models import Topic, UserTopic


class TopicDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class UserTopicDisplaySerializer(serializers.ModelSerializer):
    topic = TopicDisplaySerializer()
    class Meta:
        model = UserTopic
        fields = ['id', 'topic']
