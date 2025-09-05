"""novelibre installer library module. 

Version @release

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import gettext
import glob
import locale
import os
from pathlib import Path
import platform
from shutil import copy2
from shutil import copytree
import stat
from string import Template
import sys
import zipfile

import relocate

major = sys.version_info.major
minor = sys.version_info.minor
if  major != 3 or minor < 7:
    print(
        f'Wrong Python version installed: {major}.{minor}.\n'
        'Must be 3.7 or newer.'
    )
    input('Press ENTER to quit.')
    sys.exit(1)

try:
    from tkinter import messagebox
except ModuleNotFoundError:
    print(
        'The tkinter module is missing. '
        'Please install the tk support package for your python3 version'
        "via your distribution's package manager."
    )
    input('Press ENTER to quit.')
    sys.exit(1)

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
VERSION = '@release'
APP = f'{APPNAME}.py'
START_UP_SCRIPT = 'run.pyw'
INI_FILE = f'{APPNAME}.ini'
INI_PATH = '/config/'

SHORTCUT_MESSAGE_WIN = '''
Now you might want to create a shortcut on your desktop.  

For this, open the installation folder, 
hold down the Alt key on your keyboard, 
and then drag and drop "run.pyw" to your desktop.
'''

SHORTCUT_MESSAGE_IX = '''
Now you might want to create a shortcut on your desktop.  

For this, open the installation folder 
and then drag and drop "novelibre.desktop" to your desktop.

When using the shortcut the first time, your system may ask for confirmation. 
'''

ADD_TO_REGISTRY = fr'''Windows Registry Editor Version 5.00

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

REMOVE_FROM_REGISTRY = fr'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\\noveltree]
[-HKEY_CURRENT_USER\Software\Classes\\nv5Collection]
[-HKEY_CURRENT_USER\Software\Classes\\novelibre]
[-HKEY_CURRENT_USER\Software\Classes\\.novx]

'''

LINUX_DESKTOP_LAUNCHER = '''[Desktop Entry]
Type = Application
Name = novelibre
GenericName = Novel organizer
GenericName[de] = Roman-Organisation
Comment = A novel organizer for LibreOffice/OpenOffice users
Comment[de] = Roman-Organisation für LibreOffice/OpenOffice-Benutzer
Icon = $Install_Dir/icons/nLogo64.png
Categories = Office;
Terminal = false
Path = $Install_Dir
Exec = python3 $Install_Dir/run.pyw %f
StartupNotify = false
'''

PLUGIN_WARNING = '''
There are plugins installed. 
You may want to run the Plugin Manager for compatibility check.
'''

START_UP_CODE = f'''import logging
from tkinter import messagebox
import traceback

import $Appname
import tkinter as tk

def show_error(self, *args):
    err = traceback.format_exception(*args)
    logger.error('$Appname $Release\\n' + ''.join(err))
    messagebox.showerror(
        'An unexpected error has occurred.', 
        'See "error.log" in the installation directory.' 
    )

logger = logging.getLogger(__name__)
logging.basicConfig(filename='$InstallDir/error.log', level=logging.ERROR)
tk.Tk.report_callback_exception = show_error
$Appname.main()
'''

OBSOLETE_PLUGINS = [
    'nv_clipboard',
]

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


def create_explorer_context_menu(installPath):
    """Generate ".reg" files to extend the novelibre context menu."""

    def save_reg_file(filePath, template, mapping):
        """Save a registry file."""
        print(f'Creating "{os.path.normpath(filePath)}" ...')
        with open(filePath, 'w') as f:
            f.write(template.safe_substitute(mapping))

    python = sys.executable.replace('\\', '\\\\')
    installUrl = installPath.replace('/', '\\\\')
    script = f'{installUrl}\\\\{START_UP_SCRIPT}'
    mapping = dict(PYTHON=python, SCRIPT=script, INSTALL=installUrl)
    save_reg_file(
        f'{installPath}/add_novelibre.reg',
        Template(ADD_TO_REGISTRY),
        mapping
    )
    save_reg_file(
        f'{installPath}/remove_novelibre.reg',
        Template(REMOVE_FROM_REGISTRY),
        {}
    )


def create_desktop_launcher(installDir):
    desktopFile = f'{installDir}/novelibre.desktop'
    print(f'Creating Linux desktop launcher "{desktopFile}" ...')
    template = Template(LINUX_DESKTOP_LAUNCHER)
    mapping = dict(Install_Dir=installDir)
    with open(desktopFile, 'w', encoding='utf-8') as f:
        f.write(template.safe_substitute(mapping))


def open_folder(installDir):
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


def install(zipped):
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    print(f'*** Installing {APPNAME} {VERSION} ***\n')
    homePath = str(Path.home()).replace('\\', '/')
    installDir = f'{homePath}/.novx'
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
    else:
        copy_file = copy2
        copy_tree = cp_tree

    #--- Relocate the v1.x installation directory, if necessary.
    message = relocate.main()
    if message:
        messagebox.showinfo(
            'Moving the novelibre installation directory',
            message
        )

    #--- Create a general novxlib installation directory, if necessary.
    os.makedirs(installDir, exist_ok=True)
    if os.path.isfile(f'{installDir}/{APP}'):
        simpleUpdate = True
    else:
        simpleUpdate = False
    cnfDir = f'{installDir}/{INI_PATH}'
    os.makedirs(cnfDir, exist_ok=True)

    #--- Delete the old version, but retain configuration, if any.
    # Do not remove the locale folder, because it may contain plugin data.
    # Do not remove the icons folder, because it may contain plugin data.
    filesToDelete = [
        f'{installDir}/{APP}',
        f'{installDir}/{START_UP_SCRIPT}',
        f'{installDir}/add_novelibre.reg',
        f'{installDir}/remove_novelibre.reg',
        f'{installDir}/error.log'
        ]
    for file in filesToDelete:
        try:
            os.remove(file)
            print(f'"{os.path.normpath(file)}" removed.')
        except:
            pass

    #--- Install the new version.
    print(f'Copying "{APP}" ...')
    copy_file(APP, installDir)

    #--- Install the localization files.
    print('Copying locale ...')
    copy_tree('locale', installDir)

    #--- Create a plugin directory.
    pluginDir = f'{installDir}/plugin'
    print(f'Creating "{os.path.normpath(pluginDir)}" ...')
    os.makedirs(pluginDir, exist_ok=True)

    #--- Check plugins.
    files = glob.glob(f'{pluginDir}/*.py')
    if files:
        print(PLUGIN_WARNING)
    for filePath in files:
        moduleName, __ = os.path.splitext(os.path.basename(filePath))
        if not moduleName.startswith('nv_'):
            os.remove(filePath)
            print(f'"{os.path.normpath(filePath)}" removed.')
        if moduleName in OBSOLETE_PLUGINS:
            os.remove(filePath)
            print(f'"{os.path.normpath(filePath)}" removed.')

    #--- Create a start-up script.
    print('Creating starter script ...')
    mapping = {
        'Appname': APPNAME,
        'Apppath': f'{installDir}/{START_UP_SCRIPT}',
        'InstallDir': installDir,
        'DisplayDir': os.path.normpath(installDir),
        'Release': VERSION,
    }
    if platform.system() == 'Windows':
        shebang = ''
    else:
        shebang = '#!/usr/bin/env python3\n'
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        startupCode = Template(
            f'{shebang}{START_UP_CODE}'
        ).safe_substitute(mapping)
        f.write(startupCode)

    #--- Make the scripts executable under Linux.
    st = os.stat(f'{installDir}/{APP}')
    os.chmod(f'{installDir}/{APP}', st.st_mode | stat.S_IEXEC)
    st = os.stat(f'{installDir}/{START_UP_SCRIPT}')
    os.chmod(f'{installDir}/{START_UP_SCRIPT}', st.st_mode | stat.S_IEXEC)

    #--- Install the css files.
    print('Copying css stylesheet ...')
    copy_tree('css', installDir)

    #--- Install the icon files.
    print('Copying icons ...')
    copy_tree('icons', installDir)

    #--- Generate registry entries for the context menu (Windows only).
    if platform.system() == 'Windows':
        create_explorer_context_menu(installDir)

    #--- Display a success message.
    print(
        f'\nSucessfully installed {APPNAME} '
        f'at "{os.path.normpath(installDir)}".'
    )
    if simpleUpdate:
        input('Press ENTER to quit.')
        return

    #--- Generate a launcher for the Linux desktop (Linux/FreeBSD only).
    if platform.system() in ('Linux', 'FreeBSD'):
        create_desktop_launcher(installDir)
        print(SHORTCUT_MESSAGE_IX)

    #--- Ask for shortcut creation.
    else:
        print(SHORTCUT_MESSAGE_WIN)

    if messagebox.askyesno(
        title=f'{APPNAME} {VERSION} Setup',
        message='Open the installation folder now?',
    ):
        open_folder(installDir)
        input('Press ENTER to quit.')


def main(zipped=True):
    try:
        install(zipped)
    except Exception as ex:
        print(str(ex))
        input('Press ENTER to quit.')

