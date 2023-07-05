import pyttsx3  

#voice = sentence.getProperty('voices')[0] # the french voice
def speak_french(data, volume = 0.5, rate = 100):
   sentence = pyttsx3.init()  
   sentence.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0')

   sentence.setProperty('rate', rate)    # Speed percent (can go over 100)
   sentence.setProperty('volume', volume)  # Volume 0-1
 
   #data = "Bonjour a tous, je m'appelle Eva et je suis ravie de vous rencontrer, aujoud'hui nous allons aborder le sujet controverser de l'intelligence artificielle."  
   sentence.say(data)  
   sentence.runAndWait() 

if __name__ == '__main__':
   phrase = "tests du volume "
   speak_french(phrase)