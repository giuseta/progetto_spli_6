# coding: utf-8 -*-
import bitstring
from bitstring import *
import hashlib
from hashlib import *

def feistel_block(chunk, key_i):#funzione che applica feistel ad un blocco
	chunk=BitStream(chunk)#eventualmente da togliere
	key_i=BitStream(key_i)#eventualmente da togliere
	Li=BitStream(bin=chunk.read('bin:256'))#Leggo Li spostando il cursore di 256 pronto per leggere Ri
	key_i=key_i*8#ripeto la chiave 8 volte (128 bit di chiave per fare l'exor bit a bit con il chunk)
	Ri1=BitStream(bin=chunk.read('bin:128'))#Leggo i primi 128 bit di Ri
	Ri1_xor_key_i=BitStream(Ri1^key_i)#XOR bit a bit tra i primi 128 bit di Ri e la chiave ripetuta
	Ri_md5=hashlib.md5()#inizializzo variabile per applicare l'md5
	Ri_md5.update(Ri1_xor_key_i.read('bin:128'))#specifico su cosa devo fare l'md5(i primi 128 bit di Ri XOR chiave)
	Ri_md5=BitStream(bytes=Ri_md5.digest())#Faccio l'md5 (restituisce byte)
	Ri2=BitStream(bin=chunk.read('bin:128'))#Leggo i rimanenti 128 bit di Ri
	Ri_xor_key_i2=BitStream(Ri2^key_i)#XOR bit a bit tra gli ultimi 128 bit di Ri e la chiave ripetuta
	Ri2_md5=hashlib.md5()#inizializzo la seconda variabile per applicare l'md5
	Ri2_md5.update(Ri_xor_key_i2.read('bin:128'))#specifico su cosa devo fare l'md5 (gli ultimi 128 bit di Ri XOR chiave)
	Ri2_md5=BitStream(bytes=Ri2_md5.digest())#Faccio l'md5 (restituisce byte)
	Ri_md5.append(Ri2_md5)#concateno le due stringhe di bit ottenute tramite la codifica md5
	Riplus1=Li^Ri_md5#Ri+1 = Li XOR Ri_md5
	chunk.pos=256
	feist_block=BitStream(bin=chunk.read('bin:256'))#feist_block=Li+1=Ri
	feist_block.append(Riplus1)#feist_block=Li+1 + Ri+1
	return feist_block

def feistel(chunk, key):#funzione che applica gli 8 blocchi feistel al blocco da 512bit (chunk) con la chiave key
	key=BitStream(key)
	chunk=BitStream(chunk)
	key_rev=key
	key_rev.reverse()#chiave invertita
	key1=~key#chiave negata
	key2=key&key_rev
	key3=key|key_rev
	key4=key^key_rev
	key5=~key_rev
	key6=~(key&key_rev)
	key7=~(key|key_rev)
	key8=~(key^key_rev)

	chunk=BitStream(feistel_block(chunk, key1))#processo il chunk col blocco 1
	chunk=BitStream(feistel_block(chunk, key2))#processo il risultato del blocco 1 col blocco 2
	chunk=BitStream(feistel_block(chunk, key3))#processo il risultato del blocco 2 col blocco 3
	chunk=BitStream(feistel_block(chunk, key4))#processo il risultato del blocco 3 col blocco 4
	chunk=BitStream(feistel_block(chunk, key5))#processo il risultato del blocco 4 col blocco 5
	chunk=BitStream(feistel_block(chunk, key6))#processo il risultato del blocco 5 col blocco 6
	chunk=BitStream(feistel_block(chunk, key7))#processo il risultato del blocco 6 col blocco 7
	chunk=BitStream(feistel_block(chunk, key8))#processo il risultato del blocco 7 col blocco 8
	return chunk
