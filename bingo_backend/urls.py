from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from apps.auth_user.UserViewSet import UserAuthViewSet
from apps.card.viewsets import CardBingoViewSet
from apps.core.viewsets import BingoViewSet, RoomViewSet


router = routers.DefaultRouter()
router.register(r'bingos', BingoViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'cards', CardBingoViewSet)
router.register(r'auth_user', UserAuthViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
