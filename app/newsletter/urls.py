from django.urls import path

from app.newsletter.views import GenerateNewsletterAPIView, GenerateTrendsAPIView, SendNewsletterAPIView, \
    NewsletterTemplateCreateAPIView, NewsletterDraftCreateAPIView, NewsletterDraftDetailAPIView, \
    NewsletterDraftListAPIView, NewsLetterTemplateListFilterAPIview, NewsletterScheduleCreateAPIView

urlpatterns = [
    # Authentication
    path("generate", GenerateNewsletterAPIView.as_view(), name="generate-newsletter"),

    path("generate-trends", GenerateTrendsAPIView.as_view(), name="generate-trends"),

    path("send-newsletter", SendNewsletterAPIView.as_view(), name="send-newsletter"),

    #Newsletter Template
    path("template", NewsletterTemplateCreateAPIView.as_view(), name="newsletter-template-create"),

    path("template/list-filter", NewsLetterTemplateListFilterAPIview.as_view(), name="newsletter-template-list-filter"),

    path("draft", NewsletterDraftCreateAPIView.as_view(), name="newsletter-draft-create"),

    path("draft/<int:pk>", NewsletterDraftDetailAPIView.as_view(), name="newsletter-draft-detail"),

    path("draft/list", NewsletterDraftListAPIView.as_view(), name="newsletter-draft-list"),

    path("schedule", NewsletterScheduleCreateAPIView.as_view(), name="newsletter-schedule-create"),
]
