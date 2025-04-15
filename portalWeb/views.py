from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
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
            cardImg = None
            if 'image_uris' in card:
                cardImg = card['image_uris']['png']
            elif 'card_faces' in card and 'image_uris' in card['card_faces'][0]:
                cardImg = card['card_faces'][0]['image_uris']['png']

            # cardRarity = card.get('rarity', None)
            # cardManaCost = card.get('mana_cost', None)
            # cardToughness = card.get('toughness', None)
            # cardPower = card.get('power', None)
            # cardColor = card.get('color')
            
            # cardType = None
            # cardSubType = None
            # cardSuperType = None
            # typeLine = card.get('type_line', None)
            # cardSuperType, cardType, cardSubType = parse_type_line(typeLine)
            # cardOracleText = card.get('oracle_text', None)
            
            
            

            cards.append({'name':cardName, 
                          'img':cardImg, 
                        #   'rarity':cardRarity, 
                        #   'mana_cost':cardManaCost, 
                        #   'toughness':cardToughness, 
                        #   'power':cardPower, 
                        #   'color':cardColor, 
                        #   'type':cardType, 
                        #   'sub_type':cardSubType,
                        #   'super_type':cardSuperType,
                        #   'oracle_text':cardOracleText
            })
            # print(cards)

        return JsonResponse({
            'cards': cards,
        })
    except Exception as e:
        print("Erro:", e)
        return JsonResponse({'error': 'Not a single card was found!'}, status=400)

def buildDeck(request):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM CARD;")
    #     consulta = cursor.fetchall()
    #     print(consulta)
    return render(request,'buildDeck.html')

def selectCard(request, aCardInput):
    def parse_type_line(typeLine):
        superType = []
        type = []
        subType = []

        listSupertypes = ['Basic', 'Legendary', 'Ongoing', 'Snow', 'World']
        listTypes = [
            'Artifact', 'Battle', 'Conspiracy', 'Creature', 'Dungeon', 'Enchantment', 'Instant', 'Kindred',
            'Land', 'Phenomenon', 'Plane', 'Planeswalker', 'Scheme', 'Sorcery', 'Vanguard'
        ]

        if typeLine:
            parts = typeLine.split(' — ')
            mainTypes = parts[0].split()
            for t in mainTypes:
                if t in listSupertypes:
                    superType.append(t)
                elif t in listTypes:
                    type.append(t)
            if len(parts) > 1:
                subType = parts[1].split()
            if '//' in subType:
                subType.remove('//')

        return superType, type, subType

    try:
        aCardInput = aCardInput.replace('___', '//')
        res = requests.get(f'https://api.scryfall.com/cards/named?exact={aCardInput}')
        dataCard = res.json()

        cardName = dataCard['name']
        cardImg = None
        cardManaCost = None
        cardOracleText = None
        cardToughness = None
        cardPower = None
        typeLine = None

        if 'card_faces' in dataCard:
            cardFaces = dataCard['card_faces']
            cardImg = cardFaces[0].get('image_uris', {}).get('png')
            cardManaCost = ' // '.join([f.get('mana_cost', '') for f in cardFaces])
            cardOracleText = ' // '.join([f.get('oracle_text', '') for f in cardFaces])
            cardPower = ' // '.join([f.get('power', '') for f in cardFaces])
            cardToughness = ' // '.join([f.get('toughness', '') for f in cardFaces])
            typeLine = ' // '.join([f.get('type_line', '') for f in cardFaces])
        else:
            cardImg = dataCard.get('image_uris', {}).get('png')
            cardManaCost = dataCard.get('mana_cost')
            cardOracleText = dataCard.get('oracle_text')
            cardPower = dataCard.get('power')
            cardToughness = dataCard.get('toughness')
            typeLine = dataCard.get('type_line')

        cardRarity = dataCard.get('rarity')
        cardColor = dataCard.get('color_identity') or dataCard.get('colors')
        cardSuperType, cardType, cardSubType = parse_type_line(typeLine)

        card = {
            'name': cardName,
            'img': cardImg,
            'rarity': cardRarity,
            'mana_cost': cardManaCost,
            'toughness': cardToughness,
            'power': cardPower,
            'color': cardColor,
            'type': cardType,
            'sub_type': cardSubType,
            'super_type': cardSuperType,
            'oracle_text': cardOracleText
        }
        print(card)

        return JsonResponse(card)
    except Exception as e:
        print("Erro:", e)
        return JsonResponse({'error': 'Not a single card was found!'}, status=400)
