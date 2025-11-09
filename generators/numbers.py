import genanki
import json
import os
import sys
import shutil
import generators.gen_utils as utils

def gen_numbers(json_file, deck_name, apkg_filename, deck_type, model_id, deck_id):

    """
    Making card structure that contains numbers with images and audio
    Question: Number and Image
    {{Number}} {{Number in English}} {{Image}}
    Answer: Number in Finnish
    <table>
    <tr>
    <td>{{Number}}</td>
    <td>{{Number in Finnish}}</td>
    <td>{{Audio}}</td>
    <td>{{Image}}</td>
    </tr>
    ...
    </table>
    """
    if deck_type == 'regular':
        deck_id = deck_id + 1
    else:
        deck_id = deck_id + 2
    # Create the model for the Anki cards
    model = {}
    css = """
                .card {
                  font-family: arial;
                  font-size: 20px;
                  text-align: center;
                  color: black;
                  background-color: white;
                }
                img {
                  display: block;
                  margin-left: auto;
                  margin-right: auto;
                  max-width: 100%;
                  height: auto;
                }
            """
    if deck_type == 'regular':
        model = genanki.Model(
            model_id,
            'Numbers Table with Image and Audio',
            fields=[
                {'name': 'Question'},
                {'name': 'Image'},
                {'name': 'Finnish'},
                {'name': 'Translate'},
                {'name': 'Note'},
                {'name': 'Audio'}
            ],
            templates=[
                {
                    'name': 'Numbers Card',
                    'qfmt': """
                        <div>{{Question}}</div>
                        {{#Image}}<div><hr>{{Image}}</div>{{/Image}}
                    """,
                    'afmt': """
                        {{FrontSide}}
                        <br>
                        <hr>
                        <table style="margin: 0 auto;">
                          <tr>
                            <td>{{Finnish}}</td>
                          </tr>
                          <tr>
                            <td><i>{{Translate}}</i></td>
                          </tr>
                          <tr>
                            <td><b>{{Note}}</b></td>
                          </tr>
                          <tr>
                            <td>{{Audio}}</td>
                          </tr>
                        </table>
                    """,
                },
            ],
            css=css
        )
    else: # reverse
        model = genanki.Model(
            model_id,
            'Numbers Table with Image and Audio',
            fields=[
                {'name': 'Question'},
                {'name': 'Audio'},
                {'name': 'Image'},
                {'name': 'Finnish'},
                {'name': 'Translate'},
                {'name': 'Note'}
            ],
            templates=[
                {
                    'name': 'Numbers Card',
                    'qfmt': """
                        <div>{{Question}}</div><br/>
                        {{Audio}}<br/>
                    """,
                    'afmt': """
                        {{FrontSide}}
                        {{#Image}}<div><hr>{{Image}}</div>{{/Image}}
                        <br>
                        <hr>
                        <table style="margin: 0 auto;">
                          <tr>
                            <td>{{Finnish}}</td>
                          </tr>
                          <tr>
                            <td><i>{{Translate}}</i></td>
                          </tr>
                          <tr>
                            <td><b>{{Note}}</b></td>
                          </tr>
                        </table>
                    """,
                },
            ],
            css=css
        )

    # Create the deck
    deck = genanki.Deck(
        deck_id,
        deck_name,
    )

    # Load data from the JSON file
    with (open(json_file, 'r', encoding='utf-8') as f):
        numbers = json.load(f)

    # Directory for media files (audio and images)
    if os.path.exists('media'):
        shutil.rmtree('media')
    media_folder = 'media'
    os.makedirs(media_folder, exist_ok=True)

    # List to store paths to media files
    media_files = []

    # Add cards to the deck
    for number_data in numbers:
        number = number_data['number']
        translation = number_data['translation']
        question = ''
        if deck_type == 'regular':
            question = f"Translate the sentence '{translation}'"
        else:
            question = f"Listen and translate"
        sanitized_image_filename = ""

        # Handle optional image
        if 'image' in number_data:
            image_url = number_data['image']
            if len(image_url):
                sanitized_image_filename = os.path.basename(image_url)
                image_path = os.path.join(media_folder, sanitized_image_filename)
                utils.download_image(image_url, image_path)
                utils.resize_image_proportionally(image_path)
                media_files.append(image_path)
        elif 'image_file' in number_data:
            image_file = number_data['image_file']
            if len(image_file):
                sanitized_image_filename = os.path.basename(image_file)
                image_path = os.path.join(media_folder, sanitized_image_filename)
                shutil.copy(image_file, image_path)
                utils.resize_image_proportionally(image_path)
                media_files.append(image_path)

        # Generate conjugations and audio
        finnish = number_data['finnish']

        sanitized_audio_filename = utils.sanitize_filename(f"{number}_number_{finnish}.mp3")
        audio_path = os.path.join(media_folder, sanitized_audio_filename)
        utils.generate_audio(finnish, audio_path)
        media_files.append(audio_path)

        item_note = ""
        if 'note' in number_data:
            item_note = number_data['note']

        # Add note
        if deck_type == 'regular':
            note = genanki.Note(
                model=model,
                fields=[
                    question,                   # Question
                    f'<img src="{sanitized_image_filename}"/>' if len(sanitized_image_filename) > 0 else "",   # Image
                    finnish,
                    translation,
                    item_note,
                    f"[sound:{sanitized_audio_filename}]",        # Audio
                ],
            )
            deck.add_note(note)
        else:
            note = genanki.Note(
                model=model,
                fields=[
                    question,                   # Question
                    f"[sound:{sanitized_audio_filename}]",        # Audio
                    f'<img src="{sanitized_image_filename}"/>' if len(sanitized_image_filename) > 0 else "",   # Image
                    finnish,
                    translation,
                    item_note
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