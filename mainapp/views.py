from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import models

@login_required(login_url = 'login')
def dashboardView(request):
    return render(request, 'mainapp/dashboard.html')

@login_required(login_url = 'login')
def candidateView(request):
    return render(request, 'mainapp/profile-candidate.html')

@login_required(login_url = 'login')
def infoView(request):
    return render(request, 'mainapp/info.html')

@login_required(login_url = 'login')
def contactsView(request):
    return render(request, 'mainapp/contacts.html')

@login_required(login_url = 'login')
def personalView(request):
    context ={}
    return render(request, 'mainapp/personal.html')


def loginView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        context = {}

        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

            else:
                messages.error(request, "Data is invalid")
                return render(request, 'mainapp/login.html', context)


        return render(request, 'mainapp/login.html', context)
    


def logoutView(request):
    logout(request)
    return redirect('login')
