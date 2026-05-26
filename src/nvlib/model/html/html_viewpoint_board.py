"""Provide a class for html viewpoint structure board representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_board import HtmlBoard
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import VIEWPOINT_BOARD_SUFFFIX

from nvlib.nv_locale import _


class HtmlViewpointBoard(HtmlBoard):
    """html section cards, arranged by viewpoint."""
    DESCRIPTION = _('HTML Viewpoint board')
    SUFFIX = VIEWPOINT_BOARD_SUFFFIX

    def write(self):
        """Create a HTML page with a card for each viewpoint character and section.
        
        Overwrites the superclass method.
        """

        # Collect the section IDs by viewpoint character.
        srtCharacters = self.novel.tree.get_children(CR_ROOT)
        if not srtCharacters:
            raise UserWarning(f'{_("No characters found")}.')

        DEFAULT_BG = '##dfdfdf'
        NO_VP = ''
        viewpointSections = {NO_VP: {}}
        viewpointCharacters = {}
        srtSections = []
        # Section IDs by viewpoint character ID
        for crId in srtCharacters:
            viewpointSections[crId] = {}
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chType != 0:
                continue

            for scId in self.novel.tree.get_children(chId):
                section = self.novel.sections[scId]
                if section.scType != 0:
                    continue

                srtSections.append(scId)
                crId = section.viewpoint
                if crId:
                    viewpointSections[crId][scId] = section
                    if not crId in viewpointCharacters:
                        viewpointCharacters[crId] = self.novel.characters[crId]
                else:
                    viewpointSections[NO_VP][scId] = section

        if not viewpointCharacters:
            raise UserWarning(f'{_("No viewpoint defined")}.')

        htmlText = [self._fileHeader]

        # Character card styles.
        htmlText.extend(
            self._get_card_header_styles(
                viewpointCharacters,
                invert=True,
            )
        )
        htmlText.extend(
            self._get_card_body_styles(
                viewpointCharacters,
            )
        )

        for crId in viewpointSections:

            # Section card styles per viewpoint character
            # (the default border color is the plot line color).
            if crId == NO_VP:
                defaultBorderColor = None
            else:
                defaultBorderColor = self.novel.characters[crId].color
            htmlText.extend(
                self._get_card_header_styles(
                    viewpointSections[crId],
                    defaultBorderColor=defaultBorderColor,
                )
            )
            htmlText.extend(
                self._get_card_body_styles(
                    viewpointSections[crId],
                    defaultBorderColor=defaultBorderColor,
                )
            )

        htmlText.append(
            f'<title>{_("Viewpoint board")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} - {_("Viewpoint board")}</p>\n'
            '<table>\n'
        )

        # Viewpoint character rows.
        for crId in viewpointSections:
            if not viewpointSections[crId]:
                continue

            if crId == NO_VP:
                bgcolor = DEFAULT_BG
            else:
                bgcolor = self.novel.characters[crId].color or '#000000'
            htmlText.append(f'<tr style="background: {bgcolor}">')
            if crId == NO_VP:
                htmlText.append(
                    self._new_cell(
                        _('No viewpoint'),
                    )
                )
            else:
                htmlText.append(
                    self._new_cell(
                        self.novel.characters[crId].title,
                        attr=f'class="h{crId}"',
                    )
                )
            for scId in srtSections:
                if scId in viewpointSections[crId]:
                    htmlText.append(
                        self._new_cell(
                            self.novel.sections[scId].title,
                            attr=f'class="h{scId}"',
                        )
                    )
                else:
                    htmlText.append('<td />')
            htmlText.append('</tr>')
            htmlText.append(f'<tr style="background: {bgcolor}">')
            if crId == NO_VP:
                htmlText.append('<td />')
            else:
                htmlText.append(
                    self._new_cell(
                        (
                            f'{self.novel.characters[crId].fullName or ""}\n'
                            f'{self.novel.characters[crId].aka or ""}'
                        ),
                        attr=f'class="{crId}"',
                    )
                )
            for scId in srtSections:
                if scId in viewpointSections[crId]:
                    htmlText.append(
                        self._new_cell(
                            self.novel.sections[scId].desc,
                            attr=f'class="{scId}"',
                        )
                    )
                else:
                    htmlText.append('<td />')
            htmlText.append('</tr>')
            htmlText.append(f'<tr style="background: {DEFAULT_BG}">')
            htmlText.append('<td><br /></td></tr>')
        htmlText.append('</table>')
        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))

