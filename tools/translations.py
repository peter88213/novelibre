"""Update the .po and .json translation files.

Requires Python 3.9+

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import json
import os


def output(message):
    print(f'(translations) {message}')


class PoFile:

    def __init__(self, filePath):
        self.filePath = filePath
        self.headings = []
        self.data = {}
        self.messages = {}

    def read(self):
        output(f'Reading "{self.filePath}" ...')
        with open(self.filePath, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        self.headings.clear()
        self.data.clear()
        self.messages.clear()
        self._msgid = None
        inHeader = True
        for line in lines:
            line = line.strip()
            if line.startswith('msgid ""'):
                pass
            elif inHeader:
                if line.startswith('#'):
                    self.headings.append(line)
                elif line.startswith('"'):
                    line = line.strip('"').removesuffix('\\n')
                    key, value = line.split(': ')
                    self.data[key] = value
                elif line.startswith('msgid "'):
                    inHeader = False
            if not inHeader:
                if line.startswith('msgid "'):
                    self._msgid = line.removeprefix('msgid "').rstrip('"')
                    self.messages[self._msgid] = ''
                elif line.startswith('msgstr "'):
                    msgstr = line.removeprefix('msgstr "').rstrip('"')
                    self.messages[self._msgid] = msgstr
        output(f'{len(self.messages)} entries read.')

    def write(self, potMsgList, jsonMessages, version):
        """Write translations to the '.po' file, if there are changes.

        Create a backup file, if necessary.
        Raise RuntimeError, if messages need to be translated. 
        """
        missingCount = 0
        changesCount = 0
        messages = {}
        for msg in potMsgList:
            translation = jsonMessages.get(msg, '')
            if not translation:
                output(f'Translation missing for "{msg}".')
                missingCount += 1
            if self.messages.get(msg, None) != translation:
                changesCount += 1
            messages[msg] = translation
        self.messages = messages
        if version and self.data.get('Project-Id-Version', '') != version:
            self.data['Project-Id-Version'] = version
            changesCount += 1

        if changesCount == 0:
            output(
                f'"{self.filePath}" remains unchanged '
                f'(total: {len(self.messages)}).'
            )
        else:
            self.data['PO-Revision-Date'] = datetime.today().replace(
                microsecond=0).isoformat(sep=' ')

            lines = self.headings.copy()
            lines.append('msgid ""')
            lines.append('msgstr ""')

            if version is not None:
                self.data['Project-Id-Version'] = version
            for key in self.data:
                lines.append(f'"{key}: {self.data[key]}\\n"')

            lines.append('\n')
            for msg in self.messages:
                lines.append(f'msgid "{msg}"\nmsgstr "{self.messages[msg]}"\n')

            backedUp = False
            output(f'Writing "{self.filePath}" ...')
            try:
                if os.path.isfile(self.filePath):
                    os.replace(self.filePath, f'{self.filePath}.bak')
                    backedUp = True
                with open(self.filePath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
            except Exception as ex:
                if backedUp:
                    os.replace(f'{self.filePath}.bak', self.filePath)
                raise ex

            output(f'{len(self.messages)} entries written.')
        if missingCount > 0:
            output(f'NOTE: {missingCount} translations missing.')
            raise RuntimeError


class JsonDict:

    def __init__(self, filePath):
        self.filePath = filePath
        self.messages = {}

    def read(self):
        output(f'Reading "{self.filePath}" ...')
        with open(self.filePath, 'r', encoding='utf-8') as f:
            self.messages = json.load(f)
        output(f'{len(self.messages)} translations total.')

    def write(self, poMessages):
        """Add new translations to the JSON translation dictionary.
        
        Create a backup file, if necessary.
        """
        newMsgCount = 0
        for msg in poMessages:
            if not poMessages[msg]:
                continue

            if not self.messages.get(msg, ''):
                self.messages[msg] = poMessages[msg]
                newMsgCount += 1

        if newMsgCount == 0:
            output(
                f'"{self.filePath}" remains unchanged '
                f'(total: {len(self.messages)}).'
            )
            return

        backedUp = False
        output(f'Writing "{self.filePath}" ...')
        try:
            if os.path.isfile(self.filePath):
                os.replace(self.filePath, f'{self.filePath}.bak')
                backedUp = True
            with open(self.filePath, 'w', encoding='utf-8') as f:
                json.dump(
                    self.messages,
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2
                )
        except Exception as ex:
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise ex

        output(
            f'{newMsgCount} translations added to {self.filePath} '
            f'(total: {len(self.messages)}).'
        )


def main(potFilePath, poFilePath, jsonDictPath, version=None):
    potFile = PoFile(potFilePath)
    potFile.read()
    poFile = PoFile(poFilePath)
    poFile.read()
    jsonDict = JsonDict(jsonDictPath)
    jsonDict.read()
    jsonDict.write(poFile.messages)
    poFile.write(
        sorted(list(potFile.messages)),
        jsonDict.messages,
        version,
    )
    return poFile.data['Project-Id-Version']

