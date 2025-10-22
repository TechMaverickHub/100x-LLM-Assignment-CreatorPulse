import logging
import os
import time
from datetime import datetime

import resend
from django.db import transaction
from dotenv import load_dotenv
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.core.views import CustomPageNumberPagination
from app.global_constants import SourceTypeConstants, SuccessMessage, TopicConstants, ErrorMessage
from app.mail.models import EmailLog
from app.newsletter.ai_curator import curate_newsletter
from app.newsletter.email_sender import newsletter_to_html
from app.newsletter.models import NewsletterTemplate, NewsletterDraft
from app.newsletter.serializers import NewsletterTemplateCreateSerializer, NewsletterDraftCreateSerializer, \
    NewsletterDraftDisplaySerializer, NewsletterDraftListDisplaySerializer, NewsletterTemplateDisplaySerializer
from app.scrape.scrape_utils import scrape_api_source, scrape_reddit_source, scrape_arxiv_source, scrape_rss_source, \
    get_trends_to_watch
from app.source.models import Source
from app.topic.models import UserTopic
from app.utils import get_response_schema
from permissions import IsUser

logger = logging.getLogger('scheduler')

load_dotenv()


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
            url_source_type = list(
                Source.objects.filter(topic_id=item["topic_id"], is_active=True).values_list("url", "source_type"))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            # scrape the news
            for url, source_type in url_source_type:

                if source_type == SourceTypeConstants.API.value:
                    articles.extend(scrape_api_source(url, headers))
                elif source_type == SourceTypeConstants.REDDIT.value:
                    articles.extend(scrape_reddit_source(url, headers))
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

        newsletter_content = curate_newsletter(articles, topics, top_trends, user_id=request.user.id)

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


class SendNewsletterAPIView(GenericAPIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "html_content": openapi.Schema(type=openapi.TYPE_STRING, description="Email to send newsletter to"),
                "recipient": openapi.Schema(type=openapi.TYPE_STRING, description="Email to send newsletter to"),
            },
        )
    )
    def post(self, request):

        html_content = request.data.get("html_content")
        recipient = request.data.get("recipient")

        if recipient is None:
            recipient = request.user.email

        retries = 3
        for attempt in range(1, retries + 1):
            try:
                resend.api_key = os.getenv("RESEND_API_KEY")
                r = resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": recipient,
                    "subject": "Daily Newsletter",
                    "html": html_content
                })

                # Create DB log
                with transaction.atomic():
                    EmailLog.objects.create(
                        user_id=request.user.id,
                        recipient=recipient,
                        message=html_content,
                        status='SUCCESS'
                    )

                logger.info(f"[{datetime.now()}] Email sent successfully to {recipient}")
                return get_response_schema(None, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Attempt {attempt} failed: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff

        # If all retries failed
        EmailLog.objects.create(
            user_id=request.user.id,
            message=html_content,
            recipient="abhiroop1998.dev@gmail.com",
            status='FAILED',
            error_message=str(e)
        )
        logger.error(f"[{datetime.now()}] Email sending failed after retries.")
        return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class NewsletterTemplateCreateAPIView(GenericAPIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the template"),
                "html_content": openapi.Schema(type=openapi.TYPE_STRING, description="HTML content of the template"),
            }
        )
    )
    def post(self, request):

        name = request.data.get("name")
        html_content = request.data.get("html_content")

        if name is None or html_content is None:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            news_letter_template_data = {
                "name": name,
                "user": request.user.id
            }
            news_letter_template_serializer = NewsletterTemplateCreateSerializer(data=news_letter_template_data)

            if news_letter_template_serializer.is_valid():
                news_letter_template_serializer.save()
            else:
                transaction.set_rollback(True)
                return get_response_schema(news_letter_template_serializer.errors, ErrorMessage.BAD_REQUEST.value,
                                           status.HTTP_400_BAD_REQUEST)

            news_letter_draft_data = {
                "newsletter_template": news_letter_template_serializer.data["pk"],
                "html_content": html_content,
            }

            news_letter_draft_serializer = NewsletterDraftCreateSerializer(data=news_letter_draft_data)

            if news_letter_draft_serializer.is_valid():
                news_letter_draft_serializer.save()
                return get_response_schema(news_letter_draft_serializer.data, SuccessMessage.RECORD_CREATED.value,
                                           status.HTTP_201_CREATED)
            else:
                transaction.set_rollback(True)
                return get_response_schema(news_letter_draft_serializer.errors, ErrorMessage.BAD_REQUEST.value,
                                           status.HTTP_400_BAD_REQUEST)


