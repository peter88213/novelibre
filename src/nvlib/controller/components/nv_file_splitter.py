"""Provide a class for splitting project files.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog

from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import Error
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path


class NvFileSplitter:

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

    def split_project(self):
        """Create a new project and move the selected chapters there."""

        if self._mdl.prjFile is None:
            return

        elements = self._ui.selectedNodes
        if not elements:
            return

        if not self._ui.ask_yes_no(_('Create a new project and move the selected chapters there?')):
            return

        lastOpen = self._ctrl.get_preferences()['last_open']
        if lastOpen:
            startDir, __ = os.path.split(lastOpen)
        else:
            startDir = '.'
        fileName = filedialog.asksaveasfilename(
            filetypes=self._ctrl.fileTypes,
            defaultextension=self._ctrl.fileTypes[0][1],
            initialdir=startDir,
            )
        if not fileName:
            return

        if self._ui.tv.tree.prev(elements[0]):
            newSelection = self._ui.tv.tree.prev(elements[0])
        else:
            newSelection = self._ui.tv.tree.parent(elements[0])
        self._ui.tv.go_to_node(newSelection)

        self._ui.propertiesView.apply_changes()
        newProject = self._mdl.nvService.new_novx_file(fileName)
        newNovel = self._mdl.nvService.new_novel()
        sourceNovel = self._mdl.novel
        for chId in elements:
            if not chId.startswith(CHAPTER_PREFIX):
                continue

            newNovel.chapters[chId] = sourceNovel.chapters[chId]
            newNovel.tree.append(CH_ROOT, chId)
            for scId in sourceNovel.tree.get_children(chId):
                newNovel.sections[scId] = sourceNovel.sections[scId]
                newNovel.tree.append(chId, scId)
                for crId in newNovel.sections[scId].characters:
                    if not crId in newNovel.characters:
                        newNovel.characters[crId] = sourceNovel.characters[crId]
                        newNovel.tree.append(CR_ROOT, crId)
                for lcId in newNovel.sections[scId].locations:
                    if not lcId in newNovel.locations:
                        newNovel.locations[lcId] = sourceNovel.locations[lcId]
                        newNovel.tree.append(LC_ROOT, lcId)
                for itId in newNovel.sections[scId].items:
                    if not itId in newNovel.items:
                        newNovel.items[itId] = sourceNovel.items[itId]
                        newNovel.tree.append(IT_ROOT, itId)
                for plId in newNovel.sections[scId].scPlotLines:
                    if not plId in newNovel.plotLines:
                        newNovel.plotLines[plId] = sourceNovel.plotLines[plId]
                        newNovel.tree.append(PL_ROOT, plId)
                for ppId in newNovel.sections[scId].scPlotPoints:
                    if not ppId in newNovel.plotPoints:
                        newNovel.plotPoints[ppId] = sourceNovel.plotPoints[ppId]
                        newNovel.tree.append(sourceNovel.plotPoints[ppId], ppId)
        newProject.novel = newNovel
        try:
            newProject.write()
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
        else:
            for chId in elements:
                if chId.startswith(CHAPTER_PREFIX):
                    self._mdl.delete_element(chId, trash=False)
            self._ctrl.refresh_tree()
            self._ui.set_status(f'{_("Chapters moved to new file")}: {norm_path(fileName)}')
