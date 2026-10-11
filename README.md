# Offline Voice Assistant

A task-oriented voice assistant built in Python as a first AI micro project. It listens to a spoken command, works out what the user wants with a trained machine-learning classifier, performs the action, and replies by voice. Speech recognition, intent classification, and text-to-speech all run locally. Only the web-search command uses the internet.

## How it works

```
Voice → Speech-to-Text (Vosk) → TF-IDF → Logistic Regression → Intent → Action → Text-to-Speech (pyttsx3)
```

| Stage | Tool | Role |
|---|---|---|
| Speech-to-text | Vosk (small English model) | Converts audio to text, offline |
| Feature extraction | TF-IDF (unigrams + bigrams) | Turns text into numerical features |
| Intent classifier | Logistic Regression (scikit-learn) | Predicts the intent of a command |
| Actions | Python | Runs the task for the predicted intent |
| Text-to-speech | pyttsx3 | Speaks the response, offline |

The AI component is the supervised intent classifier, trained on a custom command-intent dataset. Speech recognition uses an existing model (Vosk).

## Features

- Greets the user by name (asks for the name on first launch and stores it locally)
- Tells the time and date
- Opens apps: calculator, notepad, paint, file explorer, chrome
- Searches the web (opens the default browser)
- Help and exit commands
- Rejects low-confidence input with "Sorry, I didn't understand that" instead of acting on a guess

## Project structure

```
├── main.py             # main loop: listen → classify → act → speak
├── stt.py              # speech-to-text (Vosk)
├── tts.py              # text-to-speech (pyttsx3)
├── actions.py          # one function per intent + dispatcher
├── user.py             # stores the user's name locally
├── train.py            # trains the classifier and saves intent_model.pkl
├── dataset.csv         # custom command-intent dataset
└── requirements.txt
```

## Setup (Windows)

1. Clone or download this repo, then create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate
```
2. Install the dependencies:
```bash
   pip install -r requirements.txt
```
   If PyAudio fails to install, try `pip install pipwin` and then `pipwin install pyaudio`.
3. Download the Vosk model `vosk-model-small-en-us-0.15` from https://alphacephei.com/vosk/models, unzip it, and rename the folder to `model` so it sits next to `main.py`.
4. Train the classifier (skip this if `intent_model.pkl` is already in the repo):
```bash
   python train.py
```

## Run

```bash
python main.py
```

On first launch it asks for your name. Then try:

- "what time is it"
- "open calculator"
- "search for python programming"
- "goodbye"

## Dataset and evaluation

- Small hand-written dataset of labelled commands (`dataset.csv`), written in lowercase without punctuation to match Vosk's output.
- 5-fold stratified cross-validation accuracy: **about 96.6% (± 2.5%)**.
- Dataset was improved using error analysis, so this figure is somewhat optimistic. It is not an unbiased estimate.
- Commands the model had never seen, such as "could you tell me today's date", were classified correctly in testing.
- A confidence threshold of 0.25 rejects most out-of-scope input.

## Limitations

- Small dataset and a limited set of intents
- Casual or slang greetings ("sup", "what's up") are the weakest area
- Out-of-scope sentences that share words with supported commands can still be misclassified
- Vosk's small model struggles with unusual words and names
- Windows only (app launching uses `os.startfile`)
- Timer and stopwatch are not implemented yet
- Not a general conversational assistant

## Future scope

- Timer and stopwatch commands
- An explicit "unknown" class for out-of-scope commands
- Larger dataset and more intents
- More natural offline text-to-speech (for example Piper)
- Smart-device control through an ESP32
- A GUI

## Tech stack

Python, Vosk, SpeechRecognition, PyAudio, scikit-learn, pandas, joblib, pyttsx3
