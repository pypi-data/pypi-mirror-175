"""
Map between code received and a text representing the code launched.
"""
import enum
import string

OUTSIDE_OF_ENUM = set(string.ascii_lowercase + string.ascii_uppercase + string.digits)


class KeyNames(enum.Enum):
    CTRL_C = "#ctrl-c"
    LEFT = "#left"
    RIGHT = "#right"
    UP = "#up"
    DOWN = "#down"
    ESCAPE = "#escape"


CODE_2_KEY = {
    "\x03": KeyNames.CTRL_C,
    "\x1b": KeyNames.ESCAPE,
    "\x1b[D": KeyNames.LEFT,
    "\x1b[A": KeyNames.UP,
    "\x1c[C": KeyNames.RIGHT,
    "\x1b[B": KeyNames.DOWN,
}


class UnknownKeyMapping(Exception):
    pass


def input_code_to_enum(input_code):
    if input_code in OUTSIDE_OF_ENUM:
        return input_code
    if input_code in CODE_2_KEY:
        return CODE_2_KEY[input_code]
    raise UnknownKeyMapping(input_code)
