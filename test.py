import sqlalchemy as db
from sqlalchemy import create_engine,inspect
import pandas as pd
 
engine = create_engine('sqlite:///database.db')
 
connection = engine.connect()
metadata = db.MetaData()
 
def avendre(txt):
    if txt.find("à") > 0 :
        txt = txt.partition("à")
        return txt[0]
    if txt.find("À") > 0 :
        txt = txt.partition("À")
        return txt[0]
    if txt.find("neuf") > 0 :
        txt = txt.partition("À")
        return txt[0]
    return txt
 
 
def suprimetxt(txt):
    txt = avendre(txt)
    txt = txt.replace('téléphone ','')
    txt = txt.replace('téléphones','')
    txt = txt.replace('téléphone','')
    txt = txt.replace('téléphone portable','')
    txt = txt.replace('telefone ','')
    txt = txt.replace('telephone','')
    txt = txt.replace('a vendre','')
    txt = txt.replace('comme Neuf','')
    txt = txt.replace('en excellent état','')
    txt = txt.replace('en bonne etat','')
    txt = txt.replace('boîte fermé','')
    txt = txt.replace('américain neuf','')
    txt = txt.replace('utilisé','')
    txt = txt.replace('en très bon état','')
    txt = txt.replace('en bon état','')
    txt = txt.replace('bon prix','')
    txt = txt.replace('bon prix','')
    txt = txt.replace('ultra neufs','')
    txt = txt.replace('presque neuf','')
    txt = txt.replace('neuf','')
    txt = txt.replace('À vendre','')
    txt = txt.replace('très bon état','')
    txt = txt.replace('bon etat','')
    txt = txt.replace('neuf emballé et jamais utilisé','')
    txt = txt.replace('neufs','')
    txt = txt.replace('bon état','')
    return txt
 
tabe_avito = db.Table('avito', metadata, autoload=True, autoload_with=engine)
 
 
def alimentatiom():
    census = db.Table('annonces', metadata, autoload=True, autoload_with=engine)
    query = db.select([census]) 
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    #Inserting record one by one
    for x in ResultSet:
        print(x)
        y = suprimetxt(x[1])
        if len(y.replace(" ", ""))==0 :
            continue
        y=y.lstrip().rstrip()
        query = db.insert(tabe_avito).values( phone=y, titre=x[1], prix=x[2], date=x[3])
        connection.execute(query)
        print(query)
 
alimentatiom() 

      
 
census = db.Table('annonces', metadata, autoload=True, autoload_with=engine)    
results = connection.execute(db.select([tabe_avito.columns.phone.distinct()]).order_by(db.asc(tabe_avito.columns.phone))).fetchall()
#results = connection.execute(db.select([census.columns.titre.distinct()]).order_by(db.asc(census.columns.titre))).fetchall()
listres= []

for i in results:
    listres.append(i[0])
    
    
    
print(listres)
