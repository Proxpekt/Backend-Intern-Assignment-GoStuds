from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello, my bratha. You are at HOme")

def about(request):
    return HttpResponse("Hello, my bratha. You are at About")

def contact(request):
    return HttpResponse("Hello, my bratha. You are at Contact")