from django.urls import path

from app.scrape.views import YoutubeScrapeAPIView

urlpatterns = [
    # Authentication
    path("youtube/", YoutubeScrapeAPIView.as_view(), name="youtube-scrape"),

]
