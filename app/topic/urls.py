from django.urls import path

from app.topic.views import TopicListAPIView

urlpatterns = [
    # Authentication
    path("list", TopicListAPIView.as_view(), name="topic-list"),

    ]