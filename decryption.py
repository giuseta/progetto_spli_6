# coding: utf-8 -*-
import bitstring #modulo da scaricare per lavorare con i bit
from bitstring import *
import encryption
from encryption import INTERCEPT,N
import defeistel
from defeistel import *

#Funzione di attacco
def attack():
	enc = BitStream(filename='/home/paolo/Pictures/encrypted.jpg')
	len_enc=enc.length
	enc.pos=len_enc-512
	last_chunk=BitStream(bin=enc.read('bin:512'))
	hyp_key=BitStream(bin='0000000000000000')#chiave ipotetica
	print('\n\n'+hyp_key.bin)
	defeist_last_chunk=BitStream(defeistel(last_chunk,hyp_key))#inizializzazione risultato che dovrò confrontare con INTERCEPT
	while defeist_last_chunk!=INTERCEPT:
		hyp_key=hyp_key.uint+1#per incrementare la chiave devo passare a interi senza segno...
		hyp_key=BitStream(uint=hyp_key,length=16)#...per poi ritornare a stringhe di bit
		print('\n'+hyp_key.bin)
		defeist_last_chunk=BitStream(defeistel(last_chunk,hyp_key))
	print('\n\nKEY FOUNDED: '+hyp_key.bin)
	print('\nThe attack was offered by Gruppo Spli 1')
	return hyp_key

#Input
logic=True
while logic:
	key=raw_input('\n\n\nDecryption: Insert key (16 bit): ')
	if ((len(key)==16)and(key.isdigit())and(key.find('2')==-1)and(key.find('3')==-1)and(key.find('4')==-1)and(key.find('5')==-1)and(key.find('6')==-1)and(key.find('7')==-1)and(key.find('8')==-1)and(key.find('9')==-1)):
		logic=False
		key=BitStream(bin=key)
	elif (key=='attack'):
		logic=False
		key=BitStream(attack())
	else:
		print('\nWarning: Key must be composed by 16 chars only (0 and 1)!\n')


#Decryption
print('\nDecryption is processing...')
bit_enc = BitStream(filename='/home/paolo/Pictures/encrypted.jpg')#apro il file encrypted.jpg in bit e li metto in bit_enc
len_bit_enc=bit_enc.length
quoziente=len_bit_enc/512

for i in range(quoziente):
	bit_enc.pos=len_bit_enc-((i+1)*512)#posiziono il cursore per la lettura in modo da leggere dall'ultimo blocco da 512 al primo
	chunk=BitStream(bin=bit_enc.read('bin:512'))#prendo un blocco da 512bit (il cursore si sposta automaticamente ogni volta che leggo)
	if bit_enc.pos==len_bit_enc:#lettura ultimo blocco
		defeist_chunk=BitStream(defeistel(chunk, key))
	elif bit_enc.pos==512:#lettura primo blocco
		defeist_chunk=defeist_chunk^chunk#Xor tra primo blocco feistelizzato e secondo blocco defeistelizzato
		original.prepend(defeist_chunk)
		defeist_chunk=defeistel(chunk, key)#applico Feistel al blocco chunk con la chiave key
		defeist_chunk=defeist_chunk^N#blocco_1 XOR bit a bit con N (512 bit random da noi scelti)		
		original.prepend(defeist_chunk)#inizializzo quello che sarà l'output
	else:#lettura blocchi dall'ultimo al secondo
		defeist_chunk=defeist_chunk^chunk
		if bit_enc.pos==len_bit_enc-512:#se sto considerando il penultimo blocco
			original=defeist_chunk#original è la variabile che conterrà i bit del file immagine che voglio ricostruire
		else:
			original.prepend(defeist_chunk)
		defeist_chunk=defeistel(chunk, key)#applico defeistel al blocco chunk con la chiave key

#Scrittura su file
print("\nDecryption Complete!\n")
d=open('/home/paolo/Pictures/decrypted.jpg', 'wb')
BitStream(original).tofile(d)
d.close()
print("Decrypted file saved in /home/paolo/Pictures/decrypted.jpg")
