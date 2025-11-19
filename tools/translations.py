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

from datetime import datetime
import json
import os
from string import Template
import sys

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


def output(message):
    print(f'(translations) {message}')


class Translations:
    """Class to handle GNU gettext translation files.
    
    - .po file and .pot file are in the same directory.
    - Existing translations are used.
    - Missing translations are taken from a JSON dictionary, if any.
    - The JSON dictionary is updated by translations found in the initial '.po' file.
    """

    def __init__(
        self,
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
        self.potMsgList = []
        self.jsonMsgDict = {}
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
        
        Parse the file and collect messages in potMsgList.
        """
        msgCount = 0
        output(f'Reading "{self.potFile}" ...')
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
                    self.potMsgList.append(self._extract_text('msgid "', line))
                    msgCount += 1
            self.potMsgList.sort()
        output(f'{msgCount} entries read.')

    def read_json(self):
        """Read a JSON dictionary and add the translations to jsonMsgDict.
        
        Return True in case of success.
        Return False, if the file cannot be read. 
        """
        try:
            output(f'Reading "{self.lngFile}" ...')
            with open(self.lngFile, 'r', encoding='utf-8') as f:
                self.jsonMsgDict = json.load(f)
            output(f'{len(self.jsonMsgDict)} translations total.')
            return True

        except Exception as ex:
            output(str(ex))
            return False

    def read_po(self):
        """Read the existing translations of the '.po' file.
        
        Parse the file and collect translations in jsonMsgDict.
        """

        output(f'Reading "{self.poFile}" ...')
        try:
            with open(self.poFile, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            output('Not found.')
            return

        inHeader = True
        msgCount = 0
        newMsgCount = 0
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
                    poTranslation = self._extract_text('msgstr "', line)
                    dictTranslation = self.jsonMsgDict.get(message, '')
                    if poTranslation and not dictTranslation:
                        self.jsonMsgDict[message] = poTranslation
                        newMsgCount += 1
        output(f'{msgCount} entries read.')
        output(f'{newMsgCount} new translations found.')

    def update_json(self):
        """Add new translations to a JSON translation file.
        
        Create a backup file.
        Return True in case of success.
        Return False, if the file cannot be written. 
        """
        backedUp = False
        try:
            if os.path.isfile(self.lngFile):
                with open(self.lngFile, 'r', encoding='utf-8') as f:
                    msgDict = json.load(f)
            else:
                msgDict = {}
            newMsgCount = 0
            for msg in self.jsonMsgDict:
                if not msgDict.get(msg, ''):
                    msgDict[msg] = self.jsonMsgDict[msg]
                    newMsgCount += 1
            if newMsgCount == 0:
                output(f'"{self.lngFile}" remains unchanged (total: {len(msgDict)}).')
                return True

            output(f'Writing "{self.lngFile}" ...')
            if os.path.isfile(self.lngFile):
                os.replace(self.lngFile, f'{self.lngFile}.bak')
                backedUp = True
            with open(self.lngFile, 'w', encoding='utf-8') as f:
                json.dump(
                    msgDict,
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2
                )
                output(f'{newMsgCount} translations added to {self.lngFile} (total: {len(msgDict)}).')
            return True

        except Exception as ex:
            if backedUp:
                os.replace(f'{self.lngFile}.bak', self.lngFile)
            output(f'ERROR: Cannot write file: "{self.lngFile}".\n{str(ex)}')
            return False

    def write_po(self):
        """Write translations to the '.po' file.

        Return True, if all messages have translations.
        Return False, if messages need to be translated. 
        """
        lines = [
            Template(poHeader).safe_substitute(self.msgMap),
        ]
        missingCount = 0
        msgCount = 0
        for message in self.potMsgList:
            translation = self.jsonMsgDict.get(message, '')
            lines.append(f'msgid "{message}"\nmsgstr "{translation}"\n\n')
            if not translation:
                output(f'Translation missing for "{message}".')
                missingCount += 1
            msgCount += 1
        output(f'Writing "{self.poFile}" ...')
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
            output(f'ERROR: Cannot write file: "{self.poFile}".\n{str(ex)}')
            return False

        if missingCount > 0:
            output(f'NOTE: {missingCount} translations missing.')
            return False

        output(f'{len(self.potMsgList)} entries written.')
        return True

    def _extract_text(self, prefix, line):
        firstPos = len(prefix)
        lastPos = len(line) - 1
        message = line[firstPos:lastPos]
        return message

    def run(self):
        """Update a '.po' translation file.
        
        - Add missing entries from the '.pot' template file.
        - Add missing translations from the JSON dictionary to the '.po' file.
        - Update the JSON dictionary from the '.po' file.
        
        Return True, if all messages have translations.
        Return False, if messages need to be translated. 
        """
        self.read_json()
        self.read_pot()
        self.read_po()
        self.update_json()
        if self.write_po():
            return True
        else:
            return False


def main(
        languageCode,
        app='',
        appVersion='unknown',
        potFile='messages.pot',
        languages='',
        translator='unknown'
    ):
    return Translations(
        languageCode,
        app,
        appVersion,
        potFile,
        languages,
        translator
    ).run()


if __name__ == '__main__':
    if not main(sys.argv[1]):
        sys.exit(1)
