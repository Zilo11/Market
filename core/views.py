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
    favorite_counter =  0

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

from django.http.request import HttpHeaders
from django.shortcuts import render

from django.http import HttpResponse
import requests
import json



def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "BK33fnQ7YPUqQgj0GgVkio-FJbIOJtW6h6-R_kWoENuNfUpE0LD7AWI21g0JOl4Bk1BhX5eWwraLYF0y--DaM_Y"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())






def send(request):
    resgistration  = [
    ]
    send_notification(resgistration , 'Code Keen added a new video' , 'Code Keen new video alert')
    return HttpResponse("sent")




def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/10.4.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyDvFZpioGYRCWtMNCBhq2-iaH4oOxvTwA8",' \
         '        authDomain: "vzilo-9335d.firebaseapp.com",' \
         '        databaseURL: "",' \
         '        projectId: "zilo-9335d",' \
         '        storageBucket: "zilo-9335d.appspot.com",' \
         '        messagingSenderId: "789137637713",' \
         '        appId: "1:789137637713:web:1ace3e6afcdf9d131b9370",' \
         '        measurementId: "G-CKSKE8910S"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")