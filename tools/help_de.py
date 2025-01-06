"""Translate GUI terms in helpfiles to German 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import glob

REPLACE = {
    'Allee': 'Alle',
    'context menu': 'Kontextmenü',
    ' menu': '-Menü',
    'Tree view': 'Baumansicht',
    'tree view': 'Baumansicht',
    }


def process_file(sourcePath, targetPath):
    with open(sourcePath, 'r', encoding='utf-8') as f:
        page = f.read()
    for term in sortedTranslations:
        if term in page:
            page = page.replace(term, translations[term])
    for r in REPLACE:
        page = page.replace(r, REPLACE[r])
    with open(targetPath, 'w', encoding='utf-8') as f:
        f.write(page)


def read_translations(filePath):
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    msgid = ''
    for line in lines:
        if line.startswith('msgid'):
            msgid = line[7:].rstrip('"\n')
        elif len(msgid) > 2 and line.startswith('msgstr'):
            if not msgid in translations:
                translations[msgid] = line[8:].rstrip('"\n')


translations = {}
read_translations('../i18n/de.po')
read_translations('../../novelibre/i18n/de.po')

# Sort the terms by length to minimize errors.
sortedTranslations = sorted(translations, key=len, reverse=True)

os.makedirs('../docs/de', exist_ok=True)
process_file('../docs/usage.md', '../docs/de/usage.md')

if os.path.exists('../docs/help'):
    os.makedirs('../docs/de/help', exist_ok=True)
    for helpFile in glob.iglob('*.md', root_dir='../docs/help'):
        process_file(f'../docs/help/{helpFile}', f'../docs/de/help/{helpFile}')
