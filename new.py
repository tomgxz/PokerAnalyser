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
    Three cards of one rank and two kickers
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

import random

class Card():

    def __init__(self,suit,value):

        if value == "T": value = "10"

        self.__is_valid = True
        self.__suit = None
        self.__suit_numeric = None
        self.__value = None
        self.__value_numeric = None

        self.__sort_value = float("inf")

        if type(suit) == str: # if the given suit is an "absolute" value

            if suit not in SUITS: self.__is_valid = False
            else:
                self.__suit = suit
                self.__suit_numeric = SUIT_MAP[suit]

        elif type(suit) == int: # if the given suit is a numeric value

            if suit < 1 or suit > len(SUITS): self.__is_valid = False
            else:
                self.__suit_numeric = suit
                self.__suit = SUITS[suit-1]

        else: self.__is_value = False

        if type(value) == str: # if the given value is an "absolute" value

            if value not in VALUES: self.__is_valid == False
            else:
                self.__value = value
                self.__value_numeric = VALUE_MAP[value]

        elif type(value) == int: # if the given value is an "absolute" value

            if value < 1 or value > len(VALUES): self.__is_valid = False
            else:
                self.__value_numeric = value
                self.__value = VALUES[value-1]

        else: self.__is_valid = False

        if self.__is_valid: self.__sort_value = (self.__suit_numeric * 100) + self.__value_numeric

    
    def __eq__(self,other): return self.__sort_value == other.sort_value
    def __gt__(self,other): return self.__sort_value > other.sort_value
    def __lt__(self,other): return self.__sort_value < other.sort_value

    def __repr__(self): return f"{self.__suit}{self.__value}"


    @property
    def suit(self): return self.__suit
        
    @property
    def suit_n(self): return self.__suit_numeric
    
    @property
    def value(self): return self.__value
        
    @property
    def value_n(self): return self.__value_numeric
    
    @property
    def valid(self): return self.__is_valid

    @property
    def sort_value(self): return self.__sort_value

