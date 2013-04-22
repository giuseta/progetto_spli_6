# coding: utf-8 -*-
import bitstring
from bitstring import *
import hashlib
from hashlib import *

def defeistel_block(chunk, key_i): # funzione che applica defeistel ad un blocco
	chunk=BitStream(chunk)     # eventualmente da togliere
	key_i=BitStream(key_i)     # eventualmente da togliere
	chunk.pos=0
	key_i=key_i*8        # ripeto la chiave 8 volte (128 bit di chiave per fare l'exor bit a bit con il chunk)
			   
	# Liplus1 (256 bit) lo divido in 2 parti perchè l'MD5 processa solo 128 bit per volta

	# Leggo i primi 128 bit di Li+1
	Liplus1=BitStream(bin=chunk.read('bin:128')) 
	Liplus1_xor_key_i=BitStream(Liplus1^key_i)
	Liplus1_md5=hashlib.md5()
	Liplus1_md5.update(Liplus1_xor_key_i.read('bin:128'))
	Liplus1_md5=BitStream(bytes=Liplus1_md5.digest())

	# Leggo i rimanenti 128 bit di Li+1
	Liplus2=BitStream(bin=chunk.read('bin:128'))
	Liplus2_xor_key_i=BitStream(Liplus2^key_i)
	Liplus2_md5=hashlib.md5()
	Liplus2_md5.update(Liplus2_xor_key_i.read('bin:128'))
	Liplus2_md5=BitStream(bytes=Liplus2_md5.digest())

	# Attacco le due parti delle funzioni MD5
	Liplus1_md5.append(Liplus2_md5)
	Riplus1=BitStream(bin=chunk.read('bin:256'))
	Li=Liplus1_md5^Riplus1

	# Creo blocco finale decriptato
	chunk.pos=0
	defeist_block=BitStream(bin=chunk.read('bin:256'))#Blocco finale = Ri
	defeist_block.prepend(Li)#attacco al blocco finale Li (a sinistra di Ri)

	return defeist_block

# Funzione che applica gli 8 blocchi Defeistel al blocco da 512bit (chunk) con la chiave key
def defeistel(chunk, key):
	key=BitStream(key)
	chunk=BitStream(chunk)
	key_rev=key
	key_rev.reverse() # Chiave invertita
	key1=~key         # Chiave negata
	key2=key&key_rev
	key3=key|key_rev
	key4=key^key_rev
	key5=~key_rev
	key6=~(key&key_rev)
	key7=~(key|key_rev)
	key8=~(key^key_rev)

	chunk=BitStream(defeistel_block(chunk, key8)) # Processo il chunk col blocco 8
	chunk=BitStream(defeistel_block(chunk, key7)) # Processo il risultato del blocco 8 col blocco 7
	chunk=BitStream(defeistel_block(chunk, key6)) # Processo il risultato del blocco 7 col blocco 6
	chunk=BitStream(defeistel_block(chunk, key5)) # Processo il risultato del blocco 6 col blocco 5
	chunk=BitStream(defeistel_block(chunk, key4)) # Processo il risultato del blocco 5 col blocco 4
	chunk=BitStream(defeistel_block(chunk, key3)) # Processo il risultato del blocco 4 col blocco 3
	chunk=BitStream(defeistel_block(chunk, key2)) # Processo il risultato del blocco 3 col blocco 2
	chunk=BitStream(defeistel_block(chunk, key1)) # Processo il risultato del blocco 2 col blocco 1

	return chunk



