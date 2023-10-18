from django.urls import path

from . import views

from item.views import add_to_favorite
app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/', views.item_detail, name='item_detail'),

    path('admin_approval/', views.admin_approval, name='admin_approval'),

    path('add_to_favorite/<int:pk>/', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/<int:pk>/', views.remove_from_favorite, name = 'remove_from_favorite'),

    path('sellers_all_items<int:created_by>', views.sellers_all_items, name = 'sellers_all_items'),
    path('items/sellers_all_items/<int:created_by>/', views.sellers_all_items, name='sellers_all_items'),

]

