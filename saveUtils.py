# saveUtils.py

import json
import os


def save_album_json(folder_path, album_data, tracks):
    album_export = {
        "album": album_data,
        "tracks": tracks
    }

    file_path = os.path.join(folder_path, "album_data.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(album_export, file, indent=4, ensure_ascii=False)

    return file_path


def save_cover_png(folder_path, cover_image):
    file_path = os.path.join(folder_path, "cover.png")
    cover_image.save(file_path)
    return file_path
