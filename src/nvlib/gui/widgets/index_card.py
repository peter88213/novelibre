"""Provide an "index card" class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License 
(https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from nvlib.gui.widgets.text_box import TextBox
from nvlib.gui.widgets.my_string_var import MyStringVar


class IndexCard(tk.Frame):
    """An "index card" class displaying a title and a text body.
    
    Public instance variables:
        title: tk.StringVar -- Editable title text.
        bodyBox: TextBox -- Body text editor.   
    """

    def __init__(
            self,
            master=None,
            cnf={},
            fg='black',
            bg='white',
            font=None,
            scrollbar=True,
            **kw
    ):
        super().__init__(master=master, cnf=cnf, **kw)
        self._bgColor = bg

        # Title label.
        titleFrame = tk.Frame(
            self,
            background=bg,
        )
        titleFrame.pack(
            fill='x',
        )
        self.colorField = tk.Label(
            titleFrame,
            width=2,
            background=bg,
        )
        self.colorField.pack(
            side='right',
            expand=False,
        )
        self.title = MyStringVar(value='')
        self.titleEntry = tk.Entry(
            titleFrame,
            bg=bg,
            bd=0,
            textvariable=self.title,
            relief='flat',
            font=font,
            background=bg,
            foreground=fg,
            insertbackground=fg,
        )
        self.titleEntry.pack(
            side='left',
            ipady=6,
            fill='x',
            expand=True,
        )

        tk.Frame(self, bg='red', height=1, bd=0).pack(fill='x')
        tk.Frame(self, bg=bg, height=1, bd=0).pack(fill='x')

        # Description window.
        self.bodyBox = TextBox(
            self,
            scrollbar=scrollbar,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            padx=5,
            pady=5,
            bg=bg,
            fg=fg,
            insertbackground=fg,
            font=font,
        )
        self.bodyBox.pack(fill='both', expand=True)

    def lock(self):
        """Inhibit element change."""
        self.titleEntry.config(state='disabled')
        self.bodyBox.config(state='disabled')

    def reset_color(self):
        self.colorField.configure(
            bg=self._bgColor,
            text='◈',
        )

    def set_color(self, color):
        self.colorField.configure(
            bg=color,
            text='',
        )

    def unlock(self):
        """Enable element change."""
        self.titleEntry.config(state='normal')
        self.bodyBox.config(state='normal')
