import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, \
    QPushButton, QLineEdit, QTextBrowser, QCheckBox, QProgressBar
from MainWindow import Ui_mainWindow
from OCRThread import *


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.file = self.findChild(QPushButton, "file")
        self.file_path = self.findChild(QLineEdit, "file_path")
        self.btn_run = self.findChild(QPushButton, "btn_run")
        self.result_box = self.findChild(QTextBrowser, "result_box")
        self.as_txt = self.findChild(QCheckBox, "as_txt")
        self.progressBar = self.findChild(QProgressBar, "progressBar")

        self.file.clicked.connect(self.getFile)
        self.btn_run.clicked.connect(self.onRun)

        self.threads = []

    def setButtonsStatus(self, status):
        self.btn_run.setEnabled(status)
        self.file.setEnabled(status)
        self.file_path.setEnabled(status)
        self.as_txt.setEnabled(status)

    def getFile(self):
        fname = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")

        if fname and fname[0] != '':
            self.file_path.setText(fname[0])
            self.btn_run.setEnabled(True)

    def onRun(self):
        self.setButtonsStatus(False)
        self.progressBar.setRange(0, 0)

        file_path = self.file_path.text()
        ocrThread = OCRThread(file_path)
        ocrThread.finished.connect(self.onOCRComplete)
        ocrThread.start()
        self.threads.append(ocrThread)

    def onOCRComplete(self, text):
        self.result_box.setText(text)

        if self.as_txt.isChecked():
            timestr = time.strftime("%Y%m%d-%H%M%S")
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, f"{timestr}.txt")
            with open(file_path, "w") as f:
                f.write(text)

        self.setButtonsStatus(True)
        self.progressBar.setRange(0, 100)

    def closeEvent(self, event):
        for thread in self.threads:
            thread.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
