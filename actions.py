from datetime import datetime
from user import get_name

def do_greet(text):
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    name = get_name()
    return f"{greeting}, {name}!" if name else f"{greeting}!"

def do_get_time(text):
    return "The time is " + datetime.now().strftime("%I:%M %p")

def do_get_date(text):
    return "Today is " + datetime.now().strftime("%A, %d %B %Y")

def do_help(text):
    return ("I can tell the time and date, open apps, and search the web")

def do_exit(text):
    return "Goodbye!"

import os

APPS = {
    "calculator": "calc",
    "notepad": "notepad",
    "paint": "mspaint",
    "file explorer": "explorer",
    "chrome": "chrome",
}

def do_open_app(text):
    for name in sorted(APPS, key=len, reverse=True):
        if name in text:
            try:
                os.startfile(APPS[name])
                return f"Opening {name}"
            except OSError:
                return f"Sorry, I couldn't open {name}."
    return "Sorry, I don't know that app."

import webbrowser
from urllib.parse import quote_plus

SEARCH_TRIGGERS = [
    "search the web for", "search online for", "find me information on",
    "find information about", "search for", "look up", "find me a",
    "find a", "google", "search",
]

def do_web_search(text):
    query = ""
    for trigger in sorted(SEARCH_TRIGGERS, key=len, reverse=True):
        if trigger in text:
            query = text.split(trigger, 1)[1].strip()
            break
    if not query:
        return "What would you like me to search for?"
    webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
    return f"Searching for {query}"

ACTIONS = {
    "greet": do_greet,
    "get_time": do_get_time,
    "get_date": do_get_date,
    "help": do_help,
    "exit": do_exit,
    "open_app": do_open_app,
    "web_search": do_web_search,
}

def handle(intent, text):
    func = ACTIONS.get(intent)
    if func is None:
        return "Sorry, I can't do that yet."
    return func(text)

if __name__ == "__main__":
        for intent, text in [
        ("web_search", "search for python programming"),
        ("web_search", "could you please look up the capital of france"),
        ("web_search", "find me a tutorial on arduino"),
        ("web_search", "search"),
    ]:
            print(intent, "->", handle(intent, text))