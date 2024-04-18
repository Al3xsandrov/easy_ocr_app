import os
import time
from PyQt5.QtWidgets import QMainWindow, QFileDialog, \
    QPushButton, QLineEdit, QTextBrowser, QCheckBox, QProgressBar
from app.MainWindow import Ui_mainWindow
from app.OCRThread import *


class Window(QMainWindow):
    """A class representing the application window."""
    def __init__(self) -> None:
        """Initializes the main window."""
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

    def setButtonsStatus(self, status: bool) -> None:
        """Enable or disable buttons based on the provided status.

        Args:
            status (bool): The status to set for buttons.
        """
        self.btn_run.setEnabled(status)
        self.file.setEnabled(status)
        self.file_path.setEnabled(status)
        self.as_txt.setEnabled(status)

    def getFile(self) -> None:
        """Opens a file dialog to get the image path."""
        fname = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")

        if fname and fname[0] != '':
            self.file_path.setText(fname[0])
            self.btn_run.setEnabled(True)

    def onRun(self) -> None:
        """Initiates OCR processing when the run button is clicked."""
        self.setButtonsStatus(False)
        self.progressBar.setRange(0, 0)

        file_path = self.file_path.text()
        ocrThread = OCRThread(file_path)
        ocrThread.finished.connect(self.onOCRComplete)
        ocrThread.start()
        self.threads.append(ocrThread)

    def onOCRComplete(self, text: str) -> None:
        """Handles OCR processing completion.

        Args:
            text (str): The extracted text.
        """
        self.result_box.setText(text)

        if self.as_txt.isChecked():
            timestr = time.strftime("%Y%m%d-%H%M%S")
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, f"{timestr}.txt")
            with open(file_path, "w") as f:
                f.write(text)

        self.setButtonsStatus(True)
        self.progressBar.setRange(0, 100)

    def closeEvent(self, event) -> None:
        """Overrides the close event of the window.

        Args:
            event: The close event.
        """
        for thread in self.threads:
            thread.terminate()
        event.accept()
