from kmk.keys import KC, make_key
import kmk.handlers.stock as handlers


OPT = {KC.LOPT, KC.ROPT}
SFT = {KC.LSFT, KC.RSFT}
CMD = {KC.LCMD, KC.RCMD}
CTL = {KC.LCTL, KC.RCTL}


class DeadKeyMeta:
    def __init__(self, deadkey):
        self.deadkey = deadkey


def deadkey_pressed(key, keyboard, *args, **kwargs):
    # Default action if OPT up. Default action if CMD or CTL down.
    if not keyboard.keys_pressed & OPT or keyboard.keys_pressed & CMD or keyboard.keys_pressed & CTL:
        keyboard.hid_pending = True
        keyboard.keys_pressed.add(key)
        return keyboard

    # deadkey up, if it's held
    for k in keyboard.keys_pressed:
        if k.code == key.meta.deadkey.code and k.__class__ == key.meta.deadkey.__class__:
            keyboard.keys_pressed.discard(k)
            keyboard._send_hid()

    oldkeys_pressed = keyboard.keys_pressed

    # deadkey won't work w/ shift pressed
    keyboard.keys_pressed = keyboard.keys_pressed - SFT

    keyboard.keys_pressed.add(key.meta.deadkey)
    keyboard._send_hid()
    # deadkey up
    keyboard.keys_pressed.discard(key.meta.deadkey)
    keyboard._send_hid()

    # base key won't work w/ option
    keyboard.keys_pressed = oldkeys_pressed - OPT

    keyboard.keys_pressed.add(key)
    keyboard._send_hid()

    # put key state back, add this one
    keyboard.keys_pressed = oldkeys_pressed
    keyboard.keys_pressed.add(key)

    return keyboard


def dead_key(prefix, key):
    return make_key(
        code=key.code,
        meta=DeadKeyMeta(prefix),
        on_press=deadkey_pressed,
        on_release=handlers.default_released,
    )

acute      = lambda key: dead_key(KC.E, key)
circumflex = lambda key: dead_key(KC.I, key)
grave      = lambda key: dead_key(KC.GRAVE, key)
tilde      = lambda key: dead_key(KC.N, key)
umlaut     = lambda key: dead_key(KC.U, key)
