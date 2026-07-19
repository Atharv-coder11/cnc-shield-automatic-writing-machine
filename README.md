# CNC Shield Automatic Writing Machine

A 2-axis CNC pen plotter built on an **Arduino Uno + CNC Shield**, running
the standard **GRBL** firmware. Give it text or an image and it converts
it into G-code, then drives the machine to physically draw/write it on
paper with a pen mounted on the Z-axis carriage.

## How it works

```
 text string  ──► render to bitmap (PIL) ─┐
                                           ├──► trace contours (OpenCV) ──► G-code ──► GRBL over serial
 image file   ─────────────────────────────┘
```

Text and images share the same drawing pipeline: text is first rendered
to a black-on-white bitmap with a TTF font, then handed to the same
contour tracer used for images. That keeps the codebase small and
consistent.

## Hardware

- Arduino Uno
- CNC Shield V3 (or similar)
- 2x stepper motors (X/Y) + drivers (A4988/DRV8825)
- Small servo (e.g. SG90) for pen lift
- Pen/marker holder on the Z-carriage
- 12V power supply for the shield

## Setup

1. Flash GRBL to the Arduino — see [`firmware/GRBL_SETUP.md`](firmware/GRBL_SETUP.md).
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Edit [`config.py`](config.py):
   - `SERIAL_PORT` — the port your Arduino shows up as
   - `FONT_PATH` — path to any `.ttf` font on your system
   - `BED_WIDTH_MM` / `BED_HEIGHT_MM` — your machine's drawable area
   - `PEN_UP_CMD` / `PEN_DOWN_CMD` — match your pen-lift wiring

## Usage

Generate G-code from text:
```bash
python main.py --text "Hello World" --out hello.gcode
```

Generate G-code from an image (traces contours/outlines):
```bash
python main.py --image logo.png --out logo.gcode
```

Generate and immediately send to the machine:
```bash
python main.py --text "Hi there" --send
```

Override the serial port for one run:
```bash
python main.py --image logo.png --send --port COM5
```

## Project structure

```
cnc-writing-machine/
├── README.md
├── requirements.txt
├── config.py                 # all machine/drawing settings
├── main.py                   # CLI entry point
├── core/
│   ├── text_to_gcode.py      # text -> bitmap -> G-code
│   ├── image_to_gcode.py     # image -> contours -> G-code
│   └── gcode_sender.py       # streams G-code to GRBL over serial
└── firmware/
    └── GRBL_SETUP.md         # how to flash GRBL onto the Arduino
```

## Notes / tuning tips

- If letters/shapes come out stretched, check the `$100`/`$101` steps/mm
  GRBL settings (see `firmware/GRBL_SETUP.md`) — this is the most common
  calibration issue.
- Increase `CONTOUR_SIMPLIFY_EPSILON` in `config.py` for cleaner, less
  jittery strokes on noisy images; decrease it to keep more fine detail.
- `DRAW_FEED_RATE` may need to be lowered if the pen skips or drags at
  higher speeds — start slow and increase once it's dialed in.

## License

MIT — free to use and modify for your own build.
