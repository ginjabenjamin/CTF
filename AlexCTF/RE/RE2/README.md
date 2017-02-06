We receive an ELF 64-bit binary that is stripped. Binary Ninja sadly only showed us '_start'. We had more success with Radare2, which allowed us to look at the program.

	[0x00400d7a]> s main
	[0x00400b89]> pdf
	/ (fcn) main 301
	|   main ();
	|           ; var int local_70h @ rbp-0x70
	|           ; var int local_64h @ rbp-0x64
	|           ; var int local_60h @ rbp-0x60
	|           ; var int local_50h @ rbp-0x50
	|           ; var int local_21h @ rbp-0x21
	|           ; var int local_20h @ rbp-0x20
	|           ; var int local_14h @ rbp-0x14
	|           ; DATA XREF from 0x00400a7d (entry0)
	|           0x00400b89      55             push rbp
	|           0x00400b8a      4889e5         mov rbp, rsp
	|           0x00400b8d      53             push rbx
	|           0x00400b8e      4883ec68       sub rsp, 0x68               ; 'h'
	|           0x00400b92      897d9c         mov dword [rbp - local_64h], edi
	|           0x00400b95      48897590       mov qword [rbp - local_70h], rsi
	|           0x00400b99      837d9c02       cmp dword [rbp - local_64h], 2 ; [0x2:4]=0x102464c
	|       ,=< 0x00400b9d      7438           je 0x400bd7

Main shows us that we need to pass exactly one argument to the program, otherwise it will display the usage and exit. Continuing to examine main() we see a series of function calls:

	fcn.00400d3d - calls fcn.00400dac twice
	fcn.00400d9a
	fcn.00400b56  - Prints 'Better luck next time' and exists; this is our jump to avoid
	fcn.00400d7a
	fcn.00400b73 (so the flag must be checked prior to this call)
		'You should have the flag…'

In trying to figure out what the local variables are (RBP-0x8, RBP-0x21 and other RBP related offsets), we step through the program to check values at time of execution. Changes to our input string do not seem to change

RAX: 0x4 
RBX: 0x7fffffffe448 --> 0x5f534c0062626262 ('bbbb')
RCX: 0x448 
RDX: 0x10 
RSI: 0x7fffffffe448 --> 0x5f534c0062626262 ('bbbb')
RDI: 0x7fffffffe448 --> 0x5f534c0062626262 ('bbbb')

After executing an address load from RBX+RAX*1, we see an interesting string in RDX:

![alt text](https://github.com/ginjabenjamin/CTF/blob/master/AlexCTF/RE/RE2/RE2a.png "OLOC_SL")

0x4f4c4f435f534c00 works out to 'OLOC_SL'. This does not prove to be the flag, even flipping it for endianess (which would have been weird since the 00 was already at the end of the value). Continuing through the program, we see some arithmetic operations against our input and the RDX value. Eventually, we get to a compare:

![alt text](https://github.com/ginjabenjamin/CTF/blob/master/AlexCTF/RE/RE2/RE2b.png "Key check")


It is comparing our input 'b' against 'A'. This must be testing against the key values. We add a breakpoint at the CMP operation and continue looping through. Since we do not have the correct values, we use JUMP to skip the call to 0x400b64, which would terminate the program:

Breakpoint 3, 0x0000000000400c75 in ?? ()
gdb-peda$ jump *0x400c83
gdb-peda$ i r dl al
dl             0x62	0x62
al             0x4c	0x4c
gdb-peda$ c

Next up 0x4c = L. 'ALEX' is shaping up. After the 'X', we were expecting a curly brace, but instead get 'C'. Seeing this, we thought to try 'ALEXCTF':

# ./re2 ALEXCTF
You should have the flag by now

So that must be the flag!
