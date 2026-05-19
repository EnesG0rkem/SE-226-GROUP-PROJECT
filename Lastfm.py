import requests
LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"
LASTFM_API_KEY = "31e3a0751475cd33069c084d4ad505b7"
def fetch_tracks_by_tag(tag, limit=10):
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "limit": limit,
        "api_key": LASTFM_API_KEY,
        "format": "json",
    }
    headers = {"User-Agent": "AlbumCoverStudio/1.0"}
    response = requests.get(LASTFM_BASE_URL, params=params,
        headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data.get("tracks", {}).get("track", [])