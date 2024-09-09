"""Provide a class for novelibre application and plugin package building. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novxlib
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC
import os
from shutil import copy2
from shutil import copytree
from shutil import make_archive
from shutil import rmtree
import sys
import zipapp

import inliner
import pgettext
import translate_de


class PackageBuilder(ABC):

    GERMAN_TRANSLATION = False

    def __init__(self, version):
        self.version = version
        self.versionIni = f'''[LATEST]
version = {self.version}
download_link = https://github.com/peter88213/{self.PRJ_NAME}/raw/main/dist/{self.PRJ_NAME}_v{self.version}.pyzw
'''
        self.versionIniPath = '../VERSION'
        self.landingPage = '../README.md'
        self.landingPageTemplate = '../docs/template/README.md'

        self.release = f'{self.PRJ_NAME}_v{self.version}'
        self.moFile = f'{self.PRJ_NAME}.mo'
        self.sourceDir = '../src/'
        self.testDir = '../test/'
        self.sourceFile = f'{self.sourceDir}{self.PRJ_NAME}.py'
        self.testFile = f'{self.testDir}{self.PRJ_NAME}.py'
        self.buildBase = '../build'
        self.buildDir = f'{self.buildBase}/{self.release}'
        self.distDir = '../dist'
        self.iconDir = f'{self.sourceDir}icons'
        self.sampleDir = '../sample'

        self.distFiles = [
            (self.testFile, self.buildDir),
            (f'{self.sourceDir}setuplib.py', self.buildDir),
            ('../LICENSE', self.buildDir),
        ]

    def add_extras(self):
        pass

    def add_icons(self):
        print('\nAdding icon files ...')
        copytree(self.iconDir, f'{self.buildDir}/icons')

    def add_sample(self):
        print('\nAdding sample files ...')
        SAMPLE_DIR = '../sample'
        copytree(SAMPLE_DIR, f'{self.buildDir}/{self.PRJ_NAME}_sample')

    def build_package(self):
        print(f'\nProviding empty "{self.distDir}" ...')
        try:
            rmtree(self.distDir)
        except FileNotFoundError:
            pass
        os.makedirs(self.distDir)
        self.make_pyz(self.buildDir, self.distDir, self.release)
        self.make_zip(self.buildDir, self.distDir, self.release)

    def build_script(self):
        os.makedirs(self.testDir, exist_ok=True)
        inliner.run(self.sourceFile, self.testFile, self.LOCAL_LIB, self.sourceDir)
        self.inline_modules(self.testFile, self.testFile)
        self.insert_version_number(self.testFile, version=self.version)

    def build_translation(self):
        if not self.GERMAN_TRANSLATION:
            return

        if not self.make_pot(self.testFile, app=self.PRJ_NAME, version=self.version):
            sys.exit(1)

        translation = translate_de.main(
            self.moFile, app=self.PRJ_NAME, version=self.version)
        if translation is None:
            sys.exit(1)

        i18Dir, moDir = translation
        self.distFiles.append(
            (f'{i18Dir}/{moDir}/{self.moFile}', f'{self.buildDir}/{moDir}')
            )

    def clean_up(self):
        print(f'\nRemoving "{self.testFile}" ...')
        os.remove(self.testFile)

    def collect_dist_files(self, distFiles):
        for file, targetDir in distFiles:
            os.makedirs(targetDir, exist_ok=True)
            print(f'Copying "{file}" to "{targetDir}" ...')
            copy2(file, targetDir)

    def inline_modules(self, source, target):
        """Inline all non-standard library modules."""
        NVLIB = 'nvlib'
        NV_PATH = '../../novelibre/src/'
        NOVXLIB = 'novxlib'
        NOVX_PATH = '../../novxlib/src/'
        inliner.run(source, target, NVLIB, NV_PATH)
        inliner.run(target, target, NOVXLIB, NOVX_PATH)

    def insert_version_number(self, source, version='unknown'):
        """Write the actual version string and make sure that Unix EOL is used."""
        with open(source, 'r', encoding='utf_8') as f:
            text = f.read().replace('@release', version)
        with open(source, 'w', encoding='utf_8', newline='\n') as f:
            f.write(text)
        print(f'Version {version} set.')

    def make_pot(self, sourcefile, app='', version='unknown'):
        """Generate a pot file for translations from the source file."""
        I18_DIR = '../i18n'
        potFile = f'{I18_DIR}/messages.pot'
        os.makedirs(I18_DIR, exist_ok=True)
        if os.path.isfile(potFile):
            os.replace(potFile, f'{potFile}.bak')
            backedUp = True
        else:
            backedUp = False
        try:
            pot = pgettext.PotFile(potFile, app=app, appVersion=version)
            pot.scan_file(sourcefile)
            print(f'Writing "{pot.filePath}"...\n')
            pot.write_pot()
            return True

        except Exception as ex:
            if backedUp:
                os.replace(f'{potFile}.bak', potFile)
            print(str(ex))
            return False

    def make_pyz(self, sourceDir, targetDir, release):
        targetFile = f'{targetDir}/{release}.pyzw'
        print(f'Writing "{targetFile}" ...')
        zipapp.create_archive(
            sourceDir,
            targetFile,
            main='setuplib:main',
            compressed=True
            )

    def make_zip(self, sourceDir, targetDir, release):
        copy2('../src/setup.pyw', sourceDir)
        copy2('../docs/usage.md', f'{sourceDir}/README.md')
        target = f'{targetDir}/{release}'
        print(f'Writing "{target}.zip" ...')
        make_archive(target, 'zip', sourceDir)

    def prepare_package(self):
        print(f'\nProviding empty "{self.buildDir}" ...')
        try:
            rmtree(self.buildBase)
        except FileNotFoundError:
            pass
        self.collect_dist_files(self.distFiles)
        self.insert_version_number(
            f'{self.buildDir}/setuplib.py',
            version=self.version
            )

    def rewrite_landing_page(self):
        print(f'\nRewriting "{self.landingPage}" ...')
        with open(self.landingPageTemplate, 'r', encoding='utf_8') as f:
            text = f.read().replace('0.99.0', self.version)
        with open(self.landingPage, 'w', encoding='utf_8', newline='\n') as f:
            f.write(text)

    def run(self):
        self.build_script()
        self.build_translation()
        self.prepare_package()
        self.add_extras()
        self.build_package()
        self.clean_up()
        self.write_version_ini()
        self.rewrite_landing_page()
        print('\nDone')

    def write_version_ini(self):
        print(f'\nRewriting "{self.versionIniPath}" ...')
        with open(self.versionIniPath, 'w', encoding='utf_8', newline='\n') as f:
            f.write(self.versionIni)

