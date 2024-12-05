import genanki
import json
from gtts import gTTS
import os
import sys


def gen_verbs():

    # Create the model for the Anki cards
    model_id = 1234567890
    model = genanki.Model(
        model_id,
        'Verb Conjugation with Image and Audio',
        fields=[
            {'name': 'Verb'},          # Verb
            {'name': 'Question'},      # Full subject description
            {'name': 'Answer'},        # Answer (conjugated form)
            {'name': 'Audio'},         # Audio playback
            {'name': 'Image'},         # Image (if any)
        ],
        templates=[
            {
                'name': 'Conjugation Card',
                'qfmt': """
                    {{#Image}}<img src="{{Image}}" style="max-width: 300px;"><br>{{/Image}}
                    {{Verb}} - {{Question}}
                """,
                'afmt': '{{FrontSide}}<br><hr><br>{{Answer}}<br>{{Audio}}',
            },
        ],
    )

    # Create the deck
    deck_id = 987654321
    deck = genanki.Deck(
        deck_id,
        'Finnish Verb Conjugation with Images and Audio',
    )

    # Load data from the JSON file
    with open('db/verbs.json', 'r', encoding='utf-8') as f:
        verbs = json.load(f)

    # Directory for media files (audio and images)
    media_folder = 'media'
    os.makedirs(media_folder, exist_ok=True)

    # List to store paths to media files
    media_files = []

    # Add cards to the deck
    for verb_data in verbs:
        verb = verb_data['verb']
        image_path = None
        sanitized_image_filename = None

        # Handle optional image
        if 'image' in verb_data:
            image_url = verb_data['image']
            sanitized_image_filename = sanitize_filename(os.path.basename(image_url))
            image_path = os.path.join(media_folder, sanitized_image_filename)
            download_image(image_url, image_path)
            media_files.append(image_path)

        for subject, form in verb_data['conjugations'].items():
            audio_filename = f"{verb}_{subject}.mp3"
            sanitized_audio_filename = sanitize_filename(audio_filename)
            audio_path = os.path.join(media_folder, sanitized_audio_filename)

            # Generate audio
            tts = gTTS(form, lang='fi')
            tts.save(audio_path)
            media_files.append(audio_path)

            # Add note
            note = genanki.Note(
                model=model,
                fields=[
                    verb,                             # Verb
                    subject,                          # Full subject description (e.g., "Minä")
                    form,                             # Answer (e.g., "nukun")
                    f"[sound:{sanitized_audio_filename}]", # Audio reference
                    os.path.basename(image_path) if sanitized_image_filename else "",  # Image reference
                ],
            )
            deck.add_note(note)

    # Create the package and include media files
    package = genanki.Package(deck)
    package.media_files = media_files  # Add media files (audio + images) to the package
    package.write_to_file('Finnish_Verbs.apkg')


if __name__ == '__main__':
    sys.exit(1)