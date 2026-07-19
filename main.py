"""
CNC Shield Automatic Writing Machine — entry point.

Examples:
    python main.py --text "Hello World" --out hello.gcode
    python main.py --image drawing.png --out drawing.gcode
    python main.py --text "Hi" --send                 # generate AND stream to the machine
    python main.py --image logo.png --send --port COM5
"""

import argparse

import config
from core.text_to_gcode import text_to_gcode
from core.image_to_gcode import image_to_gcode
from core.gcode_sender import stream_gcode


def main():
    parser = argparse.ArgumentParser(description="CNC Shield Automatic Writing Machine")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text string to write")
    group.add_argument("--image", help="Path to an image to trace")

    parser.add_argument("--out", default="output.gcode", help="Output .gcode file path")
    parser.add_argument("--send", action="store_true", help="Stream the G-code to the machine after generating it")
    parser.add_argument("--port", default=None, help="Override the serial port set in config.py")

    args = parser.parse_args()

    if args.text:
        gcode = text_to_gcode(args.text)
    else:
        gcode = image_to_gcode(image_path=args.image)

    with open(args.out, "w") as f:
        f.write(gcode)
    print(f"G-code written to {args.out} ({len(gcode.splitlines())} lines)")

    if args.send:
        print("Streaming to machine...")
        stream_gcode(gcode, port=args.port)


if __name__ == "__main__":
    main()
