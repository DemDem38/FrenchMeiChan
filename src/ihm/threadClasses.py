from PyQt5.QtCore import QThread, pyqtSignal

from src.noyau_fonctionnel.language.voice.control_time_recorder import record
from src.noyau_fonctionnel.language.voice.speak_french import speak_french

class RecordingThread(QThread):
    """
    Permet de faire l'enregistrement vocal pour ensuite envoyer la chaine de caractere correspondante
    """
    recording_finished = pyqtSignal(str)

    def __init__(self,ihm):
        super().__init__()
        self.record = record(ihm)

    def run(self):
        text = self.record.recording()

        self.recording_finished.emit(text)


class SpeakThread(QThread):
    """
    Permet de faire lire une phrase
    """
    def __init__(self,text,ihm):
        super().__init__()
        self.ihm=ihm
        self.text=text
        self.volume = (float)(self.ihm.paraWidget.volumeEntry.value()) / 200.0
        self.rate = self.ihm.paraWidget.rateEntry.value()

    def run(self):
        #self.ihm.text_entry.setReadOnly(True)
        #self.ihm.recordBoutton.setEnabled(False)
        speak_french(self.text,self.volume,self.rate)
        #self.ihm.text_entry.setReadOnly(False)
        #self.ihm.recordBoutton.setEnabled(True)