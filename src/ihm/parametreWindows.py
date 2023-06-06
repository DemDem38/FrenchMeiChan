from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,QCheckBox,QColorDialog , QDoubleSpinBox, QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QColor, QKeySequence
import json


class parametreWidget(QWidget):
    def __init__(self, parent, mainW):
        super().__init__(parent)
        self.initUI()
        self.parent = parent
        self.mainW = mainW

    def initUI(self):
        self.setWindowTitle('Exemple de widget personnalisé')
        self.setGeometry(200, 200, 300, 200)
        
        self.layout = QVBoxLayout(self)
        self.settingsFileName()
        self.importSettings()

        self.addSaveWidget()
        self.chooseLeftColor()
        self.chooseRightColor()
        self.addSizeTextWidget()

        self.returnButton = QPushButton("Return")
        self.returnButton.pressed.connect(self.returnMainWindows)
        self.returnButton.pressed.connect(self.exportSettings)

        self.layout.addWidget(self.returnButton)

    def addSaveWidget(self):
        self.saveWidget = QWidget()
        self.saveLayout = QHBoxLayout(self.saveWidget)
        self.saveLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.saveWidget)

        self.savePrint = QLabel("Save auto")
        self.saveEntry = QCheckBox()
        self.saveEntry.setChecked(True)

        self.saveLayout.addWidget(self.savePrint)
        self.saveLayout.addWidget(self.saveEntry)

    def chooseLeftColor(self):
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
        color = QColorDialog.getColor()
        if color.isValid():
            self.leftColor = color.name()
            self.leftColorEntry.setStyleSheet("background-color: {}".format(self.leftColor))
            for frame in self.parent.leftQFrame:
                self.parent.setLeftFrameApparence(frame)

    def chooseRightColor(self):
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
        color = QColorDialog.getColor()
        if color.isValid():
            self.rightColor = color.name()
            self.rightColorEntry.setStyleSheet("background-color: {}".format(self.rightColor))

            for frame in self.parent.rightQFrame:
                self.parent.setRightFrameApparence(frame)

    def addSizeTextWidget(self):
        self.sizeTextWidget = QWidget()
        self.sizeTextLayout = QHBoxLayout(self.sizeTextWidget)
        self.sizeTextLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sizeTextWidget)

        self.sizeTextPrint = QLabel("Taille du texte")
        self.sizeTextEntry = QDoubleSpinBox()
        self.sizeTextEntry.setValue(30)
        self.sizeTextEntry.valueChanged.connect(self.changeSizeText)

        self.sizeTextLayout.addWidget(self.sizeTextPrint)
        self.sizeTextLayout.addWidget(self.sizeTextEntry)
    
    def changeSizeText(self):
        self.sizeText = self.sizeTextEntry.value()
        for label,truc in self.parent.labels:
            self.parent.setLabelProp(label)

    def returnMainWindows(self):
        self.parent.mainLayout.setCurrentIndex(0)

    def settingsFileName(self):
        self.settingFileName = "data/setting/setting.json"

    def addExportButton(self):
        self.exportWidget = QWidget()
        self.exportLayout = QHBoxLayout(self.exportWidget)
        self.exportLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.exportWidget)

        self.exportButton= QPushButton("Export")
        self.exportButton.pressed.connect(self.exportSettings)

        self.exportLayout.addWidget(self.exportButton)

    def exportSettings(self):
        data = {
            'leftColor': self.leftColor,
            'rightColor': self.rightColor,
            'sizeText': self.sizeText
        }

        with open(self.settingFileName, 'w+') as file:
            json.dump(data, file)

    def addImportButton(self):
        self.importWidget = QWidget()
        self.importLayout = QHBoxLayout(self.importWidget)
        self.importLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.importWidget)

        self.importButton= QPushButton("Import")
        self.importButton.pressed.connect(self.importSettings)

        self.importLayout.addWidget(self.importButton)

    def importSettings(self):
        with open(self.settingFileName, 'r') as file:
            data = json.load(file)

        self.leftColor = data['leftColor']
        self.rightColor = data['rightColor']
        self.sizeText = data['sizeText']