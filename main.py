'''
Decks in ranking order

Royal Flush:
    AKQJ10 of one suit
Five of a kind:
    four cards of one rank and one wildcard
    the higher the card the higher the points
    ranks above straight flush
Straight flush:
    five cards of sequential rank in the same suit
    ranks above four of a kind
    Ace can't be low and high
Four of a kind:
    four cards of one rank and a kicker (card of another rank)
    When drawn, the higher rank of the four cards wins
    When drawn on the rank of the four cards, the rank of the kicker wins
Full House:
    Three cards of one rank, two of another rank
    Win decided by rank of the triplet, then rank of the pair
Flush:
    Five cards of the same suit, not all of sequential rank
    Ranked by the rank of the highest card, then going down respictivley
Straight:
    Five cards of sequential rank, not all of the same suit
    Ace can't be low and high
    Ranked by the highest ranking card
Three of a kind:
    Three cards of one trank and two kickers
    Ranked by the rank of the triplet, then the highest kicker, then the lowest kicker
Two Pair:
    Two cards of one rank, two cards of another rank, and a kicker
    Ranked by the rank of the highest pair, then the lowest pair, then the kicker
One Pair:
    Two cards of one rank, three kickers
    Ranked by the rank of the pair, then the highest to lowest kickers
High Card/Nothing:
    Does not fall into any other category
    Ranked by the highest ranking card, then the second highest, and so on
'''
from enum import Enum

class Hands(Enum):
    royalflush=0,
    fiveofakind=1,
    straightflush=2,
    fourofakind=3,
    fullhouse=4,
    flush=5,
    straight=6,
    threeofakind=7,
    twopair=8,
    onepair=9,
    highcard=10,


def getCards():
    deck=[]
    suits=["S","C","H","D"]
    cards=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    for suit in suits:
        for card in cards:
            deck.append([suit,card])
    deck.append(["JOKER"])
    deck.append(["JOKER"])
    return deck

def check(fn):
    def wrapper(*a,**kwa):
        if type(a[0]) == list:
            checkValid(cards=a[0])
        elif type(a[0]) == str:
            checkValid(card=a[0])
        return fn(*a,**kwa)
    return wrapper

def noJoker(fn):
    def wrapper(*a,**kwa):
        if ["JOKER"] in a[0]:
            return False
        return fn(*a,**kwa)
    return wrapper

def sort(fn):
    def wrapper(*a,**kwa):
        if type(a[0])==list:
            a=list(a)
            a[0]=sortDeck(a[0])
        return fn(*a,**kwa)
    return wrapper

def sortDeck(cards):
    for i in range(len(cards)):
        cards[i]=getCardNumericValue(cards[i])
    cards.sort()
    for i in range(len(cards)):
        cards[i]=getCardProperValue(cards[i])
    return cards

def getCardNumericValue(card,joker=True):
    if card[0] == "JOKER":
        if joker:
            return ["ZJOKER"]
        else:
            return [99]
    if card[1] == "A":
         return [card[0],14]
    if card[1] == "J":
         return [card[0],11]
    if card[1] == "Q":
         return [card[0],12]
    if card[1] == "K":
         return [card[0],13]
    return [card[0],int(card[1])]

def getCardProperValue(card):
    if card[0] == "ZJOKER" or card[0] == 99:
        return ["JOKER"]
    if card[1] == 14:
         return [card[0],"A"]
    if card[1] == 11:
         return [card[0],"J"]
    if card[1] == 12:
         return [card[0],"Q"]
    if card[1] == 13:
         return [card[0],"K"]
    return [card[0],str(card[1])]

def checkValid(card="",cards=[]):
    validCards=getCards()
    if card == "" and cards != []:
        for c in cards:
            if c not in validCards:
                raise Exception(f"Invalid card found: {c}")
        if len(cards) > 5:
            raise Exception(f"The deck of cards is too big! Expected <= 5, got {len(cards)}")
    elif card != "" and cards == []:
        if card not in validCards:
            raise Exception(f"Invalid card found: {card}")
    elif card == "" and cards == []:
        raise Exception("No input given to checkValid function")

def sameSuit(cards):
    suit=cards[0][0]
    for card in cards:
        if card[0]!=suit:
            return False
    return True

def sameRank(cards):
    rank=cards[0][1]
    for card in cards:
        if card[1]!=rank:
            return False
    return True

