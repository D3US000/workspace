'''
Created on May 31, 2016

@author: claudio
'''
documento=open("config_datas.txt","r")
lines=documento.readlines()
lista=[]
for l in lines:
    parola=l.split(" ")
    prec=""
    for p in parola:
        if prec!="":
            lista.append((prec , p.strip("\n")))
        prec=p
print lista