# Flashing GRBL to the Arduino

The CNC Shield doesn't need custom firmware — it runs the standard,
open-source **GRBL** firmware, which already understands the G-code this
project generates. You just flash it once.

## Steps

1. **Remove the CNC Shield** from the Arduino Uno before flashing (some
   shield pins conflict with the USB upload).
2. Open the Arduino IDE → **Sketch > Include Library > Manage Libraries**
   → search "GRBL" → install the official `grbl` library, OR download the
   latest release from https://github.com/grbl/grbl.
3. Open the example sketch: **File > Examples > grbl > grblUpload**.
4. Select **Board: Arduino Uno** and the correct **Port**, then **Upload**.
5. Re-attach the CNC Shield on top of the Arduino.
6. Open the Arduino IDE Serial Monitor (115200 baud) and reset the board —
   you should see a `Grbl 1.1h ['$' for help]` banner. That confirms GRBL
   is running.

## Pen lift (servo) wiring

Most writing-machine builds mount a small SG90 servo on the Z-axis (or a
spare pin) to lift/drop the pen, controlled through GRBL's spindle output:

- Servo signal → **spindle enable/PWM pin** on the CNC Shield (check your
  shield's silkscreen — commonly labeled `SpinEn` or the Z-limit header
  depending on shield version)
- Servo power (5V) and ground → shield 5V/GND

This project's `config.py` already sends `M3 S1000` to drop the pen and
`M5` to lift it — matching this wiring. If your build uses a different
pin or a different mechanism (e.g. a solenoid), adjust `PEN_UP_CMD` /
`PEN_DOWN_CMD` in `config.py` accordingly.

## Useful GRBL settings to check (`$$` in Serial Monitor)

| Setting | Meaning                          |
|---------|-----------------------------------|
| `$100`  | X steps/mm                        |
| `$101`  | Y steps/mm                        |
| `$110`  | X max rate (mm/min)               |
| `$111`  | Y max rate (mm/min)               |
| `$130`  | X max travel (mm)                 |
| `$131`  | Y max travel (mm)                 |

Set these to match your belt/pulley or leadscrew setup — incorrect
steps/mm is the #1 cause of distorted writing.
