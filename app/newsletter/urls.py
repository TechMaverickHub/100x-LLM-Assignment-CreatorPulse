from django.urls import path

from app.newsletter.views import GenerateNewsletterAPIView, GenerateTrendsAPIView, SendNewsletterAPIView

urlpatterns = [
    # Authentication
    path("generate", GenerateNewsletterAPIView.as_view(), name="generate-newsletter"),

    path("generate-trends", GenerateTrendsAPIView.as_view(), name="generate-trends"),

    path("send-newsletter", SendNewsletterAPIView.as_view(), name="send-newsletter"),

]
