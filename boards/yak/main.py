from kb import KMKKeyboard, remap, lprn, rprn, caret, dollar, at, lbrc, rbrc, bsls, bang, slash, comma, dot

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap
from kmk.extensions.stringy_keymaps import StringyKeymaps

keyboard = KMKKeyboard()

#  standard filler keys
_______ = KC.TRNS
XXXXXXX = KC.NO


keyboard.modules.append(Layers())
keyboard.modules.append(HoldTap())
keyboard.extensions.append(StringyKeymaps())

# kmkx extensions
keyboard.modules.append(remap)
from kmkx.opt_overrides import umlaut
Ä = umlaut(KC.A)
Ö = umlaut(KC.O)
Ü = umlaut(KC.U)


keyboard.debug_enabled = False

# make keymap

CTL_ESC = KC.HT(KC.ESC, KC.LCTRL)
DELETE  = KC.BKSP
RETURN  = KC.ENTER

keyboard.keymap = [
    [  # 0: Colemak-DH
        'GRV',   lprn,   rprn, 'MINS',  'EQL',     at,         DELETE,  caret,  slash,   lbrc,   rbrc, dollar,
        'TAB',    'Q',    'W',    'F',    'P',    'B',            'J',    'L',     Ü ,    'Y',   bang,   bsls,
      CTL_ESC,     Ä ,    'R',    'S',    'T',    'G',            'M',    'N',    'E',    'I',     Ö , 'QUOT',
       'LSFT',    'Z',    'X',    'C',    'D',    'V',            'K',    'H',  comma,    dot,XXXXXXX, 'RSFT',
                     KC.MO(1), 'LOPT', 'LCMD',   RETURN,    'SPACE',   'RCMD', 'ROPT',KC.MO(2),
    ],
    [
      _______,_______,_______,_______,_______,_______,        _______,_______,_______,_______,_______,_______,
      _______,_______,_______,_______,_______,_______,        _______,  KC.N7,  KC.N8,  KC.N9,_______,_______,
      _______,_______,_______,_______,_______,_______,        _______,  KC.N4,  KC.N5,  KC.N6,_______,_______,
      _______,_______,_______,_______,_______,_______,        _______,  KC.N1,  KC.N2,  KC.N3,_______,_______,
                      _______,_______,_______,  _______,    _______,    KC.N0, KC.DOT,_______,
    ],
    [
      _______,_______,_______,_______,_______,_______,        _______,_______,_______,_______,_______,_______,
      _______,_______,_______,_______,_______,_______,        _______,_______,  KC.UP,_______,_______,_______,
      _______,_______,_______,_______,_______,_______,        _______,KC.LEFT,KC.DOWN,KC.RGHT,_______,_______,
      _______,_______,_______,_______,_______,_______,        _______,_______,_______,_______,_______,_______,
                      _______,_______,_______,  _______,    _______,  _______,_______,_______,
    ]
]


if __name__ == '__main__':
    keyboard.go()
