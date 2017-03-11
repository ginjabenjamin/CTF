# Poker

A teammate solved this before I did, but I had already sunk enough hours that I felt compelled to finish. He also politely outlined his strategy which was far smarter than mine. His suggestion was learning which hands were winners/losers and bet accordingly. Basically, even though I knew that there was no seeding, making games completely repeatable, I was trying to cycle through the games to see if one was easier to beat than the others.

Upside of my failed strategy was finding game #794. First hand leads to four of a kind, bumping you to $25k. By this time I had already sorted out my restarting of games and battling with pwnlib's I/O and connection nonsense (seriously, dropped connections should output whatever it got back last).

In any event, the final script also had other hacky nonsense like a fully built 'win dictionary' and a hardcoded stop so that I could force the receive all and dump the flag. Probably need to store off my bet and bankroll to determine if it is a winning hand that will result in the flag, but my script eventually got it done…

```
Won:  185 [3, 5, 1]
[-] Bet Unknown hand
Betting: 1 of 994896
['6S', '9S', '9H', 'KS', '5D']
Replacing:  3 [4, 1, 5]
Result:  LOSER!

Lost:  186
[-] Bet Unknown hand
Betting: 1 of 994895
['QC', 'AH', '3H', '3D', '2H']
Replacing:  3 [2, 1, 5]
Result:  LOSER!

Lost:  187
[-] Bet Unknown hand
Betting: 1 of 994894
['7D', '2C', 'KH', '9H', 'QH']
Replacing:  3 [4, 1, 2]
Result:  LOSER!

Lost:  188
[+] Bet Known hand
Betting: 10000 of 994893
> Known Hand 189 [4, 3, 1]
Replacing:  3 [4, 3, 1]
Result:  THREE OF A KIND

Won:  189 [4, 3, 1]
[+] Receiving all data: Done (53B)
[*] Closed connection to challenge.ctf.wtf port 11235
Winnings: $30000
INDY{you_g0ts_da_r0y@l_fl0000000sh}
```
