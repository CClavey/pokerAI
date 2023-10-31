import cv2

class Cards:
    def __init__(self, name, suit ,rank):
        self.name = name
        self.suit = suit
        self.rank = rank


suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
ranks = ['Ace','Two','Three','Four','Five','Six','Seven', 'Eight','Nine','Ten','Jack','Queen','King']
cardDictionary = {}
detectedCardList = []
counter = 0

for suit in suits:
    for rank in ranks:
        cardName = f'{rank} of {suit}'
        card = Cards(cardName, suit, rank)
        cardDictionary[cardName] = card

    #for cardName in cardDictionary:
      #print(cardName)

#Retrieve a card by its name
def cardTest(card):
    global counter
    if (counter < 7):
        try:
            retrievedCard = cardDictionary[card]
            print(retrievedCard.name)
        except KeyError:
            print("Bad key")
        else:
            print(retrievedCard.name)
            if (retrievedCard.name in detectedCardList):
                print("Card already detected.")
            else:
                detectedCardList.append(retrievedCard.name)
                print("Card added")
                counter += 1
                print(counter)
    else:
        print("Card List is full. Create anti-detection code.")
        print(detectedCardList)



