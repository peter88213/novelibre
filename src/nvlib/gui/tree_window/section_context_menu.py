"""Provide a context menu class for sections in the "Chapter" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.tree_window.branch_context_menu import BranchContextMenu
from nvlib.nv_locale import _


class SectionContextMenu(BranchContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self.add_command(
            label=_('Add Section'),
            command=self._ctrl.add_new_section,
        )
        self.add_command(
            label=_('Add Chapter'),
            command=self._ctrl.add_new_chapter)
        self.add_command(
            label=_('Add Part'),
            command=self._ctrl.add_new_part,
        )
        self.add_command(
            label=_('Insert Stage'),
            command=self._ctrl.add_new_stage,
        )
        self.add_separator()
        self.add_command(
            label=_('Delete'),
            accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self.add_separator()
        self.add_command(
            label=_('Cut'),
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        self.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )
        self.add_separator()
        self.add_cascade(
            label=_('Set Type'),
            menu=master.selectTypeMenu,
        )
        self.add_cascade(
            label=_('Set Status'),
            menu=master.scStatusMenu,
        )
        self.add_command(
            label=_('Set Viewpoint...'),
            command=self._ctrl.set_viewpoint,
        )
        self.add_separator()
        self.add_command(
            label=_('Join with previous'),
            command=self._ctrl.join_sections,
        )
        self.add_separator()
        self.add_command(
            label=_('Chapter level'),
            command=master.show_chapter_level,
        )
        self.add_command(
            label=_('Expand'),
            command=master.expand_selected)
        self.add_command(
            label=_('Collapse'),
            command=master.collapse_selected,
        )
        self.add_command(
            label=_('Expand all'),
            command=master.expand_all,
        )
        self.add_command(
            label=_('Collapse all'),
            command=master.collapse_all,
        )
        self._disableOnLock = [
            _('Add Section'),
            _('Add Chapter'),
            _('Add Part'),
            _('Insert Stage'),
            _('Delete'),
            _('Cut'),
            _('Paste'),
            _('Set Type'),
            _('Set Status'),
            _('Set Viewpoint...'),
            _('Join with previous'),
        ]

