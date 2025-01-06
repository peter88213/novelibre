"""Move and rename a noveltree installation directory, if any.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import os
import sys
from shutil import move
from pathlib import Path
try:
    from tkinter import messagebox
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)


def main():
    message = []
    homePath = str(Path.home()).replace('\\', '/')
    oldDir = f'{homePath}/.noveltree'
    newDir = f'{homePath}/.novx'

    if os.path.isdir(oldDir):
        if not os.path.isdir(newDir):
            move(oldDir, newDir)
            message.append(f'Renamed {oldDir} to {newDir}.')
    try:
        os.remove(f'{newDir}/add_noveltree.reg')
    except:
        pass
    else:
        message.append('Old registry script deleted. Please run "add_novelibre.reg".')

    try:
        os.remove(f'{newDir}/remove_noveltree.reg')
    except:
        pass

    try:
        os.remove(f'{newDir}/locale/de/LC_MESSAGES/noveltree.mo')
    except:
        pass

    try:
        os.replace(f'{newDir}/config/noveltree.ini',
                   f'{newDir}/config/novx.ini')
    except:
        pass
    else:
        message.append('Configuration file renamed.')

    return '\n'.join(message)


if __name__ == '__main__':
    message = main()
    if message:
        messagebox.showinfo('Moving the novelibre installation directory', message)
    else:
        messagebox.showerror('Moving the novelibre installation directory',
                             'There is nothing to move.')
