"""Move the noveltree installation directory

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
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

    if not os.path.isdir(oldDir):
        raise Exception(f'{oldDir} does not exist.')

    if os.path.isdir(newDir):
        raise Exception(f'{newDir} already exists.')

    move(oldDir, newDir)
    message.append(f'Renamed {oldDir} to {newDir}.')
    regScript = f'{newDir}/add_noveltree.reg'
    try:
        with open(regScript, 'r', encoding='utf-8') as f:
            regTxt = f.read()
        regTxt = regTxt.replace(
            r'\\.noveltree\\',
            r'\\.novx\\'
            )
        with open(regScript, 'w', encoding='utf-8') as f:
            f.write(regTxt)
    except:
        message.append('Cannot rewrite the registry script')
    else:
        message.append(f'Registry script rewritten. Please re-run "{regScript}"')

    return '\n'.join(message)


if __name__ == '__main__':
    try:
        messagebox.showinfo(
        'Moving the noveltree installation directory',
        main()
        )
    except Exception as ex:
        messagebox.showerror(
            'Cannot move the noveltree installation directory',
            str(ex)
            )
