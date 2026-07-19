"""
Convert a text string into pen-plotter G-code.

Renders the text to a bitmap using a TTF font, then hands that bitmap
to the same contour tracer used for images (core/image_to_gcode.py) —
so text and image input share one drawing pipeline.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import config
from core.image_to_gcode import image_to_gcode


def render_text_to_array(text, font_path=None, font_size=None):
    font_path = font_path or config.FONT_PATH
    font_size = font_size or config.FONT_SIZE_PX

    font = ImageFont.truetype(font_path, font_size)

    # Measure the text first so the canvas is sized with a small margin
    dummy = Image.new("L", (10, 10), 255)
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=font)
    margin = 20
    w = (bbox[2] - bbox[0]) + margin * 2
    h = (bbox[3] - bbox[1]) + margin * 2

    img = Image.new("L", (w, h), 255)
    draw = ImageDraw.Draw(img)
    draw.text((margin - bbox[0], margin - bbox[1]), text, fill=0, font=font)

    return np.array(img)


def text_to_gcode(text, target_height_mm=None):
    """
    Render `text` and return ready-to-run G-code sized to target_height_mm.
    """
    target_height_mm = target_height_mm or config.TEXT_HEIGHT_MM
    arr = render_text_to_array(text)
    h, w = arr.shape
    # image_to_gcode scales by width, so back-calculate the width that
    # gives the desired final height at this bitmap's aspect ratio
    target_width_mm = target_height_mm * (w / h)
    return image_to_gcode(image_array=arr, target_width_mm=target_width_mm)
