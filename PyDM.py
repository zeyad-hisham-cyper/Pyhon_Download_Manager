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
from pytube import *
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
        self.setWindowIcon(QIcon('img\\logo.ico'))
        self.setWindowTitle("PyDM")
        self.setFixedSize(self.size())
        self.tabWidget.setCurrentIndex(0)
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
        self.tabWidget.setCurrentIndex(3)
    def handel_video(self):
        self.tabWidget.setCurrentIndex(1)
    def handel_pl(self):
        self.tabWidget.setCurrentIndex(2)
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
        try:
            link = self.videoURL.text()
            v = pafy.new(link)
            st = v.streams
            title = v.title
            durat = v.duration
            rate = v.rating
            rating = "%2.f" %rate

            self.label_7.setText("Title: " + title)
            self.label_8.setText("Duration: " + durat)
            self.label_9.setText("Rating: " + rating)

            for s in st:
                size = humanize.naturalsize(s.get_filesize())
                data ='{} {} {} {}'.format(s.mediatype , s.extension, s.quality, size)
                self.comboBox.addItem(data)
                QApplication.processEvents()
        except Exception:
            QMessageBox.warning(self, 'Alert', 'Faild\nTry Valid URL"' ) 
            return


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
            self.lineEdit_3.setText("")
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
        self.label_7.setText("")
        self.label_8.setText("")
        self.label_9.setText("")
        self.comboBox.setCurrentIndex(0)

    def download_playlist(self):
        try:
            self.lineEdit.setText("")
            pl_url = self.lineEdit_2.text()
            pl = Playlist(pl_url)
            save_loc = self.lineEdit_3.text()
            index = self.comboBox_2.currentIndex()
            vn = str(len(pl))
            self.label_11.setText("Videos Number: " + vn)
            if index == 0:
                for link in pl:
                    video = YouTube(link, on_progress_callback= self.pl_progress)
                    video.streams.get_highest_resolution().download(output_path=save_loc)
                    i +=1
            elif index == 1 :
                for link in pl:
                    video = YouTube(link, on_progress_callback= self.pl_progress)
                    video.streams.get_lowest_resolution().download(output_path=save_loc)
        except Exception:
            QMessageBox.warning(self, 'Alert', 'Download Faild choose valid location and URL' ) 
            return 
        QMessageBox.information(self, 'Alert', 'Download Completed')
        self.progressBar_2.setValue(0)
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        QApplication.processEvents()
    def pl_progress(self, stream , chunk , byte_remaining):
        x = round(((stream.filesize - byte_remaining) / stream.filesize)*100,0)
        self.progressBar_2.setValue(x)
        QApplication.processEvents()
    

        
def main_app():
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main_app()

