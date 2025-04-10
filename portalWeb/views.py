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

        firstCard = dataCard['data'][0]
        cardPNG = None

        if 'image_uris' in firstCard:
            cardPNG = firstCard['image_uris']['png']
        elif 'card_faces' in firstCard and 'image_uris' in firstCard['card_faces'][0]:
            cardPNG = firstCard['card_faces'][0]['image_uris']['png']

        print(cardPNG)

        return JsonResponse({
            'cardNamesList': cardNamesList,
            'cardPNG': cardPNG,
        })
    except Exception as e:
        print("Erro:", e)
        return JsonResponse({'error': 'Not a single card was found!'}, status=400)

def buildDeck(request):
    return render(request,'buildDeck.html')