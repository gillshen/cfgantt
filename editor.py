from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont


class GanttEditor(QPlainTextEdit):
    text_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFrameShape(QPlainTextEdit.Shape.NoFrame)
        self.document().setDocumentMargin(6)
        self.setFont(QFont("Consolas"))

        self._saved_text = ""
        self.textChanged.connect(self._on_text_change)

    def _on_text_change(self):
        self.text_changed.emit(self.toPlainText() != self._saved_text)

    def clear(self):
        self._saved_text = ""
        return super().clear()

    def setPlainText(self, text: str):
        self._saved_text = text
        return super().setPlainText(text)
