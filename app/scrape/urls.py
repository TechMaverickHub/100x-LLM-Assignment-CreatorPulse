from django.urls import path

from app.scrape.views import ScrapeTwitterHandleAPIView

urlpatterns = [
    # Authentication
    path('twitter-handle/', ScrapeTwitterHandleAPIView.as_view(),name="scrape-twitter-handle"),
]