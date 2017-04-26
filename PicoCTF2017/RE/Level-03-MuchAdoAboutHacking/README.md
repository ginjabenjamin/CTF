# Much Ado About Hacking

We have Shakespeare Programming Language (https://en.wikipedia.org/wiki/Shakespeare_Programming_Language) source code and a target ending string that presumably is the result of inputting the key. Since this is a reversing challenge, we probably need to determine the algorithm and reverse it so that our output is our input.

Initially, we tried to use a Python SPL interpreter to output C code. Unfortunately, that interpreter blew up halfway through the translation. Turning to the hints, we see that they specify an exact version of the SPL compiler to use, which saved some further investigation. Using the SPL compiler specified in the hint, we are able to get a working executable as well as source code in C.  The executable seems to just take a user input, but does not immediately exit. Loading up Binary Ninja, we start reversing to determine what input is needed and how to get to our target ending. 

The reversing is facilitated not just by access to the source code, but also by having all function calls in place. The only downside is that everything is lumped into main() and since we have lost our code comments, correlating is a little tedious. But, even without the source code, the executable is highly readable as it is fairly linear.

## Act I, Scene I

![alt text](https://github.com/ginjabenjamin/CTF/blob/master/PicoCTF2017/RE/Level-03-MuchAdoAboutHacking/acti_scene1.png "Act i, Scene i")

By the end of Act I, Scene I (0x00000ebe) we see three characters with zero values, Achilles (foreshadowing? sadly, no) with a value of 32 and Cleopatra a value of 96.


## Act I, Scene II

Act I, Scene II is essentially two parts. The first part takes user input, adding to Benedick, until there is a space (which explains why our command-line tampering attempts were not successful):

![alt text](https://github.com/ginjabenjamin/CTF/blob/master/PicoCTF2017/RE/Level-03-MuchAdoAboutHacking/acti_sceneii.png "Act i, Scene ii")

![alt text](https://github.com/ginjabenjamin/CTF/blob/master/PicoCTF2017/RE/Level-03-MuchAdoAboutHacking/acti_sceneii_binja "Act i, Scene ii Binja")


The second part, (after 0x00000fa7 = jne xfae) subtracts one from Beatrice. 

![alt text](https://github.com/ginjabenjamin/CTF/blob/master/PicoCTF2017/RE/Level-03-MuchAdoAboutHacking/acti_sceneiib.png "Act i, Scene ii, Part 2")

Since Beatrice is basically an input length counter, we are stripping--really skipping since we are processing string backwards--the space. So far, we have initialized some variables (our characters) in Scene I, and read a user input to Benedick, until we get a space, in Scene II.

## Act I, Scene III

This scene is where the magic happens. Following the source code makes it easier to understand the algorithm:

	Benedick -= Achilles 
	Beatrace -= 1    // Exit Beatrice
	Don John = Benedick    // Exit Don John
	Benedick += Don Pedro
	Benedick = Benedick % Cleopatra
	Don Pedro = Don John
	Benedick += Achilles

Since Achilles is 32 and remains unchanged, and Cleopatra is 96 and also unchanged, Don John is [character - 32] which is our seed value and will be a running increment (Benedick += Don Pedro; Don Pedro = Don John).

This scene loops based on Beatrice not equaling zero, so we are processing our input string backwards, which will result in a reversed output string.

We can now reproduce our reversed algorithm and validate that we have replicated it successfully. Once this is complete, we reverse the algorithm so that we can use the ending as our input, and receive the flag:

```
# cat ans.py 
#!/usr/bin/env python

donpedro = 0
achilles = 32
cleopatra = 96

ending = 'tu1|\h+&g\OP7@% :BH7M6m3g='
flag = ''

beatrice = len(ending)
for benedick in ending:
    x = ord(benedick)
    x = x - achilles
    x = x - donpedro

    # Assigning Don Pedro here, we can eliminate Don John
    donpedro = x

	# To reverse the algorithm, we add cleopatra (96) before the modulo operation
    x = (x + cleopatra) % cleopatra

    # Modulo to handle negative values
    benedick = chr((x + achilles) % 192)

    flag += benedick

# Reverse our flag string
print flag[::-1]+' '
```

```
# python ans.py 
Its@MidSuMm3rNights3xpl0!t 
# 
```
