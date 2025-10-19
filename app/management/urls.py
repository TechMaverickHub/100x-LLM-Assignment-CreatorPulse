from django.urls import path

from app.management.views import CountAdminAPIView

urlpatterns = [
    # Authentication
    path("count", CountAdminAPIView.as_view(), name="count-admin"),

]
