from django.shortcuts import render

def welcome(request):
    return render(request, 'main/welcome.html', {})

def dashboard(request):
    return render(request, 'main/dashboard.html', {})