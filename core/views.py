from django.shortcuts import render, redirect

from item.models import Category, Item
from django.contrib.auth.forms import UserCreationForm


from .forms import SignupForm
from django.contrib.auth import logout,login

def index(request):
    items = Item.objects.filter(is_approved=True, is_sold=False)[0:12]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

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
