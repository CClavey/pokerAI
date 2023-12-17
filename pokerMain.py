import cv2
import tkinter as tk
from io import StringIO
import sys
from collections import Counter

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
oddsString = ""
handString = ""
startEntered = False
secondEntered = False
thirdEntered = False
finalEntered = False

for suit in suits:
    for rank in ranks:
        cardName = f'{rank} of {suit}'
        card = Cards(cardName, suit, rank)
        cardDictionary[cardName] = card

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
        elif ((counter == 5) and (secondEntered == False)):
            handCheckTwo()
            secondEntered = True
        elif ((counter == 6) and (thirdEntered == False)):
            handCheckThree()
            thirdEntered = True
        try:
            retrievedCard = cardDictionary[card]
            print(retrievedCard.name)
        except KeyError:
            #print("Bad key")
            print()
        else:
            print(retrievedCard.name)
            if (retrievedCard.name in detectedCardList):
                boobs = 0
            else:
                detectedCardList.append(retrievedCard.name)
                print("Card added")
                counter += 1
                print(counter)
    else:
        print("Card List is full. Create anti-detection code.")
        print(detectedCardList)
        finalHandCheck()

def startHandCheck():
    currentHand = []
    score = 0
    global oddsString
    oddsString = ""
    global handString
    handString = ""
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
        currentHand.append(card)
    if (currentHand[0].rank == currentHand[1].rank):
        score = 1
        handString = "Pair"
    if (currentHand[0].suit == currentHand[1].suit):
        score = 1
        handString ="Possible Flush"
    if ((currentHand[0].rank >= 8) and (currentHand[1].rank >= 8)):
        score = 1
        handString = "High Cards"
    if ((currentHand[0].rank == currentHand[1].rank - 1) or (currentHand[1].rank == currentHand[0].rank - 1)):
        score = 1
        handString ="Possible FLush"
    if (score >= 1):
        return "Buy-In"
    else:
        return "Fold or Buy-In if you feel lucky"


def handCheckTwo():
    currentHand = []
    score = 0
    straightCheck = 0
    straightFlushCheck = 0
    royalFlushCheck = 0
    global oddsString
    oddsString = ""
    global handString
    handString = ""
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
        currentHand.append(card)
    currentHand.sort(key=lambda x: x.rank)
    print(detectedCardList)
    #Count occurrences of each rank in the currentHand
    rank_counts = Counter(card.rank for card in currentHand)
    suit_counts = Counter(card.suit for card in currentHand)
    straightChecker(currentHand)

    for card in range(len(currentHand) - 1):
        if (currentHand[card].rank + 1 == currentHand[card + 1].rank):  # Index error (No more???)
            straightCheck += 1
    for card in range(len(currentHand) - 1):
        if ((currentHand[card].rank + 1 == currentHand[card + 1].rank) and (
                currentHand[card].suit == currentHand[card + 1].suit)):  # Index error (No more???)
            straightFlushCheck += 1
    for card in range(len(currentHand) - 1):
        if ((currentHand[card].rank >= 10) and (currentHand[card].rank +1 == currentHand[card + 1].rank) and (
                currentHand[card].suit == currentHand[card + 1].suit)):  # Index error (No more???)
            royalFlushCheck += 1
    if (straightCheck >= 4):
        handString = "Straight!"
        score = 1
    if any(count == 3 for count in rank_counts.values()):
        handString ="Three of a kind!"
        oddsString = " You have a 2.127% chance of getting a four of a kind"
        score = 1
    if any(count == 4 for count in rank_counts.values()):
        handString ="Four of a kind!"
        score = 1
    if (any(count == 3 for count in rank_counts.values()) and (any(count == 2 for count in rank_counts.values()))):
        handString ="Full House!"
        score = 1
    if any(count >= 4 for count in suit_counts.values()):
        handString ="Flush or Possible Flush"
        score = 1
    if sum(1 for count in rank_counts.values() if count == 2) == 2:
        handString ="Two pairs!"
        score = 1
    if (straightFlushCheck >= 4):
        handString = "Straight Flush!"
        score = 2
    if (royalFlushCheck >= 4):
        handString = "Royal Flush!"
        score = 2
    if (score == 1):
        return "OK Hand: Check, Call, or Raise"
    if (score > 1):
        return "CALL"
    else:
        return "Check if possible or fold"




