import argparse
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import time
import hanzidentifier
import urllib.request

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
    draw.text(((300-w)/2, (300-h)/2), char, fill=args.color, font=font)
    return img

def download_image(url, filename):
    urllib.request.urlretrieve(url, filename)

def add_white_background(image):
    background = Image.new('RGB', image.size, (255, 255, 255))
    try:
        background.paste(image, mask=image.split()[3])
    except:
        background.paste(image)
    return background


parser = argparse.ArgumentParser(description='Generate images for Chinese characters.')
parser.add_argument('--output-zhuyin', action='store_true', default=True,
                    help='Include Zhuyin in the output image.')
parser.add_argument('--character-type', choices=['traditional', 'simplified'], default='traditional',
                    help='The type of Chinese characters to use.')
parser.add_argument('--output-dir', default='./images',
                    help='Directory to save the output images.')
parser.add_argument('--font', default='NotoSansTC-Regular.otf',
                    help='Path to the font file to use.')
parser.add_argument('--input-file', default='hanziDB.csv',
                    help='CSV file to read the Hanzi data from.')
parser.add_argument('--color', default='black',
                    help='Color of the text.')

args = parser.parse_args()

left_margin = 250
df = pd.read_csv(args.input_file).dropna(subset=['definition'])

for idx, row in df.iterrows():
    char = row['character']

    if args.character_type == 'traditional' and not hanzidentifier.is_traditional(char):
        continue

    elif args.character_type == 'simplified' and not hanzidentifier.is_simplified(char):
        continue

    pinyin = row['pinyin']
    definition = row['definition']

    new_img = Image.new('RGB', (1280, 720), color='white')
    img = create_character_image(char)
    new_img.paste(img, (left_margin+25, 20))

    image_url = get_image_url(char)
    if image_url:
        download_image(image_url, 'stroke_order.png')
        stroke_order = Image.open('stroke_order.png')
        stroke_order = add_white_background(stroke_order)
        new_img.paste(stroke_order, (left_margin+425, 50))

    W, H = new_img.size
    draw = ImageDraw.Draw(new_img)
    font = ImageFont.truetype(args.font, 50)

    if args.output_zhuyin:
        zhuyin_chars = get_zhuyin(char)
        zhuyin_x = left_margin+315
        zhuyin_y = 125
        for i, zhuyin_char in enumerate(zhuyin_chars):
            y = zhuyin_y + i * 50
            draw.text((zhuyin_x, y), zhuyin_char, fill=args.color, font=font)

    w = draw.textlength(text=pinyin, font=font)
    pinyin_x = (W-w)/2
    draw.text((pinyin_x, 350), pinyin, fill=args.color, font=font)

    max_width = W - left_margin
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
        draw.text((x, y), line, fill=args.color, font=font)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    new_img.save(f"{args.output_dir}/{char}.png")
