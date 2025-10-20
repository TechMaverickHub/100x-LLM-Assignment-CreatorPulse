from rest_framework import serializers

from app.sample.models import UserStyleSample


class UserStyleSampleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStyleSample
        fields = ["pk", "text", "user"]


class UserStyleSampleDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStyleSample
        fields = ["pk", "text"]


class UserStyleSampleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStyleSample
        fields = ["pk", "text",]



