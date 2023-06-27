import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QSizePolicy,
)
from PyQt6.QtGui import QAction

from gantt import parse, make_html
from editor import GanttEditor
from file_ui import FileUI


class MainWindow(QMainWindow):
    TITLE = "gantitt"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._menubar = self.menuBar()

        body = QFrame()
        body.setLayout(QVBoxLayout())
        body.layout().setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(body)

        self.editor = GanttEditor()
        body.layout().addWidget(self.editor)

        button_frame = QFrame()
        button_frame.setLayout(QHBoxLayout())
        body.layout().addWidget(button_frame)

        self.gantt_button = QPushButton("Gantt it!")
        self.gantt_button.setToolTip("Ctrl+Return")
        self.gantt_button.clicked.connect(self._gantt)
        self.gantt_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        button_frame.layout().addWidget(self.gantt_button)

        self._file_ui = FileUI()
        self._file_menu = QMenu("&File", self)
        self._menubar.addMenu(self._file_menu)
        self._file_ui.populate_menu(self._file_menu)

        self.editor.text_changed.connect(self.setWindowModified)

        self._file_ui.new_file.connect(self._new_file)
        self._file_ui.open_file.connect(self._open_file)
        self._file_ui.save_file.connect(self._save_file)
        self._file_ui.quit.connect(self.close)

        self._gantt_action = QAction()
        self._gantt_action.triggered.connect(self._gantt)
        self._gantt_action.setShortcut("Ctrl+Return")
        self.addAction(self._gantt_action)

        self.setGeometry(400, 100, 600, 600)
        self._new_file()

    def _show_error(self, e: Exception):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setWindowTitle(self.TITLE)
        message_box.setText(str(e))
        return message_box.exec()

    def _set_title(self, filepath: str):
        if not filepath:
            self.setWindowTitle(f"[*] - {self.TITLE}")
            return
        basename, _ = os.path.splitext(os.path.basename(filepath))
        self.setWindowTitle(f"{basename}[*] - {self.TITLE}")

    def _new_file(self):
        self.editor.clear()
        self.setWindowModified(False)
        self.setWindowTitle(self.TITLE)

    def _open_file(self, filepath: str):
        try:
            with open(filepath, encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            self._show_error(e)
        else:
            self.editor.setPlainText(text)
            self._file_ui.filepath = filepath
            self._set_title(filepath)
            self.setWindowModified(False)

    def _save_file(self, filepath):
        text = self.editor.toPlainText()
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            self._show_error(e)
        else:
            self._set_title(filepath)
            self.setWindowModified(False)

    def _gantt(self):
        text = self.editor.toPlainText()
        filepath = "chart.html"
        try:
            with open(filepath, mode="w", encoding="utf-8") as f:
                make_html(f, plan=parse(text))
            os.startfile(filepath)
        except Exception as e:
            self._show_error(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
