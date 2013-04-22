# coding: utf-8 -*-
import bitstring #modulo da scaricare per lavorare con i bit
from bitstring import *
import feistel
from feistel import *

#Input
logic=True
while logic:
        key=raw_input('Encryption: Insert key (16 bit): ')
        if ((len(key)==16)and(key.isdigit())and(key.find('2')==-1)and(key.find('3')==-1)and(key.find('4')==-1)and(key.find('5')==-1)and(key.find('6')==-1)and(key.find('7')==-1)and(key.find('8')==-1)and(key.find('9')==-1)):
                logic=False
        else:
                print('\nWarning: Key must be composed by 16 chars only (0 and 1)!\n')

key=BitStream(bin=key)
N=BitStream(bin='01010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101')

#Loading File + Padding
bit_img = BitStream(filename='/home/paolo/Pictures/eye.jpg')#apro il file eye.jpg in bit e li metto in bit_img
len_bit_img = bit_img.length#leggo il numero di bit
resto=len_bit_img%512#verifico che il numero di bit sia multiplo di 512
if resto!=0: #se non è multiplo
        print('\nBit Padding executed!')
        for i in range(512-resto):#faccio un ciclo che va da 0 a 512-resto della divisione
                bit_img.append('0b0')#aggiungo 512-resto zeri alla fine dello stream di bit in modo che il num totale di bit del file sia divisibile per 512
        len_bit_img = bit_img.length

#Encryption
print('\nEncryption is processing...')
quoziente=len_bit_img/512#quoziente è il numero di blocchi da 512 bit che dovrò processare
for j in range(quoziente):
	chunk=BitStream(bin=bit_img.read('bin:512'))#prendo un blocco da 512bit (il cursore si sposta automaticamente ogni volta che leggo)
	if bit_img.pos==512:#prima lettura
		chunk=chunk^N#blocco_1 XOR bit a bit con N (512 bit random da noi scelti)
		feist_chunk=BitStream(feistel(chunk, key))#applico Feistel al blocco chunk con la chiave key
		cifrato=feist_chunk#inizializzo quello che sarà l'output
		feist_chunk_prev=feist_chunk#memorizzo il blocco di dati "feistelizzato" per la successiva iterazione
	else:#letture successive alla prima
		chunk=chunk^feist_chunk_prev#XOR bit a bit tra il blocco precedente "feistelizzato" e il blocco corrente
		if(j==quoziente-1):#ultima iterazione	
			INTERCEPT=chunk#Chunk di dati intercettato che verrà utilizzato per recuperare la key nell'attacco
		feist_chunk=feistel(chunk, key)#applico Feistel al blocco chunk con la chiave key
		cifrato.append(feist_chunk)#concateno i blocchi "feistelizzati" per la creazione del messaggio cifrato
		feist_chunk_prev=feist_chunk#memorizzo il blocco di dati per la successiva iterazione

print("\nEncryption Complete!\n")
c=open('/home/paolo/Pictures/encrypted.jpg', 'wb')
BitStream(cifrato).tofile(c)
c.close()
print("Encrypted file saved in /home/paolo/Pictures/encrypted.jpg")