@noJoker
@check
def royalFlush(cards):
    # define the correct ranks
    possible=[10,11,12,13,14]
    cards=[getCardNumericValue(card) for card in cards]
    itera=0
    # check cards match the possible cards
    for card in sorted(cards):
        if card[1] != possible[itera]: # if its not a correct card
            return False
        itera+=1
    if not sameSuit(cards):
        return False
    return True

@check
def fiveKind(cards):
    cards=sorted(cards)
    # if there is not a joker, or if there is more than one joker
    if not(["JOKER"] in cards):
        return False
    c=cards
    c.remove(["JOKER"])
    if ["JOKER"] in c:
        return False
    if not sameRank(cards):
        return False
    return True

@noJoker
@check
def straightFlush(cards):  
    if not sameSuit(cards):
        return False
    cards=sortDeck(cards)
    for i in range(len(cards)):
        cards[i]=getCardNumericValue(cards[i],joker=False)
    start=cards[0][1]
    for card in cards:
        if card[1] != start:
            return False
        start+=1
    return True

@check
def fourKind(cards):
    @check
    def fourKindJoker(cards):
        card1=cards[0]
        if not("JOKER" in card1):
            card2=["JOKER"]
        c=cards
        c.remove(["JOKER"])
        for card in c:
            if card==["JOKER"]:
                return False
        c.remove(card1)
        card1counter=1
        card2counter=1
        for card in cards:
            if card[1] != card1[1]:
                if card[1] != card2[1]:
                    return False
                else:
                    card2counter+=1
            else:
                card1counter+=1
        if 4 not in [card1counter,card2counter]:
            return False
        return True

    if ["JOKER"] in cards:
        return fourKindJoker(cards)
    card1=cards[0]
    itera=1
    card2=cards[itera]
    while card2[1]==card1[1]:
        try:
            card2=cards[itera]
        except IndexError:
            return False
        itera+=1
    c=cards
    c.remove(card1)
    c.remove(card2)
    card1counter=1
    card2counter=1
    for card in cards:
        if card[1] != card1[1]:
            if card[1] != card2[1]:
                return False
            else:
                card2counter+=1
        else:
            card1counter+=1
    if 4 not in [card1counter,card2counter]:
        return False
    return True



@check
def fullHouse(cards):
    @check
    def fullHouseJoker(cards):
        jokers=cards.count(["JOKER"])
        if jokers > 3:
            return False
        if jokers == 3:
            for i in range(3):
                cards.remove(["JOKER"])
            card1=cards[0]
            for card in cards:
                if card[1] != card1[1]:
                    return False
        if jokers < 2:
            return False
        if jokers == 2:
            for i in range(2):
                cards.remove(["JOKER"])
            card1=cards[0]
            for card in cards:
                if card[1] != card1[1]:
                    return False
        return True

    if ["JOKER"] in cards:
        return fullHouseJoker(cards)
    card1=cards[0]
    itera=1
    card2=cards[itera]
    while card2[1]==card1[1]:
        try:
            card2=cards[itera]
        except IndexError:
            return False
        itera+=1
    c=cards
    c.remove(card1)
    c.remove(card2)
    card1counter=1
    card2counter=1
    for card in cards:
        if card[1] != card1[1]:
            if card[1] != card2[1]:
                return False
            else:
                card2counter+=1
        else:
            card1counter+=1
    if 3 not in [card1counter,card2counter]:
        return False
    return True

@noJoker
@check
def flush(cards):
    if sameSuit(cards):
        return True
    return False

@noJoker
@check
def straight(cards):
    cards=[getCardNumericValue(c) for c in cards]
    c=[x[1] for x in cards]
    c.sort()
    start=c[0]
    if start == 14:
        start=1
    for card in c[1:]:
        if card-1 is not start:
            return False
        start+=1
    return True

@check
def threeKind(cards):
    c=[card[1] for card in cards]
    for card1 in c:
        amount=0
        for card2 in c:
            if card1==card2:
                amount+=1
        if amount >= 3:
            return True
    return False

print(
    threeKind(
        [
            ["S","2"],
            ["C","3"],
            ["S","K"],
            ["S","K"],
            ["S","2"]
        ]
    )
)


'''
Two Pair:
    Two cards of one rank, two cards of another rank, and a kicker
    Ranked by the rank of the highest pair, then the lowest pair, then the kicker
One Pair:
    Two cards of one rank, three kickers
    Ranked by the rank of the pair, then the highest to lowest kickers
High Card/Nothing:
    Does not fall into any other category
    Ranked by the highest ranking card, then the second highest, and so on
'''