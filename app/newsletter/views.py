from django.db.models import F
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SourceTypeConstants, SuccessMessage, TopicConstants
from app.newsletter.ai_curator import curate_newsletter
from app.newsletter.email_sender import newsletter_to_html
from app.scrape.scrape_utils import scrape_api_source, scrape_reddit_source, scrape_arxiv_source, scrape_rss_source, \
    get_trends_to_watch
from app.source.models import Source
from app.topic.models import UserTopic
from app.topic.serializers import UserTopicDisplaySerializer
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class GenerateNewsletterAPIView(GenericAPIView):

    permission_classes = [IsUser]

    def post(self, request):

        user_topic_queryset = UserTopic.objects.select_related("topic") \
            .filter(user_id=request.user.id)

        user_topic_list = [
            {"topic_id": ut.topic.id, "topic_name": ut.topic.name}
            for ut in user_topic_queryset
        ]


        topics = []
        articles = []
        top_trends = []

        for item in user_topic_list:

            topics.append(item['topic_name'])

            # fetch urls and source_type
            url_source_type = list(Source.objects.filter(topic_id=item["topic_id"],is_active=True).values_list("url", "source_type"))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            #scrape the news
            for url, source_type in url_source_type:

                if source_type == SourceTypeConstants.API.value:
                    articles.extend(scrape_api_source(url, headers))
                elif source_type == SourceTypeConstants.REDDIT.value:
                    articles.extend(scrape_reddit_source(url, headers ))
                elif source_type == SourceTypeConstants.ARXIV.value:
                    articles.extend(scrape_arxiv_source(url, headers))
                elif source_type == SourceTypeConstants.RSS.value:
                    articles.extend(scrape_rss_source(url))

            # scrape the top trends
            if item["topic_id"] == TopicConstants.AI.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/7509269760615483402"

            elif item["topic_id"] == TopicConstants.BLOCKCHAIN.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/6397280906166700581"

            elif item["topic_id"] == TopicConstants.CYBERSECURITY.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/1739904053101697444"

            elif item["topic_id"] == TopicConstants.IOT.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/5112460639121574802"

            top_trends.extend(get_trends_to_watch(RSS_URL))

        newsletter_content = curate_newsletter(articles, topics, top_trends)

        html_content = newsletter_to_html(newsletter_content)

        return get_response_schema(html_content, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)



class GenerateTrendsAPIView(GenericAPIView):

    permission_classes = [IsUser]

    def post(self, request):
        user_topic_queryset = UserTopic.objects.select_related("topic") \
            .filter(user_id=request.user.id)

        user_topic_list = [
            {"topic_id": ut.topic.id, "topic_name": ut.topic.name}
            for ut in user_topic_queryset
        ]

        top_trends = []
        for item in user_topic_list:

            if item["topic_id"] == TopicConstants.AI.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/7509269760615483402"

            elif item["topic_id"] == TopicConstants.BLOCKCHAIN.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/6397280906166700581"

            elif item["topic_id"] == TopicConstants.CYBERSECURITY.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/1739904053101697444"

            elif item["topic_id"] == TopicConstants.IOT.value:

                RSS_URL = "https://www.google.com/alerts/feeds/05623958380462213229/5112460639121574802"

            top_trends.extend(get_trends_to_watch(RSS_URL))


        return get_response_schema(top_trends, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)









