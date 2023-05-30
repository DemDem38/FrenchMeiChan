from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,  QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QColor, QKeySequence


import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from src.noyau_fonctionnel.scenario.Scenario import ReadScenarioXML, Question, Reponse, Noyau

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


class MainWindow(QMainWindow):
    signal_envoi = pyqtSignal(str)
    signal_stop = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.r = record(self)

        self.mainWidget = QWidget()
        self.layout = QVBoxLayout(self.mainWidget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setStyleSheet('background-color: white;')

        self.widget_internal = QWidget()
        self.widget_internal_layout = QGridLayout(self.widget_internal)
        self.widget_internal_layout.setColumnMinimumWidth(0, 300)  # Définit la largeur minimale de la première colonne à 300 pixels
        self.widget_internal_layout.setColumnStretch(1, 1)
        self.widget_internal_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_internal_layout.setSpacing(0)
        self.widget_internal_layout.setAlignment(Qt.AlignTop) 

        
        

        default_rows = 6

        for row in range(default_rows):
                spacer_item = QSpacerItem(60, 60, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
                self.widget_internal_layout.addItem(spacer_item,row,0,1,3)

        self.labels = []

        self.scroll_area.setWidget(self.widget_internal)

        self.layout.addWidget(self.scroll_area)

        self.text_entry = QLineEdit()
        self.text_entry.returnPressed.connect(self.add_reply) # 

        self.recordBoutton = QPushButton("Vocal")
        self.recordBoutton.pressed.connect(self.add_oral_reply)

        self.stopBoutton = QPushButton("StopVocal")
        self.stopBoutton.pressed.connect(self.stop_record)
        self.stopBoutton.setVisible(False)

        self.scroll_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.layout.addWidget(self.text_entry)
        self.layout.addWidget(self.recordBoutton)
        self.layout.addWidget(self.stopBoutton)

        self.setCentralWidget(self.mainWidget)
        self.generate_images()

    def generate_images(self):

        self.classiqueImage = QPixmap("src/ihm/robot/classique.jpg")
        self.contentImage = QPixmap("src/ihm/robot/content.jpg")
        self.tristeImage = QPixmap("src/ihm/robot/triste.jpg")

        self.listeImage = []

        self.listeImage.append(self.classiqueImage)
        self.listeImage.append(self.contentImage)
        self.listeImage.append(self.tristeImage)

    def add_left_label(self, text, idImage = 0):
        
        if text:
            wid = QWidget()
            lay = QHBoxLayout()
            wid.setLayout(lay)
            lay.setAlignment(Qt.AlignLeft)

            new_label = QTextEdit(text)
            new_label.setReadOnly(True)
            new_label.setMinimumHeight(200)
            new_label.setMaximumHeight(300)
            new_label.setAlignment(Qt.AlignCenter)

            self.labels.append(new_label)

            size = self.scroll_area.size()

            frame = QFrame()
            frame.setLineWidth(1)
            frame.setStyleSheet("QFrame { background-color: #90EE90; border-radius: 20px; border-style: outset; border-width: 1px; border-color: #555555; }")
            frame.setMaximumWidth(int(0.70 * size.width()))  # Définir la largeur maximale du QFrame
            frame.setFixedHeight(200)

            new_label.setStyleSheet("QTextEdit { color: black; padding-top: 50%; padding-bottom: 50%; }")

            frame_layout = QHBoxLayout(frame)  # Utiliser QHBoxLayout pour aligner à droite
            frame_layout.addWidget(new_label)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            frame_layout.setSpacing(0)
            frame_layout.setAlignment(Qt.AlignRight)

            self.widget_internal_layout.addWidget(wid,len(self.labels)-1,1)

            tete = QLabel()
            tete.setPixmap(self.listeImage[idImage])
            self.widget_internal_layout.addWidget(tete,len(self.labels)-1,0)

            lay.addWidget(frame)
            
            self.scroll_to_bottom()
            #speak_french(text)

            


    def add_right_label(self, text):
        if text:
            wid = QWidget()
            lay = QHBoxLayout()
            wid.setLayout(lay)
            lay.setAlignment(Qt.AlignRight)

            new_label = QTextEdit(text)
            new_label.setReadOnly(True)
            new_label.setMinimumHeight(200)
            #new_label.setMaximumHeight(300)
            new_label.setAlignment(Qt.AlignCenter)

            self.labels.append(new_label)

            size = self.scroll_area.size()
            sizeH = new_label.sizeHint()

            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setLineWidth(1)
            frame.setStyleSheet("QFrame { background-color: #ADD8E6; border-radius: 20px; border-style: outset; border-width: 1px; border-color: #555555; }")

            frame.setMaximumWidth(int(0.70 * size.width()))  # Définir la largeur maximale du QFrame
            frame.setMinimumHeight(200)

            new_label.setStyleSheet("QTextEdit { color: black; padding-top: 50%; padding-bottom: 50%; float: right; }")

            frame_layout = QHBoxLayout(frame)  # Utiliser QHBoxLayout pour aligner à droite
            frame_layout.addWidget(new_label)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            frame_layout.setSpacing(0)
            frame_layout.setAlignment(Qt.AlignRight)

            
            self.widget_internal_layout.addWidget(wid,len(self.labels)-1,1)

            lay.addWidget(frame)
            
            

            self.scroll_to_bottom()


    def add_reply(self):
        text = self.text_entry.text()
        self.add_right_label(text)
        self.envoyer_string(text)
        self.text_entry.clear()

    def add_oral_reply(self):
        self.recordBoutton.setVisible(False)
        self.stopBoutton.setVisible(True)
        self.recThread = RecordingThread(self)
        self.recThread.recording_finished.connect(self.add_right_label)
        self.recThread.recording_finished.connect(self.envoyer_string)
        self.recThread.start()


    def stop_record(self):
        self.signal_stop.emit()
        self.recordBoutton.setVisible(True)
        self.stopBoutton.setVisible(False)

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    

    def envoyer_string(self, texte):
        self.signal_envoi.emit(texte)


app = QApplication([])

widget = MainWindow()

n = Noyau(widget)

screen_geometry = QDesktopWidget().availableGeometry()
widget.resize(screen_geometry.width(), int(0.95 * screen_geometry.height()))

widget.show()
app.exec_()
