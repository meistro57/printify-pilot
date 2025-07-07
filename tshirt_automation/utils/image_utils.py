# image_utils.py – Image generation functions using Pillow
from PIL import Image, ImageDraw, ImageFont
import os

def generate_text_images(phrase):
    font_path = 'arial.ttf'  # Ensure this font is available
    font_size = 200
    canvas_size = (3000, 4000)

    def create_image(text_color):
        img = Image.new('RGBA', canvas_size, (255, 255, 255, 0))
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(img)
        
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), phrase, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Draw centered text
        draw.text(((canvas_size[0]-w)/2, (canvas_size[1]-h)/2), phrase, fill=text_color, font=font)
        
        # Save the image
        os.makedirs('static/images', exist_ok=True)
        filename = f"static/images/{phrase[:10]}_{text_color}.png"
        img.save(filename)
        return filename

    black_img = create_image('black')
    white_img = create_image('white')

    return {'black': black_img, 'white': white_img}