FULL_DECK = []
SUITS = ["S", "C", "H", "D"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

SUIT_MAP = {"S":1, "C":2, "H":3, "D":4}
VALUE_MAP = {"A":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13}

DECKS = ["royalFlush", "straightFlush", "fourKind", "fullHouse",
         "flush", "straight", "threeKind", "twoPair", "onePair", "highCard"]

for suit in SUITS: 
    for value in VALUES: 
        FULL_DECK.append(Card(suit,value))


def check(fn):
    def wrapper(*a, **kwa):

        check = a[0]

        if type(check) == Card: 
            if not check.valid: raise Exception(f"Invalid card: {check}")
            
        elif type(check) == list:
            if len(check) > 5: raise Exception(f"The deck of cards is too big! Expected <= 5, got {len(check)}")
            for card in check:
                if not card.valid: raise Exception(f"Invalid card: {check}")

        else: 
            print(type(check))
            raise Exception("Invalid check input")

        return fn(*a, **kwa)
    return wrapper

FULL_DECK.sort()


def sameSuit(cards):
    suit = cards[0].suit
    for card in cards:
        if card.suit != suit: return False
    return True

def sameValue(cards):
    value = cards[0].value
    for card in cards:
        if card.value != value: return False
    return True

@check
def flush(cards): 
    return sameSuit(cards)

@check
def straight(cards):
    by_val = sorted(cards, key = lambda x: x.value_n, reverse = True)
    start = by_val[0].value_n

    for card in by_val[1:]:
        if start == 14: start = 1

        if card.value_n != start+1: return False
        start += 1

    return True

@check
def occurenceList(cards):
    occ = {}

    for v in [x.value for x in cards]:
        if v in occ: occ[v] += 1
        else: occ[v] = 1

    return occ

@check
def kind(cards,count=4): 
    occ = occurenceList(cards)

    for k in occ:
        if occ[k] == count: return True

    return False


# HAND IDENTIFICATION
#region

@check
def royalFlush(cards): return straightFlush(cards) and cards[0].value == "10" and cards[4].value == "A"

@check
def straightFlush(cards): return straight(cards) and flush(cards)

@check
def fourKind(cards): return kind(cards,4)

@check
def fullHouse(cards):
    occ = occurenceList(cards)
    found3 = False;found2 = False

    for k in occ:
        if occ[k] == 3: found3 = True
        if occ[k] == 2: found2 = True

    return found3 and found2

# FLUSH HERE

# STRAIGHT HERE

@check
def threeKind(cards): return kind(cards,3)

@check
def twoPair(cards):
    occ = occurenceList(cards)
    count = 0

    for k in occ:
        if occ[k] == 2: count += 1

    return count == 2

@check
def onePair(cards):
    occ = occurenceList(cards)
    count = 0

    for k in occ:
        if occ[k] == 2: return True

    return False

#endregion


class Deck():
    
    def __init__(self, a:Card, b:Card, c:Card, d:Card, e:Card):
        
        self.__deck = sorted([a,b,c,d,e])
        self.__deck_byval:list[Card] = sorted(self.__deck, key = lambda x: x.value_n, reverse = True) # highest card first

        self.__occ = occurenceList(self.__deck)
        self.__hand, self.__rel_score = self.__get_hand()

    def __get_hand(self):
        deck = None; sc = 0

        if flush(self.__deck):
            if straightFlush(self.__deck):
                if royalFlush(self.__deck): 
                    deck = "royalFlush"
                    sc = 1
                else: 
                    deck = "straightFlush"
                    sc = self.__deck_byval[0].value_n
            else: 
                deck = "flush"
                sc = self.__deck_byval[0].value_n *100000000 + self.__deck_byval[1].value_n *1000000 + self.__deck_byval[2].value_n *10000 + self.__deck_byval[3].value_n *100 + self.__deck_byval[4].value_n 

        if straight(self.__deck): 
            deck="straight"
            sc = self.__deck_byval[0].value_n

        if onePair(self.__deck):

            if twoPair(self.__deck): 
                deck = "twoPair"
                
                higher = 0; lower = 0; kicker = 0
                
                for k in self.__occ:
                    num = VALUE_MAP[k]
                    if self.__occ[k] == 2:
                        if num > higher:
                            lower = higher
                            higher = num
                        else:
                            lower = num
                    else: 
                        kicker = num
                
                sc = higher * 10000 + lower * 100 + kicker

            elif threeKind(self.__deck):

                if fourKind(self.__deck): 
                    deck = "fourKind"

                    rep = 0; kicker = 0

                    for k in self.__occ:
                        num = VALUE_MAP[k]
                        if self.__occ[k] == 4: rep = num
                        else: kicker = num
                
                    sc = rep * 100 + kicker

                else: 
                    deck = "threeKind"

                    rep = 0; kicker_h = 0; kicker_l = 0

                    for k in self.__occ:
                        num = VALUE_MAP[k]
                        if self.__occ[k] == 3: rep = num
                        else:
                            if num > kicker_h:
                                kicker_l = kicker_h
                                kicker_h = num
                            else:
                                kicker_l = num
                
                    sc = rep * 10000 + kicker_h * 100 + kicker_l

            else: 
                deck = "onePair"

                rep = 0; kicker_h = 0; kicker_m = 0; kicker_l = 0

                for k in self.__occ:
                    num = VALUE_MAP[k]
                    if self.__occ[k] == 2: rep = num
                    else:
                        if num > kicker_h:
                            kicker_l = kicker_m
                            kicker_m = kicker_h
                            kicker_h = num
                        elif num > kicker_m:
                            kicker_l = kicker_m
                            kicker_m = num
                        else:
                            kicker_l = num
            
                sc = rep * 1000000 + kicker_h * 10000 + kicker_m * 100 + kicker_l

        if fullHouse(self.__deck): 
            deck = "fullHouse"

            three = 0; two = 0

            for k in self.__occ:
                num = VALUE_MAP[k]
                if self.__occ[k] == 3: three = num
                if self.__occ[k] == 2: two = num
        
            sc = three * 100 + two

        if deck == None: 
            deck = "highCard"
            sc = self.__deck_byval[0].value_n *100000000 + self.__deck_byval[1].value_n *1000000 + self.__deck_byval[2].value_n *10000 + self.__deck_byval[3].value_n *100 + self.__deck_byval[4].value_n 

        return deck, sc

    def __eq__(self,other):
        return self.__hand == other.hand
    
    @property
    def hand(self): return self.__hand

    @property
    def score(self): return self.__rel_score


def interperet(file):
    rows = []
    with open(file, "r") as f:

        for r in f:
            x = (r.strip("\n")).split(" ")
            rows.append(x)

    games = []

    for row in rows:
        h1 = []; h2 = []

        for card in row[:5]: h1.append(Card(card[1],card[0]))
        for card in row[5:10]: h2.append(Card(card[1],card[0]))

        games.append([h1,h2])

    return games


def calcWin(h1,h2): # true = h1 win, false = h2 win, null = draw
    h1 = Deck(*h1)
    h2 = Deck(*h2)

    io1 = DECKS.index(h1.hand)
    io2 = DECKS.index(h2.hand)

    if io1 < io2: return True
    elif io1 > io2: return False
    else:
        if h1.score > h1.score: return True
        elif h1.score < h1.score: return False

    return None

decks = interperet("C:\\Users\\thoma\\Documents\\GitHub\\PokerAnalyser\\p054_poker.txt")

player1_wins = 0
player2_wins = 0
draws = 0

for game in decks: 
    res = calcWin(game[0], game[1])
    if res == None: draws += 1
    elif res: player1_wins += 1
    elif not res: player2_wins += 1
