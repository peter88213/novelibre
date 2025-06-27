"""Provide a base class for novelibre element representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import xml.etree.ElementTree as ET


class BasicElement:
    """Basic data model element representation.

    Public instance variables:
        on_element_change -- Points to a callback routine for element changes
        
    The on_element_change method is called when the value of any property changes.
    This method can be overridden at runtime for each individual element instance.
    """

    def __init__(
        self,
        on_element_change=None,
        title=None,
        desc=None,
        links=None
    ):
        """Set the initial values.

        If on_element_change is None, the do_nothing method will be assigned to it.
            
        General note:
        When merging files, only new elements that are not None will override 
        existing elements. This allows you to easily update a novelibre project 
        from a document that contains only a subset of the data model.
        Keep this in mind when setting the initial values.
        """
        if on_element_change is None:
            self.on_element_change = self.do_nothing
        else:
            self.on_element_change = on_element_change
        self._title = title
        self._desc = desc
        if links is None:
            self._links = {}
        else:
            self._links = links
        self._fields = {}

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._title != newVal:
            self._title = newVal
            self.on_element_change()

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._desc != newVal:
            self._desc = newVal
            self.on_element_change()

    @property
    def links(self):
        # dict: (Key:str -- relative path, value:str -- full path)
        try:
            return self._links.copy()
        except AttributeError:
            return None

    @links.setter
    def links(self, newVal):
        if newVal is not None:
            for elem in newVal:
                val = newVal[elem]
                if val is not None:
                    assert type(val) is str
        if self._links != newVal:
            self._links = newVal
            self.on_element_change()

    @property
    def fields(self):
        return self._fields.copy()

    @fields.setter
    def fields(self, newVal):
        if self._fields != newVal:
            self._fields = newVal
            self.on_element_change()

    def do_nothing(self):
        """Standard callback routine for element changes."""
        pass

    def from_xml(self, xmlElement):
        self.title = self._get_element_text(xmlElement, 'Title')
        self.desc = self._xml_element_to_text(xmlElement.find('Desc'))
        self.links = self._get_link_dict(xmlElement)
        self.fields = self._get_fields(xmlElement)

    def to_xml(self, xmlElement):
        if self.title:
            ET.SubElement(xmlElement, 'Title').text = self.title
        if self.desc:
            xmlElement.append(self._text_to_xml_element('Desc', self.desc))
        for path in self.links:
            xmlLink = ET.SubElement(xmlElement, 'Link')
            ET.SubElement(xmlLink, 'Path').text = path
            if self.links[path]:
                ET.SubElement(xmlLink, 'FullPath').text = self.links[path]
        for tag in self.fields:
            xmlField = ET.SubElement(xmlElement, 'Field')
            xmlField.set('tag', tag)
            xmlField.text = self.fields[tag]

    def _get_element_text(self, xmlElement, tag, default=None):
        """Return the text field of an XML element.
        
        If the element doesn't exist, return default.
        """
        if xmlElement.find(tag) is not None:
            return xmlElement.find(tag).text
        else:
            return default

    def _get_fields(self, xmlElement):
        fields = {}
        for xmlField in xmlElement.iterfind('Field'):
            tag = xmlField.get('tag', None)
            if tag is not None:
                fields[tag] = xmlField.text
        return fields

    def _get_link_dict(self, xmlElement):
        """Return a dictionary of links.
        
        If the element doesn't exist, return an empty dictionary.
        """
        links = {}
        for xmlLink in xmlElement.iterfind('Link'):
            xmlPath = xmlLink.find('Path')
            if xmlPath is not None:
                path = xmlPath.text
                xmlFullPath = xmlLink.find('FullPath')
                if xmlFullPath is not None:
                    fullPath = xmlFullPath.text
                else:
                    fullPath = None
            else:
                # Read deprecated attributes from DTD 1.3.
                path = xmlLink.attrib.get('path', None)
                fullPath = xmlLink.attrib.get('fullPath', None)
            if path:
                links[path] = fullPath
        return links

    def _text_to_xml_element(self, tag, text):
        """Return an ElementTree element named "tag" with paragraph subelements.
        
        Positional arguments:
        tag: str -- Name of the XML element to return.    
        text -- string to convert.
        """
        xmlElement = ET.Element(tag)
        if text:
            for line in text.split('\n'):
                ET.SubElement(xmlElement, 'p').text = line
        return xmlElement

    def _xml_element_to_text(self, xmlElement):
        """Return plain text, converted from ElementTree paragraph subelements.
        
        Positional arguments:
            xmlElement -- ElementTree element.        
        
        Each <p> subelement of xmlElement creates a line. Formatting is discarded.
        """
        lines = []
        if xmlElement is not None:
            for paragraph in xmlElement.iterfind('p'):
                lines.append(''.join(t for t in paragraph.itertext()))
        return '\n'.join(lines)

