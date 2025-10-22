from django.urls import path

from app.topic.views import TopicListAPIView, UserTopicListAPIView, UserTopicUpdateAPIView

urlpatterns = [
    # Authentication
    path("list", TopicListAPIView.as_view(), name="topic-list"),

    path('user-topic-list', UserTopicListAPIView.as_view(), name="user-topic-list"),

    path('user-topic-update', UserTopicUpdateAPIView.as_view(), name="user-topic-create"),

    ]