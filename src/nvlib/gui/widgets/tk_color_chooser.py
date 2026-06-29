"""Provide a class to choose a color.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from tkinter import colorchooser


class TkColorChooser:

    def choose_color(self, title='', initialcolor=None):
        color = colorchooser.askcolor(
            title=title,
            color=initialcolor,
        )
        if color is None:
            return None

        return color[1]
