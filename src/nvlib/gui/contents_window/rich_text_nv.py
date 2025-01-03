"""Provide a tkinter Rich Text box class with novelibre-specific highlighting.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import font as tkFont

from mvclib.widgets.rich_text_tk import RichTextTk


class RichTextNv(RichTextTk):
    """A text box applying novelibre formatting."""
    H1_UNUSED_TAG = 'h1Unused'
    H2_UNUSED_TAG = 'h2Unused'
    H3_UNUSED_TAG = 'h3Unused'
    UNUSED_TAG = 'unused'
    STAGE1_TAG = 'stage1'
    STAGE2_TAG = 'stage2'
    XML_TAG = 'xmlTag'
    COMMENT_TAG = 'commentTag'
    COMMENT_XML_TAG = 'commentXmlTag'
    NOTE_TAG = 'noteTag'
    NOTE_XML_TAG = 'noteXmlTag'
    EM_TAG = 'emTag'
    STRONG_TAG = 'strongTag'

    COLOR_XML_TAG = 'cornflower blue'
    COLOR_COMMENT_TAG = 'lemon chiffon'
    COLOR_NOTE_TAG = 'bisque'

    def __init__(self, *args, **kwargs):
        """Define some tags for novelibre-specific colors.
        
        Extends the supeclass constructor
        """
        super().__init__(*args,
                height=20,
                width=60,
                spacing1=10,
                spacing2=2,
                wrap='word',
                padx=10,
                bg=kwargs['color_text_bg'],
                fg=kwargs['color_text_fg'],
                )
        defaultFont = tkFont.nametofont(self.cget('font'))

        defaultSize = defaultFont.cget('size')
        boldFont = tkFont.Font(**defaultFont.configure())
        italicFont = tkFont.Font(**defaultFont.configure())
        h1Font = tkFont.Font(**defaultFont.configure())
        h2Font = tkFont.Font(**defaultFont.configure())
        h3Font = tkFont.Font(**defaultFont.configure())

        boldFont.configure(weight='bold')
        italicFont.configure(slant='italic')
        h1Font.configure(size=int(defaultSize * self.H1_SIZE),
                         weight='bold',
                         )
        h2Font.configure(size=int(defaultSize * self.H2_SIZE),
                         weight='bold',
                         )
        h3Font.configure(size=int(defaultSize * self.H3_SIZE),
                         slant='italic',
                         )
        self.tag_configure(self.XML_TAG,
                           foreground=self.COLOR_XML_TAG,
                           )
        self.tag_configure(self.EM_TAG,
                           font=italicFont,
                           )
        self.tag_configure(self.STRONG_TAG,
                           font=boldFont,
                           )
        self.tag_configure(self.COMMENT_TAG,
                           background=self.COLOR_COMMENT_TAG,
                           )
        self.tag_configure(self.COMMENT_XML_TAG,
                           foreground=self.COLOR_XML_TAG,
                           background=self.COLOR_COMMENT_TAG,
                           )
        self.tag_configure(self.NOTE_TAG,
                           background=self.COLOR_NOTE_TAG,
                           )
        self.tag_configure(self.NOTE_XML_TAG,
                           foreground=self.COLOR_XML_TAG,
                           background=self.COLOR_NOTE_TAG,
                           )
        self.tag_configure(self.H1_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_chapter'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H1_UNUSED_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H2_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_chapter'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H2_UNUSED_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H3_UNUSED_TAG,
                           font=h3Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H3_SPACING,
                           )
        self.tag_configure(self.UNUSED_TAG,
                           foreground=kwargs['color_unused'],
                           )
        self.tag_configure(self.STAGE1_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_stage'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.STAGE2_TAG,
                           font=h3Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_stage'],
                           justify='center',
                           spacing1=defaultSize * self.H3_SPACING,
                           )

