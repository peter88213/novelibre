"""Provide a class with key definitions.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_locale import _


class GenericKeys:

    ADD_CHILD = ('<Control-Alt-n>', f'{_("Ctrl")}-Alt-N')
    ADD_ELEMENT = ('<Control-n>', f'{_("Ctrl")}-N')
    ADD_PARENT = ('<Control-Alt-N>', f'{_("Ctrl")}-Alt-{_("Shift")}-N')
    BACK = ('<Alt-Left>', f'{_("Alt-Left")}')
    CHAPTER_LEVEL = ('<Control-Alt-c>', f'{_("Ctrl")}-Alt-C')
    COPY = ('<Control-c>', f'{_("Ctrl")}-C')
    CUT = ('<Control-x>', f'{_("Ctrl")}-X')
    DELETE = ('<Delete>', _('Del'))
    DETACH_PROPERTIES = ('<Control-Alt-d>', f'{_("Ctrl")}-Alt-D')
    FOLDER = ('<Control-p>', f'{_("Ctrl")}-P')
    FORWARD = ('<Alt-Right>', f'{_("Alt-Right")}')
    LOCK_PROJECT = ('<Control-l>', f'{_("Ctrl")}-L')
    NEXT = ('<Alt-Down>', f'{_("Alt-Down")}')
    OPEN_HELP = ('<F1>', 'F1')
    OPEN_PROJECT = ('<Control-o>', f'{_("Ctrl")}-O')
    PASTE = ('<Control-v>', f'{_("Ctrl")}-V')
    PREVIOUS = ('<Alt-Up>', f'{_("Alt-Up")}')
    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')
    REFRESH_TREE = ('<F5>', 'F5')
    RELOAD_PROJECT = ('<Control-r>', f'{_("Ctrl")}-R')
    RESTORE_BACKUP = ('<Control-b>', f'{_("Ctrl")}-B')
    RESTORE_STATUS = ('<Escape>', 'Esc')
    SAVE_AS = ('<Control-S>', f'{_("Ctrl")}-{_("Shift")}-S')
    SAVE_PROJECT = ('<Control-s>', f'{_("Ctrl")}-S')
    TOGGLE_PROPERTIES = ('<Control-Alt-t>', f'{_("Ctrl")}-Alt-T')
    TOGGLE_VIEWER = ('<Control-t>', f'{_("Ctrl")}-T')
    UNLOCK_PROJECT = ('<Control-u>', f'{_("Ctrl")}-U')

