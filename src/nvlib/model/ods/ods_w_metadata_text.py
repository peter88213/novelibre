"""Provide a class for ODS metadata text export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template

from nvlib.model.ods.ods_writer import OdsWriter
from nvlib.novx_globals import METADATA_TEXT_SUFFIX
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.nv_locale import _


class OdsWMetadataText(OdsWriter):
    """ODS metadata text templates."""

    DESCRIPTION = _('Metadata text')
    SUFFIX = METADATA_TEXT_SUFFIX

    # Column width:
    # co1 2.000cm
    # co2 3.000cm
    # co3 4.000cm
    # co4 8.000cm

    # Header structure:
    # Section ID (hidden)
    # Title
    # Description
    # Notes
    # Tags
    # Goal
    # Conflict
    # Outcome
    # All plot lines

    _fileHeader = (
        f'{OdsWriter._CONTENT_XML_HEADER}{DESCRIPTION}" '
        'table:style-name="ta1" table:print="false">\n'
        '    <table:table-column table:style-name="co1" '
        'table:visibility="collapse" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:default-cell-style-name="Default"/>\n'
        '$ArcColumns\n'
        '    <table:table-row table:style-name="ro1" '
        'table:visibility="collapse">\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Title</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Description</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Notes</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Tags</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Goal</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Conflict</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Outcome</text:p>\n'
        '     </table:table-cell>\n'
        '$ArcIdCells\n'
        '     <table:table-cell '
        'table:style-name="Heading" table:number-columns-repeated="1003"/>\n'
        '    </table:table-row>\n'
    )
    _sectionTemplate = _epigraphTemplate = (
        '   <table:table-row table:style-name="ro2">\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Title</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Desc</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Notes</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Tags</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Goal</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Conflict</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Outcome</text:p>\n'
        '     </table:table-cell>\n'
        '$ArcNoteCells\n'
        '    </table:table-row>\n'
    )
    _fileFooter = OdsWriter._CONTENT_XML_FOOTER
    _emptyDateCell = '     <table:table-cell table:style-name="ce2"/>'
    _validDateCell = (
        '     <table:table-cell '
        'office:value-type="date" office:date-value="$Date">\n'
        '      <text:p>$Date</text:p>\n'
        '     </table:table-cell>\n'
    )
    _emptyTimeCell = '     <table:table-cell table:style-name="ce4"/>'
    _validTimeCell = (
        '     <table:table-cell office:value-type="time" '
        'office:time-value="$OdsTime">\n'
        '      <text:p>$Time</text:p>\n'
        '     </table:table-cell>\n'
    )
    _arcNoteCell = (
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$ArcNote</text:p>\n'
        '     </table:table-cell>\n'
    )
    _arcIdCell = (
        '     <table:table-cell '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>$ArcId</text:p>\n'
        '     </table:table-cell>\n'
    )
    _arcTitleCell = (
        '     <table:table-cell $Link '
        'table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>$ArcTitle</text:p>\n'
        '     </table:table-cell>\n'
    )

    def _get_fileHeaderMapping(self):
        """Return a mapping dictionary for the project section.
        
        Extends the superclass method.
        """
        fileHeaderMapping = super()._get_fileHeaderMapping()

        #--- Cells for the plot line notes: one column per plot line.
        arcColumns = []
        arcIdCells = []
        arcTitleCells = []
        for plId in self.novel.tree.get_children(PL_ROOT):
            link = self._convert_from_novx(
                self.novel.plotLines[plId].title,
                isLink=True,
            )
            arcColumns.append(
                '    <table:table-column table:style-name="co4" '
                'table:default-cell-style-name="Default"/>'
            )
            mapping = dict(
                ArcId=plId,
                ArcTitle=self.novel.plotLines[plId].title,
                Link=(
                    'table:formula="of:=HYPERLINK(&quot;'
                    f'file:///{self.projectPath}/'
                    f'{self._convert_from_novx(self.projectName)}'
                    f'{PLOTLINES_SUFFIX}.odt#{plId}&quot;;&quot;'
                    f'{link}&quot;)"'
                ),
            )
            arcIdCells.append(
                Template(self._arcIdCell
            ).safe_substitute(mapping))
            arcTitleCells.append(
                Template(
                    self._arcTitleCell
                ).safe_substitute(mapping))
        fileHeaderMapping['ArcColumns'] = '\n'.join(arcColumns)
        fileHeaderMapping['ArcIdCells'] = '\n'.join(arcIdCells)
        fileHeaderMapping['ArcTitleCells'] = '\n'.join(arcTitleCells)

        return fileHeaderMapping

    def _get_sectionMapping(
            self,
            scId,
            sectionNumber,
            wordsTotal,
            firstInChapter=False,
            isEpigraph=False,
    ):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(
            scId,
            sectionNumber,
            wordsTotal,
            firstInChapter,
            isEpigraph,
        )

        #--- $DateCell: if no section date is given,
        #               the whole cell must be empty.
        if sectionMapping['Date']:
            sectionMapping['DateCell'] = Template(
                self._validDateCell
            ).safe_substitute(sectionMapping)
        else:
            sectionMapping['DateCell'] = self._emptyDateCell

        #--- $TimeCell: if no section time is given,
        #               the whole cell must be empty.
        if sectionMapping['Time']:
            sectionMapping['TimeCell'] = Template(
                self._validTimeCell
            ).safe_substitute(sectionMapping)
        else:
            sectionMapping['TimeCell'] = self._emptyTimeCell

        #--- $ArcNoteCells: one per plot line.
        arcNoteCells = []
        for plId in self.novel.tree.get_children(PL_ROOT):
            plotlineNotes = self.novel.sections[scId].plotlineNotes
            if plotlineNotes:
                arcNote = plotlineNotes.get(plId, '')
            else:
                arcNote = ''
            mapping = {'ArcNote':arcNote}
            arcNoteCells.append(
                Template(
                    self._arcNoteCell
                ).safe_substitute(mapping))
        sectionMapping['ArcNoteCells'] = '\n'.join(arcNoteCells)

        return sectionMapping

