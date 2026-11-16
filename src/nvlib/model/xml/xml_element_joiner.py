"""Provide a class to join consecutive xml elements of the same kind.

Copyright (c) 2026 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from xml import sax


class XmlElementJoiner(sax.ContentHandler):

    def __init__(self):
        super().__init__()
        self._spanEndPending = None
        self._currentSpan = None
        self._xmlOutput = []

    def join_consecutive_formatting(self, xmlText):
        for tag in(
            'em',
            'strong',
            'em',
        ):
            xmlText = xmlText.replace(f'</{tag}><{tag}>', '')
        return xmlText

    def join_consecutive_spans(self, xmlText):
        self._xmlOutput.clear()
        self._spanEndPending = False
        self._currentSpan = ''
        sax.parseString(f'<content>{xmlText}</content>', self)
        return ''.join(self._xmlOutput[1:-1])

    def characters(self, content):
        self._end_span()
        self._xmlOutput.append(sax.saxutils.escape(content))

    def endElement(self, name):
        if name == 'span':
            self._spanEndPending = True
            return

        self._end_span()
        self._xmlOutput.append(f'</{name}>')

    def startElement(self, name, attrs):
        attributes = "".join([
            f' {attrKey}="{attrValue}"'
            for attrKey, attrValue in attrs.items()
        ])
        tag = f'<{name}{attributes}>'
        if name == 'span':
            if self._spanEndPending:
                self._spanEndPending = False
                if tag == self._currentSpan:
                    return

                self._xmlOutput.append('</span>')
            self._currentSpan = tag
        else:
            self._end_span()
        self._xmlOutput.append(tag)

    def _end_span(self):
        if self._spanEndPending:
            self._spanEndPending = False
            self._xmlOutput.append('</span>')
