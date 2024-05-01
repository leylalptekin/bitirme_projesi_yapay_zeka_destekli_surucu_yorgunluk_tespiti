from PyQt5.QtWidgets import *
from compile import AnaSafanın #Anasayfayı çalıştırır
import sys

print ("Uygulama başlatılıyor lütfen bekleyiniz...")

app = QApplication([])
ex = AnaSafanın()
ex.show()
sys.exit(app.exec_())