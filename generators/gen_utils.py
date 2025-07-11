import unicodedata
import requests
from gtts import gTTS
from PIL import Image
import os

def sanitize_filename(filename):
    """Normalize and replace special characters for ASCII-safe filenames."""
    return unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')


# Function to download an image from a URL
def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to download image from {url}")

def generate_audio(text, filename, language='fi'):
    tts = gTTS(text, lang=language)
    tts.save(filename)

def resize_image_proportionally(image_path: str, max_width: int = 150, max_height: int = 100):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"No such file: '{image_path}'")

    with Image.open(image_path) as img:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        img.save(image_path)