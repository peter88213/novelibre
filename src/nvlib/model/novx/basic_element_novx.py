"""Provide a base class for novelibre element XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import xml.etree.ElementTree as ET


class BasicElementNovx:

    def import_data(self, element, xmlElement):
        element.title = self._get_element_text(xmlElement, 'Title')
        element.desc = self._xml_element_to_text(xmlElement.find('Desc'))
        element.links = self._get_link_dict(xmlElement)
        element.fields = self._get_fields(xmlElement)

    def export_data(self, element, xmlElement):
        if element.title:
            ET.SubElement(xmlElement, 'Title').text = element.title
        if element.desc:
            xmlElement.append(self._text_to_xml_element('Desc', element.desc))
        for path in element.links:
            xmlLink = ET.SubElement(xmlElement, 'Link')
            ET.SubElement(xmlLink, 'Path').text = path
            if element.links[path]:
                ET.SubElement(xmlLink, 'FullPath').text = element.links[path]
        for tag in element.fields:
            xmlField = ET.SubElement(xmlElement, 'Field')
            xmlField.set('tag', tag)
            xmlField.text = element.fields[tag]

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
        """Return an ElementTree element.

        The element is named "tag" and has paragraph subelements.
        
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
        """Return plain text.
        
        The text is converted from ElementTree paragraph subelements.
        
        Positional arguments:
            xmlElement -- ElementTree element.        
        
        Each <p> subelement of xmlElement creates a line. 
        Formatting is discarded.
        """
        lines = []
        if xmlElement is not None:
            for paragraph in xmlElement.iterfind('p'):
                lines.append(''.join(t for t in paragraph.itertext()))
        return '\n'.join(lines)

