"""Provide a tkinter text box class for "contents" viewing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.observer import Observer
from nvlib.gui.contents_window.contents_viewer_ctrl import ContentsViewerCtrl
from nvlib.gui.contents_window.rich_text_nv import RichTextNv
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class ContentsViewer(RichTextNv, Observer, ContentsViewerCtrl):
    """A tkinter text box class for novelibre file viewing.
    
    Show the novel contents in a text box.
    """

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
        super().__init__(parent, **prefs)
        self.initialize_controller(model, view, controller)

        self.pack(expand=True, fill='both')
        self.showMarkup = tk.BooleanVar(parent, value=prefs['show_markup'])
        ttk.Checkbutton(parent, text=_('Show markup'), variable=self.showMarkup).pack(anchor='w')
        self.showMarkup.trace('w', self.refresh)
        self._textMarks = {}
        self._index = '1.0'
        self._parent = parent

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
        taggedText = self.get_tagged_text()
        self._textMarks = {}

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

