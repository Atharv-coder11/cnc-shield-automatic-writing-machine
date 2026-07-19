"""
Machine & drawing configuration for the CNC Shield Automatic Writing Machine.
Tune these values to match your specific hardware before running anything.
"""

# ---- Serial connection ----
SERIAL_PORT = "COM3"          # e.g. "COM3" on Windows, "/dev/ttyUSB0" on Linux/Mac
BAUD_RATE = 115200

# ---- Drawing area (mm) ----
BED_WIDTH_MM = 200
BED_HEIGHT_MM = 200

# ---- Feed rates (mm/min) ----
DRAW_FEED_RATE = 1200     # speed while pen is down and drawing
TRAVEL_FEED_RATE = 3000   # speed while pen is up and moving between strokes

# ---- Pen lift control ----
# Most CNC-shield "writing machine" builds mount a small servo on the
# spindle/laser output to lift and drop the pen. GRBL exposes this
# through the M3 (spindle on) / M5 (spindle off) commands.
PEN_UP_CMD = "M5"                # spindle off -> pen lifts via servo horn
PEN_DOWN_CMD = "M3 S1000"        # spindle on at fixed power -> pen drops
PEN_MOVE_DELAY_S = 0.3           # settle time after a pen up/down move

# ---- Text rendering ----
FONT_PATH = "C:/Windows/Fonts/arial.ttf"   # point this at any .ttf on your system
FONT_SIZE_PX = 120           # render resolution before scaling down to mm
TEXT_HEIGHT_MM = 20          # final height of the writing on paper

# ---- Image tracing ----
IMAGE_TARGET_WIDTH_MM = 100        # width to scale a traced image to
CONTOUR_SIMPLIFY_EPSILON = 1.5     # higher = smoother/simpler paths, lower = more detail
