import Lastfm


def collect_tracks_from_tags(tags, track_count):
    all_tracks = []

    for tag in tags:
        try:
            tracks = Lastfm.fetch_tracks_by_tag(tag, limit=track_count)
            all_tracks.extend(normalize_lastfm_tracks(tracks))
        except Exception as e:
            print(f"Last.fm error for tag '{tag}':", e)

    return remove_duplicate_tracks(all_tracks)[:track_count]


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
        normalized.append({
            "name": t.get("name", ""),
            "artist": t.get("artist", {}).get("name", ""),
            "url": t.get("url", "")
        })

    return normalized

if __name__ == "__main__":
    tags = ["dream pop", "indie pop", "melancholy"]

    tracks = collect_tracks_from_tags(tags, 8)

    for track in tracks:
        print(track["name"], "-", track["artist"])
        print(track["url"])