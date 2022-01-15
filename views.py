from ctypes.wintypes import SIZE
from distutils.command.config import LANG_EXT
from marshal import load
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ModelAnnonces , listville
from Avito import Avito as avito
import csv
from moyen_price import list_des_marque as marques , moyen_du_prix
from main import reload_data
import sqlalchemy as db
from sendmail import send_annonces


myFile = open("annon.csv", "a", newline="", encoding='UTF-8')
headers = ['titre', 'ville', 'prix', 'date']
writer = csv.DictWriter(myFile, fieldnames=headers)
writer.writeheader()


class Fenetre(QDialog):
    def __init__(self):
        super(Fenetre, self).__init__()
        loadUi('UI/main.ui', self)
        self.tableWidget.setColumnWidth(0, 370)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.reload.clicked.connect(self.loaddata)
        self.list_annonces = []
        self.fichiercsv.clicked.connect(self.export_to_csv)
        self.page2.clicked.connect(self.go_to_page2)
        self.page3.clicked.connect(self.go_to_page3)
        #self.loaddata()

    def loaddata(self):
        reload_data()
        
        engine = create_engine('sqlite:///database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        annonces = session.query(ModelAnnonces).all()

        for annonce in annonces:
            self.list_annonces.append(vars(annonce))

        session.close()

        row = 0
        self.tableWidget.setRowCount(len(self.list_annonces))
        for annonce in self.list_annonces:
            self.tableWidget.setItem(
                row, 0, QtWidgets.QTableWidgetItem(annonce["titre"]))
            self.tableWidget.setItem(
                row, 1, QtWidgets.QTableWidgetItem(annonce["ville"]))
            self.tableWidget.setItem(
                row, 2, QtWidgets.QTableWidgetItem(annonce["prix"]))
            self.tableWidget.setItem(
                row, 3, QtWidgets.QTableWidgetItem(annonce["date"]))
            row = row+1

    def export_to_csv(self):
        myFile = open("annonce.csv", "a", newline="", encoding='UTF-8')
        headers = ['titre', 'ville', 'prix', 'date']
        writer = csv.DictWriter(myFile, fieldnames=headers)
        writer.writeheader()
        for annonce in self.list_annonces:
            annonce.pop("_sa_instance_state",None)
            annonce.pop('id',None)
            writer.writerow(annonce)
        myFile.close()
        
        
    def go_to_page2(self):
        page2= Page2()
        widget.addWidget(page2)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print("page2 clicked :")
        
        
    def go_to_page3(self):
        page3 = Page3()
        widget.addWidget(page3)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
            
class Page2(QDialog):
    def __init__(self):
        super(Page2, self).__init__()
        loadUi('UI/page2.ui', self)
        self.main.clicked.connect(self.back_to_main)
        self.page3.clicked.connect(self.back_to_main)
        self.tableWidget.setColumnWidth(0, 370)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.combo_list_des_marque.addItems(marques())
        self.combo_list_des_marque.currentTextChanged.connect(self.chargervue)
        
    def chargervue(self,text):
        result = moyen_du_prix(text)
        #print(result)
        
        
        row = 0
        self.tableWidget.setRowCount(len(result))
        for annonce in result:
            self.tableWidget.setItem(
                row, 0, QtWidgets.QTableWidgetItem(annonce["Ville"]))
            self.tableWidget.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(annonce["Annonces"])))
            self.tableWidget.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(annonce["Moyen de Prix"])))
            row += 1
                
    def back_to_main(self):
        main = Fenetre()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
    def back_to_page3(self):
        page3 = Page3()
        widget.addWidget(page3)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
        
class Page3(QDialog):
    def __init__(self):
        super(Page3, self).__init__()
        loadUi('UI/page3.ui', self)
        self.listville.addItems(listville())
        self.input1
        self.input2
        
        self.input3
        
        
        self.main.clicked.connect(self.back_to_main)
        self.page2.clicked.connect(self.back_to_page2)
        self.send.clicked.connect(self.clickMethod)
        
    

    
    
    def clickMethod(self):
        engine = create_engine('sqlite:///database.db')
        connection = engine.connect()
        metadata = db.MetaData()
        
        
        txtprix = self.input1.text()
        if txtprix.isdigit():
            max = int(txtprix)
        else:
            print("Max not Number")
            return
        txtprix = self.input2.text()
        if txtprix.isdigit():
            min = int(txtprix)
        else:
            print("Min not Number")
            return
        if max<=min:
            print("Min Not Samll than Max")
            return
        choixville = self.listville.currentText()
        sql = "SELECT * FROM avito WHERE prix >= '%s' AND prix <='%s' AND ville ='%s' " % (min, max, choixville,)
        result = connection.execute(sql)
        
        listtup = []
        for i in result:
            
            listtup.append(i)
        print(listtup)
        with open('mail.txt', 'w') as fp:
            fp.truncate(0) 
            fp.write('\n'.join('{}   {}  {}  {}   {} '.format(x[1],x[2],x[3],x[4],x[5]) for x in listtup))
            fp.close()
        with open ("mail.txt", "r") as myfile:
            data=myfile.read()
            receiver = self.input3.text()
            send_annonces(receiver, data)
        
        
    def back_to_main(self):
        main = Fenetre()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
    def back_to_page2(self):
        page2 = Page2()
        widget.addWidget(page2)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv)
main = Fenetre()
page2= Page2()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main)
widget.setFixedHeight(650)
widget.setFixedWidth(1000)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("xxxxx")
