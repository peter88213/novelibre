"""Provide a tkinter listbox with drag'n'drop reordering of entries.

Based on an example published in the "Python Cookbook" 
by Alex Martelli, Anna Ravenscroft, and David Ascher.
"""
import tkinter as tk


class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries."""

    def __init__(self, master, **kw):
        kw['selectmode'] = 'single'
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self._set_current)
        self.bind('<B1-Motion>', self._shift_selection)
        self.curIndex = None

    def _set_current(self, event):
        self.curIndex = self.nearest(event.y)

    def _shift_selection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i
