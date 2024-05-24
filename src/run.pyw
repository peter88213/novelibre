from tkinter import messagebox
import traceback

import novelibre_
import tkinter as tk


def show_error(self, *args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Exception', err)


tk.Tk.report_callback_exception = show_error
novelibre_.main()
