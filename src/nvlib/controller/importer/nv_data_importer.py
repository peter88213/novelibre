"""Provide a class for an elements importer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvlib.model.data.id_generator import new_id
from nvlib.model.novx.character_data_reader import CharacterDataReader
from nvlib.model.novx.item_data_reader import ItemDataReader
from nvlib.model.novx.location_data_reader import LocationDataReader
from nvlib.model.novx.plot_line_reader import PlotLineReader
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path
from nvlib.view.widgets.pick_list import PickList


class NvDataImporter(SubController):
    """Elements importer with a pick list."""

    def __init__(self, model, view, controller, filePath, elemPrefix):
        """Open a pick list with the elements of the XML data file specified by filePath.
        
        Positional arguments:
            view -- the caller.
            filePath: str -- Path of the XML data file.
            elemPrefix: str -- Prefix of the new element IDs.
        """
        SubController.initialize_controller(self, model, view, controller)
        sources = {
            CHARACTER_PREFIX:CharacterDataReader,
            LOCATION_PREFIX:LocationDataReader,
            ITEM_PREFIX:ItemDataReader,
            PLOT_LINE_PREFIX:PlotLineReader,
        }
        source = sources[elemPrefix](filePath)
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
            self._ui.set_status(f"!{errorMessages[elemPrefix]}: {norm_path(filePath)}")
            return

        sourceElements = {
            CHARACTER_PREFIX:source.novel.characters,
            LOCATION_PREFIX:source.novel.locations,
            ITEM_PREFIX:source.novel.items,
            PLOT_LINE_PREFIX:source.novel.plotLines,
        }
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
        windowTitles = {
            CHARACTER_PREFIX:_('Select characters'),
            LOCATION_PREFIX:_('Select locations'),
            ITEM_PREFIX:_('Select items'),
            PLOT_LINE_PREFIX:_('Select plot lines'),
        }
        self._add_children = {
            CHARACTER_PREFIX:self._do_nothing,
            LOCATION_PREFIX:self._do_nothing,
            ITEM_PREFIX:self._do_nothing,
            PLOT_LINE_PREFIX:self._add_plot_points,
        }
        self._srcNovel = source.novel
        self._elemPrefix = elemPrefix
        self._sourceElements = sourceElements[elemPrefix]
        self._targetElements = targetElements[elemPrefix]
        self._elemParent = elemParents[elemPrefix]
        pickButtonLabel = _('Import selected elements')
        offset = 50
        size = '300x400'
        __, x, y = self._ui.root.geometry().split('+')
        windowGeometry = f'{size}+{int(x)+offset}+{int(y)+offset}'
        PickList(
            windowTitles[elemPrefix],
            windowGeometry,
            self._sourceElements,
            pickButtonLabel,
            self._pick_element
            )

    def _pick_element(self, elements):
        """Add the selected elements to the novel."""
        i = 0
        for  elemId in elements:
            newId = new_id(self._targetElements, prefix=self._elemPrefix)
            self._targetElements[newId] = self._sourceElements[elemId]
            self._mdl.novel.tree.append(self._elemParent, newId)
            self._add_children[self._elemPrefix](newId, elemId)
            i += 1
        if i > 0:
            self._ui.tv.go_to_node(newId)
            self._ui.set_status(f'{i} {_("elements imported")}')

    def _add_plot_points(self, plId, srcPlId):
        """Add the plot points belonging to the plot line specified by plId."""
        srcPlotPoints = self._srcNovel.tree.get_children(srcPlId)
        if srcPlotPoints:
            for srcPpId in srcPlotPoints:
                ppId = new_id(self._mdl.novel.plotPoints, prefix=PLOT_POINT_PREFIX)
                self._mdl.novel.plotPoints[ppId] = self._srcNovel.plotPoints[srcPpId]
                self._mdl.novel.tree.append(plId, ppId)

    def _do_nothing(self, *args):
        pass
