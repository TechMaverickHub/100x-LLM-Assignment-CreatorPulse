from django.urls import path

from app.mail.views import EmailLogListFilterAPIView, UserEmailListFilterAPIView

urlpatterns = [
    # Authentication
    path('list-filter', EmailLogListFilterAPIView.as_view(), name="email-log-list-filter"),
    path('user-list-filter', UserEmailListFilterAPIView.as_view(), name="user-list-filter"),
    ]