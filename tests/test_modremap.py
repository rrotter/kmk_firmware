import unittest

from kmk.keys import KC, Key  # , ModifierKey, make_key
from tests.keyboard_test import KeyboardTest
from kmk.modules.modremap import ModRemap, ModRemapMeta

debug = False
# debug = True
keyboard = None


def setUpModule():
    global debug
    global keyboard

    keyboard = KeyboardTest(
        [ModRemap()],
        [
            [
                KC.LU(KC.DOLLAR, KC.PERCENT),
                KC.LSFT,
                KC.LU(KC.AT, KC.N2),
                KC.S,
                KC.LUAUA(KC.A, KC.B, KC.C, KC.D),
                KC.LUAUA(
                    KC.HASH, KC.AT, KC.RALT(KC.N3), KC.RALT(KC.N3), KC.RALT(KC.AT)
                ),
                KC.RSFT,
                KC.ROPT,
                KC.LOPT,
            ]
        ],
        keyboard_debug_enabled=debug,
        debug_enabled=debug,
    )


class TestModRemap(unittest.TestCase):
    def test_make_keycode(self):
        my_keycode = KC.LU(KC.N4, KC.N5)
        assert isinstance(my_keycode, Key)
        assert isinstance(my_keycode.meta, ModRemapMeta)

    def test_mr_keycode_no_mods(self):
        keyboard.test(
            'press mr key without mods',
            [(0, True), (0, False)],
            [
                {
                    KC.N4,
                    KC.LSFT,
                },
                {},
            ],
        )

    def test_mr_keycode_with_shift(self):
        keyboard.test(
            'press mr key with shift',
            [(1, True), (0, True), (0, False), (1, False)],
            [
                {
                    KC.LSFT,
                },
                {
                    KC.N5,
                    KC.LSFT,
                },
                {
                    KC.LSFT,
                },
                {},
            ],
        )

    def test_shift_reversal_no_mods(self):
        keyboard.test(
            'press mr key without mods',
            [(2, True), (2, False)],
            [
                {
                    KC.N2,
                    KC.LSFT,
                },
                {},
            ],
        )

    def test_shift_reversal_with_shift(self):
        keyboard.test(
            'press mr key with shift',
            [(1, True), (2, True), (2, False), (1, False)],
            [
                {
                    KC.LSFT,
                },
                {
                    KC.N2,
                },
                {
                    KC.LSFT,
                },
                {},
            ],
        )

    def test_lift_shift_while_holding_mr(self):
        keyboard.test(
            'lift shift while holding, triggers "unshifted" key',
            [(1, True), (0, True), (1, False), (0, False)],
            [
                {
                    KC.LSFT,
                },
                {
                    KC.N5,
                    KC.LSFT,
                },
                {
                    KC.N4,
                    KC.LSFT,
                },
                {},
            ],
        )

    def test_basic_keys_still_work(self):
        keyboard.test(
            'test that basic keys still work',
            [
                (3, True),
                (3, False),
                (0, True),
                (0, False),
                (0, True),
                (3, True),
                (3, False),
                (0, False),
            ],
            [
                {
                    KC.S,
                },
                {},
                {
                    KC.N4,
                    KC.LSFT,
                },
                {},
                {
                    KC.N4,
                    KC.LSFT,
                },
                {
                    KC.S,
                },
                {},
            ],
        )

    def test_luaua_simple(self):
        keyboard.test(
            'test luaua with simple keys',
            [(4, True), (4, False), (6, True), (4, True), (6, False), (4, False)],
            [
                {
                    KC.A,
                },
                {},
                {
                    KC.RSFT
                },
                {
                    KC.B
                },
                {
                    KC.A
                },
                {},
            ],
        )

    # def test_luaua_simple(self):

if __name__ == '__main__':
    unittest.main()
