from django.urls import path

from app.source.views import SourceCreateAPIView

urlpatterns = [
    # Authentication
    path("", SourceCreateAPIView.as_view(), name="source-create"),

]
