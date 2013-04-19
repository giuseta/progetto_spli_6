import bitstring
from bitstring import *
import hashlib
from hashlib import *

def feistel_block(chunk, key_i):#funzione chre applica feistel ad un blocco
chunk=BitStream(chunk)#eventualmente da togliere
key_i=BitStream(key_i)#eventualmente da togliere
chunk.pos=256
for j in range(4):
	key_i.append(key_i)#ripeto la chiave 8 volte (128 bit di chiave per fare l'exor bit a bit con il chunk)
#Ri (256 bit) lo divido in 2 parti perchè l'md5 processa solo 128 bit per volta
Ri1=BitStream(bin=chunk.read('bin:128'))#Leggo i primi 128 bit di Ri
Ri1_xor_key_i=BitStream(Ri1^key_i)
Ri_md5=hashlib.md5()
Ri_md5=update(Ri1_xor_key_i.read('bin:128'))
Ri_md5=BitStream(bytes=Ri_md5.digest())
Ri2=BitStream(bin=chunk.read('bin:128'))#Leggo i rimanenti 128 bit di Ri
Ri_xor_key_i2=BitStream(Ri2^key_i)
Ri2_md5=hashlib.md5()
Ri2_md5=update(Ri_xor_key_i2.read('bin:128'))
Ri2_md5=BitStream(bytes=Ri2_md5.digest())
Ri_md5.append(Ri2_md5)
chunk.pos=0
Li=BitStream(bin=chunk.read('bin:256'))
Riplus1=Li^Ri_md5
feist_block=BitStream(bin=chunk.read('bin:256'))
feist_block.append(Riplus1)
return feist_block

def feistel(chunk, key):#funzione che applica gli 8 blocchi feistel al blocco da 512bit (chunk) con la chiave key
#sottofunzione che rimescola i bit e applica md5 del blocco X (con X=1,..,8)
#a=BitStream(bytes=xxx)

