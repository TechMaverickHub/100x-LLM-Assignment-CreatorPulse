from django.urls import path

from app.source.views import SourceCreateAPIView, SourceDetailAPIView, SourceListFilter

urlpatterns = [
    # Authentication
    path("", SourceCreateAPIView.as_view(), name="source-create"),
    path("<int:pk>", SourceDetailAPIView.as_view(), name="source-detail"),
    path("list-filter", SourceListFilter.as_view(), name="source-list-filter")
]
