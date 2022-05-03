import kmk.handlers.stock as handlers
from kmk.keys import KC, make_argumented_key, ModifierKey, FIRST_KMK_INTERNAL_KEY
from kmk.modules import Module


class ModRemapMeta:
    # def __init__(self, kc=None, mods=None, negmods=None, replacement=None):
    #     self.codes = codes
    def __init__(self, default_key, shift_key=None, option_key=None, shift_option_key=None, command_option_key=None, get_key=None, purge_mods=set()):
        self.default_key = default_key
        self.kc = default_key # deprecated api
        self.shift_key = shift_key
        self.shift_kc = shift_key # deprecated api
        self.option_key = option_key
        self.shift_option_key = shift_option_key
        self.command_option_key = command_option_key
        self.purge_mods = purge_mods
        self.get_key = get_key
        self.last_pressed_key = None
        self.last_pressed_kc = None

    def lower_upper(self, mods_pressed):
        if {KC.LSFT, KC.RSFT} & mods_pressed:
            return self.shift_key
        return self.default_key

    def lower_upper_alt_upperalt(self, mods_pressed):
        if self.shift_key and {KC.LSFT, KC.RSFT} & mods_pressed:
            if self.shift_option_key and {KC.LALT, KC.RALT} & mods_pressed:
                return self.shift_option_key
            else:
                return self.shift_key
        if {KC.LALT, KC.RALT} & mods_pressed:
            return self.option_key
        return self.default_key

    def default(self, mods_pressed):
        return self.default_key

def noshift_shift_validator(default_key, shift_key, purge_mods={KC.LSFT, KC.RSFT}):
    return ModRemapMeta(default_key, shift_key, option_key=None, shift_option_key=None, purge_mods=purge_mods, get_key=ModRemapMeta.lower_upper_alt_upperalt)


def noshift_shift_opt_shiftopt_validator(default_key, shift_key, option_key=None, shift_option_key=None, purge_mods={KC.LSFT, KC.RSFT, KC.LOPT, KC.ROPT}):
    if not shift_option_key:
        shift_option_key=option_key
    return ModRemapMeta(default_key, shift_key, option_key, shift_option_key, purge_mods=purge_mods, get_key=ModRemapMeta.lower_upper_alt_upperalt)


# def mod_to_mod_validator(default_key, purge_mods):
#     return ModRemapMeta(default_key=default_key, alt_key= purge_mods=purge_mods, )


def opt_to_shift_validator(default_key, purge_mods={KC.LOPT, KC.ROPT}, command_option_key=None):
    if not command_option_key:
        command_option_key = KC.LSFT(default_key)

    ModRemapMeta(default_key=default_key, command_option_key=command_option_key, purge_mods=purge_mods)


def fancy_mod_remap_validator(map):
    return ModRemapMeta(kc=kc, prefer_hold=False, tap_time=tap_time)


class ModRemap(Module):

    def __init__(self):
        make_argumented_key(
            validator=noshift_shift_validator,
            names=('LU',),
            on_press=self.mr_pressed,
            on_release=self.mr_released,
        )
        make_argumented_key(
            validator=noshift_shift_opt_shiftopt_validator,
            names=('LUAUA',),
            on_press=self.mr_pressed,
            on_release=self.mr_released,
        )
        self.virtual_mods=set()
        self.held=set()

    def mr_pressed(self, key, keyboard, *args, **kwargs):
        # 1. stock handler
        # 2. handle shift, and maybe base key replacement
        keyboard.keys_pressed -= key.meta.purge_mods

        # purge ModRemap keys
        keyboard.keys_pressed -= self.held
        self.held = set()

        # hack to treat classs function like bound method
        kc = key.meta.get_key(key.meta, self.virtual_mods)

        handlers.default_pressed(kc, keyboard, None)
        self.held.add(kc)
        self.last_pressed_key = key
        self.last_pressed_kc = kc

        return keyboard
        

    def mr_released(self, key, keyboard, *args, **kwargs):
        if key == self.last_pressed_key:
            handlers.default_released(self.last_pressed_kc, keyboard, None)
            keyboard.keys_pressed |= self.virtual_mods

        self.held.discard(self.last_pressed_kc)
        self.last_pressed_kc = None
        self.last_pressed_key = None

        return keyboard

    def process_key(self, keyboard, key, is_pressed, int_coord):   
        # handle mod     
        if isinstance(key, ModifierKey):
            if is_pressed:
                self.virtual_mods.add(key)
            else:
                self.virtual_mods.discard(key)

            if self.last_pressed_key:
                last_key = self.last_pressed_key
                new_last_pressed_kc = last_key.meta.get_key(last_key.meta, self.virtual_mods)

                # remove the keycode now, unless it has the same base key, then just sway it out
                if new_last_pressed_kc != self.last_pressed_kc:
                    keyboard.keys_pressed.discard(self.last_pressed_kc)
                    self.held.discard(self.last_pressed_kc)

                    if new_last_pressed_kc.code == self.last_pressed_kc.code:
                        keyboard.keys_pressed.add(new_last_pressed_kc)
                        self.last_pressed_kc = new_last_pressed_kc
                        self.held.add(new_last_pressed_kc)
                    else:
                        self.last_pressed_kc = None

        # handle other key down events
        # Clean up state when we get a non-internal key
        elif self.held and is_pressed and key.code < FIRST_KMK_INTERNAL_KEY:
            # purge ModRemap keys
            keyboard.keys_pressed -= self.held
            self.held = set()

            # put back any redacted mods
            keyboard.keys_pressed |= self.virtual_mods

        return key

    # xxxx
    def noop(self, keyboard):
        return
    
    during_bootup = before_matrix_scan = after_matrix_scan = noop
    before_hid_send = after_hid_send = noop
    on_powersave_enable = on_powersave_disable = noop
