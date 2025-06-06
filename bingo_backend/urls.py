from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token

from apps.account.viewsets import AccountViewSet
from apps.auth_user.UserViewSet import UserAuthViewSet
from apps.card.viewsets import CardBingoViewSet
from apps.core.thred_iniciar import ThredVerifica
from apps.core.tread import ThredRegressive
from apps.core.viewsets import BingoViewSet, RoomViewSet
from apps.notifications.viewsets import NotificationViewset

router = routers.DefaultRouter()
router.register(r'bingos', BingoViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'cards', CardBingoViewSet)
router.register(r'users', UserAuthViewSet)
router.register(r'notifications', NotificationViewset)
router.register(r'account', AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

thredRegressive = ThredRegressive()
thredRegressive.start()

verifica = ThredVerifica()
verifica.start()