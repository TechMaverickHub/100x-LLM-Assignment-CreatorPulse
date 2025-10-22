from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class NewsletterTemplate(models.Model):
    """
    Base template for newsletters. shoud be saved if user save the 1st draft along with name
    """

    #Foreign Key
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_templates', related_query_name='user_template')

    #Field declarations
    name = models.CharField(max_length=255)

    #Additional fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class NewsletterDraft(models.Model):
    """
    Stores every version of a draft.
    """
    # Foreign Key
    newsletter_template = models.ForeignKey(NewsletterTemplate, on_delete=models.CASCADE, related_name="newsletter_template_drafts", related_query_name="newsletter_template_draft")

    #Field declarations
    html_content = models.TextField()
    version = models.PositiveIntegerField()


    #Additional fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.version:
            # Get the last version number for this template
            last_version = NewsletterDraft.objects.filter(
                newsletter_template=self.newsletter_template
            ).order_by('-version').first()

            self.version = 1 if not last_version else last_version.version + 1

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['newsletter_template', 'version'],
                name='unique_template_version'
            )
        ]
        ordering = ['-version']

class NewsletterSchedule(models.Model):
    """
    Schedule a newsletter for recurring or one-time sending.
    """

    # Foreign Key
    draft = models.ForeignKey(NewsletterDraft, on_delete=models.CASCADE, related_name='schedules')

    #Field declarations
    start_time = models.DateTimeField()
    frequency = models.CharField(
        max_length=20,
        choices=[('once', 'Once'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        default='once'
    )

    #Additional fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

