from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QSlider,QProgressBar, QFileDialog, QStackedLayout, QWidget,  QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap,QPalette, QColor

from datetime import datetime
import pandas as pd

from src.noyau_fonctionnel.scenario.Scenario import Noyau
from src.noyau_fonctionnel.language.voice.control_time_recorder import record
from src.noyau_fonctionnel.authentication.account import account

from src.ihm.threadClasses import RecordingThread, SpeakThread
from src.ihm.parametreWindows import parametreWidget
from src.ihm.addContactWindows import personWidget
from src.ihm.personalInformationWindows import personalInfoWidget
from src.ihm.gestionContactWindows import contactWidget
from src.ihm.changeContactWindows import modifyContactWidget

from src.noyau_fonctionnel.iaChat.ia import agent

import os

class MainWindow(QMainWindow):
    signal_envoi_on = pyqtSignal(str)
    signal_envoi_off = pyqtSignal(str)
    signal_stop = pyqtSignal()

    signal_llm_send = pyqtSignal(str)
    signal_llm_receive = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.account = None

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

        self.person_button = QPushButton("Contact")
        self.person_button.pressed.connect(self.open_person)
        self.person_layout.addWidget(self.person_button)

        self.mode = QWidget()
        self.mode_layout = QHBoxLayout(self.mode)
        self.mode_layout.setAlignment(Qt.AlignRight)

        self.switchMode = QPushButton("Changer de mode")
        self.switchMode.pressed.connect(self.change_mode)
        self.mode_layout.addWidget(self.switchMode)

        self.boolMode = True

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

        self.progressRecordBar = QProgressBar()
        self.progressRecordBar.setRange(0, 0)
        self.progressRecordBar.setVisible(False)

        palette = self.progressRecordBar.palette()
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))  # Couleur de remplissage
        palette.setColor(QPalette.Background, Qt.white)  # Couleur de fond
        self.progressRecordBar.setPalette(palette)

        self.csvButton = QPushButton("Enregistrer")
        self.csvButton.pressed.connect(self.toCSV)

        self.importButton = QPushButton("Import")
        self.importButton.pressed.connect(self.importCSV)

        self.scroll_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.chatbox_layout.addWidget(self.parametre)
        self.chatbox_layout.addWidget(self.person)
        self.chatbox_layout.addWidget(self.mode)
        self.chatbox_layout.addWidget(self.scenario_entry)
        self.chatbox_layout.addWidget(self.scroll_area)
        self.chatbox_layout.addWidget(self.text_entry)
        self.chatbox_layout.addWidget(self.recordBoutton)
        self.chatbox_layout.addWidget(self.stopBoutton)
        self.chatbox_layout.addWidget(self.progressRecordBar)
        self.chatbox_layout.addWidget(self.csvButton)
        self.chatbox_layout.addWidget(self.importButton)

        self.setCentralWidget(self.mainWidget)
        self.generate_images()

        self.paraWidget = parametreWidget(self)
        self.contactGestion = contactWidget(self)
        self.personWidget = personWidget(self)
        self.userWidget = personalInfoWidget(self)
        self.modifyContactWidget = modifyContactWidget(self)
        self.mainLayout.addWidget(self.paraWidget)
        self.mainLayout.addWidget(self.contactGestion)
        self.mainLayout.addWidget(self.personWidget)
        self.mainLayout.addWidget(self.userWidget)
        self.mainLayout.addWidget(self.modifyContactWidget)
        self.scenario = Noyau(self)
        
        self.scenario_entry.setMaximum(self.scenario.numnScenario())
        self.scenario_entry.setMinimum(1)
        self.scenario_entry.setValue(1)
        self.scenario_entry.setOrientation(Qt.Horizontal)
        self.scenario_entry.setTickPosition(QSlider.TicksBelow)

        self.llm = agent(self.signal_llm_send,self.signal_llm_receive)
        self.signal_llm_receive.connect(self.receive_llm_reply)

        self.first_windows()

        self.paraWidget.changeSizeText()
        
    def first_windows(self):
        """
        determine quelle sera la premiere fenetre affiche, selon si le fichier contenant les informations de l'utilisateur existe, ou non
        
        arg: None

        return: None
        """
        file_path = "data/account.json"

        if os.path.isfile(file_path):
            self.account = account()

            self.userWidget.infoPrint.setVisible(False)
            self.userWidget.annulerButton.setVisible(True)
        else:
            self.mainLayout.setCurrentIndex(4)

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

        self.leftQFrame = []

        self.rightQFrame = []
        
        self.scroll_area.setWidget(self.widget_internal)


    def generate_images(self):
        """
        Creer tous les QPixmap et les store dans self.listeImage

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
        """
        Change la fenêtre courante pour afficher la fenêtre de paramètre

        arg: None

        return: None
        """
        self.mainLayout.setCurrentIndex(1)

    def open_person(self):
        """
        switch the current windows for the parametre windows

        arg: None

        return: None        
        """
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
            self.setLeftFrameApparence(frame)
            frame.setMaximumWidth(int(0.70 * size.width()))  # Définir la largeur maximale du QFrame
            frame.setFixedHeight(200)
            self.leftQFrame.append(frame)

            self.setLabelProp(new_label)
            
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
        Genere un QFrame a droite du ScrollArea, qui contient un QTextEdit avec text comme contenu

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
            self.setRightFrameApparence(frame)
            self.rightQFrame.append(frame)
            frame.setMaximumWidth(int(0.70 * size.width()))  # Définir la largeur maximale du QFrame
            frame.setMinimumHeight(200)

            self.setLabelProp(new_label)

            frame_layout = QHBoxLayout(frame)  # Utiliser QHBoxLayout pour aligner à droite
            frame_layout.addWidget(new_label)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            frame_layout.setSpacing(0)
            frame_layout.setAlignment(Qt.AlignRight)

            

            self.widget_internal_layout.addWidget(wid,len(self.labels)-1,1)

            lay.addWidget(frame)
            if self.paraWidget.saveEntry.isChecked():
                self.toCSV()
            self.scroll_to_bottom()

    def setLeftFrameApparence(self,frame):
        """
        Change le StyleSheet de frame dans le but qu'il correspond au meme que les QFrame du cote gauche

        arg: -frame: QFrame | frame that we when to change the StyleSheet

        return: None
        """
        frame.setStyleSheet("QFrame{{ background-color: {}; border-radius: 20px; border-style: outset; border-width: 1px; border-color: #555555; text}}".format(self.paraWidget.leftColor))

    def setLabelProp(self,label):
        """
        Change le StyleSheet pour changer la taille du texte

        arg: -label: QLabel | label that we when to change the StyleSheet

        return: None
        """
        size = (str) ((int) (self.paraWidget.sizeText)) + "px"
        label.setStyleSheet("QTextEdit {{ color: black; font-size: {}; padding-top: 50%; padding-bottom: 50%; float: right; }}".format(size))
        

    def setRightFrameApparence(self,frame):
        """
        Change le StyleSheet de frame dans le but qu'il correspond au meme que les QFrame du cote droit

        arg: -frame: QFrame | frame that we when to change the StyleSheet

        return: None
        """
        frame.setStyleSheet("QFrame {{ background-color: {}; border-radius: 20px; border-style: outset; border-width: 1px; border-color: #555555; }}".format(self.paraWidget.rightColor))


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
        Lance un enregistrement vocal et change le bouton pour celui qui stop le record

        arg: None

        return: None
        """

        self.recordBoutton.setVisible(False)
        self.recordBoutton.setEnabled(False)
        self.text_entry.setReadOnly(True)
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
        self.progressRecordBar.setVisible(True)
        self.stopBoutton.setVisible(False)

    def scroll_to_bottom(self):
        """
        Scroll pour etre a la fin du ScrollArea

        arg: None

        return: None
        """
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    

    def envoyer_string_on(self, texte):
        """
        Envoie un string a la partie scenario

        arg: -texte: string

        return: None
        """
        self.recordBoutton.setEnabled(True)
        self.text_entry.setReadOnly(False)
        self.progressRecordBar.setVisible(False)
        self.recordBoutton.setVisible(True)
        if self.boolMode:
            self.signal_envoi_on.emit(texte)
        else:
            self.signal_llm_send.emit(texte)

    def envoyer_string_off(self, texte):
        """
        Envoie un string a la partie scenario

        arg: -texte: string

        return: None
        """
        if self.boolMode:
            self.signal_envoi_off.emit(texte)
        else:
            self.signal_llm_send.emit(texte)

    def init_filename(self):
        """
        Initialise self.filename avec l'horodatage

        arg: None

        return: None
        """
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
        if self.paraWidget.saveEntry.isChecked() and self.boolMode:
                self.toCSV()

        indice = self.scenario_entry.value()
        self.init_internat_widget()
        self.scenario.startScenario(indice)

        self.text_entry.setReadOnly(False)
        self.recordBoutton.setEnabled(True)

    def importCSV(self):
        """
        Permet de choisir un fichier csv, et remet le chat bot dans les meme conditions que lors de l'enregistrement du fichier

        arg: None

        return: None
        """
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
                
    def change_mode(self):
        if not(self.boolMode):
            self.change_scenario()
        else:
            self.init_internat_widget()
        self.boolMode = not(self.boolMode)
        self.scenario_entry.setVisible(self.boolMode)

    def receive_llm_reply(self,texte):
        self.add_left_label(texte, speak = False, idImage = 0)