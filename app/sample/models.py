from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class UserStyleSample(models.Model):
    """
    Stores a text sample (newsletter, post, or article) uploaded by a user
    for writing style conditioning during newsletter generation.
    """

    # Foreignkey
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='style_samples', related_query_name='style_sample')

    # Field Declarations
    text = models.TextField(max_length=10000)

    # Addtional Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)




