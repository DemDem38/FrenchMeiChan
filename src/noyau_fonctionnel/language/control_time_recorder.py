#!/usr/bin/env python3

import queue
import sys
import keyboard
from pynput.keyboard import Listener

import os
#from src.noyau_fonctionnel.language.reco_language import wispAnalyse as wa
from reco_language import wispAnalyse as wa

"""
import sys

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(fc_path)

from noyau_fonctionnel.reco_language import wispAnalyse as wa
"""
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

class stop_rec(Exception):
    "stop button pressed"
    pass

def record():

    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    filename = "recording.mp3"

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
                                channels=channels, callback=callback):
                print('#' * 80)
                print('press space to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())
                    if keyboard.is_pressed(" "):
                        raise stop_rec


    except stop_rec:
        print('\nRecording finished: ' + repr(filename))
        text = wa()
        os.remove(filename)
        return text
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
        
record()
