"""Locale settings for novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import gettext
import locale
import os
import sys

#--- Initialize localization.
try:
    # Check whether the importing module is already localized.
    LOCALE_PATH
except NameError:
    locale.setlocale(locale.LC_TIME, "")
    LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
    try:
        CURRENT_LANGUAGE = locale.getlocale()[0][:2]
    except:
        # Fallback for old Windows versions.
        CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
    try:
        t = gettext.translation('novelibre', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
        _ = t.gettext
    except:

        def _(message):
            return message

