import bitstring #modulo da scaricare per lavorare con i bit
from bitstring import *

#apro il file eye.jpg in bit e li metto in bit_img
bit_img = BitStream(filename='/home/paolo/Pictures/eye.jpg')#bit_img = ConstBitStream(filename='/home/paolo/Pictures/eye.jpg')
#leggo il numero di bit
len_bit_img = bit_img.length
#verifico che il numero di bit sia multiplo di 512
resto=len_bit_img%512
if resto!=0: #se non è multiplo
	for i in range(512-resto):#faccio un ciclo che va da 0 a 512-resto della divisione
		bit_img.append('0b0')#aggiungo 512-resto zeri alla fine dello stream di bit in modo che il num totale di bit del file sia divisibile per 512
	#f=open('/home/paolo/Pictures/nuovofile', 'wb')
	#BitArray(var_appoggio).tofile(f)
	#close(f)
	#bit_img= ConstBitStream(filename='/home/paolo/Pictures/nuovo_file')
	len_bit_img = bit_img.length

quoziente=len_bit_img/512#quoziente è il numero di blocchi da 512 bit che dovrò processare

for j in range(quoziente):
	chunk=BitStream('0b'+bit_img.read('bin:512'))#prendo un blocco da 512bit (il cursore si sposta automaticamente ogni volta che leggo)
	if bit_img.pos==512:#prima lettura
		chunk=chunk^N#blocco_1 XOR bit a bit con N (512 bit random da noi scelti)
		#feist_chunk=feistel(chunk,key)#applico Feistel al blocco chunk con la chiave key
		cifrato=feist_chunk#inizializzo quello che sarà l'output [Eventualmente cambiare in cifrato=BitStream(feist_chunk)]
		feist_chunk_prev=feist_chunk#memorizzo il blocco di dati "feistelizzato" per la successiva iterazione
	else:#letture successive alla prima
		chunk=chunk^feist_chunk_prev#XOR bit a bit tra il blocco precedente "feistelizzato" e il blocco corrente
		#feist_chunk=feistel(chunk,key)#applico Feistel al blocco chunk con la chiave key
		cifrato.append(feist_chunk)#concateno i blocchi "feistelizzati" per la creazione del messaggio cifrato
		feist_chunk_prev=feist_chunk#memorizzo il blocco di dati per la successiva iterazione

c=open('/home/paolo/Pictures/encrypted', 'wb')
BitStream(cifrato).tofile(c)
close(c)
