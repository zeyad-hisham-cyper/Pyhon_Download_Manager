from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
from os import path
import os , time
from os import *


FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))


class main(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)



    def handel_UI(self):
        self.setWindowTitle("PyDM")
        self.setFixedSize(737,468)
        pass

    def handel_buttons(self):
        pass

    def handel_Brows(self):
        pass
    
    def handel_progress(self):
        pass

    def download(self):
        pass


def main_app():
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main_app()

