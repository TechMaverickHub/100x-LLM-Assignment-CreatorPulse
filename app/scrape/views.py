from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SourceTypeConstants, SuccessMessage
from app.source.models import Source
from app.utils import get_response_schema


# Create your views here.
class YoutubeScrapeAPIView(GenericAPIView):

    def post(self, request):

        # Retrieve te url from data
        youtube_url_list = list(Source.objects.filter(source_type=SourceTypeConstants.YOUTUBE.value).values_list("url", flat=True))

        print(youtube_url_list)

        return get_response_schema({}, SuccessMessage.RECORD_CREATED.value, status.HTTP_200_OK)

