"""Provide a class to handle GNU gettext translation files.

This module can be used as a standalone script.

Usage: 
translations.py language-code

File structure:

├── novelibre/
│   ├── i18n/
│   │   └── <language>.json
│   └── tools/
│       └── translations.py
└── <plugin>/
    ├── i18n/ 
    │   ├── messages.pot
    │   └── <language>.po
    └── tools/
        └── <calling script>

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import sys
import os
import json
from string import Template
from datetime import datetime

POT_PATH = '../i18n'
JSON_PATH = '../../novelibre/i18n'

poHeader = '''\
# $app Dictionary ($languages)
# Copyright (C) $year $translator
#
msgid ""
msgstr ""
"Project-Id-Version: $appVersion\\n"
$potCreationLine
"PO-Revision-Date: $datetime\\n"
"Last-Translator: $translator\\n"
"Language: $languageCode\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"


'''


class Translations:
    """Class to handle GNU gettext translation files.
    
    - .po file and .pot file are in the same directory.
    - Existing translations are used.
    - Missing translations are taken from a JSON dictionary, if any.
    - The JSON dictionary is updated by translations found in the initial '.po' file.
    """

    def __init__(self,
                 languageCode,
                 app='',
                 appVersion='unknown',
                 potFile='messages.pot',
                 languages='',
                 translator='unknown',
                 ):
        self.poFile = f'{POT_PATH}/{languageCode}.po'
        self.potFile = f'{POT_PATH}/{potFile}'
        self.lngFile = f'{JSON_PATH}/{languageCode}.json'
        self.msgDict = {}
        self.msgList = []
        self.header = ''
        currentDateTime = datetime.today().replace(microsecond=0).isoformat(sep=" ")
        self.msgMap = {
            'app': app,
            'appVersion': appVersion,
            'datetime':currentDateTime,
            'potCreationLine':f'"POT-Creation-Date: {currentDateTime}\\n"',
            'languages':languages,
            'translator':translator,
            'languageCode':languageCode,
            'year':datetime.today().year,
        }

    def read_pot(self):
        """Read the messages of the '.pot' file.
        
        Parse the file and collect messages in msgList.
        """
        msgCount = 0
        print(f'Reading "{self.potFile}" ...')
        with open(self.potFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        inHeader = True
        for line in lines:
            line = line.strip()
            if line.startswith('msgid ""'):
                pass
            elif inHeader:
                if line.startswith('"POT-Creation-Date'):
                    self.msgMap['potCreationLine'] = line
                elif line.startswith('msgid "'):
                    inHeader = False
            if not inHeader:
                if line.startswith('msgid "'):
                    self.msgList.append(self._extract_text('msgid "', line))
                    msgCount += 1
            self.msgList.sort()
        print(f'{msgCount} entries read.')

    def read_json(self):
        """Read a JSON translation file and add the translations to msgDict.
        
        Return True in case of success.
        Return False, if the file cannot be read. 
        """
        try:
            with open(self.lngFile, 'r', encoding='utf-8') as f:
                print(f'Reading "{self.lngFile}" ...')
                msgDict = json.load(f)
            for message in msgDict:
                self.msgDict[message] = msgDict[message]
            print(f'{len(self.msgDict)} translations total.')
            return True

        except Exception as ex:
            print(str(ex))
            return False

    def write_json(self):
        """Add translations to a JSON translation file.
        
        Create a backup file.
        Return True in case of success.
        Return False, if the file cannot be written. 
        """
        if os.path.isfile(self.lngFile):
            os.replace(self.lngFile, f'{self.lngFile}.bak')
            backedUp = True
        else:
            backedUp = False
        try:
            with open(self.lngFile, 'w', encoding='utf-8') as f:
                print(f'Writing "{self.lngFile}" ...')
                msgDict = {}
                # dict for non-empty entries
                for msg in self.msgDict:
                    if self.msgDict[msg]:
                        msgDict[msg] = self.msgDict[msg]
                json.dump(msgDict, f, ensure_ascii=False, sort_keys=True, indent=2)
                print(f'{len(self.msgDict)} translations written.')
            return True

        except Exception as ex:
            if backedUp:
                os.replace(f'{self.lngFile}.bak', self.lngFile)
            print(f'ERROR: Cannot write file: "{self.lngFile}".\n{str(ex)}')
            return False

    def read_po(self):
        """Read the existing translations of the '.po' file.
        
        Parse the file and collect translations in msgDict.
        """

        # Create the header.
        hdTemplate = Template(poHeader)
        self.header = hdTemplate.safe_substitute(self.msgMap)

        print(f'Reading "{self.poFile}" ...')
        try:
            with open(self.poFile, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print('Not found.')
            return

        inHeader = True
        msgCount = 0
        for line in lines:
            line = line.strip()
            if line.startswith('msgid ""'):
                pass
            elif inHeader:
                if line.startswith('msgid "'):
                    inHeader = False
            if not inHeader:
                if line.startswith('msgid "'):
                    message = self._extract_text('msgid "', line)
                    msgCount += 1
                elif line.startswith('msgstr "'):
                    translation = self._extract_text('msgstr "', line)
                    if translation:
                        self.msgDict[message] = translation
        print(f'{msgCount} entries read.')
        print(f'{len(self.msgDict)} translations total.')

    def write_po(self):
        """Write translations to the '.po' file.

        Return True, if all messages have translations.
        Return False, if messages need to be translated. 
        """
        lines = [self.header]
        missingCount = 0
        msgCount = 0
        for message in self.msgList:
            try:
                translation = self.msgDict[message]
            except:
                translation = ''
            lines.append(f'msgid "{message}"\nmsgstr "{translation}"\n\n')
            if not translation:
                print(f'Translation missing for "{message}".')
                missingCount += 1
            msgCount += 1
        print(f'Writing "{self.poFile}" ...')
        if os.path.isfile(self.poFile):
            os.replace(self.poFile, f'{self.poFile}.bak')
            backedUp = True
        else:
            backedUp = False
        try:
            with open(self.poFile, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as ex:
            if backedUp:
                os.replace(f'{self.poFile}.bak', self.poFile)
            print(f'ERROR: Cannot write file: "{self.poFile}".\n{str(ex)}')
            return False

        if missingCount > 0:
            print(f'NOTE: {missingCount} translations missing.')
            return False

        print(f'{msgCount} entries written.')
        return True

    def _extract_text(self, prefix, line):
        firstPos = len(prefix)
        lastPos = len(line) - 1
        message = line[firstPos:lastPos]
        return message


def main(languageCode,
         app='',
         appVersion='unknown',
         potFile='messages.pot',
         json=False,
         languages='',
         translator='unknown'
         ):
    """Update a '.po' translation file.
    
    - Add missing entries from the '.pot' template file.
    
    If json is True:
    - Add missing translations from the JSON dictionary to the '.po' file.
    - Update the JSON dictionary from the '.po' file.
    
    Return True, if all messages have translations.
    Return False, if messages need to be translated. 
    """
    translations = Translations(
        languageCode,
        app=app,
        appVersion=appVersion,
        potFile=potFile,
        languages=languages,
        translator=translator,
        )
    if json:
        translations.read_json()
    translations.read_pot()
    translations.read_po()
    if json:
        translations.write_json()
    if translations.write_po():
        return True
    else:
        return False


if __name__ == '__main__':
    if not main(sys.argv[1]):
        sys.exit(1)
