import pyttsx3

VOICE_NAME = "Zira"      # a word from the voice name you liked
RATE = 160

def speak(text):
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.setProperty("rate", RATE)
    for v in engine.getProperty("voices"):
        if VOICE_NAME.lower() in v.name.lower():
            engine.setProperty("voice", v.id)
            break
    engine.say(text)
    engine.runAndWait()
    engine.stop()

if __name__ == "__main__":
    speak("Hello, I am your voice assistant.")
    speak("This is the second sentence.")