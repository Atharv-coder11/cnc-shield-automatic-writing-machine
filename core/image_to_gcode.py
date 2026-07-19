"""
Convert a black-and-white image into pen-plotter G-code by tracing contours.

Used directly for images, and reused internally by text_to_gcode.py
(which renders text to a bitmap first, then hands it to this same tracer).
"""

import cv2
import numpy as np

import config


def _load_grayscale(image_path=None, image_array=None):
    if image_array is not None:
        return image_array
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    return img


def _find_contours(gray_img):
    # Threshold to pure black/white, then invert so drawn shapes are white-on-black
    _, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def _simplify(contours, epsilon=None):
    epsilon = epsilon if epsilon is not None else config.CONTOUR_SIMPLIFY_EPSILON
    simplified = []
    for c in contours:
        if len(c) < 2:
            continue
        approx = cv2.approxPolyDP(c, epsilon, closed=True)
        simplified.append(approx.reshape(-1, 2))
    return simplified


def _scale_to_mm(contours, img_w, img_h, target_width_mm):
    scale = target_width_mm / img_w
    scaled = []
    for c in contours:
        pts = c.astype(float) * scale
        # Image Y grows downward; machine Y grows upward, so flip it
        pts[:, 1] = (img_h * scale) - pts[:, 1]
        scaled.append(pts)
    return scaled


def contours_to_gcode(contours, feed_draw=None, feed_travel=None):
    feed_draw = feed_draw or config.DRAW_FEED_RATE
    feed_travel = feed_travel or config.TRAVEL_FEED_RATE

    lines = [
        "G21 ; units = mm",
        "G90 ; absolute positioning",
        config.PEN_UP_CMD,
        f"G0 F{feed_travel}",
    ]

    for path in contours:
        if len(path) < 2:
            continue
        start_x, start_y = path[0]
        lines.append(f"G0 X{start_x:.2f} Y{start_y:.2f}")
        lines.append(config.PEN_DOWN_CMD)
        lines.append(f"G1 F{feed_draw}")
        for x, y in path[1:]:
            lines.append(f"G1 X{x:.2f} Y{y:.2f}")
        lines.append(config.PEN_UP_CMD)
        lines.append(f"G0 F{feed_travel}")

    lines.append(config.PEN_UP_CMD)
    lines.append("G0 X0 Y0 ; return to origin")
    return "\n".join(lines)


def image_to_gcode(image_path=None, image_array=None, target_width_mm=None):
    """
    Trace an image (by path OR as a numpy grayscale array) and return
    ready-to-run G-code as a string.
    """
    target_width_mm = target_width_mm or config.IMAGE_TARGET_WIDTH_MM
    gray = _load_grayscale(image_path, image_array)
    h, w = gray.shape
    contours = _find_contours(gray)
    contours = _simplify(contours)
    contours = _scale_to_mm(contours, w, h, target_width_mm)
    return contours_to_gcode(contours)
