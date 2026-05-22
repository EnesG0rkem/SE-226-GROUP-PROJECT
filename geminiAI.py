from google import genai
import json
import re

client = genai.Client(api_key="AIzaSyDD8CJVwHky9Ldg3BYy75UYi9Vzo_SWrII")


def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"```(json)?", "", text)
        text = text.replace("```", "").strip()
    return json.loads(text)


def generate_album_data(journal, genre, era, track_count):

    prompt = f"""
Return ONLY JSON:

Journal: {journal}
Genre: {genre}
Era: {era}
Track Count: {track_count}

Fields:
album_name, artist_name, year, label,
mood_description, cover_prompt, tags
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return clean_json(response.text)

    except Exception as e:
        print("Gemini error:", e)
        return None