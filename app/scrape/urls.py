from django.urls import path

from app.scrape.views import YoutubeScrapeAPIView, ApiScrapeAPIView, RedditScrapeAPIView, ArvixScrapeAPIView, \
    RSSScrapeAPIView

urlpatterns = [
    # Authentication
    path("youtube/", YoutubeScrapeAPIView.as_view(), name="youtube-scrape"),
    path('api', ApiScrapeAPIView.as_view(), name="api-scrape"),
    path('reddit', RedditScrapeAPIView.as_view(), name="reddit-scrape"),
    path('arvix', ArvixScrapeAPIView.as_view(), name="rss-scrape"),
    path('rss', RSSScrapeAPIView.as_view(), name="rss-scrape")

]
