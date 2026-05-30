import google.generativeai as genai
import json
import re

import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def clean_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```json", "", text)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)
        text = text.strip()

    return json.loads(text)


def generate_album_data(journal, genre, era, track_count):

    prompt = f"""
Return ONLY valid JSON.

{{
  "album_name": "string",
  "artist_name": "string",
  "year": 2010,
  "label": "string",
  "mood_description": "string",
  "cover_prompt": "string",
  "lastfm_tags": ["tag1", "tag2", "tag3", "tag4"]
}}

Journal: "{journal}"
Genre: "{genre}"
Era: "{era}"
Track Count: {track_count}

Deeply analyze the journal for song language.
The provided genre must be relevant so the songs you give.
Provided era must be satisfied by the song with maximun 5 years differance.
Do not give unrelated output.
"""

    try:
        response = model.generate_content(prompt)
        return clean_json(response.text)

    except Exception as e:
        print("Gemini error:", e)
        return None

