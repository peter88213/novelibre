"""Generate German translation files for GNU gettext.

- Update the project's 'de.po' translation file.
- Generate the language specific 'novelibre.mo' dictionary.

Usage: 
translate_de.py

File structure:

├── novxlib/
│   ├── i18n/
│   │   └── de.json
│   └── src/
│       ├── translations.py
│       └── msgfmt.py
└── novelibre/
    ├── src/ 
    ├── tools/ 
    │   └── translate_de.py
    └── i18n/
        ├── messages.pot
        ├── de.po
        └── locale/
            └─ de/
               └─ LC_MESSAGES/
                  └─ novelibre.mo
    
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from shutil import copyfile
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import translations
import msgfmt

APP_NAME = 'novelibre'
I18_DIR = '../i18n'
MO_DIR = f'{I18_DIR}/locale/de/LC_MESSAGES'
PO_PATH = f'{I18_DIR}/de.po'
MO_PATH = f'{MO_DIR}/novelibre.mo'
MO_COPY = '../src/locale/de/LC_MESSAGES/novelibre.mo'


def main(version='unknown'):
    if not translations.main('de', app=APP_NAME, appVersion=version, json=True):
        return False

    os.makedirs(MO_DIR, exist_ok=True)
    print(f'Writing "{MO_PATH}" ...')
    msgfmt.make(PO_PATH, MO_PATH)
    copyfile(MO_PATH, MO_COPY)
    return True


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        main()
