from django.urls import path

from app.source.views import SourceCreateAPIView, SourceDetailAPIView, SourceListFilter, UserSourceListAPIView, \
    SourceActivateAPIView

urlpatterns = [
    # Authentication
    path("", SourceCreateAPIView.as_view(), name="source-create"),
    path("<int:pk>", SourceDetailAPIView.as_view(), name="source-detail"),
    path("<int:pk>/activate", SourceActivateAPIView.as_view(), name="source-activate"),
    path("list-filter", SourceListFilter.as_view(), name="source-list-filter"),


    # For User
    path("user-source-list-filter", UserSourceListAPIView.as_view(), name="user-source-list"),
]
