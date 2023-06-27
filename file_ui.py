import os

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QMenu, QFileDialog


class FileUI(QWidget):
    """Initiator of file operations"""

    new_file = pyqtSignal()
    open_file = pyqtSignal(str)
    save_file = pyqtSignal(str)

    quit = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filepath = ""
        self._open_dir = ""
        self._save_dir = ""

        self._new_action = QAction("&New")
        self._new_action.triggered.connect(self._new_file)
        self._new_action.setShortcut("Ctrl+n")

        self._open_action = QAction("&Open...")
        self._open_action.triggered.connect(self._get_open_filepath)
        self._open_action.setShortcut("Ctrl+o")

        self._save_action = QAction("&Save")
        self._save_action.triggered.connect(self._get_save_filepath)
        self._save_action.setShortcut("Ctrl+s")

        self._saveas_action = QAction("Save &As...")
        self._saveas_action.triggered.connect(self._get_saveas_filepath)
        self._saveas_action.setShortcut("Ctrl+Shift+s")

        self._quit_action = QAction("&Quit")
        self._quit_action.triggered.connect(self.quit.emit)
        self._quit_action.setShortcut("Ctrl+q")

    def populate_menu(self, menu: QMenu):
        menu.addAction(self._new_action)
        menu.addAction(self._open_action)

        menu.addSeparator()
        menu.addAction(self._save_action)
        menu.addAction(self._saveas_action)

        menu.addSeparator()
        menu.addAction(self._quit_action)

    def _new_file(self):
        self._open_dir = ""
        self.new_file.emit()

    def _get_open_filepath(self):
        filepath, _ = QFileDialog.getOpenFileName(
            caption="Open File",
            directory=self._open_dir,
            filter="Text Files (*.txt)",
        )
        if filepath:
            self._open_dir = os.path.dirname(filepath)
            self.open_file.emit(filepath)

    def _get_save_filepath(self):
        if self.filepath:
            self.save_file.emit(self.filepath)
        else:
            self._get_saveas_filepath()

    def _get_saveas_filepath(self):
        filepath, _ = QFileDialog.getSaveFileName(
            caption="Save File",
            directory=self._save_dir,
            filter="TXT Files (*.txt)",
        )
        if filepath:
            self._save_dir = os.path.dirname(filepath)
            self.save_file.emit(filepath)
