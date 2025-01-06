"""Generate German translation files for GNU gettext.

- Update the project's 'de.po' translation file.
- Generate the language specific 'novelibre.mo' dictionary.

Usage: 
translate_de.py

File structure:

├── novelibre/
│   ├── i18n/
│   │   └── de.json
│   └── tools/
│       ├── translate_de.py
│       ├── translations.py
│       └── msgfmt.py
└── (app)/
    └── i18n/
        ├── messages.pot
        ├── de.po
        └── locale/
            └─ de/
               └─ LC_MESSAGES/
                  └─ (moFile)
    
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copyfile
import sys

import msgfmt
import translations

I18_DIR = '../i18n'
MO_DIR = 'locale/de/LC_MESSAGES'
PO_FILE = 'de.po'
MO_COPY_DIR = '../../novelibre/src/locale/de/LC_MESSAGES'


def main(moFile, app='', version='unknown', languages='', translator='unknown'):
    if not translations.main(
        'de',
        app=app,
        appVersion=version,
        json=True,
        languages=languages,
        translator=translator
        ):
        sys.exit(1)

    moDir = f'{I18_DIR}/{MO_DIR}'
    poPath = f'{I18_DIR}/{PO_FILE}'
    moPath = f'{I18_DIR}/{MO_DIR}/{moFile}'
    moCopyPath = f'{MO_COPY_DIR}/{moFile}'
    os.makedirs(moDir, exist_ok=True)
    os.makedirs(MO_COPY_DIR, exist_ok=True)
    print(f'Writing "{moFile}" ...')
    msgfmt.make(poPath, moPath)
    copyfile(moPath, moCopyPath)
    return I18_DIR, MO_DIR


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        main()
