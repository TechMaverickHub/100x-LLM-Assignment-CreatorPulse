from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SuccessMessage
from app.topic.models import Topic
from app.topic.serializers import TopicDisplaySerializer
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class TopicListAPIView(GenericAPIView):
    """View: Display all topics"""

    permission_classes = [IsUser]
    serializer_class = TopicDisplaySerializer
    def get(self, request):

        topic_queryset = Topic.objects.filter(is_active=True)

        serializer = TopicDisplaySerializer(topic_queryset, many=True)

        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)
