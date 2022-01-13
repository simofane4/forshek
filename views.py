from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ModelAnnonces
import pyautogui 





width, height= pyautogui.size()


class Fenetre(QDialog):
    def __init__(self):
        super(Fenetre, self).__init__()
        loadUi('UI/interfaceE.ui', self)
        self.tableWidget.setColumnWidth(0,370)
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.loaddata()
    def loaddata(self):
        engine = create_engine('sqlite:///database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        annonces =  session.query(ModelAnnonces).all()
        list_annonces = []
        for annonce in annonces:
          list_annonces.append(vars(annonce))
          
            
        session.close()
        print(list_annonces)
        

        row=0
        self.tableWidget.setRowCount(len(list_annonces))
        for annonce in list_annonces:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(annonce["titre"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(annonce["ville"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(annonce["prix"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(annonce["date"]))
            row=row+1



app =QApplication(sys.argv)
fen = Fenetre()
widget = QtWidgets.QStackedWidget()
widget.addWidget(fen)
widget.setFixedHeight(650)
widget.setFixedWidth(1000)
widget.show()
try:
  sys.exit(app.exec_())
except:
    print("xxxxx")

