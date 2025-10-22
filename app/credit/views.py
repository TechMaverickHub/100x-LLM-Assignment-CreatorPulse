from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SuccessMessage
from app.mail.models import EmailLog
from app.newsletter.models import NewsletterDraft
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class CreditDetailAPIView(GenericAPIView):
    permission_classes = [IsUser]

    def get(self, request):
        now = timezone.now()

        start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.get_current_timezone())

        total = 100
        successful_email_count = EmailLog.objects.filter(
            status='SUCCESS',
            created__gte=start_of_month,
            user_id = request.user.id
        ).count()

        draft_count = NewsletterDraft.objects.select_related("newsletter_template").filter(
            newsletter_template__user_id = request.user.id,
            created__gte=start_of_month
        ).count()

        return_data = {
            "credit_remaining": total - (successful_email_count + draft_count),
            "email_sent": successful_email_count,
            "draft_count": draft_count
        }

        return get_response_schema(
            return_data,
            SuccessMessage.RECORD_RETRIEVED.value,
            status.HTTP_200_OK
        )
