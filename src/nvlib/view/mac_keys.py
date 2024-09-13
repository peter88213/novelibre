"""Provide a class with key definitions for the Mac OS.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.view.generic_keys import GenericKeys


class MacKeys(GenericKeys):

    ADD_CHILD = ('<Command-Alt-n>', 'Cmd-Alt-N')
    ADD_ELEMENT = ('<Command-n>', 'Cmd-N')
    ADD_PARENT = ('<Command-Alt-Shift-N>', 'Cmd-Alt-Shift-N')
    CHAPTER_LEVEL = ('<Command-Alt-c>', 'Cmd-Alt-C')
    DETACH_PROPERTIES = ('<Command-Alt-d>', 'Cmd-Alt-D')
    FOLDER = ('<Command-p>', 'Cmd-P')
    LOCK_PROJECT = ('<Command-l>', 'Cmd-L')
    OPEN_PROJECT = ('<Command-o>', 'Cmd-O')
    QUIT_PROGRAM = ('<Command-q>', 'Cmd-Q')
    RELOAD_PROJECT = ('<Command-r>', 'Cmd-R')
    RESTORE_BACKUP = ('<Command-b>', 'Cmd-B')
    SAVE_AS = ('<Command-S>', 'Cmd-Shift-S')
    SAVE_PROJECT = ('<Command-s>', 'Cmd-S')
    TOGGLE_PROPERTIES = ('<Command-Alt-t>', 'Cmd-Alt-T')
    TOGGLE_VIEWER = ('<Command-t>', 'Cmd-T')
    UNLOCK_PROJECT = ('<Command-u>', 'Cmd-U')
