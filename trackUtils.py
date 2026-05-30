import Lastfm
import historyUtils

def collect_tracks_from_tags(tags, track_count, current_journal, current_genre):
    all_tracks = []

    for tag in tags:
        try:
            tracks = Lastfm.fetch_tracks_by_tag(tag, limit=track_count)
            all_tracks.extend(normalize_lastfm_tracks(tracks))
        except Exception as e:
            print(f"Last.fm error for tag '{tag}':", e)

    new_tracks = remove_duplicate_tracks(all_tracks)

    history_tracks = []

    for item in historyUtils.load_history():

        same_genre = item.get("genre") == current_genre

        mood_text = item.get("mood", "").lower()
        current_mood = current_journal.lower()

        mood_words = current_mood.split()
        similar_mood = any(word in mood_text for word in mood_words)

        if same_genre and similar_mood:
            name = item.get("name", "")
            artist = item.get("artist", "")
            url = item.get("url", "")

            if name and artist:
                history_tracks.append({
                    "name": name,
                    "artist": artist,
                    "url": url
                })

    import random
    random.shuffle(history_tracks)

    history_count = int(track_count * 0.3)

    selected_history = history_tracks[:history_count]

    combined_tracks = selected_history + new_tracks

    return remove_duplicate_tracks(combined_tracks)[:track_count]


def remove_duplicate_tracks(track_list):
    unique_tracks = []
    seen = set()

    for track in track_list:
        track_name = track.get("name", "").strip()
        artist_name = track.get("artist", "").strip()
        url = track.get("url", "")

        if not track_name or not artist_name:
            continue

        key = (track_name.lower(), artist_name.lower())

        if key not in seen:
            seen.add(key)
            unique_tracks.append({
                "name": track_name,
                "artist": artist_name,
                "url": url
            })

    return unique_tracks


def normalize_lastfm_tracks(tracks):
    normalized = []

    for t in tracks:
        track_info = t.get("track", t)

        artist = track_info.get("artist", "")

        if isinstance(artist, dict):
            artist_name = artist.get("name", "")
        else:
            artist_name = artist

        normalized.append({
            "name": track_info.get("name", ""),
            "artist": artist_name,
            "url": track_info.get("url", "")
        })

    return normalized
