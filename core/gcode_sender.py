"""
Stream a block of G-code to a GRBL-controlled CNC shield over serial,
following GRBL's standard line-by-line streaming protocol: send one
line, wait for "ok" (or "error"), then send the next.
"""

import time
import serial

import config


def stream_gcode(gcode_text, port=None, baud=None, verbose=True):
    port = port or config.SERIAL_PORT
    baud = baud or config.BAUD_RATE

    lines = [ln for ln in gcode_text.splitlines() if ln.strip() and not ln.strip().startswith(";")]

    with serial.Serial(port, baud, timeout=5) as ser:
        time.sleep(2)  # GRBL resets on serial connect — give it time to wake up
        ser.reset_input_buffer()
        ser.write(b"\r\n\r\n")
        time.sleep(2)
        ser.reset_input_buffer()

        for i, line in enumerate(lines, 1):
            clean = line.split(";")[0].strip()  # strip inline comments
            if not clean:
                continue
            ser.write((clean + "\n").encode())
            response = ser.readline().decode(errors="ignore").strip()
            if verbose:
                print(f"[{i}/{len(lines)}] > {clean}  -> {response}")
            if "error" in response.lower():
                raise RuntimeError(f"GRBL error on line {i}: '{clean}' -> {response}")

    if verbose:
        print("Streaming complete.")
