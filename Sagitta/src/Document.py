'''
Created on Jul 12, 2016

@author: claudio
'''

class Document:
    def __init__(self,name):
        self.name=name
        self.params=self.read()
        
    def read(self):
        doc= open(self.name, "r").read()
        p=doc.split("\n")
        params={}
        for i in p:
            lista_riga=i.split(";")
            if lista_riga!=[""]:
                    params[lista_riga[0]]=lista_riga[1]
        return params
    
    def update(self,params):
        for p in params:
            self.get_params()[p]=params[p]
        self.write(self.get_params())
    
    def write(self,params):
        doc = open(self.name, "w")
        for p in params.keys():
            riga = "%s;%s\n"%(p,params[p])
            doc.write(riga)
        doc.close()
        self.set_params(self.read())
        
    def delete(self):
        doc = open(self.name, "w")
        doc.write("")
        doc.close()
    
    def get_params(self):
        return self.params
    
    def get_db(self):
        if self.get_params().has_key("db"):
            return self.get_params()["db"]
        return ""
    
    def get_table(self):
        if self.get_params().has_key("table"):
            return self.get_params()["table"]
        return ""

    def get_host(self):
        if self.get_params().has_key("host"):
            return self.get_params()["host"]
        return ""
    
    def get_passwd(self):
        if self.get_params().has_key("passwd"):
            return self.get_params()["passwd"]
        return ""
    
    def get_user(self):
        if self.get_params().has_key("user"):
            return self.get_params()["user"]
        return ""
    
    def set_params(self,params):
        self.params=params
    
    def toString(self):
        s=""
        keyset=self.get_params().keys()
        keyset.sort()
        for k in keyset :
            s+= k+" = "+self.get_params()[k]+" \n"  
        return s