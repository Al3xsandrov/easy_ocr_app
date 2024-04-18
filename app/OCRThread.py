import easyocr
from PyQt5.QtCore import QThread, pyqtSignal


class OCRThread(QThread):
    """Thread for performing OCR on an image file.

    Attributes:
        finished (pyqtSignal): Signal emitted when OCR processing is complete.

    """
    finished = pyqtSignal(str)

    def __init__(self, file_path: str) -> None:
        """Initialize the OCRThread.

        Args:
            file_path (str): The path to the image file.
        """
        super().__init__()
        self.file_path = file_path

    def run(self) -> None:
        """Perform OCR processing on the image file."""
        reader = easyocr.Reader(["ru", "en"], detector=True, recognizer=True)
        result = reader.readtext(self.file_path, detail=0, paragraph=True)
        text = ''
        for line in result:
            text += f"{line}\n\n"
        self.finished.emit(text)
