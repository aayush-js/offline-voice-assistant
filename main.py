import joblib
from stt import listen
from tts import speak
from actions import handle
from user import get_name, save_name

THRESHOLD = 0.25
model = joblib.load("intent_model.pkl")

NAME_PREFIXES = ["my name is", "i am", "i'm", "it is", "it's", "call me", "this is"]

def clean_name(heard):
    for p in NAME_PREFIXES:
        if heard.startswith(p):
            heard = heard[len(p):]
    return heard.strip().title()

def first_run_setup():
    speak("Hello! I am your voice assistant. What is your name?")
    for _ in range(2):                          # two voice attempts
        heard = listen()
        if not heard:
            continue
        name = clean_name(heard)
        speak(f"Did you say {name}?")
        answer = listen()
        if answer and "yes" in answer:
            save_name(name)
            speak(f"Nice to meet you, {name}.")
            return
        speak("Sorry. Let me try again.")
    speak("Please type your name instead.")
    name = input("Your name: ").strip().title()
    save_name(name)
    speak(f"Nice to meet you, {name}.")

def predict(text):
    probs = model.predict_proba([text])[0]
    best = probs.argmax()
    return model.classes_[best], probs[best]

from stt import listen, calibrate

DEBUG = True      # show intent + confidence (handy for demos)

def main():
    if get_name() is None:
        first_run_setup()
    calibrate()
    speak("Voice assistant ready.")
    print("\nListening...")
    while True:
        text = listen()
        if text is None:
            continue                       # silence: keep waiting quietly

        print(f"\nYou: {text}")
        intent, conf = predict(text)
        if DEBUG:
            print(f"[{intent} {conf:.2f}]")

        if conf < THRESHOLD:
            speak("Sorry, I didn't understand that.")
        else:
            speak(handle(intent, text))
            if intent == "exit":
                break
        print("\nListening...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")