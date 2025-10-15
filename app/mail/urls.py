from django.urls import path

from app.mail.views import EmailLogListFilterAPIView, UserEmailListFilterAPIView, CountNewsletterReceivedAPIView, \
    LatestNewsletterAPIView

urlpatterns = [
    # Authentication
    path('list-filter', EmailLogListFilterAPIView.as_view(), name="email-log-list-filter"),
    path('user-list-filter', UserEmailListFilterAPIView.as_view(), name="user-list-filter"),

    path('count-newsletter-received', CountNewsletterReceivedAPIView.as_view(), name="count-newsletter-received"),
    path('latest-newsletter', LatestNewsletterAPIView.as_view(), name="latest-newsletter"),
    ]