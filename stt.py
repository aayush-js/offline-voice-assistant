import json
import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)               # silence Vosk's console logs
model = Model("vosk-model-small-en-us-0.15")        # loaded once, takes a couple of seconds
recognizer = sr.Recognizer()

def calibrate():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

def listen():
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return None

    raw = audio.get_raw_data(convert_rate=16000, convert_width=2)
    rec = KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(raw)
    text = json.loads(rec.FinalResult()).get("text", "").strip()
    return text or None

if __name__ == "__main__":
    calibrate()
    print("You said:", listen())