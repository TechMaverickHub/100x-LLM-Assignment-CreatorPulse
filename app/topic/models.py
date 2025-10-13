from django.db import models

# Create your models here.
class Topic(models.Model):

    # Field declarations
    name = models.CharField(max_length=100)

    # Additional field declarations
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

