from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QCheckBox,QColorDialog , QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSlider
import json


class parametreWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.setGeometry(200, 200, 300, 200)
        
        self.layout = QVBoxLayout(self)
        self.settingsFileName()
        self.importSettings()
        self.addVolumeWidget()
        self.addRateWidget()
        self.addSaveWidget()
        self.chooseLeftColor()
        self.chooseRightColor()
        self.addSizeTextWidget()
        self.addReturnButton()       

        self.layout.addWidget(self.returnButton)

    def addVolumeWidget(self):
    
        self.volumeWidget = QWidget()
        self.volumeLayout = QHBoxLayout(self.volumeWidget)
        self.volumeLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.volumeWidget)

        self.volumePrint = QLabel("Volume de lecture")
        self.volumeEntry = QSlider()

        self.volumeEntry.setMaximum(200)
        self.volumeEntry.setMinimum(0)
        self.volumeEntry.setValue(self.volumeValue)
        self.volumeEntry.setOrientation(Qt.Horizontal)
        self.volumeEntry.setTickPosition(QSlider.TicksBelow)

        self.volumeLayout.addWidget(self.volumePrint)
        self.volumeLayout.addWidget(self.volumeEntry)

    def addRateWidget(self):
        
        self.rateWidget = QWidget()
        self.rateLayout = QHBoxLayout(self.rateWidget)
        self.rateLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.rateWidget)

        self.ratePrint = QLabel("Vitesse de lecture")
        self.rateEntry = QSlider()

        

        self.rateEntry.setMaximum(200)
        self.rateEntry.setMinimum(0)
        self.rateEntry.setValue(self.rateValue)
        self.rateEntry.setOrientation(Qt.Horizontal)
        self.rateEntry.setTickPosition(QSlider.TicksBelow)

        self.rateLayout.addWidget(self.ratePrint)
        self.rateLayout.addWidget(self.rateEntry)

    def addSaveWidget(self):
        """
        Ajoute la case checkable au widget parametre
        """
        self.saveWidget = QWidget()
        self.saveLayout = QHBoxLayout(self.saveWidget)
        self.saveLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.saveWidget)

        self.savePrint = QLabel("Sauvegarde automatique")
        self.saveEntry = QCheckBox()
        self.saveEntry.setChecked(self.boolSave)

        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 100px;
                height: 60px;
            }
            
            QCheckBox::indicator:unchecked {
                background-color: #CA3C1F;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
            }
            
            QCheckBox::indicator:checked:disabled {
                background-color: #aaa;
            }
        """)

        self.saveLayout.addWidget(self.savePrint)
        self.saveLayout.addWidget(self.saveEntry)

    def chooseLeftColor(self):
        """
        Ajoute le bouton et le label permettant de choisir/visualiser la couleur des QFrame gauche
        """
        self.leftColorWidget = QWidget()
        self.leftColorLayout = QHBoxLayout(self.leftColorWidget)
        self.leftColorLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.leftColorWidget)

        self.leftColorPrint = QPushButton("Couleur de gauche")
        self.leftColorEntry = QLabel()
        self.leftColorEntry.setFixedSize(100, 100)
        self.leftColorEntry.setAutoFillBackground(True)
        self.leftColorPrint.pressed.connect(self.changeLeftColor)
        self.leftColorEntry.setStyleSheet("background-color: {}".format(self.leftColor))

        self.leftColorLayout.addWidget(self.leftColorPrint)
        self.leftColorLayout.addWidget(self.leftColorEntry)

    def changeLeftColor(self):
        """
        Fait choisir une nouvelle couleur et change la couleur de tous les QFrame gauche
        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.leftColor = color.name()
            self.leftColorEntry.setStyleSheet("background-color: {}".format(self.leftColor))
            for frame in self.parent.leftQFrame:
                self.parent.setLeftFrameApparence(frame)

    def chooseRightColor(self):
        """
        Ajoute le bouton et le label permettant de choisir/visualiser la couleur des QFrame droite
        """
        self.rightColorWidget = QWidget()
        self.rightColorLayout = QHBoxLayout(self.rightColorWidget)
        self.rightColorLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.rightColorWidget)

        self.rightColorPrint = QPushButton("Couleur de droite")
        self.rightColorEntry = QLabel()
        self.rightColorEntry.setFixedSize(100, 100)
        self.rightColorEntry.setAutoFillBackground(True)
        self.rightColorPrint.pressed.connect(self.changeRightColor)
        self.rightColorEntry.setStyleSheet("background-color: {}".format(self.rightColor))

        self.rightColorLayout.addWidget(self.rightColorPrint)
        self.rightColorLayout.addWidget(self.rightColorEntry)

    def changeRightColor(self):
        """
        Fait choisir une nouvelle couleur et change la couleur de tous les QFrame droite
        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.rightColor = color.name()
            self.rightColorEntry.setStyleSheet("background-color: {}".format(self.rightColor))

            for frame in self.parent.rightQFrame:
                self.parent.setRightFrameApparence(frame)

    def addSizeTextWidget(self):
        """
        Rajoute les widgets pour la changement de taille de texte
        """
        self.sizeTextWidget = QWidget()
        self.sizeTextLayout = QHBoxLayout(self.sizeTextWidget)
        self.sizeTextLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sizeTextWidget)

        self.sizeTextPrint = QLabel("Taille du texte")
        self.sizeTextEntry = QDoubleSpinBox()
        self.sizeTextEntry.setDecimals(0)
        self.sizeTextEntry.setValue(self.sizeText)
        self.sizeTextEntry.valueChanged.connect(self.changeSizeText)

        self.sizeTextLayout.addWidget(self.sizeTextPrint)
        self.sizeTextLayout.addWidget(self.sizeTextEntry)
    
    def changeSizeText(self):
        """
        Change self.sizeText puis change la taille du texte des differents labels
        """
        self.sizeText = self.sizeTextEntry.value()
        #for label,truc in self.parent.labels:
        #    self.parent.setLabelProp(label)

        self.changeParaSize(self.sizeText)

    def changeParaSize(self,value):
        """
        Change la taille du texte des differents labels pour qu'ils fassent value px

        arg: -value: int | taille du texte (en px) 
        """
        value = (int) (value)
        self.parent.mainWidget.setStyleSheet((f"""
                                            QPushButton {{                 
                                                font-size: {value}px;  
                                                padding: 10px;    
                                                border-radius: 10px; 
                                                border-style: outset;
                                                border-width: 2px;  
                                                border-color: #333333;          
                                                background-color: #C4BAB8;
                                            }} 
                                              
                                            QPushButton:hover {{ 
                                                background-color: white;
                                            }}                                
                                                                                
                                            QLabel{{
                                                font-size: {value}px;     
                                            }}

                                            QLineEdit{{
                                                font-size: {value}px;     
                                            }}
                                            
                                            QSlider::groove:horizontal {{
                                                border: 1px solid #bbb;
                                                background: white;
                                                height: 10px;
                                                border-radius: 5px;
                                            }}
                                            
                                            QSlider::handle:horizontal {{
                                                background: qradialgradient(
                                                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                                    radius: 1.35, stop: 0 #fff, stop: 1 #888
                                                );
                                                width: 20px;
                                                height: 20px;
                                                margin: -5px 0;
                                                border-radius: 10px;
                                            }}

                                            QCheckBox::indicator {{
                                                width: 100px;
                                                height: 60px;
                                            }}
                                            
                                            QCheckBox::indicator:unchecked {{
                                                background-color: #CA3C1F;
                                            }}
                                            
                                            QCheckBox::indicator:checked {{
                                                background-color: #4CAF50;
                                            }}
                                            
                                            QCheckBox::indicator:checked:disabled {{
                                                background-color: #aaa;
                                            }}
                                            """))

                                            

    def returnMainWindows(self):

        """
        Change le widget courant afin d'afficher la fenetre principale
        """
        self.parent.mainLayout.setCurrentIndex(0)

    def settingsFileName(self):
        """
        initialise self.settingFileName
        """
        self.settingFileName = "data/setting/setting.json"

    def exportSettings(self):
        """
        Export les parametres au format JSON
        """
        data = {
            'speed': self.volumeEntry.value(),
            'rate': self.rateEntry.value(),
            'autoSave': self.saveEntry.isChecked(),
            'leftColor': self.leftColor,
            'rightColor': self.rightColor,
            'sizeText': self.sizeText
        }

        with open(self.settingFileName, 'w+') as file:
            json.dump(data, file)


    def importSettings(self):
        """
        Importe les parametres du JSON et met a jour les variables en consequent
        """
        with open(self.settingFileName, 'r') as file:
            data = json.load(file)

        self.volumeValue = (int)(data['speed'])
        self.rateValue = (int)(data['rate'])
        self.boolSave = (bool)(data['autoSave'])
        self.leftColor = data['leftColor']
        self.rightColor = data['rightColor']
        self.sizeText = data['sizeText']

        

    def addReturnButton(self):
        """
        Ajoute le bouton return au widget parametre
        """
        self.returnWidget = QWidget()
        self.returnLayout = QHBoxLayout(self.returnWidget)
        self.returnLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.returnWidget)

        self.returnButton= QPushButton("Valider")
        self.returnButton.pressed.connect(self.returnMainWindows)
        self.returnButton.pressed.connect(self.exportSettings)

        self.returnLayout.addWidget(self.returnButton)