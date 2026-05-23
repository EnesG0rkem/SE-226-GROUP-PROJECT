import google.generativeai as genai
import json
import re

GEMINI_API_KEY = "AIzaSyAs5uU3AUltNOi7tsRvqWKcmwCiXsWgIUg"

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
"""

    try:
        response = model.generate_content(prompt)
        return clean_json(response.text)

    except Exception as e:
        print("Gemini error:", e)
        return None