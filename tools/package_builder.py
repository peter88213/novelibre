"""Provide a class for novelibre application and plugin package building. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
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


def output(message):
    print(f'(package_builder) {message}')


class PackageBuilder(ABC):

    GERMAN_TRANSLATION = False

    def __init__(self, version):
        self.version = version
        self.versionIni = f'''[LATEST]
version = {self.version}
download_link = https://github.com/peter88213/{self.PRJ_NAME}/raw/main/dist/{self.PRJ_NAME}_v{self.version}.pyz
'''
        self.setupScript = '''#!/usr/bin/python3
import setuplib

setuplib.main(False)
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
        self.sampleSource = '../sample'
        self.sampleTarget = f'{self.buildDir}/sample'

        self.distFiles = [
            (self.testFile, self.buildDir),
            (f'{self.sourceDir}setuplib.py', self.buildDir),
            ('../LICENSE', self.buildDir),
        ]

    def add_extras(self):
        """Hook for project specific content."""
        pass

    def add_icons(self):
        """Copy icon files into the package directory."""
        output('Adding icon files ...')
        copytree(self.iconDir, f'{self.buildDir}/icons')

    def add_sample(self):
        """Copy sample files into the package directory."""
        output('Adding sample files ...')
        copytree(self.sampleSource, self.sampleTarget)

    def build_package(self):
        """Pack the contents of the package directory."""
        output(f'\nProviding empty "{self.distDir}" ...')
        try:
            rmtree(self.distDir)
        except FileNotFoundError:
            pass
        os.makedirs(self.distDir)
        self.create_pyz(self.buildDir, self.distDir, self.release)
        self.make_zip(self.buildDir, self.distDir, self.release)

    def build_script(self):
        """Generate the application/plugin script in the test directory."""
        output(f'\nInlining the code of the non-standard libraries ...')
        os.makedirs(self.testDir, exist_ok=True)
        inliner.run(self.sourceFile, self.testFile, self.LOCAL_LIB, self.sourceDir)
        self.inline_modules(self.testFile, self.testFile)
        self.insert_version_number(self.testFile, version=self.version)

    def build_translation(self):
        """Generate the German language file for the distribution."""
        if not self.GERMAN_TRANSLATION:
            return

        output('Collecting the strings to translate ...')
        if not self.create_pot(
            self.testFile,
            app=self.PRJ_NAME,
            version=self.version
        ):
            sys.exit(1)

        output('Creating/updating the translations ...')
        translation = translate_de.main(
            self.moFile,
            app='novelibre',
            version=self.version,
        )
        i18Dir, moDir = translation
        self.distFiles.append(
            (f'{i18Dir}/{moDir}/{self.moFile}', f'{self.buildDir}/{moDir}')
        )

    def create_pot(self, sourcefile, app='', version='unknown'):
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
            pot = pgettext.PotFile(
                potFile,
                app=app,
                appVersion=version
            )
            pot.scan_file(sourcefile)
            output(f'Writing "{pot.filePath}" ...')
            pot.write_pot()
            return True

        except Exception as ex:
            if backedUp:
                os.replace(f'{potFile}.bak', potFile)
            output(str(ex))
            return False

    def clean_up(self):
        """Remove the application/plugin script from the test directory."""
        output(f'Removing "{self.testFile}" ...')
        os.remove(self.testFile)

    def collect_dist_files(self, distFiles):
        """Copy the listed distribution files into the package directory."""
        for file, targetDir in distFiles:
            os.makedirs(targetDir, exist_ok=True)
            output(f'Copying "{file}" to "{targetDir}" ...')
            copy2(file, targetDir)

    def inline_modules(self, source, target):
        """Inline all non-standard library modules."""
        inliner.run(
            source,
            target,
            'nvlib',
            '../../novelibre/src/',
        )

    def insert_version_number(self, source, version='unknown'):
        """Write the actual version string and make sure that Unix EOL is used."""
        with open(source, 'r', encoding='utf_8') as f:
            text = f.read().replace('@release', version)
        with open(source, 'w', encoding='utf_8', newline='\n') as f:
            f.write(text)
        output(f'Version {version} set.')

    def create_pyz(self, sourceDir, targetDir, release):
        """Create the self-extracting installation file."""
        targetFile = f'{targetDir}/{release}.pyz'
        output(f'Writing "{targetFile}" ...')
        zipapp.create_archive(
            sourceDir,
            targetFile,
            main='setuplib:main',
            compressed=True
        )

    def make_zip(self, sourceDir, targetDir, release):
        """Create the alternative zip file."""
        self.write_setup_script(sourceDir)
        copy2('../docs/usage.md', f'{sourceDir}/README.md')
        target = f'{targetDir}/{release}'
        output(f'Writing "{target}.zip" ...')
        make_archive(target, 'zip', sourceDir)

    def prepare_package(self):
        """Create the package directory and populate it with the basic files."""
        output(f'\nProviding empty "{self.buildDir}" ...')
        try:
            rmtree(self.buildBase)
        except FileNotFoundError:
            pass
        self.collect_dist_files(self.distFiles)
        self.insert_version_number(
            f'{self.buildDir}/setuplib.py',
            version=self.version
        )

    def run(self):
        output(f'*** Building the {self.PRJ_NAME} version {self.version} distribution ***')
        self.build_script()
        self.build_translation()
        self.prepare_package()
        self.add_extras()
        self.build_package()
        self.clean_up()
        self.write_version_ini()
        self.update_landing_page()
        output('Done')

    def update_landing_page(self):
        """Update the version numbers for download link and documantation."""
        output(f'\nUpdating "{self.landingPage}" ...')
        with open(self.landingPageTemplate, 'r', encoding='utf_8') as f:
            text = f.read().replace('0.99.0', self.version)
        with open(
            self.landingPage,
            'w',
            encoding='utf_8',
            newline='\n'
        ) as f:
            f.write(text)

    def write_setup_script(self, filePath):
        """Create the setup script for manual installatin from the zip file."""
        output(f'\nCreating the setup script ...')
        with open(
            f'{filePath}/setup.py',
            'w', encoding='utf_8',
            newline='\n'
        ) as f:
            f.write(self.setupScript)

    def write_version_ini(self):
        """Create an INI file with version information and download link."""
        output(f'\nRewriting "{self.versionIniPath}" ...')
        with open(
            self.versionIniPath,
            'w', encoding='utf_8',
            newline='\n'
        ) as f:
            f.write(self.versionIni)

