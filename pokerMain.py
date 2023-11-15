import cv2
from collections import Counter

class Cards:
    def __init__(self, name, suit ,rank):
        self.name = name
        self.suit = suit
        self.rank = rank


suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
ranks = ['Two','Three','Four','Five','Six','Seven', 'Eight','Nine','Ten','Jack','Queen','King']
cardDictionary = {}
detectedCardList = []
counter = 0
startEntered = False
secondtEntered = False
thirdEntered = False
finalEntered = False

for suit in suits:
    for rank in ranks:
        cardName = f'{rank} of {suit}'
        card = Cards(cardName, suit, rank)
        cardDictionary[cardName] = card

royalFlush = 10
straightFlush = 9
fourKind = 8
fullHouse = 7
flush = 6
straight = 5
threeKind = 4
twoPair = 3
pair = 2
highCard = 1

def cardTest(card):
    global counter
    global startEntered
    global secondEntered
    global thirdEntered
    global finalEntered
    if (counter < 7):
        if ((counter == 2) and (startEntered == False)):
            startHandCheck()
            startEntered = True
        elif (counter == 5):
            handCheckTwo()
        elif (counter == 6):
            handCheckThree()
        try:
            retrievedCard = cardDictionary[card]
            print(retrievedCard.name)
        except KeyError:
            #print("Bad key")
            print()
        else:
            print(retrievedCard.name)
            if (retrievedCard.name in detectedCardList):
                #print("Card already detected.")
                print()
            else:
                detectedCardList.append(retrievedCard.name)
                print("Card added")
                counter += 1
                print(counter)
    else:
        print("Card List is full. Create anti-detection code.")
        print(detectedCardList)
        finalHandCheck()
        #HAVE A COUNTER IN THE CARDDETECTOR CODE SO THAT THIS FUNCTION PATH IS BLOCKED IF ALL THE CARDS ARE READ AND THE FINAL GAME STATE IS DETERMINED

def startHandCheck():
    currentHand = []
    score = 0
    for card_name in detectedCardList:
        card = cardDictionary.get(card_name)
        if (card.rank == 'Ace'):
            card.rank = 14
        elif (card.rank == 'Two'):
            card.rank = 2
        elif (card.rank == 'Three'):
            card.rank = 3
        elif (card.rank == 'Four'):
            card.rank = 4
        elif (card.rank == 'Five'):
            card.rank = 5
        elif (card.rank == 'Six'):
            card.rank = 6
        elif (card.rank == 'Seven'):
            card.rank = 7
        elif (card.rank == 'Eight'):
            card.rank = 8
        elif (card.rank == 'Nine'):
            card.rank = 9
        elif (card.rank == 'Ten'):
            card.rank = 10
        elif (card.rank == 'Jack'):
            card.rank = 11
        elif (card.rank == 'Queen'):
            card.rank = 12
        elif (card.rank == 'King'):
            card.rank = 13
        print(card.rank)
        currentHand.append(card)
    if (currentHand[0].rank == currentHand[1].rank):
        score += 1
    if (currentHand[0].suit == currentHand[1].suit):
        score += 1
    if ((currentHand[0].rank >= 8) and (currentHand[1].rank >= 8)):
        score += 1
    if ((currentHand[0].rank == currentHand[1].rank - 1) or (currentHand[1].rank == currentHand[0].rank - 1)):
        score += 1
    if (score >= 1):
        print("Buy-In")
    else:
        print("Fold or Buy-In if you feel lucky")


def handCheckTwo():
    currentHand = []
    score = 0
    for card_name in detectedCardList:
        card = cardDictionary.get(card_name)
        if (card.rank == 'Ace'):
            card.rank = 14
        elif (card.rank == 'Two'):
            card.rank = 2
        elif (card.rank == 'Three'):
            card.rank = 3
        elif (card.rank == 'Four'):
            card.rank = 4
        elif (card.rank == 'Five'):
            card.rank = 5
        elif (card.rank == 'Six'):
            card.rank = 6
        elif (card.rank == 'Seven'):
            card.rank = 7
        elif (card.rank == 'Eight'):
            card.rank = 8
        elif (card.rank == 'Nine'):
            card.rank = 9
        elif (card.rank == 'Ten'):
            card.rank = 10
        elif (card.rank == 'Jack'):
            card.rank = 11
        elif (card.rank == 'Queen'):
            card.rank = 12
        elif (card.rank == 'King'):
            card.rank = 13
        print(card.rank)
        currentHand.append(card)
    currentHand.sort(key=lambda x: x.rank)
    for card in cardDictionary:
        print()
    #Count occurrences of each rank in the currentHand
    rank_counts = Counter(card.rank for card in currentHand)
    suit_counts = Counter(card.suit for card in currentHand)

    if any(count == 3 for count in rank_counts.values()):
        print("Three of a kind OR maybe 4!")
        score += 1
    elif any(count == 4 for count in rank_counts.values()):
        print("Four of a kind!")
        score += 1
    elif any((count == 3 for count in rank_counts.values()) and (count == 2 for count in rank_counts.values())):
        print("Full House!")
        score += 1
    if any(count >= 4 for count in suit_counts.values()):
        print("Flush")
        score += 1
    if sum(1 for count in rank_counts.values() if count == 2) == 2:
        print("Two pairs!")
        score += 1




def handCheckThree():
    currentHand = []
    score = 0
    for card_name in detectedCardList:
        card = cardDictionary.get(card_name)
        if (card.rank == 'Ace'):
            card.rank = 14
        elif (card.rank == 'Two'):
            card.rank = 2
        elif (card.rank == 'Three'):
            card.rank = 3
        elif (card.rank == 'Four'):
            card.rank = 4
        elif (card.rank == 'Five'):
            card.rank = 5
        elif (card.rank == 'Six'):
            card.rank = 6
        elif (card.rank == 'Seven'):
            card.rank = 7
        elif (card.rank == 'Eight'):
            card.rank = 8
        elif (card.rank == 'Nine'):
            card.rank = 9
        elif (card.rank == 'Ten'):
            card.rank = 10
        elif (card.rank == 'Jack'):
            card.rank = 11
        elif (card.rank == 'Queen'):
            card.rank = 12
        elif (card.rank == 'King'):
            card.rank = 13
        print(card.rank)
        currentHand.append(card)

def finalHandCheck():
    currentHand = []
    score = 0
    for card_name in detectedCardList:
        card = cardDictionary.get(card_name)
        if (card.rank == 'Ace'):
            card.rank = 14
        elif (card.rank == 'Two'):
            card.rank = 2
        elif (card.rank == 'Three'):
            card.rank = 3
        elif (card.rank == 'Four'):
            card.rank = 4
        elif (card.rank == 'Five'):
            card.rank = 5
        elif (card.rank == 'Six'):
            card.rank = 6
        elif (card.rank == 'Seven'):
            card.rank = 7
        elif (card.rank == 'Eight'):
            card.rank = 8
        elif (card.rank == 'Nine'):
            card.rank = 9
        elif (card.rank == 'Ten'):
            card.rank = 10
        elif (card.rank == 'Jack'):
            card.rank = 11
        elif (card.rank == 'Queen'):
            card.rank = 12
        elif (card.rank == 'King'):
            card.rank = 13
        print(card.rank)
        currentHand.append(card)





