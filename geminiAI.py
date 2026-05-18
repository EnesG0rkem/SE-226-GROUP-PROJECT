import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List


client = genai.Client(api_key="APIAIzaSyAlBnB6YWVouuQZV5iK7k6GUAnR5ULCJjk_KEY")

class AlbumData(BaseModel):
    album_name: str = Field(description="The name of the fictional album")
    artist_name: str = Field(description="The name of the fictional artist")
    year: str = Field(description="The release year based on the given era")
    label: str = Field(description="Fictional record label name")
    mood_description: str = Field(description="Overall mood of the album")
    cover_prompt: str = Field(description="Visual description for AI image generation (lighting, atmosphere)")
    tags: List[str] = Field(description="3 to 6 lowercase Last.fm style tags")

def generate_album_data(journal, genre, era, track_count):
    
    system_prompt = "You are a professional music curator AI. Your task is to create a fictional music album based on user input."

    user_prompt = f"""
INPUT:
Journal: {journal}
Genre: {genre}
Era: {era}
Track Count: {track_count}
"""

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema=AlbumData,
        temperature=0.7 
    )

    try:
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_prompt,
            config=config,
        )

        
        data = json.loads(response.text)
        return data

    except Exception as e:
        print("❌ Gemini API veya Parse Hatası:", str(e))
        return None
