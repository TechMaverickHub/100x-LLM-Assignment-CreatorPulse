from django.urls import path

from app.newsletter.views import GenerateNewsletterAPIView, GenerateTrendsAPIView

urlpatterns = [
    # Authentication
    path("generate", GenerateNewsletterAPIView.as_view(), name="generate-newsletter"),

    path("generate-trends", GenerateTrendsAPIView.as_view(), name="generate-trends"),

]
