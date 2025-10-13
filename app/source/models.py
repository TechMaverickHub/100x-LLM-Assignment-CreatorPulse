from django.db import models

from app.topic.models import Topic


# Create your models here.
class SourceType(models.Model):
    """ Model to store source type """

    # Field declarations
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Additional Field declarations
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Source(models.Model):
    """Model to save source type, url and topic"""

    # Foreign key declarations
    source_type = models.ForeignKey(SourceType,
                                    on_delete=models.CASCADE,
                                    related_name="source_type_sources",
                                    related_query_name="source_type_source")
    topic = models.ForeignKey(Topic,
                              on_delete=models.CASCADE,
                              related_name="topic_sources",
                              related_query_name="topic_source")

    # Field declarations
    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField(blank=True)

    # Additional Field declarations
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
