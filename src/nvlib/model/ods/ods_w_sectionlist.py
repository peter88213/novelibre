"""Provide a class for ODS section list export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.section import Section
from nvlib.model.ods.ods_w_grid import OdsWGrid
from nvlib.novx_globals import SECTIONLIST_SUFFIX
from nvlib.nv_locale import _


class OdsWSectionList(OdsWGrid):
    """ODS section list writer."""

    DESCRIPTION = _('Section list')
    SUFFIX = SECTIONLIST_SUFFIX

    # Column width:
    # co1 2.000cm
    # co2 3.000cm
    # co3 4.000cm
    # co4 8.000cm

    # Header structure:
    # Section ID (hidden)
    # Section number (link to manuscript)
    # Title
    # Description
    # Viewpoint
    # Date
    # Time
    # Day
    # Duration
    # Tags
    # Section notes
    # Scene
    # Goal
    # Conflict
    # Outcome
    # Status
    # Words total
    # Word count
    # Characters
    # Locations
    # Items

    _fileHeader = (
        f'{OdsWGrid._CONTENT_XML_HEADER}{DESCRIPTION}" table:style-name="ta1" table:print="false">\n'
        '    <table:table-column table:style-name="co1" table:visibility="collapse" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co2" table:default-cell-style-name="ce2"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="ce4"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>\n'
        '    <table:table-row table:style-name="ro1" table:visibility="collapse">\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Section</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Title</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Description</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Viewpoint</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="ce1" office:value-type="string">\n'
        '      <text:p>Date</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="ce3" office:value-type="string">\n'
        '      <text:p>Time</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Day</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Duration</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Tags</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Section notes</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Scene</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Goal</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Conflict</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Outcome</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Status</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Words total</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Word count</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Characters</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Locations</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>Items</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1003"/>\n'
        '    </table:table-row>\n'
        '    <table:table-row table:style-name="ro1">\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        '      <text:p>ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Section")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Title")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Description")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Viewpoint")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="ce1" office:value-type="string">\n'
        f'      <text:p>{_("Date")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="ce3" office:value-type="string">\n'
        f'      <text:p>{_("Time")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Day")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Duration")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Tags")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Section notes")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Scene")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>$CustomPlotProgress / {_("Goal")} / {_("Reaction")} / $CustomGoal</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>$CustomCharacterization / {_("Conflict")} / {_("Dilemma")} / $CustomConflict</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>$CustomWorldBuilding / {_("Outcome")} / {_("Choice")} / $CustomOutcome</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Status")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Words total")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Section word count")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Characters")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Locations")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" office:value-type="string">\n'
        f'      <text:p>{_("Items")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1003"/>\n'
        '    </table:table-row>\n'
    )
    _sectionTemplate = (
        '   <table:table-row table:style-name="ro2">\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:formula="of:=HYPERLINK(&quot;file:///$ProjectPath/$ProjectName$ManuscriptSuffix.odt#$ID%7Cregion&quot;;&quot;$SectionNumber&quot;)" office:value-type="string" office:string-value="$SectionNumber">\n'
        '      <text:p>$SectionNumber</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Title</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Desc</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Viewpoint</text:p>\n'
        '     </table:table-cell>\n'
        '$DateCell\n'
        '$TimeCell\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Day</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Duration</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Tags</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Notes</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Scene</text:p>\n'
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
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Status</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="float" office:value="$WordsTotal">\n'
        '      <text:p>$WordsTotal</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="float" office:value="$WordCount">\n'
        '      <text:p>$WordCount</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Characters</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Locations</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell>\n'
        '      <text:p>$Items</text:p>\n'
        '     </table:table-cell>\n'
        '    </table:table-row>\n'
    )

    def _get_sectionMapping(self, scId, sectionNumber, wordsTotal, **kwargs):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(scId, sectionNumber, wordsTotal)
        sectionMapping['Status'] = Section.STATUS[sectionMapping['Status']]
        return sectionMapping
