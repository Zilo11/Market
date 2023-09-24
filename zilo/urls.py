from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from notifications.consumers import NotificationConsumer

urlpatterns = [
    path('', include('core.urls')),
    path('items/', include('item.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('inbox/', include('conversation.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


websocket_urlpatterns=[
    path("ws/notifications/",NotificationConsumer.as_asgi())
]