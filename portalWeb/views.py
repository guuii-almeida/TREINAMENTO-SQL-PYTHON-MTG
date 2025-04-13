from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import requests
from time import sleep
# Create your views here.


def index(request):
    return render(request,'index.html')


def searchCard(request, cardInput):
    def parse_type_line(typeLine):
        superType = []
        type = []
        subType = []

        listSupertypes = ['Basic', 'Legendary', 'Ongoing', 'Snow', 'World']
        listTypes = [
            'Artifact', 'Battle', 'Conspiracy', 'Creature', 'Dungeon', 'Enchantment', 'Instant', 'Kindred',
            'Land', 'Phenomenon', 'Plane','Planeswalker', 'Scheme', 'Sorcery', 'Vanguard'
        ]

        
        if '—' in typeLine:
            left, right = typeLine.split('—')
            subtypePart = right.strip().split()
        else:
            left = typeLine
            subtypePart = []

        leftParts = left.strip().split()

        for part in leftParts:
            if part in listSupertypes:
                superType.append(part)
            elif part in listTypes:
                type.append(part)

        subType = subtypePart

        return superType, type, subType
    sleep(0.5)
    try:
        res = requests.get(f'https://api.scryfall.com/cards/search?q={cardInput}')
        dataCard = res.json()

        cards = []
        for card in dataCard['data'][:15]:
            cardName = card['name']
            cardImg = None
            if 'image_uris' in card:
                cardImg = card['image_uris']['png']
            elif 'card_faces' in card and 'image_uris' in card['card_faces'][0]:
                cardImg = card['card_faces'][0]['image_uris']['png']

            cardRarity = card.get('rarity', None)
            cardManaCost = card.get('mana_cost', None)
            cardToughness = card.get('toughness', None)
            cardPower = card.get('power', None)
            cardColor = card.get('color')
            
            cardType = None
            cardSubType = None
            cardSuperType = None
            typeLine = card.get('type_line', None)
            cardSuperType, cardType, cardSubType = parse_type_line(typeLine)
            cardOracleText = card.get('oracle_text', None)
            
            
            

            cards.append({'name':cardName, 
                          'img':cardImg, 
                          'rarity':cardRarity, 
                          'mana_cost':cardManaCost, 
                          'toughness':cardToughness, 
                          'power':cardPower, 
                          'color':cardColor, 
                          'type':cardType, 
                          'sub_type':cardSubType,
                          'super_type':cardSuperType,
                          'oracle_text':cardOracleText
            })
            # print(cards)

        return JsonResponse({
            'cards': cards,
        })
    except Exception as e:
        print("Erro:", e)
        return JsonResponse({'error': 'Not a single card was found!'}, status=400)

def buildDeck(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM CARD;")
        consulta = cursor.fetchall()
        print(consulta)
    return render(request,'buildDeck.html')