from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Django says hey there, world!<br/> <a href="/rango/about">About</a>')

def about(request):
    return HttpResponse('Rango says here is the about page. Duh!<br/> <a href="/rango/index">Index</a>')