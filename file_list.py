import tkinter as tk
from tkinter import ttk 
from tkinter import *
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.sql import select

app = tk.Tk() 
app.geometry('200x100')

labelTop = tk.Label(app, text = "Choose your favourite month")
labelTop.grid(column=0, row=0)
engine = create_engine('sqlite:///database.db')

connection = engine.connect()
metadata = db.MetaData()
tabe_avito = db.Table('avito', metadata, autoload=True, autoload_with=engine)
results = connection.execute(db.select([tabe_avito.columns.phone.distinct()]).order_by(db.asc(tabe_avito.columns.phone))).fetchall()
list1 = []
for i in results:
    list1.append(i[0])
comboExample = ttk.Combobox(app, values=list1)

comboExample.grid(column=0, row=1)
comboExample.current(1)

var = StringVar()

mylabel  = Label(app, textvariable=var, relief=RAISED)
var.set("Total")
mylabel.grid(column=0, row=2)
    
def showet(listresultat):
    global mylabel
    mylabel.destroy()
    mylabel  = Label(app, textvariable=var, relief=RAISED)
    var.set("\n".join(map(str, listresultat)))
    mylabel.grid(column=0, row=2)
          
def show(event):
    global mylabel
    print(comboExample.current(), comboExample.get())
    Query = connection.execute(select(tabe_avito).where(tabe_avito.columns.phone == comboExample.get()))
    alll = Query.fetchall()
    Query.close()
    print("Totale : ", len(alll))
    titreresult  = "Totale : "+str(len(alll))
    print("---------------------------------")
    alll.sort(key=lambda x: x[3])
    varville = ""
    listresult=[]
    totalindex = 0
    for idx, row in enumerate(alll, start=1):
        if varville != str(row[3]) :
            if totalindex > 0 :
                listresult.insert(totalindex, ">>>>>>>> Totale : "+str(i)+"       <<<<<<<<<")
                if prixnum>0 :
                    listresult.insert(totalindex+1, ">>>>>> Prix Moyen : "+str(prixtph/prixnum)+"      <<<<<<<")
            varville = str(row[3])
            listresult.append(">>>>>>>>  Ville : "+varville+"       <<<<<<<<<")
            totalindex = len(listresult)
            print("---------------------------------")
            print(varville)
            i = 0
            prixtph = 0
            prixnum = 0
        i += 1 
        if row[4] > 0 :
            prixtph += row[4]
            prixnum += 1
        titreresult = str(row[2])+" - "+str(row[4])+" - "+str(row[5])
        listresult.append(str(i)+" : "+titreresult)
        print(row)
        if idx == len(alll) :
            listresult.insert(totalindex, ">>>>>>>>    Totale : "+str(i)+"       <<<<<<<<<")
            listresult.insert(totalindex+1, ">>>>>> Prix Moyen : "+str(prixtph/prixnum)+"      <<<<<<<")
            
    #showet(listresult)
    print("---------------------------------")
    print('\n'.join(map(str, listresult)))
    app.update_idletasks ( )
    w = mylabel.winfo_width()
    h = mylabel.winfo_height()+comboExample.winfo_height()+labelTop.winfo_height()
    app.minsize(width=w, height=h) 
    
comboExample.bind("<<ComboboxSelected>>", show)
app.mainloop()