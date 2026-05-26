"""Provide a class for html chapter board representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_board import HtmlBoard
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CHAPTER_BOARD_SUFFFIX
from nvlib.nv_locale import _


class HtmlChapterBoard(HtmlBoard):
    """html section cards, arranged by chapters."""
    DESCRIPTION = _('HTML Chapter board')
    SUFFIX = CHAPTER_BOARD_SUFFFIX

    def write(self):
        """Create a HTML page with a card for each chapter and section.
        
        Overwrites the superclass method.
        """

        # Collect the chapters.
        srtChapters = []
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chType == 0:
                srtChapters.append(chId)

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
            # Section card styles per chapter
            # (the default border color is the chapter color).
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
            f'<title>{_("Chapter board")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} - {_("Chapter board")}</p>\n'
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
            htmlText.append('</tr>')
            htmlText.append('<tr>')
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
            htmlText.append('</tr></table><br />')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))

