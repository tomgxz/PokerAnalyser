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

def getCards():
    deck=[]
    suits=["S","C","H","D"]
    cards=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    for suit in suits:
        for card in cards:
            deck.append([card,suit])
    return deck

def check(fn):
    def wrapper(*a,**kwa):
        if type(a[0]) == list:
            checkValid(cards=a[0])
        elif type(a[0]) == str:
            checkValid(card=a[0])
        return fn(*a,**kwa)
    return wrapper

def sortDeck(cards):
    for i in range(len(cards)):
        cards[i]=getCardNumericValue(cards[i])
    cards.sort()
    for i in range(len(cards)):
        cards[i]=getCardProperValue(cards[i])
    return cards

def getCardNumericValue(card):
    if card[0] == "A":
         return [14,card[1]]
    if card[0] == "J":
         return [11,card[1]]
    if card[0] == "Q":
         return [12,card[1]]
    if card[0] == "K":
         return [13,card[1]]
    return [int(card[0]),card[1]]

def getCardProperValue(card):
    if card[0] == 14:
         return ["A",card[1]]
    if card[0] == 11:
         return ["J",card[1]]
    if card[0] == 12:
         return ["Q",card[1]]
    if card[0] == 13:
         return ["K",card[1]]
    return [str(card[0]),card[1]]

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
    suit=cards[0][1]
    for card in cards:
        if card[1]!=suit:
            return False
    return True

def sameRank(cards):
    rank=cards[0][0]
    for card in cards:
        if card[0]!=rank:
            return False
    return True

def interperet(file):
    rows=[]
    with open(file,"r") as f:
        

        for r in f:
            x = (r.strip("\n")).split(" ")
            rows.append(x)

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j]=[rows[i][j][0],rows[i][j][1],]
 
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if rows[i][j][0] == "T":
                rows[i][j][0] = "10"


    newrows=[]
    for row in rows:
        h1=row[:5]
        h2=row[5:10]
        newrows.append([h1,h2])
    
    return newrows

@check
def straightFlush(cards):  
    return straight(cards) and flush(cards)

@check
def fourKind(cards):
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

@check
def flush(cards):
    if sameSuit(cards):
        return True
    return False

@check
def straight(cards):
    cards=[getCardNumericValue(c) for c in cards]
    c=[x[0] for x in cards]
    c.sort()
    start=c[0]
    if start == 14:
        start=1
    for card in c[1:]:
        if card is not start+1:
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

@check
def twoPair(cards):
    c=[card[1] for card in cards]
    pair1,pair2=False,False
    for card1 in c:
        amount=0
        for card2 in c:
            if card1==card2:
                amount+=1
        if amount >= 2:
            pair1=card1
    for card1 in c:
        if card1 == pair1:
            continue
        amount=0
        for card2 in c:
            if card2 == pair1:
                continue
            if card1 == card2:
                amount+=1
        if amount >= 2:
            pair2=card1
    if pair1 is not False and pair2 is not False:
        return True
    return False

@check
def onePair(cards):
    c=[card[1] for card in cards]
    for card1 in c:
        amount=0
        for card2 in c:
            if card1==card2:
                amount+=1
        if amount >= 2:
            return True
    return False


def getDeckType(deck):
    itera=0
    for command in commands:
        if command(deck.copy()) == True:
            return itera
        itera+=1
    return itera

commands=[straightFlush,fourKind,fullHouse,flush,straight,threeKind,twoPair,onePair]

def getSortedRanks(cards):
    cards=[getCardNumericValue(c) for c in cards]
    cards=[x[0] for x in cards]
    cards.sort()
    return cards

def straightFlushScore(cards):
    cards=getSortedRanks(cards)

    for card in enumerate(cards):
        cards[card[0]] = [card[1],"H"]
    
    return [getCardProperValue(cards[-1])[0]]

def fourKindScore(cards):
    returnList=[]
    start=cards[0]
    added=True
    for card in cards[1:]:
        if card[0] == start[0] and added:
            returnList.insert(0,card[0])
            added=False
        elif card[0] != start[0] and not added:
            returnList.append(card[0])
    if len(returnList) < 1:
        returnList.append(start[0])
        start=cards[-1]
        for card in cards[:-1]:
            if card[0] == start[0]:
                returnList.insert(0,card[0])
                break
    return returnList

def fullHouseScore(cards):
    returnList=[]

    cards=getSortedRanks(cards)

    for card in cards:
        if cards.count(card) == 3:
            returnList.insert(0,card)
            break
    for card in cards:
        if cards.count(card) == 2:
            returnList.append(card)
            break

    return returnList

def flushScore(cards):
    cards=getSortedRanks(cards)
    cards.reverse()
    return cards

def straightScore(cards):
    cards=getSortedRanks(cards)
    cards.reverse()
    return [cards[0]]

def threeKindScore(cards):
    returnList=[]

    cards=getSortedRanks(cards)
    cards.reverse()

    for card in cards:
        if cards.count(card) == 3:
            returnList.append(card)
            break

    cards=[x for x in cards if x != card]
    
    for card in cards:
        returnList.append(card)
    
    returnList.sort()
    returnList.reverse()

    return returnList

def twoPairScore(cards):
    returnList=[]

    cards=getSortedRanks(cards)
    cards.reverse()

    for card in cards:
        if cards.count(card) == 2:
            returnList.append(card)
            cards=[x for x in cards if x != card]
    
    returnList.append(cards[0])

    return returnList

def onePairScore(cards):
    returnList=[]

    cards=getSortedRanks(cards)
    cards.reverse()

    for card in cards:
        if cards.count(card) == 2:
            returnList.append(card)
            cards=[x for x in cards if x != card]
    
    for card in cards:
        returnList.append(card)

    return returnList

def highCardScore(cards):
    cards=getSortedRanks(cards)
    cards.reverse()
    return cards


detectioncommands=[straightFlushScore,fourKindScore,fullHouseScore,flushScore,straightScore,threeKindScore,twoPairScore,onePairScore,highCardScore]

commandNames=["straightFlush","fourKind","fullHouse","flush","straight","threeKind","twoPair","onePair"]

def calcWin(h1,h2):
    h1v=getDeckType(h1)
    h2v=getDeckType(h2)

    if h1v == h2v:
        h1s=detectioncommands[h1v](h1)
        h2s=detectioncommands[h2v](h2)
        for i in range(len(h1s)):
            try:
                if h1s[i] > h2s[i]:
                    return True
                elif h2s[i] > h1s[i]:
                    return False
                else:
                    continue
            except IndexError as e:
                print(commandNames[h1v])
                print(h1)
                print(h2)
                print(h2s, h1s, i)
                raise SystemExit
        return None
    else:
        if h1v > h2v:
            return True
        return False
    return None



decks=interperet("p054_poker.txt")

for game in decks:
    print(calcWin(game[0],game[1]))
















    #break
