"""Provide a class for html story structure board representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.hex_color import HexColor
from nvlib.model.html.html_board import HtmlBoard
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import STAGE_CARD_SUFFIX
from nvlib.nv_locale import _


class HtmlStoryStructureBoard(HtmlBoard):
    """html story structure board representation."""
    DESCRIPTION = _('HTML Story structure board')
    SUFFIX = STAGE_CARD_SUFFIX

    def write(self):
        """Create a HTML page with a card for each stage and section.
        
        Overwrites the superclass method.
        """

        # Create a stage tree.
        stageId = NO_STAGE = ''
        stageTree = {stageId:[]}
        srtStages = {}
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                section = self.novel.sections[scId]
                if section.scType > 1:
                    stageId = scId
                    srtStages[stageId] = self.novel.sections[scId]
                    stageTree[stageId] = []
                elif section.scType == 0:
                    stageTree[stageId].append(scId)

        if not srtStages:
            raise UserWarning(f'{_("No stages found")}.')

        htmlText = [self._fileHeader]

        # Stage card styles.
        stageColor = '#FF0000'
        if HexColor.is_dark(stageColor):
            fgColor = '#FFFFFF'
        else:
            fgColor = '#000000'
        borderColor = '#FFFFFF'
        htmlText.append(
            '<style type="text/css">\n'
            'td.hstage {'
            'font-weight: bold; '
            f'border-top: 0.2em solid {stageColor}; '
            f'border-right: 0.2em solid {stageColor}; '
            f'border-left: 0.2em solid {stageColor}; '
            f'border-bottom: 0.1em solid #ff0000; '
            f'background: {stageColor}; '
            f'color: {fgColor}'
            '}\n'
            f'td.stage1 {{'
            f'border-right: 0.2em solid {stageColor}; '
            f'border-left: 0.2em solid {stageColor}; '
            f'border-bottom: 0.2em solid {stageColor}; '
            'background: #ffffff; '
            '}\n'
            f'td.stage2 {{'
            f'border-right: 0.2em solid {borderColor}; '
            f'border-left: 0.2em solid {borderColor}; '
            f'border-bottom: 0.2em solid {borderColor}; '
            'background: #ffffff; '
            '}\n'
            '</style>\n'
        )

        for stageId in stageTree:

            # Section card styles per stage
            # (the default border color is the plot line color).
            if stageId != NO_STAGE:
                defaultBorderColor = self.novel.sections[stageId].color
            else:
                defaultBorderColor = '#FFFFFF'
            sections = {}
            for scId in stageTree[stageId]:
                sections[scId] = self.novel.sections[scId]
            htmlText.extend(
                self._get_card_header_styles(
                    sections,
                    defaultBorderColor=defaultBorderColor,
                )
            )
            htmlText.extend(
                self._get_card_body_styles(
                    sections,
                    defaultBorderColor=defaultBorderColor,
                )
            )

        htmlText.append(
            f'<title>{_("Story structure board")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} - {_("Story structure board")}</p>\n'
        )

        # Stage rows.
        for stageId in stageTree:
            htmlText.append('<table><tr>')
            if stageId == NO_STAGE:
                htmlText.append('<td />')
            else:
                if self.novel.sections[stageId].scType == 2:
                    style = 'stage1'
                else:
                    style = 'stage2'
                htmlText.append(
                    self._new_cell(
                        self.novel.sections[stageId].title,
                        attr='class="hstage"',
                    )
                )
            for scId in stageTree[stageId]:
                htmlText.append(
                    self._new_cell(
                        self.novel.sections[scId].title,
                        attr=f'class="h{scId}"',
                    )
                )
            htmlText.append(f'</tr>')
            htmlText.append(f'<tr>')
            if stageId == NO_STAGE:
                htmlText.append('<td />')
            else:
                htmlText.append(
                    self._new_cell(
                        self.novel.sections[stageId].desc,
                        attr=f'class="{style}"',
                    )
                )
            for scId in stageTree[stageId]:
                htmlText.append(
                    self._new_cell(
                        self.novel.sections[scId].desc,
                        attr=f'class="{scId}"',
                    )
                )
            htmlText.append('</tr></table><br>')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))

