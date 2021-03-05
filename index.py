from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
from os import path
import os , time
import urllib.request


FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))


class main(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_UI()
        self.handel_buttons()
        



    def handel_UI(self):
        self.setWindowTitle("PyDM")
        self.setFixedSize(737,285)
        pass

    def handel_buttons(self):
        self.Download1_5.clicked.connect(self.download) 
        self.pushButton_3.clicked.connect(self.handel_Brows)

    def handel_Brows(self):
        save_loc = QFileDialog.getSaveFileName(self, caption="Save As", directory='.', filter="All Files (*,*)")
        x = str(save_loc)
        name = (x[2:].split(',')[0].replace("'", ''))
        self.lineEdit_4.setText(name)
    
    def handel_progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize

        if totalsize >0:
            percent = read*100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()

    def download(self):
        url = self.videoURL_2.text()
        loc = self.lineEdit_4.text()

        try:
            urllib.request.urlretrieve(url, loc, self.handel_progress)
        except Exception:
            QMessageBox.warning(self, 'Alert', 'Download Faild' ) 
            return 
   
        QMessageBox.information(self, 'Alert', 'Download Completed')
        self.progressBar.setValue(0)
        self.videoURL_2.setText("")
        self.lineEdit_4.setText("")


        


def main_app():
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main_app()

