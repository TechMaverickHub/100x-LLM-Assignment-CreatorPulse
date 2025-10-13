from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SourceTypeConstants, SuccessMessage
from app.scrape.scrape_utils import scrape_api_source, scrape_reddit_source, scrape_arxiv_source
from app.source.models import Source
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class YoutubeScrapeAPIView(GenericAPIView):

    def post(self, request):

        # Retrieve te url from data
        youtube_url_list = list(Source.objects.filter(source_type=SourceTypeConstants.YOUTUBE.value).values_list("url", flat=True))

        print(youtube_url_list)

        return get_response_schema({}, SuccessMessage.RECORD_CREATED.value, status.HTTP_200_OK)

class ApiScrapeAPIView(GenericAPIView):

    permission_classes = [IsUser]
    def post(self, request):

        api_urls = list(Source.objects.filter(source_type=SourceTypeConstants.API.value, is_active=True).values_list("url", flat=True))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        articles = []

        for url in api_urls:
            articles.extend(scrape_api_source(url, headers))


        return get_response_schema({}, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

class RedditScrapeAPIView(GenericAPIView):

    permission_classes = [IsUser]
    def post(self, request):
        api_urls = list(Source.objects.filter(source_type=SourceTypeConstants.REDDIT.value, is_active=True).values_list("url", flat=True))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        articles = []

        for url in api_urls:
            articles.extend(scrape_reddit_source(url, headers))

        print(articles)
        return get_response_schema({}, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

class ArvixScrapeAPIView(GenericAPIView):

    permission_classes = [IsUser]
    def post(self, request):
        api_urls = list(Source.objects.filter(source_type=SourceTypeConstants.ARXIV.value, is_active=True).values_list("url", flat=True))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        articles = []

        for url in api_urls:
            articles.extend(scrape_arxiv_source(url, headers))

        print(articles)
        return get_response_schema({}, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)








