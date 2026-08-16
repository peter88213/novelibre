"""Provide a class with color helper methods.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class HexColor:

    @classmethod
    def get_luminance(cls, hexColor):
        # The algorithm is suggested by Filip Němeček
        # https://nemecek.be/blog/172/how-to-calculate-contrast-color-in-python
        color = hexColor[1:]
        hexRed = int(color[0:2], base=16)
        hexGreen = int(color[2:4], base=16)
        hexBlue = int(color[4:6], base=16)
        return hexRed * 0.2126 + hexGreen * 0.7152 + hexBlue * 0.0722

    @classmethod
    def is_dark(cls, hexColor):
        if cls.is_hex_color(hexColor):
            return cls.get_luminance(hexColor) < 140

        return None

    @classmethod
    def is_hex_color(cls, s):
        try:
            if len(s) == 7 and s.startswith('#'):
                return all(c in '0123456789abcdefABCDEF' for c in s[1:])

        except:
            return False