def handCheckThree():
    currentHand = []
    score = 0
    straightCheck = 0
    straightFlushCheck = 0
    royalFlushCheck = 0
    global oddsString
    oddsString = ""
    global handString
    handString = ""
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
        currentHand.append(card)
    currentHand.sort(key=lambda x: x.rank)
    print(detectedCardList)
    # Count occurrences of each rank in the currentHand
    rank_counts = Counter(card.rank for card in currentHand)
    suit_counts = Counter(card.suit for card in currentHand)

    straightChecker(currentHand)

    for card in range(len(currentHand) - 1):
        if (currentHand[card].rank +1 == currentHand[card + 1].rank):  # Index error (No more???)
            straightCheck += 1
    for card in range(len(currentHand) - 1):
        if ((currentHand[card].rank + 1 == currentHand[card + 1].rank) and (
                currentHand[card].suit == currentHand[card + 1].suit)):  # Index error (No more???)
            straightFlushCheck += 1
    for card in range(len(currentHand) - 1):
        if ((currentHand[card].rank >= 10) and (currentHand[card].rank +1 == currentHand[card + 1].rank) and (
                currentHand[card].suit == currentHand[card + 1].suit)):  # Index error (No more???)
            royalFlushCheck += 1
    if sum(1 for count in rank_counts.values() if count == 2) == 2:
        handString ="Two pairs!"
        score = 1
    if (straightCheck >= 4):
        handString = "Straight"
        score = 2
    if any(count == 3 for count in rank_counts.values()):
        handString ="Three of a kind!"
        score = 2
    if (any(count == 3 for count in rank_counts.values()) and (any(count == 2 for count in rank_counts.values()))):
        handString ="Full House!"
        score = 2
    if any(count >= 4 for count in suit_counts.values()):
        handString ="Flush"
        score = 2
    if any(count == 4 for count in rank_counts.values()):
        handString ="Four of a kind!"
        score = 3
    if (straightFlushCheck >= 4):
        handString = "Straight Flush!"
        score = 4
    if (royalFlushCheck >= 4):
        handString = "Royal Flush!"
        score = 4

    print("THE SCORE IS " + str(score))
    if (score == 1):
        return "OK Hand: Check or Bluff"
    elif (score == 2):
        return "GOOD Hand: Check, Call, or Raise"
    elif (score >= 3):
        return "GREAT Hand: Check, Call or Raise"
    else:
        return "BAD Hand: Check if possible or fold"

def finalHandCheck():
    currentHand = []
    score = 0
    straightCheck = 0
    straightFlushCheck = 0
    royalFlushCheck = 0
    global oddsString
    oddsString = ""
    global handString
    handString = ""
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
        currentHand.append(card)
    currentHand.sort(key=lambda x: x.rank)
    print(detectedCardList)
    # Count occurrences of each rank in the currentHand
    rank_counts = Counter(card.rank for card in currentHand)
    suit_counts = Counter(card.suit for card in currentHand)
    for card in range(len(currentHand) - 1):
        if (currentHand[card].rank +1 == currentHand[card + 1].rank):  # Index error (No more???)
            straightCheck += 1
    for card in range(len(currentHand) - 1):
        if ((currentHand[card].rank + 1 == currentHand[card + 1].rank) and (
                currentHand[card].suit == currentHand[card + 1].suit)):  # Index error (No more???)
            straightFlushCheck += 1
    for card in range(len(currentHand) - 1):
        if ((currentHand[card].rank >= 10) and (currentHand[card].rank + 1 == currentHand[card + 1].rank) and (
                currentHand[card].suit == currentHand[card + 1].suit)):  # Index error (No more???)
            royalFlushCheck += 1
    if sum(1 for count in rank_counts.values() if count == 2) == 2:
        handString ="Two pairs!"
        score = 1
    if any(count == 3 for count in rank_counts.values()):
        handString ="Three of a kind!"
        score = 2
    if (any(count == 3 for count in rank_counts.values()) and (any(count == 2 for count in rank_counts.values()))):
        handString ="Full House!"
        score = 2
    if any(count >= 4 for count in suit_counts.values()):
        handString ="Flush"
        score = 2
    if (straightCheck >= 4):
        handString = "Straight"
        score = 2
    if any(count == 4 for count in rank_counts.values()):
        handString ="Four of a kind!"
        score = 3
    # Create a loop to check if there are at least 4 cards that could create a straight and if there are then give it a score, if not then do a probability check.
    if (straightFlushCheck >= 4):
        handString = "Straight Flush!"
        score = 4
    if (royalFlushCheck >= 4):
        handString = "Royal Flush!"
        score = 4
    print("THE FINAL SCORE IS " + str(score))
    if (score == 1):
        return "OK Hand: Check or Fold"
    elif (score == 2):
        return "GOOD Hand:Check, Call, or Raise"
    elif (score == 3):
        return "GREAT Hand: Check, Call or Raise"
    elif (score == 4):
        return "THE BEST HAND: ALL IN BABY"
    else:
        return "BAD Hand: Check if possible or fold"

