from django.shortcuts import render, redirect

from item.models import Category, Item, FavoriteItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
import json 
from django.http import HttpResponse
from asgiref.sync import async_to_sync



from .forms import SignupForm
from django.contrib.auth import logout,login


def index(request):
    items = Item.objects.filter(is_approved=True, is_sold=False)[0:24]
    
    favorite = FavoriteItem.objects.none()
    favorite_counter = None

    if request.user.is_authenticated:
        favorite = FavoriteItem.objects.filter(user=request.user)
        
        if favorite.exists():
            favorite_counter = favorite.first().counter

    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
        'room_name': "broadcast",
        'favorite_counter': favorite_counter,
        'favorite': favorite
    })

def favorite(request):
    favorites = FavoriteItem.objects.filter(user=request.user)

    favorite = FavoriteItem.objects.none()
    favorite_counter = None

    if request.user.is_authenticated:
        favorite = FavoriteItem.objects.filter(user=request.user)
        
        if favorite.exists():
            favorite_counter = favorite.first().counter



    context={
        'favorite': favorite
    }
    return render(request, 'core/favorite.html', context)

def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def termsAndConditions(request):
    return render(request, 'core/termsAndConditions.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/termsAndConditions/')  
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {'form': form})
    
def sign_out(request):
    logout(request)
    return redirect('/')


from django.shortcuts import render, redirect
from django.contrib import messages
from .email_utils import send_mail

def email_form(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        selected_users = request.POST.getlist('selected_users')
        
        users = User.objects.filter(pk__in=selected_users)
        
        for user in users:
            send_mail(subject, body, user.email)
        
        messages.success(request, "Emails sent successfully")
        return redirect('/email_form/')
    
    users = User.objects.all()
    return render(request, 'core/email_form.html', {'users': users})