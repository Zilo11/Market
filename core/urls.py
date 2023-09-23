from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm
from .views import email_form

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('termsAndConditions/', views.termsAndConditions, name='termsAndConditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/',views.sign_out,name='logout'),
    
    path('send-email/', email_form, name='send_email'),

]
