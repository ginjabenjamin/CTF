# Broadcast

Searching for the provided variables, we found a promising article (http://www.di-mgt.com.au/t_bdRsaCrack.c.html) that discussed using Chinese Remainder Theorem and Guass's Method for an exponent of 3 sent to multiple recipients. But, the program does not determine our message, so back to the drawing board.

Finally, we discovered a writeup that mentions 'Broadcast Attack,' or 'Hastad's Attack,' and includes a python script that works: https://github.com/JulesDT/RSA-Hastad

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        RSA Hastad Attack         
         JulesDT -- 2016          
         License GNU/GPL          
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Decoded Hex :
62726f6164636173745f776974685f736d616c6c5f655f69735f6b696c6c65725f3236353238303734333930
---------------------------
As Ascii :
broadcast_with_small_e_is_killer_26528074390
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

Additionally, we found Feather Duster (https://github.com/nccgroup/featherduster) which includes a Python module, cryptanalib, that also makes the Hastads Attack easy, as well as many other crypto attacks:

```
hastad_broadcast_attack(key_message_pairs, exponent)
    Uses Hastad's broadcast attack to decrypt a message encrypted under multiple
    unique public keys with the same exponent, where the exponent is lower than
    the number of distinct key/ciphertext pairs.
    
    key_message_pairs should be in the form of a list of 2-tuples like so:
    [(ciphertext1, pubkey1), (ciphertext2, pubkey2), (ciphertext3, pubkey3)]
```
