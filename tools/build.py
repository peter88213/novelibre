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

import translate_de
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import build_tools

APP = 'novelibre'
VERSION = '4.7.1'
RELEASE = f'{APP}_v{VERSION}'

SOURCE_DIR = '../src/'
TEST_DIR = '../test/'
SOURCE_FILE = f'{SOURCE_DIR}novelibre_.py'
TEST_FILE = f'{TEST_DIR}novelibre.py'
BUILD_BASE = '../build'
BUILD_DIR = f'{BUILD_BASE}/{RELEASE}'
DIST_DIR = '../dist'


def collect_dist(buildDir):
    print(f'Copying "{TEST_FILE}" to "{buildDir}" ...')
    copy2(TEST_FILE, buildDir)


def build_app():
    os.makedirs(TEST_DIR, exist_ok=True)
    build_tools.inline_modules(SOURCE_FILE, TEST_FILE)
    build_tools.insert_version_number(TEST_FILE, version=VERSION)
    if not build_tools.make_pot(TEST_FILE, app=APP, version=VERSION):
        sys.exit(1)


def build_package():
    print(f'Providing empty "{DIST_DIR}" ...')
    try:
        rmtree(DIST_DIR)
    except FileNotFoundError:
        pass
    os.makedirs(DIST_DIR)
    build_tools.make_pyz(BUILD_DIR, f'{DIST_DIR}/{RELEASE}')
    build_tools.make_zip(BUILD_DIR, f'{DIST_DIR}/{RELEASE}')


def build_translation():
    if not translate_de.main(version=VERSION):
        sys.exit(1)


def prepare_package():
    print(f'Providing empty "{BUILD_DIR}" ...')
    try:
        rmtree(BUILD_BASE)
    except FileNotFoundError:
        pass
    os.makedirs(BUILD_DIR)
    collect_dist(BUILD_DIR)


def main():
    build_app()
    build_translation()
    prepare_package()
    build_package()


if __name__ == '__main__':
    main()
