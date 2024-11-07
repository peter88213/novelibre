""" Provide a class for the properties view window.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.view.properties_window.chapter_view import ChapterView
from nvlib.view.properties_window.character_view import CharacterView
from nvlib.view.properties_window.full_section_view import FullSectionView
from nvlib.view.properties_window.item_view import ItemView
from nvlib.view.properties_window.location_view import LocationView
from nvlib.view.properties_window.no_view import NoView
from nvlib.view.properties_window.plot_line_view import PlotLineView
from nvlib.view.properties_window.plot_point_view import TurningPointView
from nvlib.view.properties_window.project_note_view import ProjectNoteView
from nvlib.view.properties_window.project_view import ProjectView
from nvlib.view.properties_window.stage_view import StageView


class PropertiesViewer(SubController, ttk.Frame):
    """A window viewing the selected element's properties."""

    def __init__(self, parent, model, view, controller, **kw):
        SubController.__init__(self, model, view, controller)
        self._clients = []

        ttk.Frame.__init__(self, parent, **kw)

        # Call a factory method to instantiate and register one view component per element type.
        self._noView = self._make_view(NoView)
        self._projectView = self._make_view(ProjectView)
        self._chapterView = self._make_view(ChapterView)
        self._stageView = self._make_view(StageView)
        self._sectionView = self._make_view(FullSectionView)
        self._characterView = self._make_view(CharacterView)
        self._locationView = self._make_view(LocationView)
        self._itemView = self._make_view(ItemView)
        self._plotlineView = self._make_view(PlotLineView)
        self._plotPointView = self._make_view(TurningPointView)
        self._projectnoteView = self._make_view(ProjectNoteView)

        self._activeView = self._noView
        self._activeView.set_data(None)
        self._activeView.doNotUpdate = False

    def apply_changes(self, event=None):
        # This is called by the controller to make sure changes take effect
        # e.g. when starting an export while a property entry still has the focus.
        if not self._ctrl.isLocked:
            self._activeView.doNotUpdate = True
            self._activeView.apply_changes()
            self._activeView.doNotUpdate = False

    def focus_title(self):
        """Prepare the current element's title entry for manual input."""
        self._activeView.focus_title()

    def lock(self):
        """Inhibit changes on the model."""
        for client in self._clients:
            client.lock()

    def on_close(self):
        """Actions to be performed when a project is closed."""
        self._view_nothing()

    def unlock(self):
        """Enable changes on the model."""
        for client in self._clients:
            client.unlock()

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
            self._view_plotline(nodeId)
        elif nodeId.startswith(PLOT_POINT_PREFIX):
            self._view_plot_point(nodeId)
        elif nodeId.startswith(PRJ_NOTE_PREFIX):
            self._view_projectnote(nodeId)
        else:
            self._view_nothing()
        self._activeView.doNotUpdate = False

    def refresh(self):
        """Refresh the active view after changes have been made "outsides".
        
        Overrides the superclass method.
        """
        if not self._activeView.doNotUpdate:
            try:
                self.show_properties(self._activeView._elementId)
            except:
                pass

    def _make_view(self, viewClass):
        """Return a viewClass instance that is registered as a local view..
        
        Positional arguments:
            viewClass: BasicView subclass.
        """
        newView = viewClass(self, self._mdl, self._ui, self._ctrl)
        self._clients.append(newView)
        # NOTE: the new view component must not be registered by the main view,
        # because the PropertiesViewer instance may be deleted and recreated
        # due to re-parenting when docking the properties window.
        return newView

    def _set_data(self, elemId):
        """Fill the widgets with the data of the element to view and change."""
        if self._ctrl.isLocked:
            self._activeView.unlock()
            self._activeView.set_data(elemId)
            self._activeView.lock()
        else:
            self._activeView.set_data(elemId)

    def _view_plotline(self, plId):
        """Show the selected plot line.
        
        Positional arguments:
            plId: str -- Plot line ID
        """
        if not self._activeView is self._plotlineView:
            self._activeView.hide()
            self._activeView = self._plotlineView
            self._activeView.show()
        self._set_data(plId)

    def _view_chapter(self, chId):
        """Show the selected chapter's properties; move to it in the content viewer.
                
        Positional arguments:
            chId: str -- chapter ID
        """
        if not self._activeView is self._chapterView:
            self._activeView.hide()
            self._activeView = self._chapterView
            self._activeView.show()
        self._set_data(chId)

    def _view_character(self, crId):
        """Show the selected character's properties.
                
        Positional arguments:
            crId: str -- character ID
        """
        if not self._activeView is self._characterView:
            self._activeView.hide()
            self._activeView = self._characterView
            self._activeView.show()
        self._set_data(crId)

    def _view_item(self, itId):
        """Show the selected item's properties.
                
        Positional arguments:
            itId: str -- item ID
        """
        if not self._activeView is self._itemView:
            self._activeView.hide()
            self._activeView = self._itemView
            self._activeView.show()
        self._set_data(itId)

    def _view_location(self, lcId):
        """Show the selected location's properties.
                
        Positional arguments:
            lcId: str -- location ID
        """
        if not self._activeView is self._locationView:
            self._activeView.hide()
            self._activeView = self._locationView
            self._activeView.show()
        self._set_data(lcId)

    def _view_nothing(self):
        """Reset properties if nothing valid is selected."""
        if not self._activeView is self._noView:
            self._activeView.hide()
            self._activeView = self._noView
            self._activeView.show()

    def _view_project(self):
        """Show the project's properties."""
        if not self._activeView is self._projectView:
            self._activeView.hide()
            self._activeView = self._projectView
            self._activeView.show()
        self._set_data(CH_ROOT)

    def _view_projectnote(self, pnId):
        """Show the selected project note.
        
        Positional arguments:
            pnId: str -- Project note ID
        """
        if not self._activeView is self._projectnoteView:
            self._activeView.hide()
            self._activeView = self._projectnoteView
            self._activeView.show()
        self._set_data(pnId)

    def _view_section(self, scId):
        """Show the selected section's properties; move to it in the content viewer.
                
        Positional arguments:
            scId: str -- section ID
        """
        if self._mdl.novel.sections[scId].scType > 1:
            if not self._activeView is self._stageView:
                self._activeView.hide()
                self._activeView = self._stageView
                self._activeView.show()
        else:
            if not self._activeView is self._sectionView:
                self._activeView.hide()
                self._activeView = self._sectionView
                self._activeView.show()
        self._set_data(scId)

    def _view_plot_point(self, ppId):
        """Show the selected plot point
        Positional arguments:
            ppId: str -- Plot point ID
        """
        if not self._activeView is self._plotPointView:
            self._activeView.hide()
            self._activeView = self._plotPointView
            self._activeView.show()
        self._set_data(ppId)

