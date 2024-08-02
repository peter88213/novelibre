"""Build a python script for the novelibre distribution.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see see https://github.com/peter88213/novxlib)
must be located on the same directory level as the novelibre project. 

For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

import translate_de
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import inliner
import pgettext

APP = 'novelibre'
VERSION = '4.7.0'

SOURCE_DIR = '../src/'
TEST_DIR = '../test/'
SOURCE_FILE = f'{SOURCE_DIR}novelibre_.py'
TEST_FILE = f'{TEST_DIR}novelibre.py'


def inline_modules(source, target):
    """Inline all non-standard library modules."""
    NVLIB = 'nvlib'
    NV_PATH = '../../novelibre/src/'
    NOVXLIB = 'novxlib'
    NOVX_PATH = '../../novxlib/src/'
    inliner.run(source, target, NVLIB, NV_PATH)
    inliner.run(target, target, NOVXLIB, NOVX_PATH)


def insert_version_number(source, version='unknown'):
    """Write the actual version string and make sure that Unix EOL is used."""
    with open(source, 'r', encoding='utf_8') as f:
        lines = f.read()
    newlines = []
    for line in lines.split('\n'):
        newlines.append(line.replace('@release', version))
    with open(TEST_FILE, 'w', encoding='utf_8', newline='\n') as f:
        f.write('\n'.join(newlines))
    print(f'Version {version} set.')


def make_pot(sourcefile, version='unknown'):
    """Generate a pot file for translations from the source file."""
    POT_FILE = '../i18n/messages.pot'
    if os.path.isfile(POT_FILE):
        os.replace(POT_FILE, f'{POT_FILE}.bak')
        backedUp = True
    else:
        backedUp = False
    try:
        pot = pgettext.PotFile(POT_FILE, app=APP, appVersion=version)
        pot.scan_file(sourcefile)
        print(f'Writing "{pot.filePath}"...\n')
        pot.write_pot()
        return True

    except Exception as ex:
        if backedUp:
            os.replace(f'{POT_FILE}.bak', POT_FILE)
        print(str(ex))
        return False


def main():
    os.makedirs(TEST_DIR, exist_ok=True)
    inline_modules(SOURCE_FILE, TEST_FILE)
    insert_version_number(TEST_FILE, version=VERSION)
    if not make_pot(TEST_FILE, version=VERSION):
        sys.exit(1)
    if not translate_de.main(version=VERSION):
        sys.exit(1)


if __name__ == '__main__':
    main()
