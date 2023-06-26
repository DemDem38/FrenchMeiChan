from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton,QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox

from src.noyau_fonctionnel.authentication.person import person,contact

class reponseWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        pass