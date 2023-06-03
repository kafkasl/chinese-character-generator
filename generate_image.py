import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from bs4 import BeautifulSoup

def get_image_url(char):
    base_url = f"https://commons.wikimedia.org/wiki/File:{char}-red.png"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the link to the image
    image_link = soup.find('a', {"class": "internal"})
    if image_link:
        return image_link['href']
    else:
        return None

def get_zhuyin(char):
    # Assuming you have the go-zhuyin tool installed and accessible in your PATH
    zhuyin = os.popen(f"zhuyin {char}").read().strip()
    return zhuyin

def create_character_image(char):
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('NotoSansTC-Regular.otf', 200)
    w, h = draw.textsize(char, font=font)
    draw.text(((300-w)/2, (300-h)/2), char, fill="black", font=font)
    return img

df = pd.read_csv('hanziDB.csv')

for idx, row in df.iterrows():
    char = row['character']
    pinyin = row['pinyin']
    definition = row['definition']

    img = create_character_image(char)
    image_url = get_image_url(char)
    stroke_order = None
    if image_url:
        response = requests.get(image_url)
        stroke_order = Image.open(BytesIO(response.content))

    # Create a new image with a larger size
    new_img = Image.new('RGB', (800, 600), color='white')

    # Paste the original image into the new image
    new_img.paste(img, (50, 20))
    new_img.paste(stroke_order, (350, 50))

    W, H = new_img.size
    draw = ImageDraw.Draw(new_img)
    font = ImageFont.truetype('NotoSansTC-Regular.otf', 50)

    zhuyin = get_zhuyin(char)

    text = f"{pinyin}\n{zhuyin}\n{definition}"
    w, h = draw.textsize(text, font=font)
    draw.text(((W-w)/2, 350), text, fill="black", font=font)

    new_img.save(f"img/{char}.png")

    break  # Remove this line to generate images for all characters
