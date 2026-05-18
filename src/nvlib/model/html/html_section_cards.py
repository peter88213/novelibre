"""Provide a class for html section cards representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_cards import HtmlCards
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_CARD_SUFFIX
from nvlib.nv_locale import _


class HtmlSectionCards(HtmlCards):
    """html section board representation."""
    DESCRIPTION = _('HTML Section cards')
    SUFFIX = SECTION_CARD_SUFFIX

    def write(self):
        """Create a HTML page with a card for each chapter and section.
        
        Overwrites the superclass method.
        """

        # Collect the chapters.
        srtChapters = self.novel.tree.get_children(CH_ROOT)
        if not srtChapters:
            raise UserWarning(f'{_("No chapters found")}.')

        htmlText = [self._fileHeader]

        # Chapter card styles.
        htmlText.extend(
            self._get_card_header_styles(
                self.novel.chapters,
                invert=True,
            )
        )
        htmlText.extend(
            self._get_card_body_styles(
                self.novel.chapters,
            )
        )

        for chId in srtChapters:

            # Section card styles per plot line
            # (the default border color is the plot line color).
            sections = {}
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType == 0:
                    sections[scId] = self.novel.sections[scId]
            htmlText.extend(
                self._get_card_header_styles(
                    sections,
                    defaultBorderColor=self.novel.chapters[chId].color,
                )
            )
            htmlText.extend(
                self._get_card_body_styles(
                    sections,
                    defaultBorderColor=self.novel.chapters[chId].color,
                )
            )

        htmlText.append(
            f'<title>{_("Section cards")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} - {_("Section cards")}</p>\n'
        )

        # Chapter rows.
        for chId in srtChapters:
            htmlText.append('<table><tr>')
            htmlText.append(
                self._new_cell(
                    self.novel.chapters[chId].title,
                    attr=f'class="h{chId}"',
                )
            )
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType == 0:
                    htmlText.append(
                        self._new_cell(
                            self.novel.sections[scId].title,
                            attr=f'class="h{scId}"',
                        )
                    )
            htmlText.append(f'</tr>')
            htmlText.append(f'<tr>')
            htmlText.append(
                self._new_cell(
                    self.novel.chapters[chId].desc,
                    attr=f'class="{chId}"',
                )
            )
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType == 0:
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

