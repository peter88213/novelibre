"""TDD support for a function cleaning cluttered HTML code.
"""

import re
import unittest

CLUTTERED = '''        <P CLASS="western"><A NAME="ScID:17"></A><A NAME="ScID:120"></A><!-- Climb up rope to safety. Back in ship for hyperspace. --><FONT COLOR="#000000"><SPAN STYLE="text-decoration: none"><FONT FACE="monospace"><FONT SIZE=3><SPAN STYLE="font-style: normal"><SPAN STYLE="font-weight: normal"><SPAN STYLE="background: #ffffff">And
        now for something </SPAN></SPAN></SPAN></FONT></FONT></SPAN></FONT><FONT COLOR="#000000"><SPAN STYLE="text-decoration: none"><FONT FACE="monospace"><FONT SIZE=3><I><SPAN STYLE="font-weight: normal"><SPAN STYLE="background: #ffffff">completely</SPAN></SPAN></I></FONT></FONT></SPAN></FONT><FONT COLOR="#000000"><SPAN STYLE="text-decoration: none"><FONT FACE="monospace"><FONT SIZE=3><SPAN STYLE="font-style: normal"><SPAN STYLE="font-weight: normal"><SPAN STYLE="background: #ffffff">
        different.</SPAN></SPAN></SPAN></FONT></FONT></SPAN></FONT></P>
'''
CLEANED = '<P CLASS="western"><A NAME="ScID:17"></A><A NAME="ScID:120"></A><!-- Climb up rope to safety. Back in ship for hyperspace. -->And now for something <I>completely</I> different.</P>'

CONVERTED = '<P CLASS="western"><A NAME="ScID:17"></A><A NAME="ScID:120"></A><!-- Climb up rope to safety. Back in ship for hyperspace. -->And now for something [i]completely[/i] different.</P>'

STRIPPED = '<P CLASS="western"><A NAME="ScID:17"></A><A NAME="ScID:120"></A><!-- Climb up rope to safety. Back in ship for hyperspace. -->And now for something completely different.</P>'


def clean(text):
    text = re.sub(r'</*font.*?>', '', text)
    text = re.sub(r'</*span.*?>', '', text)
    text = re.sub(r'</*FONT.*?>', '', text)
    text = re.sub(r'</*SPAN.*?>', '', text)
    text = text.replace('\n', ' ')

    while '  ' in text:
        text = text.replace('  ', ' ').strip()

    return text


def convert(text):
    text = text.replace('<i>', '[i]')
    text = text.replace('<I>', '[i]')
    text = text.replace('</i>', '[/i]')
    text = text.replace('</I>', '[/i]')
    text = text.replace('</em>', '[/i]')
    text = text.replace('</EM>', '[/i]')
    text = text.replace('<b>', '[b]')
    text = text.replace('<B>', '[b]')
    text = text.replace('</b>', '[/b]')
    text = text.replace('</B>', '[/b]')

    return text


def strip(text):
    text = text.replace('[i]', '')
    text = text.replace('[/i]', '')
    text = text.replace('[b]', '')
    text = text.replace('[/b]', '')
    return text


class Cleaner(unittest.TestCase):

    def test_cleaner(self):
        result = clean(CLUTTERED)
        # print(result)
        self.assertEqual(result, CLEANED)

    def test_converter(self):
        result = convert(CLEANED)
        # print(result)
        self.assertEqual(result, CONVERTED)

    def test_stripper(self):
        result = strip(CONVERTED)
        # print(result)
        self.assertEqual(result, STRIPPED)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
