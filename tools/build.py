"""Build a python script for the novelibre distribution.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see see https://github.com/peter88213/novxlib)
must be located on the same directory level as the novelibre project. 

For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copy2
from shutil import rmtree
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import build_tools
import translate_de

APP = 'novelibre'
VERSION = '4.7.0'
RELEASE = f'{APP}_v{VERSION}'
MO_FILE = 'novelibre.mo'

SOURCE_DIR = '../src/'
TEST_DIR = '../test/'
SOURCE_FILE = f'{SOURCE_DIR}novelibre_.py'
TEST_FILE = f'{TEST_DIR}novelibre.py'
BUILD_BASE = '../build'
BUILD_DIR = f'{BUILD_BASE}/{RELEASE}'
DIST_DIR = '../dist'

distFiles = [
    (TEST_FILE, BUILD_DIR),
    (f'{SOURCE_DIR}setuplib.py', BUILD_DIR),
    (f'{SOURCE_DIR}relocate.py', BUILD_DIR),
    ('../LICENSE', BUILD_DIR),
]


def build_app():
    os.makedirs(TEST_DIR, exist_ok=True)
    build_tools.inline_modules(SOURCE_FILE, TEST_FILE)
    build_tools.insert_version_number(TEST_FILE, version=VERSION)


def build_package():
    print(f'\nProviding empty "{DIST_DIR}" ...')
    try:
        rmtree(DIST_DIR)
    except FileNotFoundError:
        pass
    os.makedirs(DIST_DIR)
    build_tools.make_pyz(BUILD_DIR, DIST_DIR, RELEASE)
    build_tools.make_zip(BUILD_DIR, DIST_DIR, RELEASE)


def build_translation():
    if not MO_FILE:
        return

    if not build_tools.make_pot(TEST_FILE, app=APP, version=VERSION):
        sys.exit(1)

    translation = translate_de.main(
        MO_FILE,
        app='novelibre',
        version=VERSION
        )
    if translation is None:
        sys.exit(1)

    i18Dir, moDir = translation
    distFiles.append((
        f'{i18Dir}/{moDir}/{MO_FILE}',
        f'{BUILD_DIR}/{moDir}'
        ))


def clean_up():
    print(f'\nRemoving "{TEST_FILE}" ...')
    os.remove(TEST_FILE)


def prepare_package():
    print(f'\nProviding empty "{BUILD_DIR}" ...')
    try:
        rmtree(BUILD_BASE)
    except FileNotFoundError:
        pass
    build_tools.collect_dist_files(distFiles)
    build_tools.insert_version_number(
        f'{BUILD_DIR}/setuplib.py',
        version=VERSION
        )


def main():
    build_app()
    build_translation()
    prepare_package()
    build_package()
    clean_up()


if __name__ == '__main__':
    main()
