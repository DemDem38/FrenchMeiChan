from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMetaObject
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QColor, QKeySequence

class WorkerThread(QThread):
    message_received = pyqtSignal(str)

    def run(self):
        texte = ""
        while texte != "exit":
            texte = input("input: ")
            self.message_received.emit(texte)


# Fonction pour ajouter un label à gauche
def ajouter_label_gauche(texte):
    if texte:
        nouveau_label = QLabel(texte)
        nouveau_label.setMinimumHeight(200)
        nouveau_label.setMaximumHeight(300)
        labels.append(nouveau_label)

        # Configuration du style et de la mise en page du nouveau label
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(1)
        frame.setStyleSheet("QFrame { background-color: #90EE90; border-radius: 20px; }")
        frame_layout = QVBoxLayout(frame)
        frame_layout.addWidget(nouveau_label)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Ajout du nouveau label dans le QGridLayout
        row = len(labels) - 1
        widget_internal_layout.addWidget(frame, row, 0, 1, 2)

        # Fixer la hauteur minimale du nouveau QFrame
        frame.setMinimumHeight(nouveau_label.sizeHint().height())

        # Faire défiler la vue jusqu'au bas
        descendre_scrollbar()

# Fonction pour ajouter un label à droite
def ajouter_label_droit(texte):
    if texte:
        nouveau_label = QLabel(texte)
        nouveau_label.setMinimumHeight(200)
        nouveau_label.setMaximumHeight(300)
        nouveau_label.setAlignment(Qt.AlignCenter)

        size = nouveau_label.sizeHint()

        labels.append(nouveau_label)

        # Configuration du style et de la mise en page du nouveau label
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(1)
        frame.setStyleSheet("QFrame { background-color: #ADD8E6; border-radius: 20px; }")

        nouveau_label.setStyleSheet("color:black;")

        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(nouveau_label)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Ajout du nouveau label dans le QGridLayout
        row = len(labels) - 1
        widget_internal_layout.addWidget(frame, row, 1, 1, 2)

        # Fixer la hauteur minimale du nouveau QFrame
        frame.setFixedHeight(200)

        # Faire défiler la vue jusqu'au bas
        descendre_scrollbar()

    

def add_reply():
    texte = text_entry.text()
    ajouter_label_droit(texte)
    # Effacement du texte saisi dans la zone de texte
    text_entry.clear()

def descendre_scrollbar():
    scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())

def getLineEdit():
    return text_entry



app = QApplication([])

# Création du widget principal
widget = QWidget()

# Création du layout vertical pour les labels et la zone de texte
layout = QVBoxLayout(widget)

# Création de la QScrollArea et configuration du widget interne
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

# Création du widget interne qui contiendra les labels
widget_internal = QWidget()
widget_internal_layout = QGridLayout(widget_internal)

# Nombre de lignes et de colonnes par défaut
default_rows = 6
default_columns = 3

# Ajout d'éléments fictifs pour définir le nombre de lignes et de colonnes
for row in range(default_rows):
    for col in range(default_columns):
        widget_internal_layout.addWidget(QLabel(), row, col, 1, 1)

# Liste des labels
labels = []

# Configuration du widget interne dans la QScrollArea
scroll_area.setWidget(widget_internal)

# Ajout de la QScrollArea au layout principal
layout.addWidget(scroll_area)

# Création de la zone de texte et du bouton
text_entry = QLineEdit()

text_entry.returnPressed.connect(add_reply)

scroll_area.verticalScrollBar().rangeChanged.connect(descendre_scrollbar)

# Ajout de la zone de texte et du bouton au layout principal
layout.addWidget(text_entry)

# Récupération de la géométrie de l'écran
screen_geometry = QDesktopWidget().availableGeometry()

# Définition de la taille de la fenêtre en fonction de la géométrie de l'écran
widget.resize(screen_geometry.width(), (int) (0.95*screen_geometry.height()))

# Affichage du widget principal
widget.show()

thread = WorkerThread()
thread.message_received.connect(ajouter_label_droit)
thread.start()

app.exec_()


