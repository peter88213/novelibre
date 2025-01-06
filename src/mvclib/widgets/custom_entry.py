"""Provide an entry widget with undo/redo capability.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import Entry


class CustomEntry(Entry):
    """Custom Entry widget with undo/redo capability.
    
    Based on the code presented by Evgeny Tretyakov on Stack Overflow:
    https://stackoverflow.com/questions/4146971/undo-and-redo-in-an-tkinter-entry-widget
    
    Modifications: 
    - Initialize the buffer empty, so the last "Ctrl-Z" would not clear the entry.
    - Restore the cursor position when undoing/redoing changes.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.changes = []
        self.steps = int()
        self.bind('<Control-z>', self._undo)
        self.bind('<Control-y>', self._redo)
        self.bind('<Key>', self._add_changes)

    def _undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.delete(0, 'end')
            buffer, cursorPos = self.changes[self.steps]
            self.insert('end', buffer)
            self.icursor(cursorPos)

    def _redo(self, event=None):
        if self.steps < len(self.changes):
            self.delete(0, 'end')
            buffer, cursorPos = self.changes[self.steps]
            self.insert('end', buffer)
            self.icursor(cursorPos)
            self.steps += 1

    def _add_changes(self, event=None):
        if not self.changes or self.get() != self.changes[-1][0]:
            self.changes.append((self.get(), self.index('insert')))
            self.steps += 1
