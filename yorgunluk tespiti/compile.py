from PyQt5.QtWidgets import *
from giris import Ui_MainWindow  #from sayfa.py import method yaparak sayfayı dail ediyoruz
from cameraWatchCompile import Watch
from PyQt5 import QtWidgets

class AnaSafanın(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_3.setHidden(True)
        self.ui.lineSifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.giris = Watch()
        self.ui.QPushButton.clicked.connect(self.KameraIzle)

    def KameraIzle(self):
        if self.ui.lineKullanici.text()=="admin" and self.ui.lineSifre.text()=="0000":
            self.hide()
            self.giris.show()
        else:
            self.ui.label_3.setHidden(False)