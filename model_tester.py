import joblib

pipe = joblib.load("intent_model.pkl")

THRESHOLD = 0.30

'''for phrase in ["yo", "good night", "open calculator",
               "how do i use you", "could you launch the calculator",
               "what is the weather", "blah blah","what are you doing","who are you",
               "abracadabra","how many wheels does a bus have"]:
    probs = pipe.predict_proba([phrase])[0]
    best = probs.argmax()
    print(f"{phrase!r}: {pipe.classes_[best]} ({probs[best]:.2f})")'''

tests = [
    ("could you tell me what time it is",        "get_time"),
    ("could you tell me today's date",           "get_date"),
    ("set a timer for twenty five minutes",      "timer"),
    ("begin counting with the stopwatch",        "stopwatch"),
    ("i would like to open notepad",             "open_app"),
    ("bring up file explorer",                   "open_app"),
    ("search for the latest news about space",   "web_search"),
    ("what are the things you can do",           "help"),
    ("i will talk to you later",                 "exit"),
    ("good evening assistant",                   "greet"),
]

for phrase, expected in tests:
    probs = pipe.predict_proba([phrase])[0]
    best = probs.argmax()
    pred, conf = pipe.classes_[best], probs[best]
    ok_intent = pred == expected
    ok_conf = conf >= THRESHOLD
    flag = "OK  " if ok_intent and ok_conf else "FAIL"
    print(f"{flag} {phrase!r}: {pred} ({conf:.2f})  expected={expected}")