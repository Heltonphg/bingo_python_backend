from rest_framework import serializers

from apps.notifications.models import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('id', 'title', 'message', 'created_at', 'lida')
