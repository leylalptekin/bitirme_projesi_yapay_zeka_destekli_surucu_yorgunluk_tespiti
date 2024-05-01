from PyQt5.QtWidgets import *
from CameraWatch import Ui_KameraIzle
import compile
import YorgunlukTespiti

class Watch(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui=Ui_KameraIzle()
        self.ui.setupUi(self)

        self.ui.geriGel.clicked.connect(self.geri)
        self.ui.pushButton.clicked.connect(self.izle)

    def geri(self):
        self.hide()
        self.ana=compile.AnaSafanın()
        self.ana.show()

    def izle(self):
        if self.ui.lineEdit.text()=="0":
            YorgunlukTespiti.izle1(int(0))
        else:
            YorgunlukTespiti.izle1(self.ui.lineEdit.text())