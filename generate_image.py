from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap
import os

# Set up the font
font_path = 'NotoSansTC-Regular.otf'
base_font_size = 36
# Dimensions of the image
img_width = 800
img_height = 600

# Read the CSV file
df = pd.read_csv('hanziDB.csv')

# Create images directory if it doesn't exist
os.makedirs('img', exist_ok=True)

# Function to adjust font size based on text length
def adjust_font_size(draw, text, font_path, base_font_size, max_width):
    font_size = base_font_size
    font = ImageFont.truetype(font_path, font_size)
    w, h = draw.textsize(text, font=font)
    while w > max_width:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        w, h = draw.textsize(text, font=font)
    return font

for index, row in df.iterrows():
    character = row['character']
    pronunciation = row['pinyin']
    definition = textwrap.fill(row['definition'], width=30)  # wrap the text to fit into image

    # Create a new image
    img = Image.new('RGB', (img_width, img_height), color='white')
    d = ImageDraw.Draw(img)

    # Add the text to the image
    char_font = ImageFont.truetype(font_path, base_font_size)
    d.text((10, 10), character, font=char_font, fill='black')
    _, char_height = d.textsize(character, font=char_font)

    def_font = adjust_font_size(d, definition, font_path, base_font_size, img.width - 20)
    d.text((10, char_height + 20), definition, font=def_font, fill='black')
    _, def_height = d.textsize(definition, font=def_font)

    pron_font = ImageFont.truetype(font_path, base_font_size)
    d.text((10, char_height + def_height + 30), pronunciation, font=pron_font, fill='black')

    # Save the image
    img.save(f'img/{pronunciation}.png')

    # Stop after generating one image
    break
