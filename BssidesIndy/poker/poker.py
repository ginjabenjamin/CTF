#/usr/bin/env python
from pwn import *

TIMEOUT = 10
GAME = 0

# Divide line of cards and return as a list
def parseCard(hand):
    for line in hand.split('\n'):
        if(line.startswith('Cards:')):
            line = line[7:21]
            return line.split(' ')

# Extract amount of money we have
def parseMoney(text):
    for line in text.split('\n'):
        if(line.startswith('Money:')):
            return int(line.split('$')[1])

# Figure out what to discard, returning as a list
def replaceCards(hand):
    # List for value, list for suit
    val = []    # Card values
    suit = []   # Card suits

    discard = {}

    for card in hand:
        discard[card] = 1
        val += card[0]
        suit += card[1]

    # Check for possible flush
    flush = ''

    if(suit.count('S') > 2 
        or suit.count('D') > 2 
        or suit.count('H') > 2
        or suit.count('C') > 2
    ):
        flush = max(set(suit), key = suit.count)

    # Check for multiple cards
    pair = max(set(val), key = val.count)
    pairCount = val.count(pair)

    # Determine which to discard
    for card in hand:
        # Keep pairs
        if(pairCount > 1):
            if(card[0] == pair):
                discard[card] = 0
        # Try for flush
        elif(card == flush):
            discard[card] = 0
        else:
            # Otherwise, check for paints...
            if(card[0] in ['A', 'J', 'Q', 'K']):
                discard[card] = 0

    ret = []
    for c, d in discard.iteritems():
        if(d == 1):
            x = hand.index(c) + 1
            ret.append(x)

    return ret

# Start a game...
def startGame():
    global GAME

    print '[+] New game...', GAME
    p = remote('challenge.ctf.wtf', 11235)

    # Start game
    p.recvuntil('>')

    # Eventually, we exploited unseeded randomness
    # and used game 794, since we can start with a winning four of a kind
    # p.sendline(str(GAME))
    p.sendline('794')
    GAME += 1
    p.recvuntil('10000):', timeout=TIMEOUT)

    # Send initial bet
    p.sendline('1000')
    return p


p = startGame()

# This will be populated with winning hands…
#hands = {1: [4, 5], 2: [1, 5, 3]}

