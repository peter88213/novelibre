"""Provide a class for novx file import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import os

from nvlib.model.data.basic_element import BasicElement
from nvlib.model.data.chapter import Chapter
from nvlib.model.data.character import Character
from nvlib.model.data.plot_line import PlotLine
from nvlib.model.data.plot_point import PlotPoint
from nvlib.model.data.section import Section
from nvlib.model.data.world_element import WorldElement
from nvlib.model.file.file import File
from nvlib.model.xml.xml_filter import strip_illegal_characters
from nvlib.model.xml.xml_indent import indent
from nvlib.model.xml.xml_open import get_xml_root
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import Error
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import intersection
from nvlib.novx_globals import norm_path
from nvlib.novx_globals import verified_int_string
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class NovxFile(File):
    """novx file representation.

    Public instance variables:
        xmlTree -- xml element tree of the novelibre project
        wcLog: dict[str, list[str, str]] -- Daily word count logs.
        wcLogUpdate: dict[str, list[str, str]] -- Word counts missing in the log.
        timestamp: float -- Time of last file modification (number of seconds since the epoch).
    
    
    """
    DESCRIPTION = _('novelibre project')
    EXTENSION = '.novx'

    MAJOR_VERSION = 1
    MINOR_VERSION = 6
    # DTD version;
    # compatible, if the file's major version number equals MAJOR_VERSION,
    # and the minor version number is equal or less than MINOR_VERSION

    XML_HEADER = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE novx SYSTEM "novx_{MAJOR_VERSION}_{MINOR_VERSION}.dtd">
<?xml-stylesheet href="novx.css" type="text/css"?>
'''

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the novx file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.on_element_change = None
        self.xmlTree = None

        self.wcLog = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.wcLogUpdate = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.timestamp = None

    def adjust_section_types(self):
        """Make sure that nodes with "Unused" parents inherit the type."""
        partType = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chLevel == 1:
                partType = self.novel.chapters[chId].chType
            elif partType != 0 and not self.novel.chapters[chId].isTrash:
                self.novel.chapters[chId].chType = partType
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType < self.novel.chapters[chId].chType:
                    self.novel.sections[scId].scType = self.novel.chapters[chId].chType

    def count_words(self):
        """Return a tuple of word count totals.
        
        count: int -- Total words of "normal" type sections.
        totalCount: int -- Total words of "normal" and "unused" sections.
        """
        count = 0
        totalCount = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if not self.novel.chapters[chId].isTrash:
                for scId in self.novel.tree.get_children(chId):
                    if self.novel.sections[scId].scType < 2:
                        totalCount += self.novel.sections[scId].wordCount
                        if self.novel.sections[scId].scType == 0:
                            count += self.novel.sections[scId].wordCount
        return count, totalCount

    def read(self):
        """Read and parse the novx file.
        
        Overrides the superclass method.
        """
        xmlRoot = get_xml_root(self.filePath)
        self._check_version(xmlRoot)
        try:
            locale = xmlRoot.attrib['{http://www.w3.org/XML/1998/namespace}lang']
            self.novel.languageCode, self.novel.countryCode = locale.split('-')
        except:
            pass
        self.novel.tree.reset()
        try:
            self._read_project(xmlRoot)
            self._read_locations(xmlRoot)
            self._read_items(xmlRoot)
            self._read_characters(xmlRoot)
            self._read_chapters_and_sections(xmlRoot)
            self._read_plot_lines_and_points(xmlRoot)
            self._read_project_notes(xmlRoot)
            self.adjust_section_types()
            self._read_word_count_log(xmlRoot)
        except Exception as ex:
            raise Error(f"{_('Corrupt project data')} ({str(ex)})")
        self._get_timestamp()
        self._keep_word_count()

    def write(self):
        """Build the xml tree and write the novx file.
        
        Overrides the superclass method.
        """
        self._update_word_count_log()
        self.adjust_section_types()
        self.novel.get_languages()

        attrib = {
            'version':f'{self.MAJOR_VERSION}.{self.MINOR_VERSION}',
            'xml:lang':f'{self.novel.languageCode}-{self.novel.countryCode}',
        }
        xmlRoot = ET.Element('novx', attrib=attrib)
        self._build_project(xmlRoot)
        self._build_chapters_and_sections(xmlRoot)
        self._build_characters(xmlRoot)
        self._build_locations(xmlRoot)
        self._build_items(xmlRoot)
        self._build_plot_lines_and_points(xmlRoot)
        self._build_project_notes(xmlRoot)
        self._build_word_count_log(xmlRoot)

        indent(xmlRoot)
        # using a custom routine, making sure not to indent inline elements within paragraphs

        self.xmlTree = ET.ElementTree(xmlRoot)
        self._write_element_tree(self)
        self._postprocess_xml_file(self.filePath)
        self._get_timestamp()

    def _build_project(self, root):
        xmlProject = ET.SubElement(root, 'PROJECT')
        self.novel.to_xml(xmlProject)

    def _build_chapters_and_sections(self, root):
        xmlChapters = ET.SubElement(root, 'CHAPTERS')
        for chId in self.novel.tree.get_children(CH_ROOT):
            xmlChapter = ET.SubElement(xmlChapters, 'CHAPTER', attrib={'id':chId})
            self.novel.chapters[chId].to_xml(xmlChapter)
            for scId in self.novel.tree.get_children(chId):
                self.novel.sections[scId].to_xml(ET.SubElement(xmlChapter, 'SECTION', attrib={'id':scId}))

    def _build_characters(self, root):
        xmlCharacters = ET.SubElement(root, 'CHARACTERS')
        for crId in self.novel.tree.get_children(CR_ROOT):
            self.novel.characters[crId].to_xml(ET.SubElement(xmlCharacters, 'CHARACTER', attrib={'id':crId}))

    def _build_locations(self, root):
        xmlLocations = ET.SubElement(root, 'LOCATIONS')
        for lcId in self.novel.tree.get_children(LC_ROOT):
            self.novel.locations[lcId].to_xml(ET.SubElement(xmlLocations, 'LOCATION', attrib={'id':lcId}))

    def _build_items(self, root):
        xmlItems = ET.SubElement(root, 'ITEMS')
        for itId in self.novel.tree.get_children(IT_ROOT):
            self.novel.items[itId].to_xml(ET.SubElement(xmlItems, 'ITEM', attrib={'id':itId}))

    def _build_plot_lines_and_points(self, root):
        xmlPlotLines = ET.SubElement(root, 'ARCS')
        for plId in self.novel.tree.get_children(PL_ROOT):
            xmlPlotLine = ET.SubElement(xmlPlotLines, 'ARC', attrib={'id':plId})
            self.novel.plotLines[plId].to_xml(xmlPlotLine)
            for ppId in self.novel.tree.get_children(plId):
                self.novel.plotPoints[ppId].to_xml(ET.SubElement(xmlPlotLine, 'POINT', attrib={'id':ppId}))

    def _build_project_notes(self, root):
        xmlProjectNotes = ET.SubElement(root, 'PROJECTNOTES')
        for pnId in self.novel.tree.get_children(PN_ROOT):
            self.novel.projectNotes[pnId].to_xml(ET.SubElement(xmlProjectNotes, 'PROJECTNOTE', attrib={'id':pnId}))

    def _build_word_count_log(self, root):
        if not self.wcLog:
            return

        xmlWcLog = ET.SubElement(root, 'PROGRESS')
        wcLastCount = None
        wcLastTotalCount = None
        for wc in self.wcLog:
            wcCount, wcTotalCount = self.wcLog[wc]
            if self.novel.saveWordCount:
                # Skip entries with unchanged word count.
                if wcCount == wcLastCount and wcTotalCount == wcLastTotalCount:
                    continue

                wcLastCount = wcCount
                wcLastTotalCount = wcTotalCount
            xmlWc = ET.SubElement(xmlWcLog, 'WC')
            ET.SubElement(xmlWc, 'Date').text = wc
            ET.SubElement(xmlWc, 'Count').text = wcCount
            ET.SubElement(xmlWc, 'WithUnused').text = wcTotalCount

    def _check_id(self, elemId, elemPrefix):
        """Raise an exception if elemId does not start with the correct prefix."""
        if not elemId.startswith(elemPrefix):
            raise Error(f"bad ID: '{elemId}'")

    def _check_version(self, xmlRoot):
        """Raise an exception if the xmlRoot element is not compatible with the supported DTD."""
        if xmlRoot.tag != 'novx':
            raise Error(f'{_("No valid xml root element found in file")}: "{norm_path(self.filePath)}".')
        try:
            majorVersionStr, minorVersionStr = xmlRoot.attrib['version'].split('.')
            majorVersion = int(majorVersionStr)
            minorVersion = int(minorVersionStr)
        except:
            raise Error(f'{_("No valid version found in file")}: "{norm_path(self.filePath)}".')
        if majorVersion > self.MAJOR_VERSION:
            raise Error(_('The project "{}" was created with a newer novelibre version.').format(norm_path(self.filePath)))
        elif majorVersion < self.MAJOR_VERSION:
            raise Error(_('The project "{}" was created with an outdated novelibre version.').format(norm_path(self.filePath)))
        elif minorVersion > self.MINOR_VERSION:
            raise Error(_('The project "{}" was created with a newer novelibre version.').format(norm_path(self.filePath)))

    def _get_timestamp(self):
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None

    def _keep_word_count(self):
        """Keep the actual wordcount, if not logged."""
        if not self.wcLog:
            return

        actualCountInt, actualTotalCountInt = self.count_words()
        actualCount = str(actualCountInt)
        actualTotalCount = str(actualTotalCountInt)
        latestDate = list(self.wcLog)[-1]
        latestCount = self.wcLog[latestDate][0]
        latestTotalCount = self.wcLog[latestDate][1]
        if actualCount != latestCount or actualTotalCount != latestTotalCount:
            try:
                fileDateIso = date.fromtimestamp(self.timestamp).isoformat()
            except:
                fileDateIso = date.today().isoformat()
            self.wcLogUpdate[fileDateIso] = [actualCount, actualTotalCount]

    def _postprocess_xml_file(self, filePath):
        """Postprocess an xml file created by ElementTree.
        
        Positional argument:
            filePath: str -- path to xml file.
        
        Read the xml file and put a header on top. 
        Overwrite the .novx xml file.
        Raise the "Error" exception in case of error. 
        
        Note: The path is given as an argument rather than using self.filePath. 
        So this routine can be used for novelibre-generated xml files other than .novx as well. 
        """
        with open(filePath, 'r', encoding='utf-8') as f:
            text = f.read()
            text = strip_illegal_characters(text)
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(f'{self.XML_HEADER}{text}')
        except:
            raise Error(f'{_("Cannot write file")}: "{norm_path(filePath)}".')

    def _read_chapters_and_sections(self, root):
        """Read data at chapter level from the xml element tree."""
        xmlChapters = root.find('CHAPTERS')
        if xmlChapters is None:
            return

        for xmlChapter in xmlChapters.iterfind('CHAPTER'):
            chId = xmlChapter.attrib['id']
            self._check_id(chId, CHAPTER_PREFIX)
            self.novel.chapters[chId] = Chapter(on_element_change=self.on_element_change)
            self.novel.chapters[chId].from_xml(xmlChapter)
            self.novel.tree.append(CH_ROOT, chId)

            for xmlSection in xmlChapter.iterfind('SECTION'):
                scId = xmlSection.attrib['id']
                self._check_id(scId, SECTION_PREFIX)
                self._read_section(xmlSection, scId)
                self.novel.tree.append(chId, scId)

    def _read_characters(self, root):
        """Read characters from the xml element tree."""
        xmlCharacters = root.find('CHARACTERS')
        if xmlCharacters is None:
            return

        for xmlCharacter in xmlCharacters.iterfind('CHARACTER'):
            crId = xmlCharacter.attrib['id']
            self._check_id(crId, CHARACTER_PREFIX)
            self.novel.characters[crId] = Character(on_element_change=self.on_element_change)
            self.novel.characters[crId].from_xml(xmlCharacter)
            self.novel.tree.append(CR_ROOT, crId)

    def _read_items(self, root):
        """Read items from the xml element tree."""
        xmlItems = root.find('ITEMS')
        if xmlItems is None:
            return

        for xmlItem in xmlItems.iterfind('ITEM'):
            itId = xmlItem.attrib['id']
            self._check_id(itId, ITEM_PREFIX)
            self.novel.items[itId] = WorldElement(on_element_change=self.on_element_change)
            self.novel.items[itId].from_xml(xmlItem)
            self.novel.tree.append(IT_ROOT, itId)

    def _read_locations(self, root):
        """Read locations from the xml element tree."""
        xmlLocations = root.find('LOCATIONS')
        if xmlLocations is None:
            return

        for xmlLocation in xmlLocations.iterfind('LOCATION'):
            lcId = xmlLocation.attrib['id']
            self._check_id(lcId, LOCATION_PREFIX)
            self.novel.locations[lcId] = WorldElement(on_element_change=self.on_element_change)
            self.novel.locations[lcId].from_xml(xmlLocation)
            self.novel.tree.append(LC_ROOT, lcId)

    def _read_plot_lines_and_points(self, root):
        """Read plot lines and plot points from the xml element tree."""
        xmlPlotLines = root.find('ARCS')
        if xmlPlotLines is None:
            return

        for xmlPlotLine in xmlPlotLines.iterfind('ARC'):
            plId = xmlPlotLine.attrib['id']
            self._check_id(plId, PLOT_LINE_PREFIX)
            self.novel.plotLines[plId] = PlotLine(on_element_change=self.on_element_change)
            self.novel.plotLines[plId].from_xml(xmlPlotLine)
            self.novel.tree.append(PL_ROOT, plId)

            # Remove dead references.
            self.novel.plotLines[plId].sections = intersection(self.novel.plotLines[plId].sections, self.novel.sections)

            # Create back references.
            for scId in self.novel.plotLines[plId].sections:
                self.novel.sections[scId].scPlotLines.append(plId)

            for xmlPlotPoint in xmlPlotLine.iterfind('POINT'):
                ppId = xmlPlotPoint.attrib['id']
                self._check_id(ppId, PLOT_POINT_PREFIX)
                self._read_plot_point(xmlPlotPoint, ppId, plId)
                self.novel.tree.append(plId, ppId)

    def _read_plot_point(self, xmlPlotPoint, ppId, plId):
        """Read a plot point from the xml element tree."""
        self.novel.plotPoints[ppId] = PlotPoint(on_element_change=self.on_element_change)
        self.novel.plotPoints[ppId].from_xml(xmlPlotPoint)

        # Verify section and create back reference.
        scId = self.novel.plotPoints[ppId].sectionAssoc
        if scId in self.novel.sections:
            self.novel.sections[scId].scPlotPoints[ppId] = plId
        else:
            self.novel.plotPoints[ppId].sectionAssoc = None

    def _read_project(self, root):
        """Read data at project level from the xml element tree."""
        xmlProject = root.find('PROJECT')
        if xmlProject is None:
            return

        self.novel.from_xml(xmlProject)

    def _read_project_notes(self, root):
        """Read project notes from the xml element tree."""
        xmlProjectNotes = root.find('PROJECTNOTES')
        if xmlProjectNotes is None:
            return

        for xmlProjectNote in xmlProjectNotes.iterfind('PROJECTNOTE'):
            pnId = xmlProjectNote.attrib['id']
            self._check_id(pnId, PRJ_NOTE_PREFIX)
            self.novel.projectNotes[pnId] = BasicElement()
            self.novel.projectNotes[pnId].from_xml(xmlProjectNote)
            self.novel.tree.append(PN_ROOT, pnId)

    def _read_section(self, xmlSection, scId):
        """Read data at section level from the xml element tree."""
        self.novel.sections[scId] = Section(on_element_change=self.on_element_change)
        self.novel.sections[scId].from_xml(xmlSection)

        # Remove dead references.
        self.novel.sections[scId].characters = intersection(self.novel.sections[scId].characters, self.novel.characters)
        self.novel.sections[scId].locations = intersection(self.novel.sections[scId].locations, self.novel.locations)
        self.novel.sections[scId].items = intersection(self.novel.sections[scId].items, self.novel.items)

    def _read_word_count_log(self, xmlRoot):
        """Read the word count log from the xml element tree."""

        def verified_date(dateStr):
            # Return a verified iso dateStr or None.
            if dateStr is not None:
                date.fromisoformat(dateStr)
                # raising an exception if dateStr is not an iso-formatted date
            return dateStr

        xmlWclog = xmlRoot.find('PROGRESS')
        if xmlWclog is None:
            return

        for xmlWc in xmlWclog.iterfind('WC'):
            wcDate = verified_date(xmlWc.find('Date').text)
            wcCount = verified_int_string(xmlWc.find('Count').text)
            wcTotalCount = verified_int_string(xmlWc.find('WithUnused').text)
            if wcDate and wcCount and wcTotalCount:
                self.wcLog[wcDate] = [wcCount, wcTotalCount]

    def _update_word_count_log(self):
        """Add today's word count and word count when reading, if not logged."""
        if self.novel.saveWordCount:
            newCountInt, newTotalCountInt = self.count_words()
            newCount = str(newCountInt)
            newTotalCount = str(newTotalCountInt)
            todayIso = date.today().isoformat()
            self.wcLogUpdate[todayIso] = [newCount, newTotalCount]
            for wcDate in self.wcLogUpdate:
                self.wcLog[wcDate] = self.wcLogUpdate[wcDate]
        self.wcLogUpdate.clear()

    def _write_element_tree(self, xmlProject):
        """Write back the xml element tree to a .novx xml file located at filePath.
        
        If a novx file already exists, rename it for backup.
        If writing the file fails, restore the backup copy, if any.
        
        Raise the "Error" exception in case of error. 
        """
        backedUp = False
        if os.path.isfile(xmlProject.filePath):
            try:
                os.replace(xmlProject.filePath, f'{xmlProject.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(xmlProject.filePath)}".')
            else:
                backedUp = True
        try:
            xmlProject.xmlTree.write(xmlProject.filePath, xml_declaration=False, encoding='utf-8')
        except:
            if backedUp:
                os.replace(f'{xmlProject.filePath}.bak', xmlProject.filePath)
            raise Error(f'{_("Cannot write file")}: "{norm_path(xmlProject.filePath)}".')

