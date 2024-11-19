"""Provide a mixin class for controlling the contents viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import _
from nvlib.controller.contents_window.content_view_parser import ContentViewParser


class ContentsViewerCtrl(SubController):

    def initialize_controller(self, model, view, controller):
        super().initialize_controller(model, view, controller)

        self._contentParser = ContentViewParser()
        self._contentParser.xmlTag = self.XML_TAG
        self._contentParser.emTag = self.EM_TAG
        self._contentParser.strongTag = self.STRONG_TAG
        self._contentParser.commentTag = self.COMMENT_TAG
        self._contentParser.commentXmlTag = self.COMMENT_XML_TAG
        self._contentParser.noteTag = self.NOTE_TAG
        self._contentParser.noteXmlTag = self.NOTE_XML_TAG

    def _convert_from_novx(self, text, textTag):
        """Return a section's content as a list of (text, tag) tuples.
        
        Positional arguments:
            text: str -- a section's xml text.
            textTag: str -- default tag used for body text.
        """
        if not self.showMarkup.get():
            self._contentParser.showTags = False
        else:
            self._contentParser.showTags = True
        self._contentParser.textTag = textTag
        self._contentParser.feed(text)
        return self._contentParser.taggedText[1:-1]

    def get_tagged_text(self):
        """Return the whole novel as a list of (text, tag) tuples."""

        # Build a list of (text, tag) tuples for the whole book.
        taggedText = []
        for chId in self._mdl.novel.tree.get_children(CH_ROOT):
            chapter = self._mdl.novel.chapters[chId]
            taggedText.append(chId)
            # inserting a chapter mark
            if chapter.chLevel == 2:
                if chapter.chType == 0:
                    headingTag = self.H2_TAG
                else:
                    headingTag = self.H2_UNUSED_TAG
            else:
                if chapter.chType == 0:
                    headingTag = self.H1_TAG
                else:
                    headingTag = self.H1_UNUSED_TAG
            if chapter.title:
                heading = f'{chapter.title}\n'
            else:
                    heading = f"[{_('Unnamed')}]\n"
            taggedText.append((heading, headingTag))

            for scId in self._mdl.novel.tree.get_children(chId):
                section = self._mdl.novel.sections[scId]
                taggedText.append(scId)
                # inserting a section mark
                textTag = ''
                if section.scType == 3:
                    headingTag = self.STAGE2_TAG
                elif section.scType == 2:
                    headingTag = self.STAGE1_TAG
                elif section.scType == 0:
                    headingTag = self.H3_TAG
                else:
                    headingTag = self.H3_UNUSED_TAG
                    textTag = self.UNUSED_TAG
                if section.title:
                    heading = f'[{section.title}]\n'
                else:
                    heading = f"[{_('Unnamed')}]\n"
                taggedText.append((heading, headingTag))

                if section.sectionContent:
                    textTuples = self._convert_from_novx(section.sectionContent, textTag)
                    taggedText.extend(textTuples)

        if not taggedText:
            taggedText.append((f'({_("No text available")})', self.ITALIC_TAG))
        return taggedText

