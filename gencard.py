import os
import random
from PIL import Image, ImageDraw, ImageFont

# Dictionary to store template-specific details
templates = {
    # "template1.png": {
    #     "bounding_box": (45, 380, 810, 140),
    #     "font_path": "fonts/American Captain.ttf",
    #     "text_color": (255, 255, 255),
    #     "max_font_size": 1000,
    #     "uppercase": False
    # },
    # "template2.png": {
    #     "bounding_box": (310, 380, 790, 140),
    #     "font_path": "fonts/American Captain.ttf",
    #     "text_color": (255, 255, 255),
    #     "max_font_size": 1000,
    #     "uppercase": False
    # },
    # "template3.png": {
    #     "bounding_box": (280, 440, 880, 140),
    #     "font_path": "fonts/Holiday.otf",
    #     "text_color": (77, 75, 76),
    #     "max_font_size": 1000,
    #     "uppercase": False
    # },
    # "template4.png": {
    #     "bounding_box": (380, 400, 700, 200),
    #     "font_path": "fonts/American Captain.ttf",
    #     "text_color": (30, 31, 30),
    #     "max_font_size": 150,
    #     "uppercase": False
    # },
    # "template5.png": {
    #     "bounding_box": (250, 500, 950, 200),
    #     "font_path": "fonts/Holiday.otf",
    #     "text_color": (188, 76, 175),
    #     "max_font_size": 250,
    #     "uppercase": False
    # },
    "template6.png": {
        "bounding_box": (310, 410, 790, 150),
        "font_path": "fonts/Mistrully.ttf",
        "text_color": (0, 0, 0),
        "max_font_size": 250,
        "uppercase": False
    }
}

def generate_birthday_card(name):
    # Randomly select a template
    template_name = random.choice(list(templates.keys()))
    template_details = templates[template_name]

    # Capitalize and transform the name based on the "uppercase" flag
    name = name.title()  # Default title-cased
    if template_details.get("uppercase", False):  # Apply uppercase if flag is True
        name = name.upper()

    # Extract details from the template dictionary
    bounding_box = template_details["bounding_box"]
    font_path = template_details["font_path"]
    text_color = template_details["text_color"]
    max_font_size = template_details["max_font_size"]

    # Open the template image
    template_path = f"./templates/{template_name}"
    print(template_path)
    cert_img = Image.open(template_path)
    draw = ImageDraw.Draw(cert_img)

    # Determine the appropriate font size
    font_size = max_font_size
    while font_size > 10:
        font = ImageFont.truetype(font_path, font_size)
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        box_x, box_y, box_width, box_height = bounding_box
        if text_width <= box_width and text_height <= box_height:
            break
        font_size -= 2

    # Calculate text position to center it in the bounding box
    text_x = box_x + (box_width - text_width) / 2
    text_y = box_y + (box_height - text_height) / 2

    # Add the name to the template
    draw.text((text_x, text_y), name, fill=text_color, font=font)

    # Save the output in the "temp" folder
    output_dir = "temp"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}_card.png")
    cert_img.save(output_path)
    return output_path

# Example usage
if __name__ == "__main__":
    # generated_card = generate_birthday_card("Sarkar shahul hameed hull hussain")
    generated_card = generate_birthday_card("Dhanush N")
    print(f"Card generated and saved at: {generated_card}")
