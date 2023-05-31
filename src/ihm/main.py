import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from PyQt5.QtWidgets import QApplication, QDesktopWidget
from src.ihm.mainWindows import MainWindow


app = QApplication([])
widget = MainWindow()

screen_geometry = QDesktopWidget().availableGeometry()
widget.resize(screen_geometry.width(), int(0.95 * screen_geometry.height()))

widget.show()
app.exec_()
