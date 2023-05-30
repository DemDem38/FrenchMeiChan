#!/usr/bin/env python3

import queue
import sys
import keyboard
from pynput.keyboard import Listener

import os
from src.noyau_fonctionnel.language.voice.reco_language import wispAnalyse as wa
#from reco_language import wispAnalyse as wa

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

class stop_rec(Exception):
    "stop button pressed"
    pass
class record():

    def __init__(self, signal):
        self.q = queue.Queue()
        self.stop = False
        self.signal = signal
        self.signal.signal_stop.connect(self.stop_rec)
    
    def stop_rec(self):
        self.stop = True

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def recording(self):
        filename = "recording.mp3"

        if os.path.exists(filename):
            os.remove(filename)

        channels = 1

        device = 1

        device_info = sd.query_devices(device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])

        try:
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                                channels=channels) as file:
                with sd.InputStream(samplerate=samplerate, device=device,
                                    channels=channels, callback=self.callback):
                    print('#' * 80)
                    print('press button to stop the recording')
                    print('#' * 80)
                    while True:
                        file.write(self.q.get())
                        if self.stop == True:
                            raise stop_rec


        except stop_rec:
            print('\nRecording finished: ' + repr(filename))
            text = wa()
            os.remove(filename)
            return text
        except KeyboardInterrupt:
            os.remove(filename)
            exit(0)
        except Exception as e:
            print("erreur")
            os.remove(filename)
            exit(type(e).__name__ + ': ' + str(e))

if __name__ == '__main__':  
    record()
