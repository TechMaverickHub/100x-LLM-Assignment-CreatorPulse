from django.urls import path

from app.newsletter.views import GenerateNewsletterAPIView

urlpatterns = [
    # Authentication
    path("generate", GenerateNewsletterAPIView.as_view(), name="generate-newsletter"),

]
