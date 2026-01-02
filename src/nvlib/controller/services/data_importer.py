"""Provide a class for an XML data importer.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.services.service_base import ServiceBase
from nvlib.model.data.id_generator import new_id
from nvlib.model.novx.character_data_reader import CharacterDataReader
from nvlib.model.novx.item_data_reader import ItemDataReader
from nvlib.model.novx.location_data_reader import LocationDataReader
from nvlib.model.novx.plot_line_reader import PlotLineReader
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _


class DataImporter(ServiceBase):

    def __init__(self, model, view, controller):
        super().__init__(model, view, controller)
        self.sourceNovel = None
        self.sourceElements = None

    def read_source(self, filePath, prefix):
        """Read the elements of the XML data file specified by filePath.
        
        Positional arguments:
            filePath: str -- Path of the XML data file.
            prefix: str -- Prefix of the new element IDs.
        """
        sources = {
            CHARACTER_PREFIX:CharacterDataReader,
            LOCATION_PREFIX:LocationDataReader,
            ITEM_PREFIX:ItemDataReader,
            PLOT_LINE_PREFIX:PlotLineReader,
        }
        source = sources[prefix](filePath)
        source.novel = self._mdl.nvService.new_novel()

        errorMessages = {
            CHARACTER_PREFIX:_('No character data found'),
            LOCATION_PREFIX:_('No location data found'),
            ITEM_PREFIX:_('No item data found'),
            PLOT_LINE_PREFIX:_('No plot lines found'),
        }
        try:
            source.read()
        except:
            raise RuntimeError(
                f'{_("Cannot process file")}: {norm_path(filePath)}'
            )

        sourceElements = {
            CHARACTER_PREFIX:source.novel.characters,
            LOCATION_PREFIX:source.novel.locations,
            ITEM_PREFIX:source.novel.items,
            PLOT_LINE_PREFIX:source.novel.plotLines,
        }
        if not sourceElements[prefix]:
            raise UserWarning(
                f'{errorMessages[prefix]}: {norm_path(filePath)}'
            )

        self.sourceElements = sourceElements[prefix]
        self.sourceNovel = source.novel

    def add_elements(self, selectedIds=None):
        """Add the elements specified by selectedIds to the novel."""
        if self.sourceNovel is None:
            return

        if self.sourceElements is None:
            return

        if selectedIds is None:
            selectedIds = self.sourceElements

        targetElements = {
            CHARACTER_PREFIX:self._mdl.novel.characters,
            LOCATION_PREFIX:self._mdl.novel.locations,
            ITEM_PREFIX:self._mdl.novel.items,
            PLOT_LINE_PREFIX:self._mdl.novel.plotLines,
        }
        elemParents = {
            CHARACTER_PREFIX:CR_ROOT,
            LOCATION_PREFIX:LC_ROOT,
            ITEM_PREFIX:IT_ROOT,
            PLOT_LINE_PREFIX:PL_ROOT,
        }
        add_children = {
            CHARACTER_PREFIX:self._do_nothing,
            LOCATION_PREFIX:self._do_nothing,
            ITEM_PREFIX:self._do_nothing,
            PLOT_LINE_PREFIX:self._add_plot_points,
        }
        i = 0
        for  elemId in selectedIds:
            prefix = elemId[:2]
            newId = new_id(targetElements[prefix], prefix=prefix)
            targetElements[prefix][newId] = self.sourceElements[elemId]
            self._mdl.novel.tree.append(elemParents[prefix], newId)
            add_children[prefix](newId, elemId)
            i += 1
        if i > 0:
            self._ui.tv.go_to_node(newId)
            self._ui.set_status(f'{i} {_("elements imported")}')
        self.sourceNovel = None
        self.sourceElements = None

    def _add_plot_points(self, plId, srcPlId):
        """Add the plot points belonging to the plot line specified by plId."""
        srcPlotPoints = self.sourceNovel.tree.get_children(srcPlId)
        if srcPlotPoints:
            for srcPpId in srcPlotPoints:
                ppId = new_id(
                    self._mdl.novel.plotPoints,
                    prefix=PLOT_POINT_PREFIX,
                )
                self._mdl.novel.plotPoints[ppId] = (
                    self.sourceNovel.plotPoints[srcPpId]
                )
                self._mdl.novel.tree.append(plId, ppId)

    def _do_nothing(self, *args):
        pass
