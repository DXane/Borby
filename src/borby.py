#!/usr/bin/env python
# coding: utf-8
#Author: Daniel Förderer
#Date: 04.11.2019
#Version: 1.0
#Description: Calculates the Entropy of a File in Sections and displays the Highest Entropy of the File
#To-Do's: Add CSV export

import math, sys, os, heapq
import matplotlib.pyplot as plt

file=''         #Filename
step=1024       #Site of Section that will be given to Entropy Calc
csv=False       #Prüfe ob eine CSV-Datei erstellt werden soll

#Berechne die Entropy des übergebenen Bytearrays und gebe sie zurück
def entropy_calc(bytearr : bytes) -> float:
    entropy=0
    bytes_count=[bytearr.count(i) for i in range(256)]#Zähle die Anzahl der Bytes mit den Werten 0-255
    for count in bytes_count:
        if count == 0:
            continue
        p=1.0*count/len(bytearr) #Berechne die Wahrscheinlichkeit des aktuellen Bytes 
        entropy-=p*math.log(p,2)
    return entropy

#Sotiert die Parameter
def parameter(para : list):
    global file
    global step
    global csv
    #Display Help Screen
    if '-h' in para or '--help' in para or len(para)==0:
        print("usage: borby.py [-h] [--bytes size] [--csv [FILE]] FILE\n\npositional arguments:\n  FILE        a File or Path to a File to calculate the Entropy of\n\noptional arguments:\n -h, --help   show this message and exit\n --bytes size   Set the Size of the Byte Chunk that will be used\n --csv [FILE] Export the Result in a CSV-File if no File is given a File with the same Name as the used File is generated")
    #Setze die Bytegröße wenn übergeben. Standart=1024 Bytes
    if '--bytes' in para:
        step=int(para[para.index('--bytes')+1])
        para.remove(str(step))
        para.remove('--bytes')
    #To-Do Speichere die Werte in eine CSV-Datei
    if '--csv' in para:
        csv=True
        para.remove('--csv')
    para=[i for i in para if not str(i).startswith('--')]

    if os.path.isfile(para[0]):
        file=para[0]
        para.remove(file)

#Displays the Highest Entropy Value and the Bytes at that Section
def printmax(bytearray:list):
    global f
    n=5
    print('Displaying highest Entropie-Values. How many should be Displayed?(Default 5)')
    m=input()
    if m.isdigit():
        n=int(m)
    maxarr=heapq.nlargest(n,bytearray)#Gib die 3 Grössten Entropien aus
    for var in maxarr:
        print(str(bytearray.index(var)) +"(Offset at:"+str(bytearray.index(var)*step)+")-> "+str(var))
    m=input("Should the bytes be Displayed?(y/[n]):")
    if m.isalnum() and m[0]=='y':
        m=input("Type the Index that will be Displayed:(Max Index="+str(len(bytearray))+")")
        print("Displaying Byte-Section at Offset"+str(int(m)*step))
        f.seek(int(m)*step,0)
        print(f.read(step))
        print("------End")
    print("Exiting")
    

parameter(sys.argv[1:])

#Check of given File exist
if not os.path.isfile(file):
    print(file)
    print("Please give a valid File with the correct Path")
    exit()

entropydict=[]
entropy_raw=[] 

print('---Using '+file+' as input---\n---Using Sections of '+str(step)+' bytes')

f= open(file,'rb')#Öffnet Datei als Binary
ba=bytes(f.read())            #Speichere die Datei in einem Array

#Berechne die Entropy der Sektionen der Bytes
for i in range(math.floor(len(ba)/step)):
    k=entropy_calc(ba[step*i:step*(i+1)])
    entropy_raw.append(k)
    entropydict.append(k/8)

#Graph Display
m=input("Display Graph?(y/[n]):")
if m.isalpha() and m[0]=='y':
    #Create Graph of the Entropy
    plt.ylabel('Entropy Bytes')
    plt.xlabel('Byte Position i*'+str(step))
    plt.title('Entropy of '+file)
    plt.plot(entropydict,'-o')
    plt.grid()
    plt.show()

printmax(entropydict)
f.close()
exit()
