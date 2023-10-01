from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm
from .views import email_form

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('termsAndConditions/', views.termsAndConditions, name='termsAndConditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/',views.sign_out,name='logout'),
    
    path('send-email/', email_form, name='send_email'),

    path('favorite',  views.favorite, name = 'favorite')
    
    #Password reset
#     path('reset_password/',auth_views.PasswordResetView.as_view(),name='reset_password'),
#     path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(), name ="password_reset_done"),
#     path('password_reset_confirm/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
#     path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
