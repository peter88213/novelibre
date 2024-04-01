""" Provide a class for the properties view window.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.view.properties_window.plot_line_view import PlotLineView
from nvlib.view.properties_window.chapter_view import ChapterView
from nvlib.view.properties_window.character_view import CharacterView
from nvlib.view.properties_window.full_section_view import FullSectionView
from nvlib.view.properties_window.item_view import ItemView
from nvlib.view.properties_window.location_view import LocationView
from nvlib.view.properties_window.no_view import NoView
from nvlib.view.properties_window.project_view import ProjectView
from nvlib.view.properties_window.project_note_view import ProjectNoteView
from nvlib.view.properties_window.stage_view import StageView
from nvlib.view.properties_window.plot_point_view import TurningPointView
from novxlib.novx_globals import PLOT_POINT_PREFIX
from novxlib.novx_globals import PLOT_LINE_PREFIX
from novxlib.novx_globals import CHAPTER_PREFIX
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import PRJ_NOTE_PREFIX
from novxlib.novx_globals import SECTION_PREFIX


class PropertiesViewer(ttk.Frame):
    """A window viewing the selected element's properties."""

    def __init__(self, parent, model, view, controller, **kw):
        super().__init__(parent, **kw)
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._noView = NoView(self, self._mdl, self._ui, self._ctrl)
        self._projectView = ProjectView(self, self._mdl, self._ui, self._ctrl)
        self._chapterView = ChapterView(self, self._mdl, self._ui, self._ctrl)
        self._stageView = StageView(self, self._mdl, self._ui, self._ctrl)
        self._sectionView = FullSectionView(self, self._mdl, self._ui, self._ctrl)
        self._characterView = CharacterView(self, self._mdl, self._ui, self._ctrl)
        self._locationView = LocationView(self, self._mdl, self._ui, self._ctrl)
        self._itemView = ItemView(self, self._mdl, self._ui, self._ctrl)
        self._arcView = PlotLineView(self, self._mdl, self._ui, self._ctrl)
        self._plotPointView = TurningPointView(self, self._mdl, self._ui, self._ctrl)
        self._projectnoteView = ProjectNoteView(self, self._mdl, self._ui, self._ctrl)
        self._elementView = self._noView
        self._elementView.set_data(None)
        self._elementView.doNotUpdate = False
        self._allViews = [
            self._projectView,
            self._chapterView,
            self._stageView,
            self._sectionView,
            self._characterView,
            self._locationView,
            self._itemView,
            self._arcView,
            self._plotPointView,
            self._projectnoteView,
            ]

    def apply_changes(self, event=None):
        # This is called by the controller to make sure changes take effect
        # e.g. when starting an export while a property entry still has the focus.
        if not self._ctrl.isLocked:
            self._elementView.doNotUpdate = True
            self._elementView.apply_changes()
            self._elementView.doNotUpdate = False

    def focus_title(self):
        """Prepare the current element's title entry for manual input."""
        self._elementView.focus_title()

    def lock(self):
        """Inhibit element change."""
        for view in self._allViews:
            view.lock()

    def show_properties(self, nodeId):
        """Show the properties of the selected element."""
        if self._mdl is None:
            self._view_nothing()
        elif nodeId.startswith(SECTION_PREFIX):
            self._view_section(nodeId)
        elif nodeId == self._mdl.trashBin:
            self._view_nothing()
        elif nodeId.startswith(CHAPTER_PREFIX):
            self._view_chapter(nodeId)
        elif nodeId.startswith(CH_ROOT):
            self._view_project()
        elif nodeId.startswith(CHARACTER_PREFIX):
            self._view_character(nodeId)
        elif nodeId.startswith(LOCATION_PREFIX):
            self._view_location(nodeId)
        elif nodeId.startswith(ITEM_PREFIX):
            self._view_item(nodeId)
        elif nodeId.startswith(PLOT_LINE_PREFIX):
            self._view_arc(nodeId)
        elif nodeId.startswith(PLOT_POINT_PREFIX):
            self._view_plot_point(nodeId)
        elif nodeId.startswith(PRJ_NOTE_PREFIX):
            self._view_projectnote(nodeId)
        else:
            self._view_nothing()
        self._elementView.doNotUpdate = False

    def unlock(self):
        """enable element change."""
        for view in self._allViews:
            view.unlock()

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if not self._elementView.doNotUpdate:
            try:
                self.show_properties(self._elementView._elementId)
            except:
                pass

    def _set_data(self, elemId):
        """Fill the widgets with the data of the element to view and change."""
        if self._ctrl.isLocked:
            self._elementView.unlock()
            self._elementView.set_data(elemId)
            self._elementView.lock()
        else:
            self._elementView.set_data(elemId)

    def _view_arc(self, plId):
        """Show the selected plot line.
        
        Positional arguments:
            plId: str -- Plot line ID
        """
        if not self._elementView is self._arcView:
            self._elementView.hide()
            self._elementView = self._arcView
            self._elementView.show()
        self._set_data(plId)

    def _view_chapter(self, chId):
        """Show the selected chapter's properties; move to it in the content viewer.
                
        Positional arguments:
            chId: str -- chapter ID
        """
        if not self._elementView is self._chapterView:
            self._elementView.hide()
            self._elementView = self._chapterView
            self._elementView.show()
        self._set_data(chId)

    def _view_character(self, crId):
        """Show the selected character's properties.
                
        Positional arguments:
            crId: str -- character ID
        """
        if not self._elementView is self._characterView:
            self._elementView.hide()
            self._elementView = self._characterView
            self._elementView.show()
        self._set_data(crId)

    def _view_item(self, itId):
        """Show the selected item's properties.
                
        Positional arguments:
            itId: str -- item ID
        """
        if not self._elementView is self._itemView:
            self._elementView.hide()
            self._elementView = self._itemView
            self._elementView.show()
        self._set_data(itId)

    def _view_location(self, lcId):
        """Show the selected location's properties.
                
        Positional arguments:
            lcId: str -- location ID
        """
        if not self._elementView is self._locationView:
            self._elementView.hide()
            self._elementView = self._locationView
            self._elementView.show()
        self._set_data(lcId)

    def _view_nothing(self):
        """Reset properties if nothing valid is selected."""
        if not self._elementView is self._noView:
            self._elementView.hide()
            self._elementView = self._noView
            self._elementView.show()

    def _view_project(self):
        """Show the project's properties."""
        if not self._elementView is self._projectView:
            self._elementView.hide()
            self._elementView = self._projectView
            self._elementView.show()
        self._set_data(CH_ROOT)

    def _view_projectnote(self, pnId):
        """Show the selected project note.
        
        Positional arguments:
            pnId: str -- Project note ID
        """
        if not self._elementView is self._projectnoteView:
            self._elementView.hide()
            self._elementView = self._projectnoteView
            self._elementView.show()
        self._set_data(pnId)

    def _view_section(self, scId):
        """Show the selected section's properties; move to it in the content viewer.
                
        Positional arguments:
            scId: str -- section ID
        """
        if self._mdl.novel.sections[scId].scType > 1:
            if not self._elementView is self._stageView:
                self._elementView.hide()
                self._elementView = self._stageView
                self._elementView.show()
        else:
            if not self._elementView is self._sectionView:
                self._elementView.hide()
                self._elementView = self._sectionView
                self._elementView.show()
        self._set_data(scId)

    def _view_plot_point(self, ppId):
        """Show the selected plot point
        Positional arguments:
            ppId: str -- Plot point ID
        """
        if not self._elementView is self._plotPointView:
            self._elementView.hide()
            self._elementView = self._plotPointView
            self._elementView.show()
        self._set_data(ppId)

