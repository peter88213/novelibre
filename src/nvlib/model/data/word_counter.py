"""Provide a strategy class for counting words.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re


class WordCounter:

    # Regular expressions for counting words and characters like in LibreOffice.
    # See:
    # https://help.libreoffice.org/latest/en-GB/text/swriter/guide/words_count.html
    ADDITIONAL_WORD_LIMITS = re.compile(r'--|—|–|\<\/p\>')
    # this is to be replaced by spaces when counting words

    NO_WORD_LIMITS = re.compile(
        r'\<note\>.*?\<\/note\>|\<comment\>.*?\<\/comment\>|\<.+?\>'
    )
    # this is to be replaced by empty strings when counting words

    def get_word_count(self, text):
        """Return the total word count of text as an integer."""
        text = self.ADDITIONAL_WORD_LIMITS.sub(' ', text)
        text = self.NO_WORD_LIMITS.sub('', text)
        return len(text.split())
