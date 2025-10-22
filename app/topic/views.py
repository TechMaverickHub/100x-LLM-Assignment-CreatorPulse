from django.db import transaction
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SuccessMessage
from app.topic.models import Topic, UserTopic
from app.topic.serializers import TopicDisplaySerializer, UserTopicDisplaySerializer
from app.utils import get_response_schema
from permissions import IsUser, IsSuperAdminOrUser


# Create your views here.
class TopicListAPIView(GenericAPIView):
    """View: Display all topics"""

    permission_classes = [IsSuperAdminOrUser]
    serializer_class = TopicDisplaySerializer
    def get(self, request):

        topic_queryset = Topic.objects.filter(is_active=True)

        serializer = TopicDisplaySerializer(topic_queryset, many=True)

        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


class UserTopicListAPIView(GenericAPIView):
    """View: Display all user topics"""

    permission_classes = [IsUser]
    serializer_class = UserTopicDisplaySerializer

    def get(self, request):

        user_topic_queryset = UserTopic.objects.select_related("topic","user").filter(user_id=request.user.id)
        serializer = UserTopicDisplaySerializer(user_topic_queryset, many=True)
        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


class UserTopicUpdateAPIView(GenericAPIView):
    """View: Update user topic"""

    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,  # The body is a list
            items=openapi.Schema(type=openapi.TYPE_INTEGER),  # Each item is an integer
            description="List of topic IDs"
        )
    )
    def post(self, request):
        topic_ids = request.data  # since the request body is a simple list

        # Use transaction.atomic to make add/delete operations atomic
        with transaction.atomic():
            existing_user_topics = list(
                UserTopic.objects.filter(user_id=request.user.id)
                .values_list("topic_id", flat=True)
            )

            topics_to_add = list(set(topic_ids) - set(existing_user_topics))
            topics_to_remove = list(set(existing_user_topics) - set(topic_ids))

            # Bulk create new topics
            UserTopic.objects.bulk_create([
                UserTopic(user_id=request.user.id, topic_id=topic_id)
                for topic_id in topics_to_add
            ])

            # Delete topics that are no longer selected
            UserTopic.objects.filter(
                user_id=request.user.id,
                topic_id__in=topics_to_remove
            ).delete()

        return get_response_schema({}, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)

