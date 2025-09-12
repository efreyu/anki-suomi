import genanki
import json
import os
import sys
import shutil
import generators.gen_utils as utils

def gen_dialogs(json_file, deck_name, apkg_filename='Finnish_Dialogs.apkg'):
    """
    Making card structure that contains dialogs
    Question: Dialog questions
    {{Question}}
    Answer: Dialog answers in Finnish with English translation
    <table>
    <tr>
    <td>{{Finnish}}</td>
    <td>{{Translation}}</td>
    <td>{{Audio}}</td>
    </tr>
    ...
    </table>
    """

    # Create the model for the Anki cards
    model_id = 1234567890
    model = genanki.Model(
        model_id,
        'Numbers Table with Image and Audio',
        fields=[
            {'name': 'Question'},
            {'name': 'Finnish'},
            {'name': 'Translate'},
            {'name': 'Audio'}
        ],
        templates=[
            {
                'name': 'Numbers Card',
                'qfmt': """
                    <div>{{Question}}</div>
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
                        <td>{{Translate}}</td>
                      </tr>
                      <tr>
                        <td>{{Audio}}</td>
                      </tr>
                    </table>
                """,
            },
        ],
        css="""
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
    )

    # Create the deck
    deck_id = 987654321
    deck = genanki.Deck(
        deck_id,
        deck_name,
    )

    json_data = []
    # Load data from the JSON file
    with (open(json_file, 'r', encoding='utf-8') as f):
        json_data = json.load(f)

    # Directory for media files (audio and images)
    if os.path.exists('media'):
        shutil.rmtree('media')
    media_folder = 'media'
    os.makedirs(media_folder, exist_ok=True)

    # List to store paths to media files
    media_files = []

    # Add cards to the deck
    for json_item in json_data:
        questions = json_item['questions']
        question = ""
        audio_text = ""
        for i in range(len(questions)):
            question += f"{i + 1}. {questions[i]} "
            audio_text += f"{questions[i]}\n"

        questions_translation = json_item['questions_translation']
        for i in range(len(questions_translation)):
            question += f"{i + 1}. {questions_translation[i]} "

        answers = json_item['answer']
        answer = ""
        for i in range(len(answers)):
            answer += f"{i + 1}. {answers[i]} "
            audio_text += f"{answers[i]}\n"

        answer_translation = json_item['answer_translation']
        for i in range(len(answer_translation)):
            question += f"{i + 1}. {answer_translation[i]} "


        sanitized_audio_filename = utils.sanitize_filename(f"{number}_number_{finnish}.mp3")
        audio_path = os.path.join(media_folder, sanitized_audio_filename)
        utils.generate_audio(finnish, audio_path)
        media_files.append(audio_path)

        item_note = ""
        if 'note' in json_item:
            item_note = json_item['note']

        # Add note
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

    # Create the package and include media files
    package = genanki.Package(deck)
    package.media_files = media_files  # Add media files (audio + images) to the package
    package.write_to_file(apkg_filename)

    return True


if __name__ == '__main__':
    sys.exit(1)