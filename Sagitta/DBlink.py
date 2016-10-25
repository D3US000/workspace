'''
Created on 01 lug 2016

@author: claudio
'''
import mysql.connector as mysql
from Document import Document
class DBlink:
    '''
    classdocs
    '''
    
    def __init__(self):
        self.config=Document("config.txt")
        self.default_host='www.medcordex.eu'
        self.default_user='sagitta'
        self.default_passwd='sagitta'
        self.default_db='medcordex'
        
    def set_config(self,params):
        self.config.update(params)
    
    def get_config_toString(self):
        return self.config.toString()
    
    def del_config(self):
        self.config.delete()
        
    def get_doc(self):
        return self.config
    
    def get_table(self):
        return self.config.get_parameter("table")
    
    def get_db(self):
        return self.config.get_parameter("db")
    
    def get_url(self):
        url= self.config.get_parameter("url")
        if url=="":
            if self.config.get_parameter("host")=="www.medcordex.eu":
                url="ftp://"+self.config.get_parameter("user")+":"+self.config.get_parameter("passwd")+"@"+self.config.get_parameter("host")+"/ALL/"
        return url
        
    def send_query(self,query):
        # default configuration for medcordex users
        if self.config.get_parameter("host")=='' and self.config.get_parameter('db')=='':
            database=mysql.connect(host=self.default_host,
                                     user=self.default_user,
                                     passwd=self.default_passwd,
                                     db=self.default_db)
        # presonal configuration for all other cases
        else:
            database=mysql.connect(host=self.config.get_parameter("host"),
                                     user=self.config.get_parameter("user"),
                                     passwd=self.config.get_parameter("passwd"),
                                     db=self.config.get_parameter("db"))
        cursore=database.cursor()
        cursore.execute(query)
        return cursore.fetchall()
        
