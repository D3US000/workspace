'''
Created on 01 lug 2016

@author: claudio
'''
import os
from DBlink import DBlink
from Document import Document,KL_Document

class Query:
    '''
    the aim of this class is to build the query with different info by alias.txt,lastquery.txt and argoments 
    and let DBLink class to send the query to the database
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.dblink=DBlink()
        self.lastquery=Document("lastquery.txt")
	path=os.path.dirname(os.path.abspath(__file__))
        self.alias=KL_Document("alias.txt",path)
        self.default_table='MEDCORDEX'
        
    def is_defined(self,name,describe):
        #this operation defines the field into 'where' query to send to the database
        nameDefined=self.is_alias(name)
        if nameDefined!='':
            return nameDefined
        return name
    
    def is_alias(self,name):
        #search the alias for 'name' into alias.txt, if it's null return ""
        alias_map=self.alias.get_params()
        for k in alias_map:
            for v in alias_map[k]:
                if v==name:
                    return k
        return ""
        
    def build_where(self,args):
        #build where of query
        s=""
        describe=self.do_describe()
        for name in args.keys():
            #nameDefined is the name of camp build by describe or alias
            nameDefined=self.is_defined(name,describe)
            if nameDefined!="":
                if s!="":
                    s+=" and"
                s+= " "+nameDefined+" = '"+args[name]+"'"
            else:
                raise Exception("error field name: '"+name+"'")
        if s!="":
            s=" where"+s
        return s
    
    def save_query(self,q):
        #save query in lastquery.txt
        a={"query":q}
        self.lastquery.write(a)
        
    def save_datasets(self,datasets):
        #save in lastquery.txt {row:dataset name} (no delete query)
        i=1
        lq={}
        lq["query"]=self.lastquery.get_parameter("query")
        for d in datasets:
            lq[i]=d
            i+=1
        self.lastquery.update(lq)
        
    def double2table(self,triple):
        #return N Datasets, N files, N size(MB)
        #double=((dataset1,size1),(dataset2,size2),....)
        t={}
        f={}
        i=0
        if len(triple)>0:
            s="row %69s %13s %14s\n"%("DATASET NAME","N FILES","N MBs")
        for dataset,size,fname in triple:
            if dataset in t:
                t[dataset]+=size
                f[dataset]+=1
            else:
                t[dataset]=size
                f[dataset]=1
        #save dataset in lastquery.txt
        self.save_datasets(t.keys())
        for d in t:
            i+=1
            s+= "%02d %70s : %5d files %10.2f MB \n"%(i,d,f[d],t[d])
        return "\nFound "+str(sum(f.values()))+" files in "+str(len(t))+" Datasets, total size "+str(sum(t.values()))+"MB\n\n"+s
        
    def do_query(self,args={},select="*",save=True):
        #this builds the query, sends the query, save the query in lastquery.txt and returns the result(tupla)
        #this function saves only query, doesn't save dataset
        table=self.dblink.get_table()
        if table=='': table=self.default_table
        query="select "+select+" from "+table+self.build_where(args)
        tupla=self.dblink.send_query(query)
        if save: self.save_query(query)
        return tupla
    
    def do_describe(self):
        #searches all fields in the database 
        describe=self.dblink.send_query("describe MEDCORDEX")
        l=[]
        for elem in describe:
            l.append(elem[0])
        return l
    
    def get_config_toString(self):
        return self.dblink.get_config_toString()
    
    def config_dblink(self,params):
        self.dblink.set_config(params)
        
    def del_config(self):
        self.dblink.del_config()
    
    def get_last_query(self):
        return self.lastquery.get_parameter("query")
        
    def send_query(self,query):
        tupla=self.dblink.send_query(query)
        self.save_query(query)
        return tupla
    
    def get_row_dataset(self,num):
        return self.lastquery.get_parameter(num)
    
    def get_select(self):
        #return a string of all select filed ('*' or 'field1,field2,...fieldN')
        return self.lastquery.get_parameter("query").split(" ")[1] 
        
    def get_index(self,name):
        #return index of tupla where the name == a field name
        select=self.get_select()
        if select =='*':
            #case 1: select *
            index=0
            for a in self.do_describe():
                if a==name: return index
                index+=1
            raise Exception(name+" are not in table")
        else:
            #case 2: select ...,name,...
            index=0
            for field in select.split(','):
                if name==field: return index
                index+=1
        #case 3: select ...,other,...
        raise Exception("Index not found")
    def get_url(self):
        return self.dblink.get_url()
    
    def get_path(self):
        return self.dblink.get_doc().get_parameter("path")
        
    def find_conn_probls(self):
        #check if some info into config.txt is/are null
        return self.dblink.find_conn_probls()
