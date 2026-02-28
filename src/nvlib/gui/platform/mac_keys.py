"""Provide a class with key definitions for the Mac OS.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.generic_keys import GenericKeys
from nvlib.nv_locale import _


class MacKeys(GenericKeys):

    ADD_CHILD = ('<Command-Option-n>', 'Cmd-Option-N')
    ADD_ELEMENT = ('<Command-n>', 'Cmd-N')
    ADD_PARENT = ('<Command-Option-Shift-N>', 'Cmd-Option-Shift-N')
    CHAPTER_LEVEL = ('<Command-Option-c>', 'Cmd-Option-C')
    COPY = ('<Command-c>', 'Cmd-C')
    CUT = ('<Command-x>', 'Cmd-X')
    DETACH_PROPERTIES = ('<Command-Option-d>', 'Cmd-Option-D')
    FOLDER = ('<Command-p>', 'Cmd-P')
    FORWARD = ('<Option-Right>', f'{_("Option-Right")}')
    LOCK_PROJECT = ('<Command-l>', 'Cmd-L')
    NEXT = ('<Option-Down>', f'{_("Option-Down")}')
    OPEN_PROJECT = ('<Command-o>', 'Cmd-O')
    PASTE = ('<Command-v>', 'Cmd-V')
    PREVIOUS = ('<Option-Up>', f'{_("Option-Up")}')
    QUIT_PROGRAM = ('<Command-q>', 'Cmd-Q')
    RELOAD_PROJECT = ('<Command-r>', 'Cmd-R')
    RESTORE_BACKUP = ('<Command-b>', 'Cmd-B')
    SAVE_AS = ('<Command-S>', 'Cmd-Shift-S')
    SAVE_PROJECT = ('<Command-s>', 'Cmd-S')
    TOGGLE_PROPERTIES = ('<Command-Option-t>', 'Cmd-Option-T')
    TOGGLE_VIEWER = ('<Command-t>', 'Cmd-T')
    UNLOCK_PROJECT = ('<Command-u>', 'Cmd-U')

