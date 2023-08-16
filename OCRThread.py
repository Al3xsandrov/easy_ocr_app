import easyocr
from PyQt5.QtCore import QThread, pyqtSignal


class OCRThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):

        reader = easyocr.Reader(["ru", "en"], detector=True, recognizer=True)
        result = reader.readtext(self.file_path, detail=0, paragraph=True)
        text = ''
        for line in result:
            text += f"{line}\n\n"
        self.finished.emit(text)
