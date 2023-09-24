from django.urls import path
from .import views 

app_name = 'notifications'

urlpatterns = [
    path('notification/',views.notifications_page_view, name="notification_page")
]