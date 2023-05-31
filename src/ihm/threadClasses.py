from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget,  QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget

from datetime import datetime
import pandas as pd

from src.noyau_fonctionnel.scenario.Scenario import Noyau
from src.noyau_fonctionnel.language.voice.control_time_recorder import record
from src.noyau_fonctionnel.language.voice.speak_french import speak_french

class RecordingThread(QThread):

    recording_finished = pyqtSignal(str)

    def __init__(self,ihm):
        super().__init__()
        self.record = record(ihm)

    def run(self):
        text = self.record.recording()

        self.recording_finished.emit(text)


class SpeakThread(QThread):

    def __init__(self,text):
        super().__init__()
        self.text=text

    def run(self):
        speak_french(self.text)