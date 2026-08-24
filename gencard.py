import os
import random

from PIL import Image, ImageDraw, ImageFont

from config import BASE_DIR, TEMP_DIR

TEMPLATES = {
    "template1.png": {
        "bounding_box": (45, 380, 810, 140),
        "font_path": "fonts/American Captain.ttf",
        "text_color": (255, 255, 255),
        "max_font_size": 1000,
        "uppercase": False,
    },
    "template2.png": {
        "bounding_box": (310, 380, 790, 140),
        "font_path": "fonts/American Captain.ttf",
        "text_color": (255, 255, 255),
        "max_font_size": 1000,
        "uppercase": False,
    },
    "template3.png": {
        "bounding_box": (280, 440, 880, 140),
        "font_path": "fonts/Holiday.otf",
        "text_color": (77, 75, 76),
        "max_font_size": 1000,
        "uppercase": False,
    },
    "template4.png": {
        "bounding_box": (380, 400, 700, 200),
        "font_path": "fonts/American Captain.ttf",
        "text_color": (30, 31, 30),
        "max_font_size": 150,
        "uppercase": False,
    },
    "template5.png": {
        "bounding_box": (250, 500, 950, 200),
        "font_path": "fonts/Holiday.otf",
        "text_color": (188, 76, 175),
        "max_font_size": 250,
        "uppercase": False,
    },
    "template6.png": {
        "bounding_box": (310, 410, 790, 150),
        "font_path": "fonts/Mistrully.ttf",
        "text_color": (0, 0, 0),
        "max_font_size": 250,
        "uppercase": False,
    },
    "template7.png": {
        "bounding_box": (490, 390, 530, 180),
        "font_path": "fonts/Gagalin-Regular.otf",
        "text_color": (62, 27, 14),
        "max_font_size": 250,
        "uppercase": False,
    },
}


def generate_birthday_card(name):
    template_name = random.choice(list(TEMPLATES.keys()))
    details = TEMPLATES[template_name]
    name = name.title()
    if details.get("uppercase"):
        name = name.upper()

    bounding_box = details["bounding_box"]
    font_path = os.path.join(BASE_DIR, details["font_path"])
    text_color = details["text_color"]
    max_font_size = details["max_font_size"]

    template_path = os.path.join(BASE_DIR, "templates", template_name)
    cert_img = Image.open(template_path)
    draw = ImageDraw.Draw(cert_img)

    font_size = max_font_size
    font = ImageFont.load_default()
    box_x, box_y, box_width, box_height = bounding_box
    text_width = box_width
    text_height = box_height
    while font_size > 10:
        font = ImageFont.truetype(font_path, font_size)
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        if text_width <= box_width and text_height <= box_height:
            break
        font_size -= 2

    text_x = box_x + (box_width - text_width) / 2
    text_y = box_y + (box_height - text_height) / 2
    draw.text((text_x, text_y), name, fill=text_color, font=font)

    os.makedirs(TEMP_DIR, exist_ok=True)
    output_path = os.path.join(TEMP_DIR, f"{name}_card.png")
    cert_img.save(output_path)
    return output_path
