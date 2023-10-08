from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import *

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('items/', include('item.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('inbox/', include('conversation.urls')),
    path('notification/', include('notifications_app.urls')),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
    path('send/',send,name="show_firebase_js"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='core/passwordReset.html'),name='reset_password'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='core/passwordResetSent.html'), name ="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/passwordResetForm.html'), name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='core/passwordResetDone.html'),name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
