from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SuccessMessage
from app.scrape.scrape_utils import extract_twitter_handle, daily_newsletter_scrape
from app.source.models import Source
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class ScrapeTwitterHandleAPIView(GenericAPIView):
    permission_classes = [IsUser]

    def post(self, request):

        sources = list(
            Source.objects
            .filter(user_id=request.user.id, is_active=True)
            .order_by('-updated')
            .values_list('url', flat=True)
        )
        handle = [extract_twitter_handle(sources[0])]
        print(handle)
        daily_newsletter_scrape(sources)

        return get_response_schema({}, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)
