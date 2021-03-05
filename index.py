from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
from os import path
import os , time
import urllib.request
import pafy
import humanize


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
        self.Download1_2.clicked.connect(self.Youtube_video)
        self.pushButton.clicked.connect(self.brows_video_loc)
        self.Download1.clicked.connect(self.download_video)

    def handel_Brows(self):
        save_loc = QFileDialog.getSaveFileName(self, caption="Save As", directory='.', filter="All Files (*,*)")
        x = str(save_loc)
        name = (x[2:].split(',')[0].replace("'", ''))
        self.lineEdit_4.setText(name)
    
    def handel_progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize

        if totalsize >0:
            percent = read*100 / totalsize
            self.progressBar_3.setValue(percent)
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

    def Youtube_video(self):
        link = self.videoURL.text()
        v = pafy.new(link)
        st = v.videostreams
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data ='{} {} {} {}'.format(s.mediatype , s.extension, s.quality, size)
            self.comboBox.addItem(data)
            QApplication.processEvents()
    
    def brows_video_loc(self):
        save = QFileDialog.getExistingDirectory(self, "Save As")
        self.lineEdit.setText(save)

    def video_progressbar(self,total, recvd, ratio, rate, eta):
        self.progressBar.setValue(ratio * 100)
        x= '%2.f' % rate
        text = "Speed = {} KB/S, Time remaining = {} secs".format(x, eta)
        self.label_4.setText(text)
        QApplication.processEvents()

    def download_video(self):
        try:
            link = self.videoURL.text()
            video_loc = self.lineEdit.text()
            v = pafy.new(link)
            st = v.videostreams
            quality = self.comboBox.currentIndex()
            start_download = st[quality].download(filepath=video_loc,callback=self.video_progressbar)
        
        except Exception:
            QMessageBox.warning(self, 'Alert', 'Download Faild' ) 
            return
        QMessageBox.information(self, 'Alert', 'Download Completed')
        self.progressBar.setValue(0)
        self.videoURL.setText("")
        self.lineEdit.setText("")            
        

def main_app():
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main_app()

