This challenge seemed related to another challenge I had recently done and failed to get, so I did not start confident that I would get it. Trying to chase down weak primes, I did some googling and turned up an article that was key to solving it:

https://m0x39.blogspot.com/2012/12/0x00-introduction-this-post-is-going-to.html

After dealing with Nettle not properly linking libraries, I managed to get pkcs1-conv working. This was critical to identifying the modulus for public and private keys (n). 
```
	# pkcs1-conv key.pub | xxd
	00000000: 2831 303a 7075 626c 6963 2d6b 6579 2839  (10:public-key(9
	00000010: 3a72 7361 2d70 6b63 7331 2831 3a6e 3530  :rsa-pkcs1(1:n50
	00000020: 3a52 a99e 249e e7cf 3c0c bf96 3a00 9661  :R..$...<...:..a
	00000030: 772b c9cd f6e1 e3fb fc6e 44a0 7a5e 0f89  w+.......nD.z^..
	00000040: 4457 a9f8 1c3a e132 ac56 83d3 5b28 ba5c  DW...:.2.V..[(.\
	00000050: 3242 4329 2831 3a65 333a 0100 0129 2929  2BC)(1:e3:...)))
```

There were a few false values of 'n' identified along the way. Ultimately, paying attention to the format allowed me to recognize that the article for 768-bit keys would have a different length for the value of 'n'. I assumed that the first byte after the colon separator (R = 0x52) should be skipped, and to start with byte 33, per the article; he was not doing that just because his value was zero. I then adjusted the range to end at the closing parenthesis (0x29). 
```
	# pkcs1-conv key.pub | xxd -s 33 -l 50 -p
	52a99e249ee7cf3c0cbf963a009661772bc9cdf6e1e3fbfc6e44a07a5e0f
	894457a9f81c3ae132ac5683d35b28ba5c324243
```
Using Python, we convert to an integer:
```
	>>> int("0x52a99e249ee7cf3c0cbf963a009661772bc9cdf6e1e3fbfc6e44a07a5e0f894457a9f81c3ae132ac5683d35b28ba5c324243", 16)
	833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019L
	>>> 
```
We then check FactorDB (http://www.factordb.com/index.php?query=833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019), which fortunately contained our factors. Unlike our false values, our candidate modulus value resulted in only two primes, which support the RSA algorithm since n = p * q.

Two 60 digit primes, which we will use for values of 'p' and 'q'. 

	Factors:
	  p = 863653476616376575308866344984576466644942572246900013156919
	  q = 965445304326998194798282228842484732438457170595999523426901

Armed with n, p and q, we are ready to check for the private key exponent (d):
```
	root@kali:~/Projects/CTF/AlexCTF/crypt# python rsatool.py -n 833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019 -p 863653476616376575308866344984576466644942572246900013156919 -q 965445304326998194798282228842484732438457170595999523426901
	Using (p, q) to initialise RSA instance
	
	n =
	52a99e249ee7cf3c0cbf963a009661772bc9cdf6e1e3fbfc6e44a07a5e0f894457a9f81c3ae132ac
	5683d35b28ba5c324243
	
	e = 65537 (0x10001)
	
	d =
	33ad09ca06f50f9e90b1acae71f390d6b92f1d6d3b6614ff871181c4df08da4c5f5012457a643094
	05eaecd6341e43027931
	
	p =
	899683060c76b9c0de581a69e0ea9d91bed1071beb1d924a37
	
	q =
	99cde74aedee87adffdd684cbc478e759870b4f20692f65255
```

Testing the private key exponent (d) with the key modulus (n), we attempt to crack the flag file, using rsacrack. The format being 'rsacrack -d [value of d] [hex value of n]':
```
	# base64 -d flag.b64 | python rsacrack.py -d 33ad09ca06f50f9e90b1acae71f390d6b92f1d6d3b6614ff871181c4df08da4c5f5012457a64309405eaecd6341e43027931 0x52a99e249ee7cf3c0cbf963a009661772bc9cdf6e1e3fbfc6e44a07a5e0f894457a9f81c3ae132ac5683d35b28ba5c324243
	 & d  #H u6Lۮ  :ALEXCTF{SMALL_PRIMES_ARE_BAD}
	# 
```
What is bad for crypto is great for CTF. And that is the first scoring flag I have gotten for OpenToAll.
