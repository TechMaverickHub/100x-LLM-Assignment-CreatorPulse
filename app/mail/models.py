from django.db import models

# Create your models here.

class EmailLog(models.Model):

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


