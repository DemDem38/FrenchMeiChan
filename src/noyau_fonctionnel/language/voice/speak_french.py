import pyttsx3  

#voice = sentence.getProperty('voices')[0] # the french voice
def speak_french(data):
   sentence = pyttsx3.init()  
   sentence.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0')

   #data = "Bonjour a tous, je m'appelle Eva et je suis ravie de vous rencontrer, aujoud'hui nous allons aborder le sujet controverser de l'intelligence artificielle."  
   sentence.say(data)  
   sentence.runAndWait() 