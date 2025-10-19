from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SuccessMessage, RoleConstants
from app.mail.models import EmailLog
from app.source.models import Source
from app.user.models import User
from app.utils import get_response_schema
from permissions import IsSuperAdmin


# Create your views here.
class CountAdminAPIView(GenericAPIView):
    """View: Show Total source, active sources, Total Users, TOtal Newsletters sent"""

    permission_classes = [IsSuperAdmin]

    def get(self, request):

        total_source = Source.objects.count()
        active_source = Source.objects.filter(is_active=True).count()
        total_users = User.objects.filter(role_id=RoleConstants.USER.value).count()
        total_newsletter_sent = EmailLog.objects.filter(status='SUCCESS').count()

        return_data = {
            "total_source": total_source,
            "active_source": active_source,
            "total_users": total_users,
            "total_newsletter_sent": total_newsletter_sent
        }

        return get_response_schema(return_data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


