import json
import os

HISTORY_FILE = "listening_history.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_track(track, mood, genre):

    history = load_history()

    record = {
        "name": track["name"],
        "artist": track["artist"],
        "url": track["url"],
        "mood": mood,
        "genre": genre
    }

    history.append(record)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)