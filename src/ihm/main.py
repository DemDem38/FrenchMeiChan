from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QColor, QKeySequence


import sys
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from src.noyau_fonctionnel.scenario.Scenario import ReadScenarioXML, Question, Reponse, Noyau
from src.noyau_fonctionnel.language.voice.control_time_recorder import record
from src.noyau_fonctionnel.language.voice.speak_french import speak_french

class WorkerThread(QThread):
    message_received = pyqtSignal(str)

    def run(self):
        listeScenario = ReadScenarioXML("src/noyau_fonctionnel/scenario/listScenario.xml")
        q = listeScenario[1]

        self.message_received.emit("Bonjour")
        reponse = input()

        while q is not None:
            self.message_received.emit(q.getTxt())
            reponse = input()

            listeReponse = q.getReponse()
            rep = 0
            for i in range(len(listeReponse)):
                if listeReponse[i].compared(reponse) and rep == 0:
                    listeReponse[i].print()
                    self.message_received.emit(listeReponse[i].getTxt())
                    rep += 1
                    q = listeReponse[i].getQuestion()
            if rep == 0:
                print("Je ne comprends pas")
            print("ok")
            self.message_received.emit("ok")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWidget = QWidget()
        self.layout = QVBoxLayout(self.mainWidget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.widget_internal = QWidget()
        self.widget_internal_layout = QGridLayout(self.widget_internal)

        default_rows = 6
        default_columns = 3

        for row in range(default_rows):
            for col in range(default_columns):
                self.widget_internal_layout.addWidget(QLabel(), row, col, 1, 1)

        self.labels = []

        self.scroll_area.setWidget(self.widget_internal)

        self.layout.addWidget(self.scroll_area)

        self.text_entry = QLineEdit()
        self.text_entry.returnPressed.connect(self.add_reply) # 

        self.boutton = QPushButton("Vocal")
        self.boutton.pressed.connect(self.add_oral_reply)

        self.scroll_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.layout.addWidget(self.text_entry)
        self.layout.addWidget(self.boutton)

        self.setCentralWidget(self.mainWidget)

    def add_left_label(self, text):
        
        if text:
            new_label = QLabel(text)
            new_label.setMinimumHeight(200)
            new_label.setMaximumHeight(300)
            self.labels.append(new_label)

            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setLineWidth(1)
            frame.setStyleSheet("QFrame { background-color: #90EE90; border-radius: 20px; }")
            frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(new_label)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            frame_layout.setSpacing(0)

            row = len(self.labels) - 1
            self.widget_internal_layout.addWidget(frame, row, 0, 1, 2)

            frame.setMinimumHeight(new_label.sizeHint().height())

            self.scroll_to_bottom()
            speak_french(text)

    def add_right_label(self, text):
        if text:
            new_label = QLabel(text)
            new_label.setMinimumHeight(200)
            new_label.setMaximumHeight(300)
            new_label.setAlignment(Qt.AlignCenter)

            size = new_label.sizeHint()

            self.labels.append(new_label)

            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setLineWidth(1)
            frame.setStyleSheet("QFrame { background-color: #ADD8E6; border-radius: 20px; }")

            new_label.setStyleSheet("color: black;")

            frame_layout = QVBoxLayout(frame)
            frame_layout.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(new_label)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            frame_layout.setSpacing(0)

            row = len(self.labels) - 1
            self.widget_internal_layout.addWidget(frame, row, 1, 1, 2)

            frame.setFixedHeight(200)

            self.scroll_to_bottom()

    def add_reply(self):
        text = self.text_entry.text()
        self.add_right_label(text)
        self.envoyer_string(text)
        self.text_entry.clear()

    def add_oral_reply(self):
        text = record()
        self.add_right_label(text)
        self.envoyer_string(text)


    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    signal_envoi = pyqtSignal(str)

    def envoyer_string(self, texte):
        self.signal_envoi.emit(texte)



app = QApplication([])

widget = MainWindow()

n = Noyau(widget)

screen_geometry = QDesktopWidget().availableGeometry()
widget.resize(screen_geometry.width(), int(0.95 * screen_geometry.height()))

widget.show()
app.exec_()