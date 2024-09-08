"""Build the novelibre application package.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see see https://github.com/peter88213/novxlib)
must be located on the same directory level as the novelibre project. 

For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from shutil import copytree
import os
from shutil import rmtree
import sys
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import build_tools
import translate_de

VERSION = '4.9.6'
PRJ_NAME = 'novelibre'

VERSION_INI = f'''[LATEST]
version = {VERSION}
download_link = https://github.com/peter88213/{PRJ_NAME}/raw/main/dist/{PRJ_NAME}_v{VERSION}.pyzw'''
VERSION_INI_PATH = '../VERSION'
LANDING_PAGE = '../README.md'
LANDING_PAGE_TEMPLATE = '../docs/template/README.md'

RELEASE = f'{PRJ_NAME}_v{VERSION}'
MO_FILE = f'{PRJ_NAME}.mo'
SOURCE_DIR = '../src/'
TEST_DIR = '../test/'
SOURCE_FILE = f'{SOURCE_DIR}{PRJ_NAME}_.py'
TEST_FILE = f'{TEST_DIR}{PRJ_NAME}.py'
BUILD_BASE = '../build'
BUILD_DIR = f'{BUILD_BASE}/{RELEASE}'
DIST_DIR = '../dist'
ICON_DIR = f'{SOURCE_DIR}icons'
CSS_DIR = f'../../novxlib/css'

distFiles = [
    (TEST_FILE, BUILD_DIR),
    (f'{SOURCE_DIR}setuplib.py', BUILD_DIR),
    (f'{SOURCE_DIR}relocate.py', BUILD_DIR),
    ('../LICENSE', BUILD_DIR),
]


def add_css():
    print('\nAdding css ...')
    copytree(CSS_DIR, f'{BUILD_DIR}/css')


def add_icons():
    print('\nAdding icon files ...')
    copytree(ICON_DIR, f'{BUILD_DIR}/icons')


def build_application():
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

    if not build_tools.make_pot(TEST_FILE, app=PRJ_NAME, version=VERSION):
        sys.exit(1)

    translation = translate_de.main(
        MO_FILE, app=PRJ_NAME, version=VERSION)
    if translation is None:
        sys.exit(1)

    i18Dir, moDir = translation
    distFiles.append(
        (f'{i18Dir}/{moDir}/{MO_FILE}', f'{BUILD_DIR}/{moDir}')
        )


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


def rewrite_landing_page():
    print(f'\nRewriting "{LANDING_PAGE}" ...')
    with open(LANDING_PAGE_TEMPLATE, 'r', encoding='utf_8') as f:
        text = f.read().replace('0.99.0', VERSION)
    with open(LANDING_PAGE, 'w', encoding='utf_8', newline='\n') as f:
        f.write(text)


def write_version_ini():
    print(f'\nRewriting "{VERSION_INI_PATH}" ...')
    with open(VERSION_INI_PATH, 'w', encoding='utf_8', newline='\n') as f:
        f.write(VERSION_INI)


def main():
    build_application()
    build_translation()
    prepare_package()
    add_icons()
    add_css()
    build_package()
    clean_up()
    write_version_ini()
    rewrite_landing_page()


if __name__ == '__main__':
    main()
