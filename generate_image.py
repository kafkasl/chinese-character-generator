# Python script that generates images of Chinese characters with their pronunciation and translation using the Google Translate API and the Pillow library:
# This script uses the `googletrans` library to translate Chinese characters to English and get their pronunciation. It also uses the `Pillow` library to generate images with the character, its translation, and pronunciation. You can modify this script to use a different list of characters or change the layout of the generated images.

# Please note that you'll need to install the `googletrans` and `Pillow` libraries by running `pip install googletrans Pillow` before running this script.

from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont

# Set up the translator
translator = Translator()

# Set up the font
#font = ImageFont.truetype('Arial.ttf', 36)
font = ImageFont.truetype('NotoSansTC-Regular.otf', 36)


# List of Chinese characters
characters = ['你', '好', '吗']

for character in characters:
    # Get the translation and pronunciation
    translation = translator.translate(character, src='zh-cn', dest='en')
    pronunciation = translation.extra_data['origin_pronunciation']

    # Create a new image
    img = Image.new('RGB', (200, 200), color='white')
    d = ImageDraw.Draw(img)

    # Add the text to the image
    d.text((10, 10), character, font=font, fill='black')
    d.text((10, 60), translation.text, font=font, fill='black')
    d.text((10, 110), pronunciation, font=font, fill='black')

    # Save the image
    img.save(f'{pronunciation}.png')
