"""Provide a tkinter Rich Text box class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk


class RichTextTk(tk.Text):
    """A text box with a ttk scrollbar, applying formatting.
    
    Kudos to Bryan Oakley
    https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter
    """
    H1_TAG = 'h1'
    H2_TAG = 'h2'
    H3_TAG = 'h3'
    ITALIC_TAG = 'italic'
    BOLD_TAG = 'bold'
    CENTER_TAG = 'center'
    BULLET_TAG = 'bullet'

    H1_SIZE = 1.2
    H2_SIZE = 1.1
    H3_SIZE = 1.0
    H1_SPACING = 2
    H2_SPACING = 2
    H3_SPACING = 1.5
    CENTER_SPACING = 1.5

    def __init__(self, master=None, **kw):
        """Define tags for headings and bold/italic.
        
        Copied from tkinter.scrolledtext and modified (use ttk widgets).
        Extends the supeclass constructor.
        """
        # Add a scrollbar:
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side='right', fill='y')

        kw.update({'yscrollcommand': self.vbar.set})
        tk.Text.__init__(self, self.frame, **kw)
        self.pack(side='left', fill='both', expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

        # This part is "rich text" specific:
        defaultFont = tkFont.nametofont(self.cget('font'))

        em = defaultFont.measure('m')
        defaultSize = defaultFont.cget('size')
        boldFont = tkFont.Font(**defaultFont.configure())
        italicFont = tkFont.Font(**defaultFont.configure())
        h1Font = tkFont.Font(**defaultFont.configure())
        h2Font = tkFont.Font(**defaultFont.configure())
        h3Font = tkFont.Font(**defaultFont.configure())

        boldFont.configure(weight='bold')
        italicFont.configure(slant='italic')
        h1Font.configure(size=int(defaultSize * self.H1_SIZE), weight='bold')
        h2Font.configure(size=int(defaultSize * self.H2_SIZE), weight='bold')
        h3Font.configure(size=int(defaultSize * self.H3_SIZE), slant='italic')

        self.tag_configure(self.BOLD_TAG, font=boldFont)
        self.tag_configure(self.ITALIC_TAG, font=italicFont)
        self.tag_configure(self.H1_TAG, font=h1Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H1_SPACING)
        self.tag_configure(self.H2_TAG, font=h2Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H2_SPACING)
        self.tag_configure(self.H3_TAG, font=h3Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H3_SPACING)
        self.tag_configure(self.CENTER_TAG, justify='center', spacing1=defaultSize * self.CENTER_SPACING)

        lmargin2 = em + defaultFont.measure('\u2022 ')
        self.tag_configure(self.BULLET_TAG, lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f'\u2022 {text}', self.BULLET_TAG)
