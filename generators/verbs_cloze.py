import genanki
import json
import os
import sys
import shutil
import generators.gen_utils as utils

def gen_verbs_cloze(json_file, deck_name, apkg_filename='Finnish_Verbs.apkg'):

    # Create the model for the Anki cards
    model_id = 3414565112
    model = genanki.Model(
        model_id,
        'Verb Conjugation Table with Image and Audio',
        fields=[
            {'name': 'Verb'},
            {'name': 'Image'},
            {'name': 'Text'},
            {'name': 'Translation'},
            {'name': 'Node'},
            {'name': 'KPT'}
        ],
        templates=[
            {
                'name': 'Verb Conjugation Cloze Card',
                'qfmt': '{{#Image}}<br>{{cloze:Text}}',
                'afmt': """
                {{FrontSide}}<br><hr>
                {{cloze:Text}}
                <br>
                {{Translation}}
                <br>
                {{Node}}
                <br>
                {{KPT}}
            """,
            },
        ],
    )

    # Create the deck
    deck_id = 987654321
    deck = genanki.Deck(
        deck_id,
        deck_name,
    )

    # Load data from the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        verbs = json.load(f)

    # Directory for media files (audio and images)
    if os.path.exists('media'):
        shutil.rmtree('media')
    media_folder = 'media'
    os.makedirs(media_folder, exist_ok=True)

    # List to store paths to media files
    media_files = []

    # Add cards to the deck
    for verb_data in verbs:
        verb = verb_data['verb']
        question = f"Conjugate the verb '{verb}'"
        sanitized_image_filename = ""

        # Handle optional image
        if 'image' in verb_data:
            image_url = verb_data['image']
            if len(image_url):
                sanitized_image_filename = os.path.basename(image_url)
                image_path = os.path.join(media_folder, sanitized_image_filename)
                utils.download_image(image_url, image_path)
                media_files.append(image_path)

        # Generate conjugations and audio
        text = verb_data['text']
        translation = verb_data['translation']
        keys = verb_data['keys']
        result_parts = []
        for i, (txt, key) in enumerate(zip(text, keys), start=1):
            cloze = f"{{{{c{i}::{key}}}}}"
            result_parts.append(txt.format(cloze))

        result = "<br>".join(result_parts)


# todo continue here
        conjugations = verb_data['conjugations']
        translations = verb_data['translations']
        conjugation_fields = []
        for i, conjugation in enumerate(conjugations):
            translate = translations[i]
            sanitized_audio_filename = utils.sanitize_filename(f"{verb}_conjugation_{i + 1}.mp3")
            audio_path = os.path.join(media_folder, sanitized_audio_filename)
            utils.generate_audio(conjugation, audio_path)
            media_files.append(audio_path)
            conjugation_fields.extend([conjugation, translate, f"[sound:{sanitized_audio_filename}]"])

        # Fill missing fields if there are fewer than 6 conjugations
        while len(conjugation_fields) < 6 * 3:
            conjugation_fields.extend(["", ""])

        note_field = ""
        if 'note' in verb_data:
            note_field = verb_data['note']
        # Add note
        note = genanki.Note(
            model=model,
            fields=[
                question,                   # Question
                f'<img src="{sanitized_image_filename}"/>' if len(sanitized_image_filename) > 0 else "",   # Image
                *conjugation_fields,        # Conjugations and audio
                note_field,                 # Note
            ],
        )
        deck.add_note(note)

    # Create the package and include media files
    package = genanki.Package(deck)
    package.media_files = media_files  # Add media files (audio + images) to the package
    package.write_to_file(apkg_filename)

    return True


if __name__ == '__main__':
    sys.exit(1)