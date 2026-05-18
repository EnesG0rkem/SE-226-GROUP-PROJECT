import google.generativeai as genai
import json


genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_album_data(journal, genre, era, track_count):

    generation_config = {
        "response_mime_type": "application/json"
    }

    prompt = f"""
You are a professional music curator AI.

Your task is to create a fictional music album based on user input.

RULES:
- Return ONLY valid JSON
- No explanation, no markdown, no extra text
- Tags must be lowercase and realistic Last.fm style tags

INPUT:
Journal: {journal}
Genre: {genre}
Era: {era}
Track Count: {track_count}

OUTPUT FORMAT:
{{
    "album_name": "string",
    "artist_name": "string",
    "year": "string",
    "label": "string",
    "mood_description": "string",
    "cover_prompt": "visual description for AI image generation",
    "tags": ["tag1", "tag2", "tag3"]
}}
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        
        data = json.loads(response.text)

        return data

    except json.JSONDecodeError:
        print("JSON parse error from Gemini output")
        print("RAW OUTPUT:")
        print(response.text)
        return None

    except Exception as e:
        print("Gemini API error:", str(e))
        return None
