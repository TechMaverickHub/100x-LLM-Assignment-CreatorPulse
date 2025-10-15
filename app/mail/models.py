from django.db import models

from app.user.models import User


# Create your models here.

class EmailLog(models.Model):

    #Foreign key declaration
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_logs',
        related_query_name='email_log'
    )

    #Field declarations
    recipient = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ])
    error_message = models.TextField(blank=True, null=True)


    # Additional fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


