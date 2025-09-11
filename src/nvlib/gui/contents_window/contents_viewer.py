"""Provide a tkinter text box class for "contents" viewing.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.contents_window.content_view_parser import ContentViewParser
from nvlib.gui.contents_window.rich_text_nv import RichTextNv
from nvlib.gui.observer import Observer
from nvlib.novx_globals import CH_ROOT
from nvlib.nv_locale import _
import tkinter as tk


class ContentsViewer(RichTextNv, Observer, SubController):
    """A tkinter text box class for novelibre file viewing.
    
    Show the novel contents in a text box.
    """

    def __init__(self, parent, model, controller):
        """Put a text box to the specified window.
        
        Positional arguments:
            parent: tk.Frame -- The parent window.
            model -- reference to the novelibre main model instance.
            controller -- reference to the novelibre main controller instance.
        
        Required keyword arguments:
            show_markup: bool 
        """
        prefs = controller.get_preferences()
        super().__init__(parent, **prefs)
        self._mdl = model

        self.pack(expand=True, fill='both')
        self.showMarkup = tk.BooleanVar(parent, value=prefs['show_markup'])
        ttk.Checkbutton(
            parent,
            text=_('Show markup'),
            variable=self.showMarkup
        ).pack(anchor='w')
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

    def on_close(self):
        """Actions to be performed when a project is closed."""
        self.reset_view()

    def refresh(self, event=None, *args):
        """Reload the text to view."""
        if self._mdl.prjFile is None:
            return

        if self._parent.winfo_manager():
            self.view_text()
            try:
                super().see(self._index)
            except KeyError:
                pass

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

    def view_text(self):
        """Get a list of "tagged text" tuples and send it to the text box."""
        taggedText = self._get_tagged_text()
        self._textMarks.clear()

        # Clear the text box first.
        self.config(state='normal')
        self.delete('1.0', 'end')

        # Send the (text, tag) tuples to the text box.
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

    def _convert_from_novx(self, text, textTag):
        # Return a section's content as a list of (text, tag) tuples.
        # text: str -- a section's xml text.
        # textTag: str -- default tag used for body text.
        if not self.showMarkup.get():
            self._contentParser.showTags = False
        else:
            self._contentParser.showTags = True
        self._contentParser.textTag = textTag
        self._contentParser.feed(text)
        return self._contentParser.taggedText[1:-1]

    def _get_tagged_text(self):
        # Return the whole novel as a list of (text, tag) tuples.
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

            isEpigraph = chapter.hasEpigraph
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
                    if isEpigraph:
                        headingTag = self.H3_EPIGRAPH_TAG
                        textTag = self.EPIGRAPH_TAG
                    else:
                        headingTag = self.H3_TAG
                else:
                    headingTag = self.H3_UNUSED_TAG
                    textTag = self.UNUSED_TAG
                if isEpigraph and section.scType == 0:
                    heading = ''
                elif section.title:
                    heading = f'[{section.title}]\n'
                else:
                    heading = f"[{_('Unnamed')}]\n"
                taggedText.append((heading, headingTag))

                if section.sectionContent:
                    textTuples = self._convert_from_novx(
                        section.sectionContent,
                        textTag
                    )
                    taggedText.extend(textTuples)

                if isEpigraph and section.scType == 0 and section.desc:
                    taggedText.append(
                        (f'{section.desc}\n', self.EPIGRAPH_SRC_TAG)
                    )

                isEpigraph = False

        if not taggedText:
            taggedText.append(
                (f'({_("No text available")})', self.ITALIC_TAG)
            )
        return taggedText

