"""Provide a class for parsing ODT documents.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml import sax
import zipfile

from nvlib.model.odf.odf_file import OdfFile
from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class OdtParser(sax.ContentHandler):
    """An ODT document parser, using the html.parser.HTMLParser API."""

    def __init__(self, client):
        super().__init__()

        self._emTags = ['Emphasis']
        # Collection of "emphasis" styles used in the ODT document.

        self._strongTags = ['Strong_20_Emphasis']
        # Collection of "strong emphasis" styles used in the ODT document.

        self._blockquoteTags = ['Quotations']
        # Collection of "blockquote" paragraph styles
        # used in the ODT document.

        self._languageTags = {}
        # Collection of language tags used in the ODT document.

        self._headingTags = {}
        # Collection of heading style names used in the ODT document.

        self._heading = None
        # Transformed heading element.

        self._getData = False
        # If True, handle the characters.

        self._span = []
        # Stack of novx elements created from ODT spans.
        # Each entry is a list of novx element names
        # created from one ODT span.
        # For skipped spans, the list entry is None.

        self._paraSpan = []
        # Stack of additionsl spans created from ODT paragraph attributes.
        # Each list entry is the novx element name of the additional span.
        # If no additional span was created, the list entry is None.

        self._style = None
        # ODT style being processed.

        self._novelLocale = None
        # str: the document's global locale
        #      used for filtering redundant paragraph language assignments

        self._currentLocale = []
        # str: the current locale,
        #      used for filtering redundant inline language assignments

        self._client = client

    def feed_file(self, filePath):
        """Feed an ODT file to the parser.
        
        Positional arguments:
            filePath: str -- ODT document path.
        
        First unzip the ODT file located at self.filePath, 
        and get languageCode, countryCode, title, desc, and authorName,        
        Then call the sax parser for content.xml.
        """
        styles, meta, content = self._unzip_odt_file(filePath)
        self._read_styles_xml(styles, OdfFile.NAMESPACES)
        self._read_meta_xml(meta, OdfFile.NAMESPACES)
        sax.parseString(content, self)

    def characters(self, content):
        """Receive notification of character data.
        
        Overrides the xml.sax.ContentHandler method             
        """
        if self._getData:
            self._client.handle_data(sax.saxutils.escape(content))

    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method     
        """
        if name in ('text:p', 'text:h'):
            try:
                span = self._paraSpan.pop()
                if span is not None:
                    self._client.handle_endtag(span)
            except:
                pass
            self._getData = False
            if self._heading:
                self._client.handle_endtag(self._heading)
                self._heading = None
            else:
                self._client.handle_endtag('p')
            return

        if name == 'text:span':
            try:
                spans = self._span.pop()
                for span in reversed(spans):
                    if span is not None:
                        self._client.handle_endtag(span)
                        if span == 'lang':
                            self._currentLocale.pop()
                return

            except:
                return

        if name == 'text:section':
            self._client.handle_endtag('div')
            return

        if name == 'office:annotation':
            self._client.handle_endtag('comment')
            self._getData = True
            return

        if name == 'dc:creator':
            self._client.handle_endtag('creator')
            self._getData = False
            return

        if name == 'dc:date':
            self._client.handle_endtag('date')
            self._getData = False
            return

        if name == 'text:note':
            self._client.handle_endtag('note')
            self._getData = True
            return

        if name == 'text:note-citation':
            self._client.handle_endtag('note-citation')
            self._getData = False
            return

        if name == 'text:h':
            self._client.handle_endtag(self._heading)
            self._heading = None
            return

        if name == 'text:list-item':
            self._client.handle_endtag('li')
            return

        if name == 'text:list':
            self._client.handle_endtag('ul')
            return

        if name == 'style:style':
            self._style = None

    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method             
        """
        xmlAttributes = {}
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            xmlAttributes[attrKey] = attrValue
        style = xmlAttributes.get('text:style-name', '')

        if name in ('text:p', 'text:h'):
            self._getData = True
            self._currentLocale = [self._novelLocale]
            param = []
            if style in self._languageTags:
                self._currentLocale.append(self._languageTags[style])
                if self._currentLocale[-1] != self._novelLocale:
                    param.append(('xml:lang', self._currentLocale[-1]))
            if style in self._blockquoteTags:
                param.append(('style', 'quotations'))
                self._client.handle_starttag('p', param)
            elif style.startswith('Heading'):
                self._heading = f'h{style[-1]}'
                self._client.handle_starttag(self._heading, [()])
            elif style in self._headingTags:
                self._heading = self._headingTags[style]
                self._client.handle_starttag(self._heading, [()])
            else:
                if not param:
                    param = [()]
                self._client.handle_starttag('p', param)
            if style in self._strongTags:
                # Priority for "strong emphasis"
                self._paraSpan.append('strong')
                self._client.handle_starttag('strong', [()])
            elif style in self._emTags:
                self._paraSpan.append('em')
                self._client.handle_starttag('em', [()])
            else:
                self._paraSpan.append(None)
            return

        if name == 'text:span':
            spans = []
            if style in self._emTags:
                spans.append('em')
                self._client.handle_starttag('em', [()])
            elif style in self._strongTags:
                spans.append('strong')
                self._client.handle_starttag('strong', [()])
            if style in self._languageTags:
                if self._languageTags[style] != self._currentLocale[-1]:
                    spans.append('lang')
                    self._client.handle_starttag(
                        'lang',
                        [('lang', self._languageTags[style])]
                    )
                    self._currentLocale.append(self._languageTags[style])
            if not spans:
                spans.append(None)
            self._span.append(spans)
            return

        if name == 'text:section':
            self._client.handle_starttag(
                'div',
                [('id', xmlAttributes['text:name'])]
            )
            return

        if name == 'office:annotation':
            self._client.handle_starttag('comment', [()])
            self._getData = False
            return

        if name == 'dc:date':
            self._client.handle_starttag('date', [()])
            self._getData = True
            return

        if name == 'dc:creator':
            self._client.handle_starttag('creator', [()])
            self._getData = True
            return

        if name == 'text:note':
            self._client.handle_starttag(
                'note',
                [
                    (
                        'id',
                        xmlAttributes.get('text:id', '')
                    ),
                    (
                        'class',
                        xmlAttributes.get('text:note-class', '')
                    )
                ]
            )
            self._getData = False
            return

        if name == 'text:note-citation':
            self._client.handle_starttag('note-citation', [()])
            self._getData = True
            return

        if name == 'text:h':
            try:
                self._heading = f'h{xmlAttributes["text:outline-level"]}'
            except:
                self._heading = f'h{style[-1]}'
            self._client.handle_starttag(self._heading, [()])
            return

        if name == 'text:list-item':
            self._client.handle_starttag('li', [()])
            return

        if name == 'text:list':
            self._client.handle_starttag('ul', [()])
            return

        if name == 'style:style':
            self._style = xmlAttributes.get('style:name', None)
            styleName = xmlAttributes.get('style:parent-style-name', '')
            if styleName.startswith('Heading'):
                self._headingTags[self._style] = f'h{styleName[-1]}'
            elif styleName == 'Quotations':
                self._blockquoteTags.append(self._style)
            return

        if name == 'style:text-properties':

            if xmlAttributes.get('fo:font-style', None) == 'italic':
                self._emTags.append(self._style)

            if xmlAttributes.get('fo:font-weight', None) == 'bold':
                self._strongTags.append(self._style)

            if xmlAttributes.get('fo:language', False):
                languageCode = xmlAttributes['fo:language']
                countryCode = xmlAttributes['fo:country']
                if countryCode != 'none':
                    locale = f'{languageCode}-{countryCode}'
                else:
                    locale = languageCode
                self._languageTags[self._style] = locale
            return

        if name == 'text:s':
            self._client.handle_starttag('s', [()])

    def _read_meta_xml(self, meta, namespaces):
        # Pass title, description, and author from 'meta.xml'
        # to the client.
        if meta is None:
            return

        root = ET.fromstring(meta)
        meta = root.find('office:meta', namespaces)
        title = meta.find('dc:title', namespaces)
        if title is not None:
            if title.text:
                self._client.handle_starttag('title', [()])
                self._client.handle_data(title.text)
                self._client.handle_endtag('title')
        author = meta.find('meta:initial-creator', namespaces)
        if author is not None:
            if author.text:
                self._client.handle_starttag(
                    'meta',
                    [
                        ('', 'author'),
                        ('', author.text)
                    ]
                )
        desc = meta.find('dc:description', namespaces)
        if desc is not None:
            if desc.text:
                self._client.handle_starttag(
                    'meta',
                    [
                        ('', 'description'),
                        ('', desc.text),
                    ]
                )

    def _read_styles_xml(self, styles, namespaces):
        # Pass language and country from 'styles.xml'
        # to the client.
        root = ET.fromstring(styles)
        styles = root.find('office:styles', namespaces)
        for defaultStyle in styles.iterfind(
            'style:default-style',
            namespaces,
        ):
            if defaultStyle.get(
                f'{{{namespaces["style"]}}}family'
            ) == 'paragraph':
                textProperties = defaultStyle.find(
                    'style:text-properties',
                    namespaces,
                )
                languageCode = textProperties.get(
                    f'{{{namespaces["fo"]}}}language'
                )
                countryCode = textProperties.get(
                    f'{{{namespaces["fo"]}}}country'
                )
                self._novelLocale = f'{languageCode}-{countryCode}'
                self._client.handle_starttag(
                    'body',
                    [
                        ('language', languageCode),
                        ('country', countryCode),
                    ]
                )
                return

    def _unzip_odt_file(self, filePath):
        # Return three xml strings from from an ODS file
        # specified by filePath.
        try:
            with zipfile.ZipFile(filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
                styles = odfFile.read('styles.xml')
                try:
                    meta = odfFile.read('meta.xml')
                except KeyError:
                    # meta.xml may be missing in outlines
                    # created with e.g. FreeMind
                    meta = None
                return styles, meta, content

        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(filePath)}".')

