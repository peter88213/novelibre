"""Provide a custom variant of the tkinter simpledialog module by Frederik Lundh.

This modification of the tkinter simpledialog module
is slightly refactored, features ttk widgets, and is 
prepared for translation with GNU gettext.

This modules handles dialog boxes.

It contains the following public symbols:

SimpleDialog -- A simple but flexible modal dialog box

Dialog -- a base class for dialogs

askinteger -- get an integer from the user

askfloat -- get a float from the user

askstring -- get a string from the user

Copyright (c) 1997 by Fredrik Lundh
fredrik@pythonware.com
http://www.pythonware.com

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import _get_temp_root, _destroy_temp_root
from tkinter import messagebox
from tkinter import ttk

from novxlib.novx_globals import _
import tkinter as tk


class SimpleDialog:

    def __init__(self, master,
                 text='', buttons=[], default=None, cancel=None,
                 title=None, class_=None):
        if master is None:
            master = _get_temp_root()
        if class_:
            self.root = tk.Toplevel(master, class_=class_)
        else:
            self.root = tk.Toplevel(master)
        if title:
            self.root.title(title)
            self.root.iconname(title)

        _setup_dialog(self.root)

        self.message = tk.Message(self.root, text=text, aspect=400, bg='white')
        self.message.pack(expand=1, fill='both')
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.num = default
        self.cancel = cancel
        self.default = default
        self.root.bind('<Return>', self.return_event)
        for num in range(len(buttons)):
            s = buttons[num]
            b = ttk.Button(self.frame, text=s,
                       command=(lambda self=self, num=num: self.done(num)))
            if num == default:
                b.focus()
            b.pack(side='left', fill='both', expand=1, padx=5, pady=10)
        self.root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
        self.root.transient(master)
        _place_window(self.root, master)

    def go(self):
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.mainloop()
        self.root.destroy()
        return self.num

    def return_event(self, event):
        if self.default is None:
            self.root.bell()
        else:
            self.done(self.default)

    def wm_delete_window(self):
        if self.cancel is None:
            self.root.bell()
        else:
            self.done(self.cancel)

    def done(self, num):
        self.num = num
        self.root.quit()


class Dialog(tk.Toplevel):

    """Class to open dialogs.

    This class is intended as a base class for custom dialogs
    """

    def __init__(self, parent, title=None):
        """Initialize a dialog.

        Arguments:

            parent -- a parent window (the application window)

            title -- the dialog title
        """
        master = parent
        if master is None:
            master = _get_temp_root()

        tk.Toplevel.__init__(self, master)

        self.withdraw()  # remain invisible for now
        # If the parent is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent is not None and parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        _setup_dialog(self)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if self.initial_focus is None:
            self.initial_focus = self

        self.protocol('WM_DELETE_WINDOW', self.cancel)

        _place_window(self, parent)

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self):
        """Destroy the window"""
        self.initial_focus = None
        tk.Toplevel.destroy(self)
        _destroy_temp_root(self.master)

    #
    # construction hooks

    def body(self, master):
        """create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        """
        pass

    def buttonbox(self):
        """add standard button box.

        override if you do not want the standard buttons
        """

        box = tk.Frame(self)

        w = ttk.Button(box, text=_('OK'), width=10, command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=10)
        w = ttk.Button(box, text=_('Cancel'), width=10, command=self.cancel)
        w.pack(side='left', padx=5, pady=10)

        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        """validate the data

        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        """

        return 1  # override

    def apply(self):
        """process the data

        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        """

        pass  # override


# Place a toplevel window at the center of parent or screen
# It is a Python implementation of ::tk::PlaceWindow.
def _place_window(w, parent=None):
    w.wm_withdraw()  # Remain invisible while we figure out the geometry
    w.update_idletasks()  # Actualize geometry information

    minwidth = w.winfo_reqwidth()
    minheight = w.winfo_reqheight()
    maxwidth = w.winfo_vrootwidth()
    maxheight = w.winfo_vrootheight()
    if parent is not None and parent.winfo_ismapped():
        x = parent.winfo_rootx() + (parent.winfo_width() - minwidth) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - minheight) // 2
        vrootx = w.winfo_vrootx()
        vrooty = w.winfo_vrooty()
        x = min(x, vrootx + maxwidth - minwidth)
        x = max(x, vrootx)
        y = min(y, vrooty + maxheight - minheight)
        y = max(y, vrooty)
        if w._windowingsystem == 'aqua':
            # Avoid the native menu bar which sits on top of everything.
            y = max(y, 22)
    else:
        x = (w.winfo_screenwidth() - minwidth) // 2
        y = (w.winfo_screenheight() - minheight) // 2

    w.wm_maxsize(maxwidth, maxheight)
    w.wm_geometry('+%d+%d' % (x, y))
    w.wm_deiconify()  # Become visible at the desired location


def _setup_dialog(w):
    if w._windowingsystem == 'aqua':
        w.tk.call('::tk::unsupported::MacWindowStyle', 'style',
                  w, 'moveableModal', '')
    elif w._windowingsystem == 'x11':
        w.wm_attributes('-type', 'dialog')

# --------------------------------------------------------------------
# convenience dialogues


class _QueryDialog(Dialog):

    def __init__(self, title, prompt,
                 initialvalue=None,
                 minvalue=None, maxvalue=None,
                 parent=None):

        self.prompt = prompt
        self.minvalue = minvalue
        self.maxvalue = maxvalue

        self.initialvalue = initialvalue

        Dialog.__init__(self, parent, title)

    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    def body(self, master):

        w = ttk.Label(master, text=self.prompt, justify='left')
        w.grid(row=0, padx=5, sticky='w')

        self.entry = ttk.Entry(master, name='entry')
        self.entry.grid(row=1, padx=5, pady=5, sticky='w' + 'e')

        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, 'end')

        return self.entry

    def validate(self):
        try:
            result = self.getresult()
        except ValueError:
            messagebox.showwarning(
                _('Illegal value'),
                f'{self.errormessage}\n{_("Please try again")}.',
                parent=self
            )
            return 0

        if self.minvalue is not None and result < self.minvalue:
            messagebox.showwarning(
                _('Too small'),
                f'{_("The allowed minimum value is")} {self.minvalue}.\n{_("Please try again")}.',
                parent=self
            )
            return 0

        if self.maxvalue is not None and result > self.maxvalue:
            messagebox.showwarning(
                _('Too large'),
                f'{_("The allowed maximum value is")} {self.maxvalue}.\n{_("Please try again")}.',
                parent=self
            )
            return 0

        self.result = result

        return 1


class _QueryInteger(_QueryDialog):
    errormessage = _('Not an integer.')

    def getresult(self):
        return self.getint(self.entry.get())


def askinteger(title, prompt, **kw):
    """get an integer from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is an integer
    """
    d = _QueryInteger(title, prompt, **kw)
    return d.result


class _QueryFloat(_QueryDialog):
    errormessage = _('Not a floating point value.')

    def getresult(self):
        return self.getdouble(self.entry.get())


def askfloat(title, prompt, **kw):
    """get a float from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is a float
    """
    d = _QueryFloat(title, prompt, **kw)
    return d.result


class _QueryString(_QueryDialog):

    def __init__(self, *args, **kw):
        if 'show' in kw:
            self.__show = kw['show']
            del kw['show']
        else:
            self.__show = None
        _QueryDialog.__init__(self, *args, **kw)

    def body(self, master):
        entry = _QueryDialog.body(self, master)
        if self.__show is not None:
            entry.configure(show=self.__show)
        return entry

    def getresult(self):
        return self.entry.get()


def askstring(title, prompt, **kw):
    """get a string from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is a string
    """
    d = _QueryString(title, prompt, **kw)
    return d.result

