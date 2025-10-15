from rest_framework import serializers

from app.mail.models import EmailLog
from app.user.models import User


class UserNameDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class EmailLogListFilterSerializer(serializers.ModelSerializer):
    user = UserNameDisplaySerializer()

    class Meta:
        model = EmailLog
        fields = ('user', 'recipient', 'message', 'status', 'error_message')

class UserEmailListFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailLog
        fields = ('recipient', 'message', 'status', 'error_message')