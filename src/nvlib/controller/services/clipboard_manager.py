"""Provide a servide class to manage the novelibre tree view clipboard transfer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml.etree import ElementTree as ET

from nvlib.controller.services.service_base import ServiceBase
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX


class ClipboardManager(ServiceBase):

    def cut_element(self, elemPrefix=None):
        if self._mdl.prjFile is None:
            return

        if self._ctrl.check_lock():
            return

        try:
            node = self._ui.selectedNode
        except:
            return

        if self.copy_element(elemPrefix) is None:
            return

        if self._ui.tv.tree.prev(node):
            self._ui.tv.go_to_node(self._ui.tv.tree.prev(node))
        else:
            self._ui.tv.go_to_node(self._ui.tv.tree.parent(node))
        self._mdl.delete_element(node, trash=False)
        return 'break'

    def copy_element(self, elemPrefix=None):
        if self._mdl.prjFile is None:
            return

        try:
            node = self._ui.selectedNode
        except:
            return

        nodePrefix = node[:2]
        if elemPrefix is not None:
            if nodePrefix != elemPrefix:
                return

        elementContainers = {
            CHAPTER_PREFIX: (
                self._mdl.novel.chapters,
                'CHAPTER',
                self._mdl.prjFile.chapterCnv,
            ),
            SECTION_PREFIX: (
                self._mdl.novel.sections,
                'SECTION',
                self._mdl.prjFile.sectionCnv,
            ),
            PLOT_LINE_PREFIX: (
                self._mdl.novel.plotLines,
                'ARC',
                self._mdl.prjFile.plotLineCnv,
            ),
            PLOT_POINT_PREFIX: (
                self._mdl.novel.plotPoints,
                'POINT',
                self._mdl.prjFile.plotPointCnv,
            ),
            CHARACTER_PREFIX: (
                self._mdl.novel.characters,
                'CHARACTER',
                self._mdl.prjFile.characterCnv,
            ),
            LOCATION_PREFIX: (
                self._mdl.novel.locations,
                'LOCATION',
                self._mdl.prjFile.worldElementCnv,
            ),
            ITEM_PREFIX: (
                self._mdl.novel.items,
                'ITEM',
                self._mdl.prjFile.worldElementCnv,
            ),
            PRJ_NOTE_PREFIX: (
                self._mdl.novel.projectNotes,
                'PROJECTNOTE',
                self._mdl.prjFile.basicElementCnv,
            ),
        }
        if not nodePrefix in elementContainers:
            return

        elementContainer, xmlTag, elementCnv = elementContainers[nodePrefix]
        element = elementContainer[node]
        xmlElement = ET.Element(xmlTag)
        elementCnv.export_data(element, xmlElement)
        self._remove_references(xmlElement)

        # Get children, if any.
        if nodePrefix == CHAPTER_PREFIX:
            for scId in self._mdl.novel.tree.get_children(node):
                xmlSection = ET.SubElement(xmlElement, 'SECTION')
                self._mdl.prjFile.sectionCnv.export_data(
                    self._mdl.novel.sections[scId],
                    xmlSection
                )
                self._remove_references(xmlSection)
        elif nodePrefix == PLOT_LINE_PREFIX:
            for ppId in self._mdl.novel.tree.get_children(node):
                xmlPlotPoint = ET.SubElement(xmlElement, 'POINT')
                self._mdl.prjFile.plotPointCnv.export_data(
                    self._mdl.novel.plotPoints[ppId],
                    xmlPlotPoint
                )
                self._remove_references(xmlPlotPoint)

        text = ET.tostring(xmlElement)
        # no utf-8 encoding here, because the text is escaped
        self._ui.root.clipboard_clear()
        self._ui.root.clipboard_append(text)
        self._ui.root.update()
        return 'break'

    def paste_element(self, elemPrefix=None):
        if self._mdl.prjFile is None:
            return

        if self._ctrl.check_lock():
            return

        try:
            node = self._ui.selectedNode
        except:
            return

        try:
            text = self._ui.root.clipboard_get()
            xmlElement = ET.fromstring(text)
        except:
            return

        prefixes = {
            'CHAPTER': CHAPTER_PREFIX,
            'SECTION': SECTION_PREFIX,
            'ARC': PLOT_LINE_PREFIX,
            'POINT': PLOT_POINT_PREFIX,
            'CHARACTER': CHARACTER_PREFIX,
            'LOCATION': LOCATION_PREFIX,
            'ITEM': ITEM_PREFIX,
            'PROJECTNOTE': PRJ_NOTE_PREFIX
        }
        nodePrefix = prefixes.get(xmlElement.tag, None)
        if nodePrefix is None:
            return

        if elemPrefix is not None:
            if nodePrefix != elemPrefix:
                return

        if nodePrefix == SECTION_PREFIX:
            typeStr = xmlElement.get('type', 0)
            if int(typeStr) > 1:
                elemCreator = self._mdl.add_new_stage
            else:
                elemCreator = self._mdl.add_new_section
            elemContainer = self._mdl.novel.sections
            elemCnv = self._mdl.prjFile.sectionCnv
        else:
            elementControls = {
                CHAPTER_PREFIX: (
                    self._mdl.add_new_chapter,
                    self._mdl.novel.chapters,
                    self._mdl.prjFile.chapterCnv,
                ),
                PLOT_LINE_PREFIX: (
                    self._mdl.add_new_plot_line,
                    self._mdl.novel.plotLines,
                    self._mdl.prjFile.plotLineCnv,
                ),
                PLOT_POINT_PREFIX: (
                    self._mdl.add_new_plot_point,
                    self._mdl.novel.plotPoints,
                    self._mdl.prjFile.plotPointCnv,
                ),
                CHARACTER_PREFIX: (
                    self._mdl.add_new_character,
                    self._mdl.novel.characters,
                    self._mdl.prjFile.characterCnv,
                ),
                LOCATION_PREFIX: (
                    self._mdl.add_new_location,
                    self._mdl.novel.locations,
                    self._mdl.prjFile.worldElementCnv
                ),
                ITEM_PREFIX: (
                    self._mdl.add_new_item,
                    self._mdl.novel.items,
                    self._mdl.prjFile.worldElementCnv
                ),
                PRJ_NOTE_PREFIX: (
                    self._mdl.add_new_project_note,
                    self._mdl.novel.projectNotes,
                    self._mdl.prjFile.basicElementCnv,
                )
            }
            if not nodePrefix in elementControls:
                return

            elemCreator, elemContainer, elemCnv = elementControls[nodePrefix]

        elemId = elemCreator(targetNode=node)
        if not elemId:
            return

        elemCnv.import_data(
            elemContainer[elemId],
            xmlElement
        )

        # Get children, if any.
        targetNode = elemId
        if nodePrefix == CHAPTER_PREFIX:
            for xmlSection in xmlElement.iterfind('SECTION'):
                typeStr = xmlSection.get('type', 0)
                if int(typeStr) > 1:
                    scId = self._mdl.add_new_stage(targetNode=targetNode)
                else:
                    scId = self._mdl.add_new_section(targetNode=targetNode)
                self._mdl.prjFile.sectionCnv.import_data(
                    self._mdl.novel.sections[scId],
                    xmlSection
                )
                targetNode = scId
        elif nodePrefix == PLOT_LINE_PREFIX:
            for xmlPoint in xmlElement.iterfind('POINT'):
                ppId = self._mdl.add_new_plot_point(targetNode=targetNode)
                self._mdl.prjFile.plotPointCnv.import_data(
                    self._mdl.novel.plotPoints[ppId],
                    xmlPoint
                )
                targetNode = ppId

        self._ctrl.refresh_tree()
        self._ui.tv.go_to_node(elemId)
        return 'break'

    def _remove_references(self, xmlElement):
        references = [
            'Characters',
            'Locations',
            'Items',
            'PlotlineNotes',
            'Sections',
            'Section',
            'Viewpoint',
        ]
        for ref in references:
            for xmlRef in xmlElement.findall(ref):
                xmlElement.remove(xmlRef)
