"""Provide a widget that shows a percentage bar.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from tkinter import ttk


class PercentageBar(ttk.Frame):
    """A progress bar widget with a label on the left side.
    
    public properties:
        label: ttk.Label -- Label for text display.
        spacer: ttk.Label -- Spacer to control the distance between the label and the progress bar.
        progressBar: ttk.Progressbar -- A bar of variable width, displaying its percentage value.
    
    public methods: 
        set(value) -- Set the value at runtime.
    """

    def __init__(self, parent, text='', value=None, lblWidth=None, lblDist=0, anchor='e', **kwargs):
        """Configure the label and the progress bar.
        
        Positional arguments:
            parent - parent widget.
            
        Optional arguments:
            text: str -- Text to be displayed on the label.
            value: Initial progress bar display value in percents.
            lblWidth: int -- Label width in characters. If None, the geometry manager does the job.
            lblDist: int -- Distance between label and progress bar in characters.
            anchor: str -- if 'e', align text right, if 'w', align text left.  
        
        Extends the superclass constructor.
        """
        super().__init__(parent, **kwargs)
        self.pack(fill='x', expand=True)

        # Place the label.
        self.label = ttk.Label(self, text=text, anchor=anchor, width=lblWidth)
        if lblWidth is not None:
            self.label.configure(width=lblWidth)
        self.label.pack(side='left')

        # Place a spacer between the label and the progress bar.
        self.spacer = ttk.Label(self, width=lblDist)
        self.spacer.pack(side='left')

        # Place the progress bar.
        self.progressBar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progressBar.pack(side='left', fill='x', expand=True)
        if value is not None:
            self.set(value)

    def set(self, value):
        """Set the value at runtime.
        
        Positional arguments:
            value - Progress bar display value in percents.
        """
        self.progressBar['value'] = value

