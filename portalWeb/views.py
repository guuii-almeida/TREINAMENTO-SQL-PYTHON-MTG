from django.shortcuts import render
from django.http import JsonResponse
import requests
from time import sleep
# Create your views here.


def index(request):
    return render(request,'index.html')


def searchCard(request):
    
    return JsonResponse

def buildDeck(request):
    
    return render(request,'buildDeck.html')