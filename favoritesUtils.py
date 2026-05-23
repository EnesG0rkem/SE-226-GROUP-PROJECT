import json
import os

FAVORITES_FILE = "favorites.json"


def load_favorites():

    if not os.path.exists(FAVORITES_FILE):
        return []

    with open(FAVORITES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_favorites(favorites):

    with open(FAVORITES_FILE, "w", encoding="utf-8") as file:
        json.dump(favorites, file, indent=4, ensure_ascii=False)


def is_favorite(track):

    favorites = load_favorites()

    for fav in favorites:

        if (
            fav.get("name") == track.get("name")
            and fav.get("artist") == track.get("artist")
        ):
            return True

    return False


def toggle_favorite(track):

    favorites = load_favorites()

    for fav in favorites:
        if fav.get("name") == track.get("name") and fav.get("artist") == track.get("artist"):
            favorites.remove(fav)
            save_favorites(favorites)
            return False

    favorites.append({
        "name": track["name"],
        "artist": track["artist"],
        "url": track["url"]
    })

    save_favorites(favorites)
    return True

    save_favorites(favorites)