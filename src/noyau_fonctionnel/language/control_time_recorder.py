#!/usr/bin/env python3

import queue
import sys

import os
from reco_language import wispAnalyse as wa
from speak_french import speak_french

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

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
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())


    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(filename))
        text = wa()
        os.remove(filename)
        speak_french(text)
        return text
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
        
record()
