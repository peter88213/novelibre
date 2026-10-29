"""Helper module for novx xml pretty printing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


def indent(elem, level=0):
    """xml pretty printer for the novx file format.
    
    Indent the xml tree up to the novx content paragraph level.
    Do not indent inline elements within paragraphs.

    Based on a code example by Fredrik Lundh. 
    """
    PARAGRAPH_LEVEL = 5

    i = f'\n{level * "  "}'
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = f'{i}  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        if level < PARAGRAPH_LEVEL:
            for elem in elem:
                indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
