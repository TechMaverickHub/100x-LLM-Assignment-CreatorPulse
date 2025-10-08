from django.db import models


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
    """Model to save source type, url and user"""

    # Foreign key declarations
    source_type = models.ForeignKey(SourceType,
                                    on_delete=models.CASCADE,
                                    related_name="source_type_sources",
                                    related_query_name="source_type_source")
    user = models.ForeignKey('user.User',
                             on_delete=models.CASCADE,
                             related_name="user_sources",
                             related_query_name="user_source")

    # Field declarations
    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField(blank=True)

    # Additional Field declarations
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
