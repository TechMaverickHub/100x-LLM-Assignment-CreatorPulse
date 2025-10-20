from django.urls import path

from app.analytics.views import DailyRegistrationsAPIView, ActiveUsersAPIView, UserTopicsAPIView

urlpatterns = [
    # Authentication
    path("users/daily-registrations/", DailyRegistrationsAPIView.as_view(), name="daily-registrations"),
    path("users/active/", ActiveUsersAPIView.as_view(), name="active-users"),
    path("users/topics/", UserTopicsAPIView.as_view(), name="user-topics"),

]
