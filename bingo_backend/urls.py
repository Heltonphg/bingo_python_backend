from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from apps.core.viewsets import EventViewSet, RoomViewSet
from apps.users.viewsets import UserViewSet, CardBingoViewSet

router = routers.DefaultRouter()
router.register(r'eventos', EventViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'users', UserViewSet)
router.register(r'cards', CardBingoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
