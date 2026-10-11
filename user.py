import json
import os

FILE = "user_data.json"

def get_name():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f).get("name")
    return None

def save_name(name):
    with open(FILE, "w") as f:
        json.dump({"name": name}, f)