import unicodedata
import requests
import time
from gtts import gTTS
from gtts.tts import gTTSError
from PIL import Image
import os
import hashlib

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

def generate_audio(text, filename, language='fi', retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            tts = gTTS(text, lang=language)
            tts.save(filename)
            return  # Success, exit the function
        except (gTTSError, Exception) as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All attempts failed.")
                raise

def resize_image_proportionally(image_path: str, max_width: int = 150, max_height: int = 100):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"No such file: '{image_path}'")

    with Image.open(image_path) as img:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        img.save(image_path)

def short_hash(text: str, length: int = 8) -> str:
    if not (6 <= length <= 8):
        raise ValueError("Length must be between 6 and 8")

    full_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return full_hash[:length]