# Or, we can jump the gun:
hands = {512: [1, 2, 3], 1: [4, 5], 2: [1, 5, 3], 3: [5, 1, 3, 4], 5: [2, 5], 8: [1, 3, 4], 9: [5, 1, 4], 523: [4, 2, 1], 13: [2, 4, 1], 14: [4, 1, 2], 15: [5, 3, 4], 528: [5, 1, 4], 17: [3, 4, 1], 530: [2, 4, 5], 19: [3, 5, 4], 20: [4, 5, 2], 533: [1, 3, 2], 25: [1, 3, 5], 538: [3, 2, 5, 1], 540: [3, 5, 4], 541: [4, 3, 1], 517: [5, 2, 4, 3], 32: [2, 5, 4, 1], 33: [1, 2, 5], 34: [5, 2, 3], 36: [1, 3, 5], 37: [2, 3], 38: [4, 3, 5], 552: [1, 4, 5], 41: [2, 5, 4], 554: [5, 3, 1], 555: [5, 4, 1], 44: [1, 5, 3, 2], 46: [5, 3, 2], 559: [5, 3, 1], 48: [2, 4, 3], 49: [2, 4, 1], 53: [5, 1, 4], 55: [4, 3, 5], 56: [1, 4, 2], 57: [1, 4, 3], 60: [4, 5, 1], 62: [2, 1, 5], 68: [1, 2, 4], 69: [5, 2, 4, 1], 72: [2, 5, 1], 74: [5, 1, 4], 75: [3, 2, 1], 77: [1, 2, 3, 5], 81: [1, 3, 2], 514: [4, 5], 83: [4, 1, 3, 2], 84: [1, 2, 4, 3], 85: [3, 2, 1], 86: [4, 2, 1], 88: [3, 4, 1], 527: [4, 3, 1], 92: [2, 3], 94: [3, 1, 2, 4], 101: [4, 5], 103: [1, 3, 2], 106: [3, 1, 4], 108: [5, 2], 109: [5, 2, 1], 515: [2, 4, 3], 113: [4, 3, 1], 114: [2, 1, 3], 115: [3, 4], 119: [4, 5, 3], 121: [4, 3, 2, 5], 123: [3, 2, 1], 124: [5, 2, 4], 125: [2, 4, 1], 127: [4, 2, 1], 128: [5, 1, 4], 132: [3, 2, 4], 137: [4, 3, 2], 142: [4, 3, 1, 5], 145: [5, 1], 146: [5, 3, 1], 148: [3, 1, 5], 149: [1, 4, 2], 151: [3, 2], 153: [5, 4, 1, 2], 154: [1, 4, 5], 155: [5, 3, 1], 156: [1, 2, 4], 162: [1, 4, 5], 164: [1, 2, 4, 3], 165: [2, 1, 5], 167: [5, 2, 3], 171: [4, 1, 3], 172: [2, 1, 5], 567: [4, 2, 1, 3], 179: [5, 1, 3], 180: [5, 3, 1], 182: [3, 4, 1], 185: [3, 5, 1], 189: [4, 3, 1], 190: [2, 3, 1], 191: [5, 4, 3], 194: [3, 2, 1], 197: [3, 1], 200: [3, 5, 1], 202: [4, 2, 3], 203: [5, 4, 1], 546: [1, 5, 4], 208: [2, 3, 4], 209: [5, 1, 4], 211: [4, 2, 1], 212: [4, 1, 3], 214: [1, 3, 5], 216: [1, 5, 3], 217: [4, 2, 5], 218: [4, 2, 1], 219: [5, 3, 4], 221: [1, 4, 2], 222: [4, 3, 5], 549: [3, 5, 4], 224: [3, 5], 225: [2, 4, 1], 231: [1, 3, 5], 234: [2, 5], 235: [2, 4, 5], 236: [5, 3], 241: [3, 2, 4, 1], 242: [5, 1, 2], 243: [5, 1, 2], 246: [1, 3], 247: [5, 1, 4, 3, 2], 254: [5, 1, 2], 259: [1, 3, 4], 260: [2, 3, 5], 261: [5, 2, 1], 520: [1, 2, 3], 264: [3, 5, 2, 1, 4], 556: [2, 1, 4], 270: [3, 4, 1, 2, 5], 272: [2, 3, 5], 274: [1, 4, 2], 275: [5, 2, 4, 1], 276: [4, 3, 5], 277: [5, 1, 3], 279: [1, 4, 5, 3], 280: [3, 4, 5], 283: [2, 4], 285: [2, 5, 4], 560: [3, 4, 2], 290: [5, 3, 1], 291: [4, 3, 1, 2], 292: [2, 4, 1, 5, 3], 561: [4, 5, 3], 298: [4, 1, 2], 299: [5, 3, 1, 4], 300: [5, 3, 1], 302: [1, 3, 5], 303: [4, 2, 3], 304: [2, 1, 3], 307: [2, 5, 3], 309: [3, 1, 4], 310: [5, 4, 2, 3], 311: [2, 3, 5, 4], 312: [2, 3, 5], 317: [2, 4, 5], 318: [1, 3, 5], 325: [1, 3, 4], 326: [3, 4], 331: [2, 1, 5], 332: [1, 4, 3, 5], 335: [2, 3, 4], 336: [1, 2, 5], 337: [5, 2, 4], 339: [2, 4, 5], 340: [1, 5, 4], 341: [5, 2, 4, 1], 346: [3, 5, 2, 1], 347: [5, 2, 4], 350: [4, 1], 352: [5, 1, 3], 355: [5, 2, 4], 356: [1, 2, 5], 357: [1, 2], 359: [5, 4, 1], 363: [2, 1, 3, 5], 367: [2, 4, 1, 3], 368: [5, 1], 371: [3, 4, 5], 374: [5, 3, 4], 375: [1, 3, 4], 376: [1, 2, 5], 558: [2, 1, 5], 380: [4, 5, 3, 2], 384: [4, 5, 2], 385: [4, 3, 5], 386: [1, 5, 4], 388: [3, 1, 4], 390: [5, 4, 3, 1], 391: [2, 5, 4, 1], 392: [5, 4, 1], 396: [4, 3], 397: [5, 4, 1, 3], 400: [2, 4, 1], 403: [3], 405: [1, 2, 3], 409: [2, 1, 5], 411: [3, 5, 4], 413: [4, 2, 3], 415: [1, 5, 4], 416: [2, 5], 418: [5, 3, 4], 420: [4, 2, 3], 423: [3, 1, 4], 425: [1, 3, 4], 429: [5, 4], 430: [2, 1, 4], 432: [1, 5, 4], 434: [2, 1, 3], 436: [4, 1, 5], 437: [3, 2, 4], 439: [3, 4, 1], 440: [4, 3, 5], 443: [2, 5, 1], 446: [3, 2, 5], 449: [4, 1, 5], 450: [2, 3, 1], 451: [5, 1, 2], 454: [3, 5, 4, 1], 456: [3, 5, 1], 457: [5, 2, 1], 462: [2, 3, 1, 4], 464: [1, 3, 2], 465: [3, 2, 1, 5, 4], 468: [1, 2, 5], 472: [2, 4, 5], 473: [3, 5, 4], 474: [4, 5, 1, 2], 476: [5, 4, 3], 479: [1, 5, 3], 480: [3, 2, 5], 489: [1, 2, 4, 3, 5], 493: [2, 3, 1], 495: [4, 2, 3], 496: [5, 2, 3], 498: [2, 5], 501: [4, 3, 5], 502: [2, 1, 4], 504: [1, 3, 5], 505: [3, 5, 1], 507: [3, 5, 2], 509: [3, 2, 4]}

