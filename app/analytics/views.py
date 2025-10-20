from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import GlobalValues, SuccessMessage
from app.topic.models import UserTopic
from app.utils import get_response_schema
from permissions import IsSuperAdmin


# Create your views here.
class DailyRegistrationsAPIView(GenericAPIView):
    """View: Count of new users per day (using User.created)"""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        user_queryset = get_user_model().objects.filter(role_id=GlobalValues.USER.value).order_by('-created')

        # group by days and limit to 7 days
        user_queryset = user_queryset.values('created__date').annotate(count=Count('id')).order_by('-created__date')[:7]

        return_data = {
            "date": [item['created__date'].isoformat() for item in user_queryset],
            "count": [item['count'] for item in user_queryset]
        }

        return get_response_schema(return_data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


class ActiveUsersAPIView(GenericAPIView):
    """View: Count of active users per day (using User.is_active and User.last_login)"""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        user_queryset = get_user_model().objects.filter(role_id=GlobalValues.USER.value, is_active=True).order_by(
            '-created')

        # group by days and limit to 7 days
        user_queryset = user_queryset.values('last_login__date').annotate(count=Count('id')).order_by(
            '-last_login__date')[:7]

        return_data = {
            "date": [item['last_login__date'].isoformat() for item in user_queryset],
            "count": [item['count'] for item in user_queryset]
        }

        return get_response_schema(return_data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


class UserTopicsAPIView(GenericAPIView):
    """View: Count of users per topic (using User.topics)"""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        user_counts = (
            UserTopic.objects
            .select_related('topic')
            .values('topic__name')  # include topic fields
            .annotate(user_count=Count('user'))
            .order_by('-user_count')
        )

        return_data = {
            "topic": [item['topic__name'] for item in user_counts],
            "count": [item['user_count'] for item in user_counts]
        }

        return get_response_schema(return_data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)
