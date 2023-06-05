from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication,QSlider, QFileDialog, QStackedLayout, QWidget,  QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QColor, QKeySequence

from datetime import datetime
import pandas as pd

from src.noyau_fonctionnel.scenario.Scenario import Noyau
from src.noyau_fonctionnel.language.voice.control_time_recorder import record

from src.ihm.threadClasses import RecordingThread, SpeakThread
from src.ihm.parametreWindows import parametreWidget
from src.ihm.personWindows import personWidget

class MainWindow(QMainWindow):
    signal_envoi_on = pyqtSignal(str)
    signal_envoi_off = pyqtSignal(str)
    signal_stop = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.r = record(self)

        
        self.mainWidget = QWidget()
        self.mainLayout = QStackedLayout(self.mainWidget)
        self.layout = QVBoxLayout()
        

        self.chatboxWidget = QWidget()
        self.chatbox_layout = QVBoxLayout(self.chatboxWidget)
        self.mainLayout.addWidget(self.chatboxWidget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setStyleSheet('background-color: white;')
        
        self.parametre = QWidget()
        self.para_layout = QHBoxLayout(self.parametre)
        self.para_layout.setAlignment(Qt.AlignRight)

        self.para_button = QPushButton("Parametre")
        self.para_button.pressed.connect(self.open_parametre)
        self.para_layout.addWidget(self.para_button)

        self.person = QWidget()
        self.person_layout = QHBoxLayout(self.person)
        self.person_layout.setAlignment(Qt.AlignRight)

        self.person_button = QPushButton("Person")
        self.person_button.pressed.connect(self.open_person)
        self.person_layout.addWidget(self.person_button)

        self.init_internat_widget()
        
        self.scenario_entry = QSlider()
        
        self.scenario_entry.sliderReleased.connect(self.change_scenario) 

        self.text_entry = QLineEdit()
        self.text_entry.returnPressed.connect(self.add_reply)

        self.recordBoutton = QPushButton("Vocal")
        self.recordBoutton.pressed.connect(self.add_oral_reply)

        self.stopBoutton = QPushButton("StopVocal")
        self.stopBoutton.pressed.connect(self.stop_record)
        self.stopBoutton.setVisible(False)

        self.csvButton = QPushButton("Enregistrer")
        self.csvButton.pressed.connect(self.toCSV)

        self.importButton = QPushButton("Import")
        self.importButton.pressed.connect(self.importCSV)

        self.scroll_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.chatbox_layout.addWidget(self.parametre)
        self.chatbox_layout.addWidget(self.person)
        self.chatbox_layout.addWidget(self.scenario_entry)
        self.chatbox_layout.addWidget(self.scroll_area)
        self.chatbox_layout.addWidget(self.text_entry)
        self.chatbox_layout.addWidget(self.recordBoutton)
        self.chatbox_layout.addWidget(self.stopBoutton)
        self.chatbox_layout.addWidget(self.csvButton)
        self.chatbox_layout.addWidget(self.importButton)

        self.setCentralWidget(self.mainWidget)
        self.generate_images()

        self.paraWidget = parametreWidget(self,self.mainWidget)
        self.personWidget = personWidget(self)
        self.mainLayout.addWidget(self.paraWidget)
        self.mainLayout.addWidget(self.personWidget)
        self.scenario = Noyau(self)
        self.scenario_entry.setMaximum(self.scenario.numnScenario())
        self.scenario_entry.setMinimum(1)
        self.scenario_entry.setOrientation(Qt.Horizontal)
        self.scenario_entry.setTickPosition(QSlider.TicksBelow)

    def init_internat_widget(self):
        """
        Creer, setup et add le widget qui est dans le QScrollArea (self.scroll_area)

        arg: None

        return: None
        """
        self.init_filename()
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

    def generate_images(self):
        """
        create all QPixmap and store them in self.listeImage

        arg: None

        return: None
        """
        self.classiqueImage = QPixmap("src/ihm/robot/classique.jpg")
        self.contentImage = QPixmap("src/ihm/robot/content.jpg")
        self.tristeImage = QPixmap("src/ihm/robot/triste.jpg")

        self.listeImage = []

        self.listeImage.append(self.classiqueImage)
        self.listeImage.append(self.contentImage)
        self.listeImage.append(self.tristeImage)

    def open_parametre(self):
        
        self.mainLayout.setCurrentIndex(1)

    def open_person(self):
        
        self.mainLayout.setCurrentIndex(2)


    def add_left_label(self, text, idImage = 0 , speak = True):
        """
        Genere un QFrame a gauche du ScrollArea, qui contient un QTextEdit avec text comme contenu ainsi qu'une image de robot

        arg: -text: str | Texte a afficher dans le QFrame
             -idImage: int | ID de l'image a afficher a cote du texte, id correspond a l'indice dans self.listeImage
             -speak: bool | Boolean pour determiner si le texte doit etre si a haute voix ou non

        return: None
        """

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

            self.labels.append([new_label,"bot"])

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
            if speak:
                self.speak = SpeakThread(text,self)
                self.speak.start()
            


    def add_right_label(self, text):
        """
        Genere un QFrame a droite du ScrollArea, qui contient un QTextEdit avec text comme contenu ainsi qu'une image de robot

        arg: -text: str | Texte a afficher dans le QFrame

        return: None
        """
        if text:
            wid = QWidget()
            lay = QHBoxLayout()
            wid.setLayout(lay)
            lay.setAlignment(Qt.AlignRight)

            new_label = QTextEdit(text)
            new_label.setReadOnly(True)
            new_label.setMinimumHeight(200)
            new_label.setAlignment(Qt.AlignCenter)

            self.labels.append([new_label,"user"])

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
            if self.paraWidget.saveEntry.isChecked():
                print("save")
                self.toCSV()
            self.scroll_to_bottom()


    def add_reply(self):
        """
        Recupere le texte dans self.text_entry l'ajoute a droite du ScrollArea
        Envoie aussi le string au scenario afin d'avoir la suite du dialog

        arg: None

        return: None
        """
        text = self.text_entry.text()
        self.add_right_label(text)
        self.envoyer_string_on(text)
        self.text_entry.clear()

    def add_oral_reply(self):
        """
        Lance un enregistrement vocal et change le boutton pour celui qui stop le record

        arg: None

        return: None
        """
        self.recordBoutton.setVisible(False)
        self.stopBoutton.setVisible(True)
        self.recThread = RecordingThread(self)
        self.recThread.recording_finished.connect(self.add_right_label)
        self.recThread.recording_finished.connect(self.envoyer_string_on)
        self.recThread.start()


    def stop_record(self):
        """
        Stop le record

        arg: None

        return: None
        """
        self.signal_stop.emit()
        self.recordBoutton.setVisible(True)
        self.stopBoutton.setVisible(False)

    def scroll_to_bottom(self):
        """
        Scroll pour etre a la fin du ScrollArea
        """
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    

    def envoyer_string_on(self, texte):
        """
        Envoie un string a la partie scenario

        arg: -texte: string

        return: None
        """
        self.signal_envoi_on.emit(texte)

    def envoyer_string_off(self, texte):
        """
        Envoie un string a la partie scenario

        arg: -texte: string

        return: None
        """
        self.signal_envoi_off.emit(texte)

    def init_filename(self):
        horodatage_actuel = datetime.now()
        # Formater l'horodatage
        format_horodatage = "%Y-%m-%d_%H-%M-%S"
        horodatage_formate = horodatage_actuel.strftime(format_horodatage)
        self.filename = "data/log/"+horodatage_formate+".csv"

    def toCSV(self):
        """
        Prend la conversation actuel et l'export au format csv. Le fichier est enregistrer dans data/log et le nom du fichier et l'horodatage

        arg: None

        return: None
        """
        

        idScenario = self.scenario.getIDscenario()

        conversation = []
        for i in self.labels:
            lab,stri = i
            txt = lab.toPlainText()
            conversation.append({'auteur': stri, 'contenu': txt, 'scenario': idScenario})

        df = pd.DataFrame(conversation)
        df = df[['auteur', 'contenu','scenario']]
        df.to_csv(self.filename, index=False)

    def change_scenario(self):
        """
        Change le scenario qui s'execute

        arg: None

        return: None
        """
        indice = self.scenario_entry.value()
        self.init_internat_widget()
        self.scenario.startScenario(indice-1)

        self.text_entry.setReadOnly(False)
        self.recordBoutton.setEnabled(True)

    def importCSV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileDialog = QFileDialog()
        fileDialog.setOptions(options)

        fileDialog.setNameFilter("Fichiers CSV (*.csv)")

        fileDialog.setDirectory("data/log")  # Définir le répertoire de départ

        if fileDialog.exec_() == QFileDialog.Accepted:
            selected_path = fileDialog.selectedFiles()[0]
            print("Chemin sélectionné:", selected_path)

            df = pd.read_csv(selected_path)

            num_scenario = df.iloc[0]["scenario"]
            print(num_scenario)

            for index, row in df.iterrows():
                if row["auteur"] == "user":
                    self.add_right_label(row["contenu"])
                    self.envoyer_string_off(row["contenu"])
                
