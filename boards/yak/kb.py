import board
import digitalio
import busio
import adafruit_74hc595


from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners import DiodeOrientation


spi = busio.SPI(board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D7)
sr = adafruit_74hc595.ShiftRegister74HC595(spi, cs, number_of_shift_registers=2)


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.D3, board.D4, board.D5, board.D6)
    col_pins = (
        sr.get_pin(15),
        sr.get_pin(14),
        sr.get_pin(13),
        sr.get_pin(12),
        sr.get_pin(11),
        sr.get_pin(10),

        sr.get_pin(9),

        sr.get_pin(7),

        sr.get_pin(6),
        sr.get_pin(5),
        sr.get_pin(4),
        sr.get_pin(3),
        sr.get_pin(2),
        sr.get_pin(1)
    )

    diode_orientation = DiodeOrientation.COLUMNS

    matrix = MatrixScanner(
        cols = col_pins,
        rows = row_pins,
        diode_orientation = diode_orientation,
    )

    rgb_pixel_pin = board.A2
    rgb_num_pixels = 48


    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,     8,  9, 10, 11, 12, 13,
    14, 15, 16, 17, 18, 19,    22, 23, 24, 25, 26, 27,
    28, 29, 30, 31, 32, 33,    36, 37, 38, 39, 40, 41,
    42, 43, 44, 45, 46, 47,    50, 51, 52, 53, 54, 55,
            48, 34, 20,   6,  7,   21, 35, 49
    ]


from kmkx.modules.modremap import ModRemap, ModRemapMeta
from kmk.keys import KC, Key

remap = ModRemap()

'''
 label Base  None    Shift   Opt       Shift-Opt
 (     9     +shift  ,       w+shift   \ -shift
 )     0     +shift  .       [         \
 &     6     +shift  7       [+shift   None
 $     4     +shift  5       2+shift   None
 #     3     +shift  2       no ∆      None
 !     1     +shift  /       no ∆      /
'''

lprn = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: s and a, KC.BSLASH, {KC.LSFT,KC.RSFT}),
        (lambda c,s,a,g: s, KC['<']),
        (lambda c,s,a,g: a, KC.LSFT(KC.W)),
        (lambda c,s,a,g: True, KC['(']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


rprn = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: s and a, KC.BSLASH),
        (lambda c,s,a,g: s, KC['>']),
        (lambda c,s,a,g: a, KC['[']),
        (lambda c,s,a,g: True, KC[')']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


caret = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: s and a, KC.N7, {KC.LSFT,KC.RSFT}),
        (lambda c,s,a,g: a, KC.N6),
        (lambda c,s,a,g: s, KC.N7),
        (lambda c,s,a,g: True, KC['^']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


dollar = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: s and a, KC.N5, {KC.LSFT,KC.RSFT}),
        (lambda c,s,a,g: a, KC['@']),
        (lambda c,s,a,g: s, KC.N5),
        (lambda c,s,a,g: True, KC['$']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


at = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: a, KC.N3, {KC.LSFT,KC.RSFT}),
        (lambda c,s,a,g: s, KC.N3),
        (lambda c,s,a,g: True, KC['@']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


bang = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: s and a, KC['/']),
        (lambda c,s,a,g: s, KC['/']),
        (lambda c,s,a,g: a, KC.N1),
        (lambda c,s,a,g: True, KC['!']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


slash = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: not s and not a, KC['/']),
        (lambda c,s,a,g: True, KC.N8),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


lbrc = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: g and a, KC['{'], {KC.LALT,KC.RALT}),
        (lambda c,s,a,g: a, KC['['], {KC.LALT,KC.RALT}),
        (lambda c,s,a,g: True, KC['[']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


rbrc = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: g and a, KC['}'], {KC.LALT,KC.RALT}),
        (lambda c,s,a,g: a, KC[']'], {KC.LALT,KC.RALT}),
        (lambda c,s,a,g: True, KC[']']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


bsls = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: a and not g, KC['\\'], {KC.LALT,KC.RALT}),
        (lambda c,s,a,g: True, KC['\\']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


comma = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: a, KC[';'], {KC.LSFT,KC.RSFT}),
        (lambda c,s,a,g: s, KC[';'], {KC.LSFT,KC.RSFT}),
        (lambda c,s,a,g: True, KC[',']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)


dot = Key(
    code=9999,
    has_modifiers=None,
    meta=ModRemapMeta([
        (lambda c,s,a,g: a, KC[';'], {KC.LSFT,KC.RSFT}),
        (lambda c,s,a,g: s, KC[';']),
        (lambda c,s,a,g: True, KC['.']),
    ]),
    on_press=remap.press,
    on_release=remap.release
)