handCounter = 1

while(True):
    # Shuffling...
    pout = p.recvline(timeout=TIMEOUT)

    # Grab up to 'Cards to replace' prompt
    pout = p.recvuntil('replace:', timeout=TIMEOUT)

    # Check if we know the play
    if(hands.get(handCounter) is not None):
        print '> Known Hand', handCounter, hands.get(handCounter)
        replace = hands.get(handCounter)
    else:
        # Determine cards
        hand = parseCard(pout)
        print hand

        # Find cards to discard
        replace = replaceCards(hand)

    print 'Replacing: ', str(len(replace)), replace
    p.sendline(str(len(replace)))

    # Submit discards
    for r in sorted(replace):
        # print 'Replace: ', r
        x = p.recvuntil('(1-5):', timeout=TIMEOUT)
        p.sendline(str(r))

    # Should be final cards...
    pout = p.recvline(timeout=3)
    # print 'Hand: ', pout

    # Should be result
    pout = p.recvline(timeout=3)
    print 'Result: ', pout

    # If we win, add to hands{}
    if('LOSER' not in pout):
        print 'Won: ', handCounter, replace
        hands[handCounter] = replace

        # Kludgy force to dump flag
        if(handCounter == 189):
            pout = p.recvall(timeout=TIMEOUT)
            print pout
            break
    else:
        print 'Lost: ', handCounter

    handCounter += 1
    restart = 0

    # Should receive cards (updated hand), result, winnings and win/loss line
    # followed by the next prompt to bet
    try:
        pout = p.recvuntil('10000):', timeout=TIMEOUT)

        # Check our funds
        money = parseMoney(pout)

        # Check if we know the result (true bet)
        if(hands.get(handCounter) is not None):
            print '[+] Bet Known hand'
            if(money <= 10000):
                bet = money
            else:
                bet = 10000
        else:
            print '[-] Bet Unknown hand'
            bet = 1

        print('Betting: %d of %d' % (bet, money))

        # Kludgy bit above because this didn't work
        if(money >= 1000000):
            print pout
            break

        # Submit bet
        p.sendline(str(bet))
    except:
        print pout
        p = startGame()
        handCounter = 1

    # If we have 250 winning hands, restart so we can bet
    if(len(hands) >= 250 and handCounter >= 250):
        p = startGame()
        restart = 1
        handCounter = 1
        print hands
