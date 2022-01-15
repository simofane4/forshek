from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, create_session
import sqlalchemy as db

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


class ModelAnnonces(Base):
    __tablename__ = "annonces"
    id = Column(Integer, primary_key=True,autoincrement=True)
    titre = Column(String(200))
    ville=Column(String(200))
    prix = Column(String(30))
    date=Column(String(200))
    



class ModelAvito(Base):
    __tablename__ = "avito"
    id = Column(Integer, primary_key=True,autoincrement=True)
    phone = Column(String(200))
    titre = Column(String(200))
    ville=Column(String(200))
    prix = Column(String(30))
    date=Column(String(200))
    
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session=session()



def add_to_db(annonces):
    for annonce in annonces:
                field = ModelAnnonces()
                
                
                field_titre = [r.titre for r in session.query(ModelAnnonces.titre)]
                field_prix = [r.prix for r in session.query(ModelAnnonces.prix)]
                field_ville = [r.ville for r in session.query(ModelAnnonces.ville)]
                field_date = [r.date for r in session.query(ModelAnnonces.date)]
                if annonce['titre']  in  field_titre and annonce['prix']  in field_prix and annonce['ville']  in field_ville and annonce['date'] in  field_date :
                    pass
                    print(" hade  lfilter  khedam !!!!!")
                else:
                    field.titre=annonce['titre']
                    field.ville=annonce['ville']
                    field.prix=annonce['prix']
                    field.date=annonce['date']
                    session.add(field)
                    session.commit()
                    print('hada  li bedelti !!!!!')
                    
                session.close()
                
engine = create_engine('sqlite:///database.db')
connection = engine.connect()
metadata = db.MetaData()
tabe_avito = db.Table('avito', metadata, autoload=True, autoload_with=engine)

def listville():
    results = connection.execute(db.select([tabe_avito.columns.ville.distinct()]).order_by(db.asc(tabe_avito.columns.ville))).fetchall()
    list1 = []
    for i in results:
        list1.append(i[0])
    return list1