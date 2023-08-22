import argparse
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
import hanzidentifier
import urllib.request
import time

W = 1280

def get_image_url(char):
    base_url = f"https://commons.wikimedia.org/wiki/File:{char}-red.png"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_link = soup.find('a', {"class": "internal"})
    if image_link:
        return image_link['href']
    else:
        return None

def get_zhuyin(char):
    zhuyin = os.popen(f"zhuyin {char}").read().strip()
    return zhuyin

def create_character_image(char):
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(args.font, 200)
    w, h = draw.textsize(char, font=font)
    draw.text(((300-w)/2, (300-h)/2), char, fill="black", font=font)
    return img

def download_image(url, filename):
    headers = {'User-Agent': 'YourAppName/1.0'} # Replace with appropriate value
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            with open(filename, 'wb') as file:
                file.write(response.read())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            retry_after = int(e.headers.get('Retry-After', 0))
            print(f"Received 429, sleeping for {retry_after} seconds.")
            time.sleep(retry_after)
            # Optionally, you could call download_image again to retry after waiting


def add_white_background(image):
    background = Image.new('RGB', image.size, (255, 255, 255))
    try:
        background.paste(image, mask=image.split()[3])
    except:
        background.paste(image)
    return background



def check_character_type(char: str, character_type: str) -> bool:
    """
    Check if the character matches the specified type (traditional or simplified).

    Parameters:
    char (str): The character to check.
    character_type (str): The type of character to check for ('traditional' or 'simplified').

    Returns:
    bool: True if the character matches the specified type, False otherwise.
    """
    if character_type == 'traditional' and hanzidentifier.is_traditional(char):
        return True
    elif character_type == 'simplified' and hanzidentifier.is_simplified(char):
        return True
    else:
        return False

def add_normal_character(draw: ImageDraw.Draw, char: str, x: int, y: int):
    """
    Add the normal character to the image.

    Parameters:
    draw (ImageDraw.Draw): The ImageDraw instance for the image.
    char (str): The character to add.
    x (int): The x-coordinate at which to add the character.
    y (int): The y-coordinate at which to add the character.
    """
    img = create_character_image(char)
    new_img.paste(img, (x, y))

def add_stroke_order_character(new_img: Image, char: str, x: int, y: int):
    """
    Add the stroke order character to the image if available.

    Parameters:
    new_img (Image): The image to add the stroke order character to.
    char (str): The character to add.
    x (int): The x-coordinate at which to add the character.
    y (int): The y-coordinate at which to add the character.
    """
    image_url = get_image_url(char)
    if image_url:
        download_image(image_url, 'stroke_order.png')
        stroke_order = Image.open('stroke_order.png')
        stroke_order = add_white_background(stroke_order)
        new_img.paste(stroke_order, (x, y))
        return True
    return False

def add_zhuyin(draw: ImageDraw.Draw, char: str, x: int, y: int):
    """
    Add Zhuyin to the image if the `output_zhuyin` argument is set to `True`.

    Parameters:
    draw (ImageDraw.Draw): The ImageDraw instance for the image.
    char (str): The character for which to add Zhuyin.
    x (int): The starting x-coordinate for the Zhuyin.
    y (int): The starting y-coordinate for the Zhuyin.
    """
    zhuyin_chars = get_zhuyin(char)
    for i, zhuyin_char in enumerate(zhuyin_chars):
        draw.text((x, y + i * 50), zhuyin_char, fill="black", font=font)

def add_pinyin(draw: ImageDraw.Draw, pinyin: str):
    """
    Add Pinyin to the image.

    Parameters:
    draw (ImageDraw.Draw): The ImageDraw instance for the image.
    pinyin (str): The Pinyin to add.
    """
    w = draw.textlength(text=pinyin, font=font)
    pinyin_x = (W-w)/2
    draw.text((pinyin_x, 350), pinyin, fill="black", font=font)

def add_definition(draw: ImageDraw.Draw, definition: str, max_width: int):
    """
    Add the definition to the image.

    Parameters:
    draw (ImageDraw.Draw): The ImageDraw instance for the image.
    definition (str): The definition to add.
    max_width (int): The maximum width for the definition text.
    """
    lines = []
    words = definition.split()
    current_line = words.pop(0)

    for word in words:
        w, h = draw.textbbox((0, 0), current_line + " " + word, font=font)[2:]
        if w > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line += " " + word

    lines.append(current_line)

    for i, line in enumerate(lines):
        w, h = draw.textbbox((0, 0), line, font=font)[2:]
        x = (W-w)/2
        y = 350 + 60 + i*60
        draw.text((x, y), line, fill="black", font=font)


if __name__ == '__main__':
    # Parser for command-line options
    parser = argparse.ArgumentParser(description='Generate images for Chinese characters.')
    parser.add_argument('--output-zhuyin', action='store_true', default=True,
                        help='Include Zhuyin in the output image.')
    parser.add_argument('--character-type', choices=['traditional', 'simplified'], default='traditional',
                        help='The type of Chinese characters to use.')
    parser.add_argument('--output-dir', default='./images',
                        help='Directory to save the output images.')
    parser.add_argument('--font', default='fonts/NotoSansTC-Regular.otf',
                        help='Path to the font file to use.')
    parser.add_argument('--input-file', default='hanziDB.csv',
                        help='CSV file to read the Hanzi data from.')
    parser.add_argument('--hsk-level', type=int,
                        help='HSK level for which characters should be generated. By default, generate for all levels.')
    parser.add_argument('--skip-missing', type=bool, default=True,
                        help='Skip characters missing the stroke order.')

    # Parse the arguments
    args = parser.parse_args()

    # Margin for the image
    left_margin = 250

    # Read the Hanzi data from the CSV file
    df = pd.read_csv(args.input_file).dropna(subset=['definition'])

    for idx, row in df.iterrows():
        char = row['character']
        if not check_character_type(char, args.character_type):
            continue

        pinyin = row['pinyin']
        definition = row['definition']

        new_img = Image.new('RGB', (1280, 720), color='white')
        draw = ImageDraw.Draw(new_img)
        font = ImageFont.truetype(args.font, 50)

        add_normal_character(draw, char, left_margin + 25, 20)
        added = add_stroke_order_character(new_img, char, left_margin + 425, 50)
        if not added and args.skip_missing:
            continue

        if args.output_zhuyin:
            add_zhuyin(draw, char, left_margin + 315, 125)

        add_pinyin(draw, pinyin)
        add_definition(draw, definition, W - left_margin)

            # Create the output directory if it doesn't exist
        output_dir = os.path.join(args.output_dir, str(int(row['hsk_level'])))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the image
        new_img.save(f"{output_dir}/{char}.png")
