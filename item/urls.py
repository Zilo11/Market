from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/', views.item_detail, name='item_detail'),

    path('admin_approval/', views.admin_approval, name='admin_approval')
]