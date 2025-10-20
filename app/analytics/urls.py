from django.urls import path

from app.analytics.views import DailyRegistrationsAPIView, ActiveUsersAPIView, UserTopicsAPIView, \
    DailyEmailCountAPIView, EmailStatusBreakdownAPIView, SourcesByTopicAPIView, TopicsTopAPIView, CountAdminAPIView

urlpatterns = [
    # User Analytics
    path("users/daily-registrations/", DailyRegistrationsAPIView.as_view(), name="daily-registrations"),
    path("users/active/", ActiveUsersAPIView.as_view(), name="active-users"),
    path("users/topics/", UserTopicsAPIView.as_view(), name="user-topics"),

    # Email / Newsletter Analytics
    path("emails/daily-count/", DailyEmailCountAPIView.as_view(), name="daily-email-count"),
    path("emails/status-breakdown/", EmailStatusBreakdownAPIView.as_view(), name="email-status-breakdown"),

     # Topic & Source Analytics
    path("sources/by-topic/", SourcesByTopicAPIView.as_view(), name="sources-by-topic"),
    path("topics/top/", TopicsTopAPIView.as_view(), name="topics-top"),

    path("count", CountAdminAPIView.as_view(), name="count-admin"),

]
