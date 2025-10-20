from django.urls import path

from app.sample.views import UserStyleSampleCreateAPIView, UserStyleSampleDetailAPIView, \
    UserStyleSampleListFilterAPIView

urlpatterns = [
    # Authentication
    path("", UserStyleSampleCreateAPIView.as_view(), name="user-style-sample-create"),
    path("<int:pk>", UserStyleSampleDetailAPIView.as_view(), name="user-style-sample-detail"),
    path("list-filter", UserStyleSampleListFilterAPIView.as_view(), name="user-style-sample-list-filter"),

]
