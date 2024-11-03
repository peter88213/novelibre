"""Helper module for opening documents.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.novx_globals import norm_path


def open_document(document):
    """Open a document with the operating system's standard application."""
    try:
        os.startfile(norm_path(document))
        # Windows
    except:
        try:
            os.system('xdg-open "%s"' % norm_path(document))
            # Linux
        except:
            try:
                os.system('open "%s"' % norm_path(document))
                # Mac
            except:
                pass
