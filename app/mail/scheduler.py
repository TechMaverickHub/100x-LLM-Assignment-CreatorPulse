import logging
import os
import time
from datetime import datetime

import resend
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db import transaction
from dotenv import load_dotenv

from app.global_constants import RoleConstants, SourceTypeConstants, TopicConstants
from app.mail.models import EmailLog
from app.newsletter.ai_curator import curate_newsletter
from app.newsletter.email_sender import newsletter_to_html
from app.scrape.scrape_utils import scrape_api_source, scrape_rss_source, scrape_reddit_source, scrape_arxiv_source, \
    get_trends_to_watch
from app.source.models import Source
from app.topic.models import UserTopic
from app.user.models import User
from app.user.serializers import UserDisplaySerializer

logger = logging.getLogger('scheduler')

load_dotenv()
def send_daily_email():
    """Function that sends email and logs results."""

    print("sending email")
    subject = "Daily Newsletter"
    retries = 3

    user_queryset = User.objects.filter(role_id=RoleConstants.USER.value, is_active=True)

    user_list = UserDisplaySerializer(user_queryset, many=True).data

    print(user_list)
    for user in user_list:
        user_topic_queryset = UserTopic.objects.select_related("topic") \
            .filter(user_id=user.get("pk"))

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

        newsletter_content = curate_newsletter(articles, topics, top_trends)

        html_content = newsletter_to_html(newsletter_content)

        for attempt in range(1, retries + 1):
            try:
                resend.api_key = os.getenv("RESEND_API_KEY")
                r = resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": "abhiroop1998.dev@gmail.com",
                    "subject": subject,
                    "html": html_content
                })


                # Create DB log
                with transaction.atomic():
                    EmailLog.objects.create(
                        recipient="abhiroop1998.dev@gmail.com",
                        message=html_content,
                        status='SUCCESS'
                    )

                logger.info(f"[{datetime.now()}] Email sent successfully to abhiroop1998.dev@gmail.com")
                return

            except Exception as e:
                logger.error(f"Attempt {attempt} failed: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff

        # If all retries failed
        EmailLog.objects.create(
            message=html_content,
            recipient="abhiroop1998.dev@gmail.com",
            status='FAILED',
            error_message=str(e)
        )
        logger.error(f"[{datetime.now()}] Email sending failed after retries.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_email, CronTrigger(hour=20, minute=26))
    scheduler.start()
    logger.info("Daily email scheduler started (runs at 8:00 AM every day)")
