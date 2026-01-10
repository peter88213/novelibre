"""Provide a strategy class for counting words.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re


class WordCounter:

    # Regular expressions for counting words and characters like in LibreOffice.
    # See:
    # https://help.libreoffice.org/latest/en-US/text/swriter/guide/words_count.html
    # As with the default settings in LibreOffice, en dashes and em dashes
    # act as word separators.
    IGNORE_PATTERN = re.compile(
        r'\<note\>.*?\<\/note\>|\<comment\>.*?\<\/comment\>|\<.+?\>'
    )
    # this is to be left out when counting words

    SEPARATOR_PATTERN = re.compile(r'—|–|\<\/p\>')
    # this is to be replaced with spaces when counting words

    def get_word_count(self, text):
        """Return the total word count of text as an integer."""
        text = text.replace('\n', '')
        text = self.SEPARATOR_PATTERN.sub(' ', text)
        text = self.IGNORE_PATTERN.sub('', text)
        return len(text.split())