class NewsletterDraftCreateAPIView(GenericAPIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "newsletter_template_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the template"),
                "html_content": openapi.Schema(type=openapi.TYPE_STRING, description="HTML content of the draft"),
            }
        )
    )
    def post(self, request):

        newsletter_template_id = request.data.get("newsletter_template_id")
        html_content = request.data.get("html_content")

        if newsletter_template_id is None or html_content is None:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        # check if newsletter_template exists and belongs to user
        newsletter_template = NewsletterTemplate.objects.filter(id=newsletter_template_id, user_id=request.user.id,
                                                                is_active=True).first()
        if not newsletter_template:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        with transaction.atomic():

            newsletter_draft_data = {
                "newsletter_template": newsletter_template_id,
                "html_content": html_content,
            }

            newsletter_draft_serializer = NewsletterDraftCreateSerializer(data=newsletter_draft_data)

            if newsletter_draft_serializer.is_valid():
                newsletter_draft_serializer.save()
                return get_response_schema(newsletter_draft_serializer.data, SuccessMessage.RECORD_CREATED.value,
                                           status.HTTP_201_CREATED)
            else:
                transaction.set_rollback(True)
                return get_response_schema(newsletter_draft_serializer.errors, ErrorMessage.BAD_REQUEST.value,
                                           status.HTTP_400_BAD_REQUEST)


class NewsletterDraftDetailAPIView(GenericAPIView):
    permission_classes = [IsUser]

    def get_object(self, request, pk):
        news_letter_draft_queryset = NewsletterDraft.objects.select_related("newsletter_template").filter(pk=pk,
                                                                                                         newsletter_template__user_id=request.user.id,
                                                                                                         newsletter_template__is_active=True).first()
        if not news_letter_draft_queryset:
            return None
        return news_letter_draft_queryset

    def get(self, request, pk):
        newsletter_draft = self.get_object(request, pk)
        if not newsletter_draft:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)
        serializer = NewsletterDraftDisplaySerializer(newsletter_draft)
        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


class NewsletterDraftListAPIView(GenericAPIView):

    permission_classes = [IsUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("newsletter_template_id", openapi.IN_QUERY, description="ID of the template", type=openapi.TYPE_INTEGER, required=True),
        ]
    )
    def get(self, request):
        newsletter_drafts = NewsletterDraft.objects.select_related("newsletter_template").filter(newsletter_template_id=request.query_params.get("newsletter_template_id"),
                                                                                             newsletter_template__user_id=request.user.id,
                                                                                             newsletter_template__is_active=True)
        serializer = NewsletterDraftListDisplaySerializer(newsletter_drafts, many=True)
        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


class NewsLetterTemplateListFilterAPIview(ListAPIView):
    """View: Newsletter templates ListFilter"""

    serializer_class = NewsletterTemplateDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    def get_queryset(self):

        news_letter_template_queryset = NewsletterTemplate.objects.select_related("user").filter(user_id=self.request.user.id, is_active=True).order_by("-updated")

        # Filter by name
        name = self.request.query_params.get("name", None)
        if name:
            news_letter_template_queryset = news_letter_template_queryset.filter(name__istartswith=name)

        return news_letter_template_queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("name", openapi.IN_QUERY, description="Name of the template", type=openapi.TYPE_STRING, required=False),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



