"""Provide a mixin class for controlling the properties viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

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
from nvlib.gui.properties_window.chapter_view import ChapterView
from nvlib.gui.properties_window.character_view import CharacterView
from nvlib.gui.properties_window.item_view import ItemView
from nvlib.gui.properties_window.location_view import LocationView
from nvlib.gui.properties_window.no_view import NoView
from nvlib.gui.properties_window.plot_line_view import PlotLineView
from nvlib.gui.properties_window.plot_point_view import PlotPointView
from nvlib.gui.properties_window.project_note_view import ProjectNoteView
from nvlib.gui.properties_window.project_view import ProjectView
from nvlib.gui.properties_window.section_view import SectionView
from nvlib.gui.properties_window.stage_view import StageView


class PropertiesViewerCtrl(SubController):

    def initialize_controller(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self._clients = []

        # Call a factory method to instantiate and register one view component per element type.
        self.noView = self._make_view(NoView)
        self.projectView = self._make_view(ProjectView)
        self.chapterView = self._make_view(ChapterView)
        self.stageView = self._make_view(StageView)
        self.sectionView = self._make_view(SectionView)
        self.characterView = self._make_view(CharacterView)
        self.locationView = self._make_view(LocationView)
        self.itemView = self._make_view(ItemView)
        self.plotlineView = self._make_view(PlotLineView)
        self.plotPointView = self._make_view(PlotPointView)
        self.projectnoteView = self._make_view(ProjectNoteView)

        self.activeView = self.noView
        self.activeView.set_data(None)
        self.activeView.doNotUpdate = False

    def apply_changes(self, event=None):
        # This is called by the controller to make sure changes take effect
        # e.g. when starting an export while a property entry still has the focus.
        if not self._ctrl.isLocked:
            self.activeView.doNotUpdate = True
            self.activeView.apply_changes()
            self.activeView.doNotUpdate = False

    def focus_title(self):
        """Prepare the current element's title entry for manual input."""
        self.activeView.focus_title()

    def lock(self):
        """Inhibit changes on the model."""
        for client in self._clients:
            client.lock()

    def on_close(self):
        """Actions to be performed when a project is closed."""
        self._view_nothing()

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
        self.activeView.doNotUpdate = False

    def refresh(self):
        """Refresh the active view after changes have been made "outsides".
        
        Overrides the superclass method.
        """
        if not self.activeView.doNotUpdate:
            try:
                self.show_properties(self.activeView.elementId)
            except:
                pass

    def unlock(self):
        """Enable changes on the model."""
        for client in self._clients:
            client.unlock()

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
            self.activeView.unlock()
            self.activeView.set_data(elemId)
            self.activeView.lock()
        else:
            self.activeView.set_data(elemId)

    def _view_plotline(self, plId):
        """Show the selected plot line.
        
        Positional arguments:
            plId: str -- Plot line ID
        """
        if not self.activeView is self.plotlineView:
            self.activeView.hide()
            self.activeView = self.plotlineView
            self.activeView.show()
        self._set_data(plId)

    def _view_chapter(self, chId):
        """Show the selected chapter's properties; move to it in the content viewer.
                
        Positional arguments:
            chId: str -- chapter ID
        """
        if not self.activeView is self.chapterView:
            self.activeView.hide()
            self.activeView = self.chapterView
            self.activeView.show()
        self._set_data(chId)

    def _view_character(self, crId):
        """Show the selected character's properties.
                
        Positional arguments:
            crId: str -- character ID
        """
        if not self.activeView is self.characterView:
            self.activeView.hide()
            self.activeView = self.characterView
            self.activeView.show()
        self._set_data(crId)

    def _view_item(self, itId):
        """Show the selected item's properties.
                
        Positional arguments:
            itId: str -- item ID
        """
        if not self.activeView is self.itemView:
            self.activeView.hide()
            self.activeView = self.itemView
            self.activeView.show()
        self._set_data(itId)

    def _view_location(self, lcId):
        """Show the selected location's properties.
                
        Positional arguments:
            lcId: str -- location ID
        """
        if not self.activeView is self.locationView:
            self.activeView.hide()
            self.activeView = self.locationView
            self.activeView.show()
        self._set_data(lcId)

    def _view_nothing(self):
        """Reset properties if nothing valid is selected."""
        if not self.activeView is self.noView:
            self.activeView.hide()
            self.activeView = self.noView
            self.activeView.show()

    def _view_project(self):
        """Show the project's properties."""
        if not self.activeView is self.projectView:
            self.activeView.hide()
            self.activeView = self.projectView
            self.activeView.show()
        self._set_data(CH_ROOT)

    def _view_projectnote(self, pnId):
        """Show the selected project note.
        
        Positional arguments:
            pnId: str -- Project note ID
        """
        if not self.activeView is self.projectnoteView:
            self.activeView.hide()
            self.activeView = self.projectnoteView
            self.activeView.show()
        self._set_data(pnId)

    def _view_section(self, scId):
        """Show the selected section's properties; move to it in the content viewer.
                
        Positional arguments:
            scId: str -- section ID
        """
        if self._mdl.novel.sections[scId].scType > 1:
            if not self.activeView is self.stageView:
                self.activeView.hide()
                self.activeView = self.stageView
                self.activeView.show()
        else:
            if not self.activeView is self.sectionView:
                self.activeView.hide()
                self.activeView = self.sectionView
                self.activeView.show()
        self._set_data(scId)

    def _view_plot_point(self, ppId):
        """Show the selected plot point
        Positional arguments:
            ppId: str -- Plot point ID
        """
        if not self.activeView is self.plotPointView:
            self.activeView.hide()
            self.activeView = self.plotPointView
            self.activeView.show()
        self._set_data(ppId)

