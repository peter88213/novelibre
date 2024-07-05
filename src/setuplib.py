"""novelibre installer library module. 

Version @release

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from shutil import copytree
from shutil import copy2
import zipfile
import os
import sys
import stat
import glob
from pathlib import Path
from string import Template
import gettext
import locale
import platform
try:
    import tkinter as tk
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)

from tkinter import messagebox
import relocate

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('reg', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPNAME = 'novelibre'
VERSION = ' @release'
APP = f'{APPNAME}.py'
START_UP_SCRIPT = 'run.pyw'
INI_FILE = f'{APPNAME}.ini'
INI_PATH = '/config/'
SUCCESS_MESSAGE = '''

$Appname is installed here:

$Apppath'''

SHORTCUT_MESSAGE = '''
Now you might want to create a shortcut on your desktop.  

On Windows, open the installation folder, hold down the Alt key on your keyboard, 
and then drag and drop "run.pyw" to your desktop.

On Linux, create a launcher on your desktop. With xfce for instance, the launcher's command may look like this:
python3 '$Apppath' %f
'''

ADD_TO_REGISTRY = f'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\\noveltree]
[-HKEY_CURRENT_USER\Software\Classes\\novelibre]
[-HKEY_CURRENT_USER\Software\Classes\\novelibre]
[-HKEY_CURRENT_USER\Software\Classes\\novxCollection]
[-HKEY_CURRENT_USER\Software\Classes\\.novx]
[HKEY_CURRENT_USER\Software\Classes\\.novx]
"Content Type"="text/xml"
@="novelibre"
[HKEY_CURRENT_USER\Software\Classes\\novelibre]
@="novelibre Project"
[HKEY_CURRENT_USER\Software\Classes\\novelibre\DefaultIcon]
@="$INSTALL\\\\icons\\\\nLogo64.ico"
[HKEY_CURRENT_USER\Software\Classes\\novelibre\shell\open\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\""
[HKEY_CURRENT_USER\Software\Classes\\.nvcx]
"Content Type"="text/xml"
@="novxCollection"
[HKEY_CURRENT_USER\Software\Classes\\novxCollection]
@="novelibre Collection"
[HKEY_CURRENT_USER\Software\Classes\\novxCollection\DefaultIcon]
@="$INSTALL\\\\icons\\\\cLogo64.ico"

'''

REMOVE_FROM_REGISTRY = f'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\\noveltree]
[-HKEY_CURRENT_USER\Software\Classes\\nv5Collection]
[-HKEY_CURRENT_USER\Software\Classes\\novelibre]
[-HKEY_CURRENT_USER\Software\Classes\\.novx]

'''

PLUGIN_OUTDATED = '''There are outdated plugins installed, which will be ignored by novelibre from now on. 
Please update your plugins.
'''

PLUGIN_WARNING = '''
There are plugins installed. 
You may want to run the Plugin Manager for compatibility check.
'''

START_UP_CODE = f'''import {APPNAME}
import tkinter as tk
from tkinter import messagebox
import traceback

def show_error(self, *args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Exception', err)


tk.Tk.report_callback_exception = show_error
{APPNAME}.main()
'''

root = tk.Tk()
processInfo = tk.Label(root, text='')
message = []

pyz = os.path.dirname(__file__)


def extract_file(sourceFile, targetDir):
    with zipfile.ZipFile(pyz) as z:
        z.extract(sourceFile, targetDir)


def extract_tree(sourceDir, targetDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(f'{sourceDir}/'):
                z.extract(file, targetDir)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


def make_context_menu(installPath):
    """Generate ".reg" files to extend the novelibre context menu."""

    def save_reg_file(filePath, template, mapping):
        """Save a registry file."""
        with open(filePath, 'w') as f:
            f.write(template.safe_substitute(mapping))
        output(f'Creating "{os.path.normpath(filePath)}"')

    python = sys.executable.replace('\\', '\\\\')
    installUrl = installPath.replace('/', '\\\\')
    script = f'{installUrl}\\\\{START_UP_SCRIPT}'
    mapping = dict(PYTHON=python, SCRIPT=script, INSTALL=installUrl)
    save_reg_file(f'{installPath}/add_novelibre.reg', Template(ADD_TO_REGISTRY), mapping)
    save_reg_file(f'{installPath}/remove_novelibre.reg', Template(REMOVE_FROM_REGISTRY), {})


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def open_folder(installDir):
    """Open an installation folder window in the file manager.
    """
    try:
        os.startfile(os.path.normpath(installDir))
        # Windows
    except:
        try:
            os.system('xdg-open "%s"' % os.path.normpath(installDir))
            # Linux
        except:
            try:
                os.system('open "%s"' % os.path.normpath(installDir))
                # Mac
            except:
                pass


def install(installDir, zipped):
    """Install the application."""
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
    else:
        copy_file = copy2
        copy_tree = cp_tree

    #--- Relocate the v1.x installation directory, if necessary.
    message = relocate.main()
    if message:
        messagebox.showinfo('Moving the novelibre installation directory', message)

    #--- Create a general novxlib installation directory, if necessary.
    os.makedirs(installDir, exist_ok=True)
    cnfDir = f'{installDir}/{INI_PATH}'
    if os.path.isfile(f'{installDir}/{APP}'):
        simpleUpdate = True
    else:
        simpleUpdate = False

    os.makedirs(cnfDir, exist_ok=True)

    #--- Delete the old version, but retain configuration, if any.
    # Do not remove the locale folder, because it may contain plugin data.
    # Do not remove the icons folder, because it may contain plugin data.
    with os.scandir(installDir) as files:
        for file in files:
            try:
                os.remove(file)
                output(f'"{file.name}" removed.')
            except:
                pass

    #--- Install the new version.
    output(f'Copying "{APP}" ...')
    copy_file(APP, installDir)

    # Create a starter script.
    output('Creating starter script ...')
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        f.write(f'import {APPNAME}\n{APPNAME}.main()')

    # Install the localization files.
    output('Copying locale ...')
    copy_tree('locale', installDir)

    # Install the icon files.
    output('Copying icons ...')
    copy_tree('icons', installDir)

    # Install the css files.
    output('Copying css stylesheet ...')
    copy_tree('css', installDir)

    #--- Make the scripts executable under Linux.
    st = os.stat(f'{installDir}/{APP}')
    os.chmod(f'{installDir}/{APP}', st.st_mode | stat.S_IEXEC)
    st = os.stat(f'{installDir}/{START_UP_SCRIPT}')
    os.chmod(f'{installDir}/{START_UP_SCRIPT}', st.st_mode | stat.S_IEXEC)

    #--- Create a plugin directory.

    pluginDir = f'{installDir}/plugin'
    output(f'Creating "{os.path.normpath(pluginDir)}" ...')
    os.makedirs(pluginDir, exist_ok=True)

    #--- Check plugins.
    files = glob.glob(f'{pluginDir}/*.py')
    if files:
        output(PLUGIN_WARNING)
    for filePath in files:
        moduleName = os.path.split(filePath)[1][:-3]
        if not moduleName.startswith('nv_'):
            messagebox.showwarning('Plugin check', PLUGIN_OUTDATED)
            break

    #--- Generate registry entries for the context menu (Windows only).
    if os.name == 'nt':
        make_context_menu(installDir)

    #--- Display a success message.
    mapping = {'Appname': APPNAME, 'Apppath': f'{installDir}/{START_UP_SCRIPT}'}
    output(Template(SUCCESS_MESSAGE).safe_substitute(mapping))

    #--- Ask for shortcut creation.
    if not simpleUpdate:
        output(Template(SHORTCUT_MESSAGE).safe_substitute(mapping))

    #--- Create a start-up script.
    if platform.system() == 'Windows':
        shebang = ''
    else:
        shebang = '#!/usr/bin/env python3\n'
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        f.write(f'{shebang}{START_UP_CODE}')


def main(zipped=True):
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.geometry("800x700")
    root.title(f'Install {APPNAME}{VERSION}')
    header = tk.Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Run the installation.
    homePath = str(Path.home()).replace('\\', '/')
    novxlibPath = f'{homePath}/.novx'
    try:
        install(novxlibPath, zipped)
    except Exception as ex:
        output(str(ex))

    # Show options: open installation folders or quit.
    root.openButton = tk.Button(text="Open installation folder", command=lambda: open_folder(f'{homePath}/.novx'))
    root.openButton.config(height=1, width=30)
    root.openButton.pack(padx=5, pady=5)
    root.quitButton = tk.Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()

