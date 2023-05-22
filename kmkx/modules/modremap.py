from kmk.keys import KC, Key, ModifierKey, make_key
from kmk.modules import Module


CTL = {KC.LCTL, KC.RCTL}
SFT = {KC.LSFT, KC.RSFT}
ALT = {KC.LALT, KC.RALT}
GUI = {KC.LGUI, KC.RGUI}


class ModRemapMeta:
    def __init__(self, overrides=None):
        self.override_map = []

        for ovr in overrides:
            self.add_override(*ovr)


    def add_override(self, fn, key, hide_mods=None):
        self.override_map.append((fn, key, hide_mods))

        

class ModRemap(Module):
    def __init__(self):
        self.virtual_mods = set()
        self.last_pressed = KC.NO


    def set_keycode(self, key, keyboard):
        old_code = key.code

        # what mods are held down???
        ctl = self.virtual_mods & CTL
        sft = self.virtual_mods & SFT
        alt = self.virtual_mods & ALT
        gui = self.virtual_mods & GUI

        for ovr in key.meta.override_map:
            if ovr[0](c=ctl,s=sft,a=alt,g=gui):
                key.code = ovr[1].code
                key.has_modifiers = ovr[1].has_modifiers

                if ovr[2]:
                    keyboard.keys_pressed -= ovr[2]

                break

        # report whether we changed the keycode
        return old_code != key.code


    def process_key(self, keyboard, key, is_pressed, *args):
        # handle mod
        if isinstance(key, ModifierKey):
            # track state of physical mod keys
            if is_pressed:
                self.virtual_mods.add(key)
            else:
                self.virtual_mods.discard(key)

            # modify state for held ModRemap key
            if isinstance(self.last_pressed.meta, ModRemapMeta):
                keyboard.keys_pressed |= self.virtual_mods

                if not is_pressed:
                    keyboard.keys_pressed.discard(key)

                if self.set_keycode(self.last_pressed, keyboard):
                    # release it if it will produce erronious keypress
                    self.release(self.last_pressed, keyboard)

                # send report and block remaining handlers
                keyboard._send_hid()
                return

        # clear any held modremap keys when we get another keypress
        elif is_pressed:
            self.release_all(keyboard)
            self.last_pressed = key

        return key


    def release_all(self, keyboard):

        for key in keyboard.keys_pressed:
            if isinstance(key.meta, ModRemapMeta):
                keyboard.keys_pressed.discard(key)

        keyboard.keys_pressed |= self.virtual_mods


    def press(self, key, keyboard, *args, **kwargs):

        self.set_keycode(key, keyboard)

        keyboard.hid_pending = True

        keyboard.keys_pressed.add(key)

        return keyboard


    def release(self, key, keyboard, *args, **kwargs):
        
        keyboard.hid_pending = True

        keyboard.keys_pressed.discard(key)
        if self.last_pressed == key:
            self.last_pressed = KC.NO

        keyboard.keys_pressed |= self.virtual_mods

        return keyboard


    # xxxx
    def noop(self, keyboard):
        return
    
    during_bootup = before_matrix_scan = after_matrix_scan = noop
    before_hid_send = after_hid_send = noop
    on_powersave_enable = on_powersave_disable = noop

