import genanki
import json
import os
import sys
import shutil
import glob
import generators.gen_utils as utils

def gen_verbs_cloze(deck_id, json_dir, deck_name, apkg_filename='Finnish_Verbs.apkg'):

    # Create the model for the Anki cards
    model_id = 3414565112

    front_html = utils.load_text('templates/verbs_cloze/front.html')
    back_html = utils.load_text('templates/verbs_cloze/back.html')
    css_text = utils.load_text('templates/verbs_cloze/styles.css')

    model = genanki.Model(
        model_id,
        'Verb Cloze with Image and Audio',
        fields=[
            {'name': 'Verb'},
            {'name': 'Image'},
            {'name': 'Text'},
            {'name': 'Translation'},
            {'name': 'Node'},
            {'name': 'KPT'},
            {'name': 'Audio'},
        ],
        templates=[
            {
                'name': 'Verb Conjugation Cloze Card',
                'qfmt': front_html,
                'afmt': back_html,
            },
        ],
        css=css_text,
        model_type=genanki.Model.CLOZE
    )

    # Create the decks
    deck = genanki.Deck(
        deck_id,
        deck_name,
    )

    # Directory for media files (audio and images)
    if os.path.exists('media'):
        shutil.rmtree('media')
    media_folder = 'media'
    os.makedirs(media_folder, exist_ok=True)

    # List to store paths to media files
    media_files = []
    verbs = []

    json_files = glob.glob(json_dir)
    skip_media = False

    # skip_media = True
    # json_files = json_files[:1]

    for json_file in json_files:
        print(f"Processing file: {json_file}")

        # Load data from the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            verbs = json.load(f)

        # Add cards to the deck
        for verb_data in verbs:
            verb = verb_data['verb']
            question = verb
            sanitized_image_filename = ""

            # Handle optional image
            if 'image' in verb_data and not skip_media:
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
            audio_parts = ""
            for i, (txt, key) in enumerate(zip(text, keys), start=1):
                audio_parts += txt.replace("{}", key) + " "
                # cloze = f"{{{{c{i}::{key}}}}}"
                cloze = f"{{{{c1::{key}}}}}"
                result_parts.append(txt.format(cloze))

            result = "<br/>".join(result_parts)
            sanitized_audio_filename = ""
            if not skip_media:
                sanitized_audio_filename = utils.sanitize_filename(f"{verb}_{utils.short_hash(audio_parts, 8)}.mp3")
                audio_path = os.path.join(media_folder, sanitized_audio_filename)
                utils.generate_audio(audio_parts.strip(), audio_path)
                media_files.append(audio_path)

            note_field = ""
            if 'note' in verb_data:
                note_field = verb_data['note']

            kpt_field = ""
            # if 'KPT' in verb_data:
            #     kpt_field = verb_data['KPT']
            # Add note
            note = genanki.Note(
                model=model,
                fields=[
                    question,
                    f'<img src="{sanitized_image_filename}" style="max-width:200px; height:auto;"/>' if len(sanitized_image_filename) > 0 else "",   # Image
                    result,
                    translation,
                    note_field,
                    kpt_field,
                    f"[sound:{sanitized_audio_filename}]" if len(sanitized_audio_filename) > 0 else ""
                ],
                guid=utils.short_hash(audio_parts, 8)  # Unique identifier based on audio content
            )
            deck.add_note(note)

    # Create the package and include media files
    package = genanki.Package(deck)
    package.media_files = media_files  # Add media files (audio + images) to the package
    package.write_to_file(apkg_filename)

    return True


if __name__ == '__main__':
    sys.exit(1)