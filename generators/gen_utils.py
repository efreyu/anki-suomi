import unicodedata
import requests
from gtts import gTTS

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