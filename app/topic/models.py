from django.db import models

from app.user.models import User


# Create your models here.
class Topic(models.Model):

    # Field declarations
    name = models.CharField(max_length=100)

    # Additional field declarations
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class UserTopic(models.Model):
    # Link to User
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="topics",  # access all topics of a user: user.topics.all()
        related_query_name="topic"  # filter users by a specific topic: User.objects.filter(topic=some_topic)
    )

    # Link to Topic
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="users",  # access all users subscribed to a topic: topic.users.all()
        related_query_name="user"  # filter topics by a specific user: Topic.objects.filter(user=some_user)
    )

    class Meta:
        unique_together = ('user', 'topic')  # optional: prevent duplicate user-topic mappings