def straightChecker(currentHand):
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    cards = currentHand
    suit_counts = Counter(card.suit for card in cards)
    testSuit = suit_counts.most_common(1)
    cardRankList = [Cards(f'{rank} of {testSuit}', testSuit, rank) for rank in ranks]
    ranksNeeded = []
    flushCheck = 0
    royalCheck = 0
    global oddsString
    for cardRank in cardRankList:
        if cardRank.rank not in [card.rank for card in cards]:
            counter = 0
            flushCounter = 0
            royalCounter = 0
            cards.append(cardRank)
            cards.sort(key=lambda x: x.rank)
            for i in range(len(cards) - 1):
                if cards[i].rank == (cards[i + 1].rank - 1):
                    counter += 1
                    if cards[i].suit == cards[i + 1].suit:
                        flushCounter += 1
                        if cards[i].rank >= 10:
                            royalCounter += 1
                else:
                    counter = 0
                    flushCounter = 0
                    royalCounter = 0
                if counter >= 4:
                    print("ALMOST STRAIGHT")
                    ranksNeeded.append(cardRank)
                    if flushCounter >= 4:
                        print("ALMOST STRAIGHT FLUSH")
                        flushCheck = 1
                        if royalCounter >= 4:
                            print("ALMOST ROYAL FLUSH")
                            royalCheck = 1
                    break
            cards.remove(cardRank)

    print(royalCheck)
    if len(ranksNeeded) == 1:
        odds = (4 / (52 - len(cards))) * 100
        odds = round(odds, 3)
        oddsString = ("You need a " + str(ranksNeeded[0].rank) + " to get a Straight. The odds of this are " + str(
            odds) + "%")
    if len(ranksNeeded) == 2:
        odds = (8 / (52 - len(cards))) * 100
        odds = round(odds, 3)
        oddsString = ("You need a " + str(ranksNeeded[0].rank) + " or a " + str(
            ranksNeeded[1].rank) + " to get a Straight. The odds of this are " + str(odds) + "%")
    if len(ranksNeeded) == 1 and flushCheck == 1:
        odds = (1 / (52 - len(cards))) * 100
        odds = round(odds, 3)
        oddsString = ("You need a " + str(ranksNeeded[0].rank) + " to get a Straight Flush. The odds of this are " + str(
            odds) + "%")
    if len(ranksNeeded) == 2 and flushCheck == 1:
        odds = (2 / (52 - len(cards))) * 100
        odds = round(odds, 3)
        oddsString = ("You need a " + str(ranksNeeded[0].rank) + " or a " + str(
            ranksNeeded[1].rank) + " to get a Straight Flush. The odds of this are " + str(odds) + "%")
    if ((len(ranksNeeded) == 1 or len(ranksNeeded) == 2) and royalCheck == 1):
        odds = (1 / (52 - len(cards))) * 100
        odds = round(odds, 3)
        largestRank = max(ranksNeeded, key=lambda x: x.rank).rank
        oddsString = ("You need a " + str(largestRank) + " to get a Royal Flush. The odds of this are " + str(
            odds) + "%")



