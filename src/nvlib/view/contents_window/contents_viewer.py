"""Provide a tkinter text box class for "contents" viewing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
from tkinter import ttk

from nvlib.nv_globals import prefs
from nvlib.view.contents_window.content_view_parser import ContentViewParser
from nvlib.view.contents_window.rich_text_nv import RichTextNv
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import _
import tkinter as tk


class ContentsViewer(RichTextNv):
    """A tkinter text box class for noveltree file viewing.
    
    Show the novel contents in a text box.
    """
    NO_TEXT = re.compile('\<note\>.*?\<\/note\>|\<comment\>.*?\<\/comment\>|\<.+?\>')

    def __init__(self, parent, model, view, controller):
        """Put a text box to the specified window.
        
        Positional arguments:
            parent: tk.Frame -- The parent window.
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
        
        Required keyword arguments:
            show_markup: bool 
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        super().__init__(parent, **prefs)
        self.pack(expand=True, fill='both')
        self.showMarkup = tk.BooleanVar(parent, value=prefs['show_markup'])
        ttk.Checkbutton(parent, text=_('Show markup'), variable=self.showMarkup).pack(anchor='w')
        self.showMarkup.trace('w', self.refresh)
        self._textMarks = {}
        self._index = '1.0'
        self._parent = parent
        self._contentParser = ContentViewParser()
        self._contentParser.xmlTag = self.XML_TAG
        self._contentParser.emTag = self.EM_TAG
        self._contentParser.strongTag = self.STRONG_TAG
        self._contentParser.commentTag = self.COMMENT_TAG
        self._contentParser.commentXmlTag = self.COMMENT_XML_TAG
        self._contentParser.noteTag = self.NOTE_TAG
        self._contentParser.noteXmlTag = self.NOTE_XML_TAG

    def reset_view(self):
        """Clear the text box."""
        self.config(state='normal')
        self.delete('1.0', 'end')
        self.config(state='disabled')

    def see(self, idStr):
        """Scroll the text to the position of the idStr node.
        
        Positional arguments:
            idStr: str -- Chapter or section node (tree selection).
        """
        try:
            self._index = self._textMarks[idStr]
            super().see(self._index)
        except KeyError:
            pass

    def refresh(self, event=None, *args):
        """Reload the text to view."""
        if self._mdl.prjFile is None:
            return

        if self._parent.winfo_manager():
            self.reset_view()
            self.view_text()
            try:
                super().see(self._index)
            except KeyError:
                pass

    def view_text(self):
        """Build a list of "tagged text" tuples and send it to the text box."""

        def convert_from_noveltree(text):

            if not self.showMarkup.get():
                self._contentParser.showTags = False
            else:
                self._contentParser.showTags = True
            self._contentParser.textTag = textTag
            self._contentParser.feed(text)
            return self._contentParser.taggedText[1:-1]

        taggedText = []
        for chId in self._mdl.novel.tree.get_children(CH_ROOT):
            chapter = self._mdl.novel.chapters[chId]
            taggedText.append(chId)
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

            # Get chapter titles.
            if chapter.title:
                heading = f'{chapter.title}\n'
            else:
                    heading = f"[{_('Unnamed')}]\n"
            taggedText.append((heading, headingTag))

            for scId in self._mdl.novel.tree.get_children(chId):
                section = self._mdl.novel.sections[scId]
                taggedText.append(scId)
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
                    textTuples = convert_from_noveltree(section.sectionContent)
                    taggedText.extend(textTuples)

        if not taggedText:
            taggedText.append(('(No text available)', self.ITALIC_TAG))
        self._textMarks = {}
        self.config(state='normal')
        self.delete('1.0', 'end')
        for entry in taggedText:
            if len(entry) == 2:
                # entry is a regular (text, tag) tuple.
                text, tag = entry
                self.insert('end', text, tag)
            else:
                # entry is a mark to insert.
                index = f"{self.count('1.0', 'end', 'lines')[0]}.0"
                self._textMarks[entry] = index
        self.config(state='disabled')

