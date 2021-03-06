RE: Skipper

```
0x0804a08e      lea eax, dword [ebp - local_40ch]
0x0804a094      push eax

// The first call:
0x0804a095      call sub.memset_871        ; void *memset(void *s, int c, size_t n);
0x0804a09a      add esp, 0x10
0x0804a09d      sub esp, 8
0x0804a0a0      lea eax, dword [ebp - local_40ch]
0x0804a0a6      push eax
0x0804a0a7      push str.Computer_name:__s_n ; str.Computer_name:__s_n ; "Computer name: %s." @ 0x804a31f
0x0804a0ac      call sym.imp.printf        ; int printf(const char *format);
0x0804a0b1      add esp, 0x10
0x0804a0b4      sub esp, 8

// Test string:
0x0804a0b7      push str.hax0rz__ ; str.hax0rz__ ; "hax0rz!~" @ 0x804a332

0x0804a0bc      lea eax, dword [ebp - local_40ch]
0x0804a0c2      push eax

// String comparison:
0x0804a0c3      call sym.imp.strcmp        ; int strcmp(const char *s1, const char *s2);
0x0804a0c8      add esp, 0x10

// Test:
0x0804a0cb      test eax, eax
0x0804a0cd      je 0x804a0f3
```

By examining the file, we can see that it is checking various values; hostname needs to be 'hax0rz!~', OS Version needs to be '2.4.31' and  CPU needs to be 'AMDisbetter!'. Passing these three tests leads to 0x08048a63 which seems to do a lot of operations against a few character values, and presumably returns the flag. 

```
// Start of function related to flag generation
0x08048a63      push ebp
0x08048a64      mov ebp, esp
0x08048a66      sub esp, 0x68               ; 'h'
0x08048a69      mov eax, dword gs:[0x14]    ; [0x14:4]=1
0x08048a6f      mov dword [ebp - local_ch], eax
0x08048a72      xor eax, eax

// Loading values that will be decoded to flag
0x08048a74      mov dword [ebp - local_35h], 0x34373738
0x08048a7b      mov dword [ebp - local_31h], 0x39643462
0x08048a82      mov dword [ebp - local_2dh], 0x35343763
0x08048a89      mov dword [ebp - local_29h], 0x34313461
0x08048a90      mov dword [ebp - local_25h], 0x35356338
0x08048a97      mov dword [ebp - local_21h], 0x66383439
0x08048a9e      mov dword [ebp - local_1dh], 0x36336235
0x08048aa5      mov dword [ebp - local_19h], 0x37336636
0x08048aac      mov dword [ebp - local_15h], 0x65643039
0x08048ab3      mov dword [ebp - local_11h], 0x38623035
```

Since we know that the flag is returned by the application, based on the challenge description, we attempt to patch the executable at its first call to 0x08048871 (call sub.memset_871 in radare2) and replace it with a call to 0x08048a63. Using the patched binary, we score our flag:

Result: FLAG:f51579e9ca38ba87d71539a9992887ff
