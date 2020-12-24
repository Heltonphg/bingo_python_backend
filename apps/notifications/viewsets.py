from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.notifications.models import Notifications
from apps.notifications.serializers import NotificationSerializer
from onesignal_sdk.client import Client
from onesignal_sdk.error import OneSignalHTTPError


class NotificationViewset(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()

    @receiver(post_save, sender=Notifications)
    def pos_save(sender, instance, created, **kwargs):
        client = Client(app_id='bcff3245-e74f-48a4-95b1-2992f2bedd68',
                        rest_api_key='MDMxNzNjNWMtYjIzZC00NjdmLWI4ZTItNzBhY2Y3MmE3N2M1',
                        user_auth_key='ZWFjMzk5YjAtZWQyZC00NmU3LWFlMTgtZDkxMGM5NjQ5YzRi')

        if created:
            try:
                notification_body = {
                    'contents': {'tr': 'Yeni bildirim', 'en': instance.title},
                    'include_player_ids': [str(instance.user.token_notification)],
                }
                response = client.send_notification(notification_body)
            except OneSignalHTTPError as e:
                print(e)
                print(e.status_code)

    @action(methods=['GET'], detail=False)
    def minhas_notificacoes(self, request):
        notificacoes = Notifications.objects.filter(user=self.request.user).all().order_by('lida')
        serializer = NotificationSerializer(notificacoes, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def ler_notificacao(self, request):
        notificacoes = Notifications.objects.filter(user=self.request.user).all()
        for notifica in notificacoes:
            notifica.lida = True
            notifica.save()
        return Response("ok", status=status.HTTP_200_OK)
