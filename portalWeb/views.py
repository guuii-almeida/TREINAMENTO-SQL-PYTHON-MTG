from django.shortcuts import render
from django.http import JsonResponse
import requests
from time import sleep
# Create your views here.


def index(request):
    return render(request,'index.html')


def searchCard(request, cardInput):
    sleep(0.5)
    try:
        res = requests.get(f'https://api.scryfall.com/cards/search?q={cardInput}')
        dataCard = res.json()

        cardNamesList = [card['name'] for card in dataCard['data'][:5]]
        print(cardNamesList)
        return JsonResponse({
            'cardNamesList': cardNamesList,
        })
    except Exception as e:
        return JsonResponse({'error': 'Not a single card was found!'}, status=400)

def buildDeck(request):
    return render(request,'buildDeck.html')