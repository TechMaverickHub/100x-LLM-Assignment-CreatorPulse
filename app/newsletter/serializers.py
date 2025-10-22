from rest_framework import serializers

from app.newsletter.models import NewsletterTemplate, NewsletterDraft, NewsletterSchedule


class NewsletterTemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterTemplate
        fields = ['pk', 'name', 'user']


class NewsletterTemplateDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterTemplate
        fields = ['pk', 'name', ]


class NewsletterDraftCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsletterDraft
        fields = ['pk', 'newsletter_template', 'html_content', 'created']

class NewsletterDraftDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsletterDraft
        fields = ['pk', 'html_content', 'version']

class NewsletterDraftListDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsletterDraft
        fields = ['pk', 'version']

class NewsletterScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSchedule
        fields = ['pk', 'draft', 'start_time', 'frequency']