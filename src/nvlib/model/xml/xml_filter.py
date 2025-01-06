"""Helper module for removing illegal xml characters.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re


def strip_illegal_characters(text):
    return re.sub('[\x00-\x08|\x0b-\x0c|\x0e-\x1f]', '', text)

