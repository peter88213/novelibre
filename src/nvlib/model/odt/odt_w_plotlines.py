"""Provide a class for ODT plot line descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template

from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.novx_globals import SECTIONS_SUFFIX
from nvlib.nv_locale import _


class OdtWPlotlines(OdtWriter):
    """ODT plot lines description file representation.

    Export descriptions of plot lines and plot points.
    """
    DESCRIPTION = _('Plot lines')
    SUFFIX = PLOTLINES_SUFFIX

    _fileHeader = f'''{OdtWriter._CONTENT_XML_HEADER}<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    _arcHeadingTemplate = f'''<text:h text:style-name="Heading_20_1" text:outline-level="1">{_('Plot lines')}</text:h>
'''

    _arcTemplate = '''$Heading<text:h text:style-name="Heading_20_2" text:outline-level="2"><text:bookmark text:name="$ID"/>$Title</text:h>
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
$TurningPoints
'''
    _plotPointTemplate = '''<text:h text:style-name="Heading_20_3" text:outline-level="3"><text:bookmark text:name="$ID"/>$Title</text:h>
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
'''
    _assocSectionTemplate = '''<text:p text:style-name="Text_20_body" />
<text:p text:style-name="Text_20_body">$Section: <text:span text:style-name="Emphasis">$SectionTitle</text:span></text:p>    
<text:p text:style-name="Text_20_body">→ <text:a xlink:href="../$ProjectName$SectionsSuffix.odt#$scID%7Cregion">$Description</text:a></text:p>
<text:p text:style-name="Text_20_body">→ <text:a xlink:href="../$ProjectName$ManuscriptSuffix.odt#$scID%7Cregion">$Manuscript</text:a></text:p>
'''

    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

    def write(self):
        """Initialize "first plot line" flag.

       Extends the superclass constructor.
        """
        self._firstPlotLine = True
        super().write()

    def _get_arcMapping(self, plId):
        """Add associated sections to the plot line mapping dictionary.
        
        Extends the superclass method.
        """
        arcMapping = super()._get_arcMapping(plId)
        if self._firstPlotLine:
            arcMapping['Heading'] = self._arcHeadingTemplate
            self._firstPlotLine = False
        else:
            arcMapping['Heading'] = ''
        plotPoints = []
        for ppId in self.novel.tree.get_children(plId):
            plotPointMapping = dict(
                ID=ppId,
                Title=self.novel.plotPoints[ppId].title,
                Desc=self._convert_from_novx(self.novel.plotPoints[ppId].desc),
            )
            template = Template(self._plotPointTemplate)
            plotPoints.append(template.safe_substitute(plotPointMapping))
            scId = self.novel.plotPoints[ppId].sectionAssoc
            if scId:
                sectionAssocMapping = dict(
                    SectionTitle=self.novel.sections[scId].title,
                    ProjectName=self._convert_from_novx(self.projectName, True),
                    Section=_('Section'),
                    Description=_('Description'),
                    Manuscript=_('Manuscript'),
                    scID=scId,
                    ManuscriptSuffix=MANUSCRIPT_SUFFIX,
                    SectionsSuffix=SECTIONS_SUFFIX,
                )
                template = Template(self._assocSectionTemplate)
                plotPoints.append(template.safe_substitute(sectionAssocMapping))
        arcMapping['TurningPoints'] = '\n'.join(plotPoints)
        return arcMapping

