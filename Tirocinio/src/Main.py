'''
Created on 29 mag 2016

@author: claudio
'''
from query.Query import Query
from connection.Connection import Connection

q=Query()
q.set_where_with_args()
q.setFrom("MEDCORDEX")
q.setSelect("fname")
q.add_in_select("size")
print q.toString()

c=Connection(host="www.medcordex.eu",user="mdcx172",passwd="23=Dh+1",db="medcordex")
for line in c.send_query(q.toString()):
    print line
    
c.set_from_file()
c.toString()