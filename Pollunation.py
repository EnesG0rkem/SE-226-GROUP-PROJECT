import requests
from PIL import Image
import io
from urllib.parse import quote
def generate_cover(prompt):
    encoded = quote(prompt)
    url = (f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=600&height=600&nologo=true")
    response = requests.get(url, timeout=90)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content)).convert("RGB")

