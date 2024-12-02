"""Provide an XML item data file reader class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.novx_file import NovxFile
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class PlotLineReader(NovxFile):
    """XML iplot line file reader."""
    DESCRIPTION = _('XML plot line file')
    EXTENSION = '.xml'

    def read(self):
        """Parse the xml files and get the instance variables.
        
        Overrides the superclass method.
        """
        self._references = [
            'Sections',
            'Section',
        ]
        tree = ET.parse(self.filePath)
        root = ET.Element('ROOT')
        root.append(tree.getroot())
        xmlPlotLines = root.find('ARCS')
        if xmlPlotLines is not None:
            for xmlPlotLine in xmlPlotLines.iterfind('ARC'):
                self._remove_references(xmlPlotLine)
                for xmlPlotPoint in xmlPlotLine.iterfind('POINT'):
                    self._remove_references(xmlPlotPoint)
        self._read_plot_lines_and_points(root)

    def _remove_references(self, xmlElement):
        for ref in self._references:
            for xmlRef in xmlElement.findall(ref):
                xmlElement.remove(xmlRef)
