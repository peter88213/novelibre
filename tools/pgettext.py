"""Provide a pygettext substitute.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novxlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
VERSION = '0.3'

import os
import sys
import re
from string import Template
from datetime import datetime

msgPatterns = [re.compile(r'_\(\"(.+?)\"\)'),
              re.compile(r'_\(\'(.+?)\'\)'),
              ]

potHeader = '''\
# ${app} Dictionary
# Copyright (C) 2023 Peter Triesberger
#
msgid ""
msgstr ""
"Project-Id-Version: ${appVersion}\\n"
"POT-Creation-Date: ${datetime}\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language: LANGUAGE\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: novxlib pgettext.py ${version}\\n"

'''
POT_FILE = '../i18n/messages.pot'


class PotFile:
    """GNU gettext pot file generator.
    
    Recursive source code scanner looking for message strings.
    Escape double quotes in messages.
    This works also for Python 3.6+ f-strings.   
    """

    def __init__(self, filePath='messages.pot', app='', appVersion='unknown'):
        self.filePath = filePath
        self.msgList = []
        self.app = app
        self.appVersion = appVersion

    def write_pot(self):
        msgMap = {'app':self.app,
                'appVersion': self.appVersion,
                'datetime':datetime.today().replace(microsecond=0).isoformat(sep=' '),
                'version': VERSION,
                }
        hdTemplate = Template(potHeader)
        potText = hdTemplate.safe_substitute(msgMap)
        self.msgList = list(set(self.msgList))
        self.msgList.sort()
        for message in self.msgList:
            message = message.replace('"', '\\"')
            entry = f'\nmsgid "{message}"\nmsgstr ""\n'
            potText += entry
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write(potText)
            print(f'\nPot file "{self.filePath}" written.')

    def get_messages(self, text):
        result = []
        for msgPattern in msgPatterns:
            result.extend(msgPattern.findall(text))
        return result

    def scan_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            print(f'Processing "{filename}"...')
        self.msgList.extend(self.get_messages(text))

    def scan_dir(self, path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.name.endswith('.py') and entry.is_file():
                    file = f'{entry.path}'.replace('\\', '/')
                    self.scan_file(file)
                elif entry.is_dir():
                    self.scan_dir(entry.path)


def main(path):
    # Generate a template file (pot) for message translation.
    print(f'Writing "{POT_FILE}" ...')
    if os.path.isfile(POT_FILE):
        os.replace(POT_FILE, f'{POT_FILE}.bak')
        backedUp = True
    else:
        backedUp = False
    try:
        pot = PotFile(POT_FILE)
        pot.scan_dir(path)
        pot.write_pot()
    except Exception as ex:
        if backedUp:
            os.replace(f'{POT_FILE}.bak', POT_FILE)
        print(f'ERROR: Cannot write file: "{POT_FILE}".\n{ex}')


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except:
        path = '.'
    main(path)
