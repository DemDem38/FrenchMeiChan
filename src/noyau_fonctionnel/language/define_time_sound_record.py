# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

extension = ".mp3"
# Sampling frequency
freq = 44100

# Recording duration (second)
duration = 5
# Start recorder with the given values of duration and sample frequency
recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

# Record audio for the given number of seconds
sd.wait()

# Convert the NumPy array to audio file
wv.write("recording"+extension, recording, freq, sampwidth=2)





