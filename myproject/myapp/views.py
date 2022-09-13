import email
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature

# Create your views here.
def index(request):
    
    features = Feature.objects.all()       
    context = {
        'features': features
    }
    return render(request, 'index.html', context)

def counter(request):
    words = request.POST['textform']
    amount_of_words = len(words.split())
    context = {
        'amount': amount_of_words
    }
    return render(request, 'counter.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
    
        if password == password_repeat:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
                user.save()
                return redirect('login')
            
        else:
            messages.info(request, 'Password does not match')
            return redirect('register')
                
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,
                                 password=password)
        
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Credentials invalid")
            return redirect('login')
        
        
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def post(request, pk):
    context = {
        'pk': pk
    }
    return render(request, 'post.html', context)