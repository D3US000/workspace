'''
Created on 04 lug 2016

@author: claudio
'''
from Query import Query
import sys

def riempiArgs(lista):
    args={}
    i=0
    key=""
    for arg in sys.argv:
        if i>1:
            if arg[0]=='-':
                key=arg[1:]
            else :
                if key!="":
                    args[key]=arg
                    key=""
        i+=1
    return args

def definisci_args():
    risultato=[]
    for arg in sys.argv:
        risultato.append(arg)
    return risultato

def help1():
    lista=["find","help1","describe","config","getconfig"]
    print "Lista di comandi disponibili"
    for elem in lista:
        print elem+"  "

q=Query()
args=definisci_args()
operazione=args[1]
if operazione=="find":
    args=riempiArgs(args[2:]) 
    print q.do_query(args)
elif operazione=="describe":
    print q.do_describe()
elif operazione=="config":
    args=riempiArgs(args[2:])
    q.config_dblink(args)
elif operazione=="getconfig":
    print q.get_config_toString()
elif operazione=="delconfig":
    q.del_config()
elif operazione=="help":
    help1()
else:
    print operazione+"  comando sconosciuto"
    help1()
    
    
    
    
    
    
    
    