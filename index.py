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
from pytube import Playlist
import webbrowser


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
        self.setFixedSize(self.size())
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget.tabBar().setVisible(False)

    def handel_buttons(self):
        self.Download1_5.clicked.connect(self.download) 
        self.pushButton_3.clicked.connect(self.handel_Brows)
        self.Download1_2.clicked.connect(self.Youtube_video)
        self.pushButton.clicked.connect(self.brows_video_loc)
        self.Download1.clicked.connect(self.download_video)
        self.pushButton_2.clicked.connect(self.brows_video_loc)
        self.Download2.clicked.connect(self.download_playlist)
        self.pushButton_4.clicked.connect(self.handel_file)
        self.pushButton_5.clicked.connect(self.handel_video)
        self.pushButton_6.clicked.connect(self.handel_pl)
        self.pushButton_8.clicked.connect(self.git)
        self.pushButton_7.clicked.connect(self.linked)
        self.pushButton_9.clicked.connect(self.face)
        


    def handel_file(self):
        self.tabWidget.setCurrentIndex(2)
    def handel_video(self):
        self.tabWidget.setCurrentIndex(0)
    def handel_pl(self):
        self.tabWidget.setCurrentIndex(1)
    def git(self):
        webbrowser.open_new_tab("https://github.com/zeyad-hisham-cyper")
    def face(self):
        webbrowser.open_new_tab("https://www.facebook.com/zeyad.hisham.716/")
    def linked(self):
        webbrowser.open_new_tab("https://www.linkedin.com/in/zeyad-hisham-a5127519b/")

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
        st = v.streams
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data ='{} {} {} {}'.format(s.mediatype , s.extension, s.quality, size)
            self.comboBox.addItem(data)
            QApplication.processEvents()
    
    def brows_video_loc(self):
        save = QFileDialog.getExistingDirectory(self, "Save As")
        self.lineEdit.setText(save)
        self.lineEdit_3.setText(save)

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
            st = v.streams
            quality = self.comboBox.currentIndex()
            start_download = st[quality].download(filepath=video_loc,callback=self.video_progressbar)
        
        except Exception:
            QMessageBox.warning(self, 'Alert', 'Download Faild\nTry Valid URL or Choose "Best quality"' ) 
            return
        QMessageBox.information(self, 'Alert', 'Download Completed')
        self.progressBar.setValue(0)
        self.videoURL.setText("")
        self.lineEdit.setText("")            
        self.label_4.setText("")
        self.comboBox.setCurrentIndex(0)

    def download_playlist(self):
        try:
            pl_url = self.lineEdit_2.text()
            pl = Playlist(pl_url)
            save_loc = self.lineEdit_3.text()
            for video in pl.videos:
                video.streams.first().download(output_path=save_loc)
                QApplication.processEvents()
        except Exception:
            QMessageBox.warning(self, 'Alert', 'Download Faild choose valid location and URL' ) 
            return 
   
        QMessageBox.information(self, 'Alert', 'Download Completed')
        self.progressBar_2.setValue(0)
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        
def main_app():
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main_app()

