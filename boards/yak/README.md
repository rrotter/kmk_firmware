# yak - yet another keyboard

yak uses two 74hc595 shift registers for column pins. rrotter uses a ton of custom mapping with it.
This is on a branch that should not be upstreamed. To make yak dance:

- install CircuitPython 8
- copy /kmk from the current repo, or better yet get a zip of the .mpy version from [github actions](https://github.com/KMKfw/kmk_firmware/actions/workflows/compile.yml)
- copy over /kmkx from this branch
- download the current [CircuitPython Library Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases) and install under `/lib`:
  - adafruit_74hc595.mpy
  - neopixel.mpy (okay, this isn't used, but yak has them, so it _could be_)
- add kb.py and from this dir
- optionally, add boot.py and reset.py as well:
  - boot.py suppresses the CIRCUITPYTHON drive from mounting
  - reset.py lets you bypass boot.py and mount it anyway: ^C on serial console (Mu is good for this), `import reset`, and you're in. Press the reset button or unplug to get back to normal.