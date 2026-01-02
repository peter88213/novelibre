"""Provide a class for splitting project files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog

from nvlib.controller.services.service_base import ServiceBase
from nvlib.model.data.novel import Novel
from nvlib.model.data.nv_tree import NvTree
from nvlib.model.nv_work_file import NvWorkFile
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _


class FileSplitter(ServiceBase):

    def split_project(self):
        """Create a new project and move the selected chapters there."""

        if self._mdl.prjFile is None:
            return

        elements = self._ui.selectedNodes
        if not elements:
            return

        msg = _('Create a new project and move the selected chapters there?')
        if not self._ui.ask_yes_no(message=msg):
            return

        lastOpen = self._ctrl.get_preferences()['last_open']
        if lastOpen:
            startDir = os.path.dirname(lastOpen)
        else:
            startDir = '.'
        fileTypes = [(NvWorkFile.DESCRIPTION, NvWorkFile.EXTENSION)]
        fileName = filedialog.asksaveasfilename(
            filetypes=fileTypes,
            defaultextension=fileTypes[0][1],
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

        sourceNovel = self._mdl.novel
        newProject = self._mdl.nvService.new_novx_file(fileName)
        newNovel = Novel(
            links=sourceNovel.links,
            authorName=sourceNovel.authorName,
            languageCode=sourceNovel.languageCode,
            countryCode=sourceNovel.countryCode,
            renumberChapters=sourceNovel.renumberChapters,
            renumberParts=sourceNovel.renumberParts,
            renumberWithinParts=sourceNovel.renumberWithinParts,
            romanChapterNumbers=sourceNovel.romanChapterNumbers,
            romanPartNumbers=sourceNovel.romanPartNumbers,
            saveWordCount=sourceNovel.saveWordCount,
            workPhase=sourceNovel.workPhase,
            chapterHeadingPrefix=sourceNovel.chapterHeadingPrefix,
            chapterHeadingSuffix=sourceNovel.chapterHeadingSuffix,
            partHeadingPrefix=sourceNovel.partHeadingPrefix,
            partHeadingSuffix=sourceNovel.partHeadingSuffix,
            noSceneField1=sourceNovel.noSceneField1,
            noSceneField2=sourceNovel.noSceneField2,
            noSceneField3=sourceNovel.noSceneField3,
            otherSceneField1=sourceNovel.otherSceneField1,
            otherSceneField2=sourceNovel.otherSceneField2,
            otherSceneField3=sourceNovel.otherSceneField3,
            crField1=sourceNovel.crField1,
            crField2=sourceNovel.crField2,
            referenceDate=sourceNovel.referenceDate,
            tree=NvTree(),
        )

        for chId in elements:
            if chId.startswith(CHAPTER_PREFIX):
                newNovel.chapters[chId] = sourceNovel.chapters[chId]
                newNovel.tree.append(CH_ROOT, chId)
                for scId in sourceNovel.tree.get_children(chId):
                    newNovel.sections[scId] = sourceNovel.sections[scId]
                    newNovel.tree.append(chId, scId)
                    self._copy_related_elements(sourceNovel, newNovel, scId)
        newProject.novel = newNovel
        try:
            newProject.write()
        except RuntimeError as ex:
            self._ui.set_status(f'!{str(ex)}')
        else:
            for chId in elements:
                if chId.startswith(CHAPTER_PREFIX):
                    self._mdl.delete_element(chId, trash=False)
            for ppId in newNovel.plotPoints:
                self._mdl.delete_element(ppId)
            self._ctrl.refresh_tree()
            self._ui.set_status(
                f'{_("Chapters moved to new file")}: {norm_path(fileName)}'
            )

    def _copy_related_elements(self, sourceNovel, newNovel, scId):
        # Update newNovel.
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
                plId = sourceNovel.tree.parent(ppId)
                newNovel.tree.append(plId, ppId)

