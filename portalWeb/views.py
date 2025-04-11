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

        cards = []
        for card in dataCard['data'][:15]:
            cardName = card['name']
            cardPNG = None
            if 'image_uris' in card:
                cardPNG = card['image_uris']['png']
            elif 'card_faces' in card and 'image_uris' in card['card_faces'][0]:
                cardPNG = card['card_faces'][0]['image_uris']['png']

            cards.append({'name':cardName, 'img':cardPNG
            })
            # print(cards)
            # print(cards['name'])
        return JsonResponse({
            'cards': cards,
            # 'cardNamesList': cardNamesList,
            # 'cardPNG': cardPNG,
        })
    except Exception as e:
        print("Erro:", e)
        return JsonResponse({'error': 'Not a single card was found!'}, status=400)

def buildDeck(request):
    return render(request,'buildDeck.html')