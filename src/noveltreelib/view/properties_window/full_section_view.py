"""Provide a tkinter based class for viewing and editing all section properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from noveltreelib.noveltree_globals import prefs
from noveltreelib.view.properties_window.dated_section_view import DatedSectionView
from noveltreelib.widgets.collection_box import CollectionBox
from noveltreelib.widgets.folding_frame import FoldingFrame
from noveltreelib.widgets.label_combo import LabelCombo
from noveltreelib.widgets.my_string_var import MyStringVar
from noveltreelib.widgets.text_box import TextBox
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import AC_ROOT
from novxlib.novx_globals import ARC_PREFIX
from novxlib.novx_globals import _
from novxlib.novx_globals import list_to_string
from novxlib.novx_globals import string_to_list
import tkinter as tk


class FullSectionView(DatedSectionView):
    """Class for viewing and editing section properties.
       
    Adds to the right pane:
    - A combobox for viewpoint character selection.
    - A checkbox "unused".
    - A checkbox "append to previous".
    - A "Plot" folding frame for arcs and turning point associations.
    - An "Action/Reaction" folding frame for Goal/Reaction/Outcome.
    """

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            view: NoveltreeUi -- Reference to the user interface.
            parent -- Parent widget to display this widget.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Viewpoint' combobox.
        self._viewpoint = MyStringVar()
        self._characterCombobox = LabelCombo(
            self._sectionExtraFrame,
            text=_('Viewpoint'),
            textvariable=self._viewpoint,
            values=[],
            )
        self._characterCombobox.pack(anchor='w', pady=2)
        inputWidgets.append(self._characterCombobox)
        self._characterCombobox.combo.bind('<<ComboboxSelected>>', self.apply_changes)
        self._vpList = []

        #--- 'Unused' checkbox.
        self._isUnused = tk.BooleanVar()
        self._isUnusedCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Unused'),
            variable=self._isUnused,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._isUnusedCheckbox.pack(anchor='w')
        inputWidgets.append(self._isUnusedCheckbox)

        #--- 'Append to previous section' checkbox.
        self._appendToPrev = tk.BooleanVar()
        self._appendToPrevCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Append to previous section'),
            variable=self._appendToPrev,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._appendToPrevCheckbox.pack(anchor='w')
        inputWidgets.append(self._appendToPrevCheckbox)

        ttk.Separator(self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for arcs and plot.
        self._arcFrame = FoldingFrame(self._sectionExtraFrame, _('Plot'), self._toggle_arc_frame)

        # 'Arcs' listbox.
        self._arcTitles = ''
        self._arcLabel = ttk.Label(self._arcFrame, text=_('Arcs'))
        self._arcLabel.pack(anchor='w')
        self._arcCollection = CollectionBox(
            self._arcFrame,
            cmdAdd=self._pick_arc,
            cmdRemove=self._remove_arc,
            cmdOpen=self._go_to_arc,
            cmdActivate=self._activate_arc_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._arcCollection.pack(fill='x')
        inputWidgets.extend(self._arcCollection.inputWidgets)

        tk.Label(self._arcFrame, text=_('Turning points')).pack(anchor='w')

        #--- 'Turning points' label.
        self._turningPointsDisplay = tk.Label(self._arcFrame, anchor='w', bg='white')
        self._turningPointsDisplay.pack(anchor='w', fill='x')

        ttk.Separator(self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Action'/'Reaction'/'Custom'.
        self._pacingFrame = FoldingFrame(self._sectionExtraFrame, _('Action/Reaction'), self._toggle_pacing_frame)

        # 'Action'/'Reaction'/'Custom' radiobuttons.
        selectionFrame = ttk.Frame(self._pacingFrame)
        self._customGoal = ''
        self._customConflict = ''
        self._customOutcome = ''
        self._sectionPacingType = tk.IntVar()

        self._actionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Action'),
            variable=self._sectionPacingType,
            value=0, command=self._set_action_section,
            )
        self._actionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._actionRadiobutton)

        self._reactionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Reaction'),
            variable=self._sectionPacingType,
            value=1,
            command=self._set_reaction_section,
            )
        self._reactionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._reactionRadiobutton)

        self._customRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Custom'),
            variable=self._sectionPacingType,
            value=2,
            command=self._set_custom_ar_section
            )
        self._customRadiobutton.pack(anchor='w')
        inputWidgets.append(self._customRadiobutton)

        selectionFrame.pack(fill='x')

        # 'Goal/Reaction' window. The labels are configured dynamically.
        self._goalLabel = ttk.Label(self._pacingFrame)
        self._goalLabel.pack(anchor='w')
        self._goalWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=prefs['gco_height'],
                padx=5,
                pady=5,
                bg=prefs['color_text_bg'],
                fg=prefs['color_text_fg'],
                insertbackground=prefs['color_text_fg'],
                )
        self._goalWindow.pack(fill='x')
        inputWidgets.append(self._goalWindow)

        # 'Conflict/Dilemma' window. The labels are configured dynamically.
        self._conflictLabel = ttk.Label(self._pacingFrame)
        self._conflictLabel.pack(anchor='w')
        self._conflictWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=prefs['gco_height'],
                padx=5,
                pady=5,
                bg=prefs['color_text_bg'],
                fg=prefs['color_text_fg'],
                insertbackground=prefs['color_text_fg'],
                )
        self._conflictWindow.pack(fill='x')
        inputWidgets.append(self._conflictWindow)

        # 'Outcome/Choice' window. The labels are configured dynamically.
        self._outcomeLabel = ttk.Label(self._pacingFrame)
        self._outcomeLabel.pack(anchor='w')
        self._outcomeWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=prefs['gco_height'],
                padx=5,
                pady=5,
                bg=prefs['color_text_bg'],
                fg=prefs['color_text_fg'],
                insertbackground=prefs['color_text_fg'],
                )
        self._outcomeWindow.pack(fill='x')
        inputWidgets.append(self._outcomeWindow)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        super().apply_changes()
        # updating the character list before the viewpoints

        #--- 'Viewpoint' combobox.
        scCharacters = self._element.characters
        if scCharacters:
            option = self._characterCombobox.current()
            if option >= 0:
                # Put the selected character at the first position of related characters.
                vpId = self._vpList[option]
                if vpId in scCharacters:
                    scCharacters.remove(vpId)
                scCharacters.insert(0, vpId)
                self._element.characters = scCharacters

        #--- 'Unused' checkbox.
        if self._isUnused.get():
            self._element.scType = 1
        else:
            self._element.scType = 0

        #--- 'Append to previous section' checkbox.
        self._element.appendToPrev = self._appendToPrev.get()

        #--- 'Goal/Reaction' window.
        if self._goalWindow.hasChanged:
            self._element.goal = self._goalWindow.get_text()

        #--- 'Conflict/Dilemma' window.
        if self._conflictWindow.hasChanged:
            self._element.conflict = self._conflictWindow.get_text()

        #--- 'Outcome/Choice' window.
        if self._outcomeWindow.hasChanged:
            self._element.outcome = self._outcomeWindow.get_text()

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

        #--- 'Viewpoint' combobox.
        charNames = []
        self._vpList = []
        for crId in self._mdl.novel.tree.get_children(CR_ROOT):
            charNames.append(self._mdl.novel.characters[crId].title)
            self._vpList.append(crId)
        self._characterCombobox.configure(values=charNames)
        if self._element.characters:
            vp = self._mdl.novel.characters[self._element.characters[0]].title
        else:
            vp = ''
        self._viewpoint.set(value=vp)

        #--- 'Arcs' listbox.
        self._arcTitles = self._get_arc_titles(self._element.scArcs, self._mdl.novel.arcs)
        self._arcCollection.cList.set(self._arcTitles)
        listboxSize = len(self._arcTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._arcCollection.cListbox.config(height=listboxSize)
        if not self._arcCollection.cListbox.curselection() or not self._arcCollection.cListbox.focus_get():
            self._arcCollection.deactivate_buttons()

        #--- "Turning points" label
        turningPointTitles = []
        for tpId in self._element.scTurningPoints:
            acId = self._element.scTurningPoints[tpId]
            turningPointTitles.append(f'{self._mdl.novel.arcs[acId].shortName}: {self._mdl.novel.turningPoints[tpId].title}')
        self._turningPointsDisplay.config(text=list_to_string(turningPointTitles))

        #--- 'Unused' checkbox.
        if self._element.scType > 0:
            self._isUnused.set(True)
            # self._ctrl.set_type(1)
        else:
            self._isUnused.set(False)
            # self._ctrl.set_type(0)

        #--- 'Append to previous section' checkbox.
        if self._element.appendToPrev:
            self._appendToPrev.set(True)
        else:
            self._appendToPrev.set(False)

        # Customized Goal/Conflict/Outcome configuration.
        if self._mdl.novel.customGoal:
            self._customGoal = self._mdl.novel.customGoal
        else:
            self._customGoal = _('N/A')

        if self._mdl.novel.customConflict:
            self._customConflict = self._mdl.novel.customConflict
        else:
            self._customConflict = _('N/A')

        if self._mdl.novel.customOutcome:
            self._customOutcome = self._mdl.novel.customOutcome
        else:
            self._customOutcome = _('N/A')

        #--- Frame for narrative arcs.
        if prefs['show_sc_arcs']:
            self._arcFrame.show()
        else:
            self._arcFrame.hide()

        #--- Frame for 'Action'/'Reaction'/'Custom'.
        if prefs['show_action_reaction']:
            self._pacingFrame.show()
        else:
            self._pacingFrame.hide()

        #--- 'Action'/'Reaction'/'Custom' radiobuttons.
        self._sectionPacingType.set(self._element.scPacing)

        #--- 'Goal/Reaction' window.
        self._goalWindow.set_text(self._element.goal)

        #--- 'Conflict/Dilemma' window.
        self._conflictWindow.set_text(self._element.conflict)

        #--- 'Outcome/Choice' window.
        self._outcomeWindow.set_text(self._element.outcome)

        # Configure the labels.
        if self._element.scPacing == 2:
            self._set_custom_ar_section()
        elif self._element.scPacing == 1:
            self._set_reaction_section()
        else:
            self._set_action_section()

    def _activate_arc_buttons(self, event=None):
        if self._element.scArcs:
            self._arcCollection.activate_buttons()
        else:
            self._arcCollection.deactivate_buttons()

    def _add_arc(self, event=None):
        # Add the selected element to the collection, if applicable.
        arcList = self._element.scArcs
        acId = self._ui.tv.tree.selection()[0]
        if not acId.startswith(ARC_PREFIX):
            # Restore the previous section selection mode.
            self._end_picking_mode()
        elif not acId in arcList:
            arcList.append(acId)
            self._element.scArcs = arcList
            arcSections = self._mdl.novel.arcs[acId].sections
            if not self._elementId in arcSections:
                arcSections.append(self._elementId)
                self._mdl.novel.arcs[acId].sections = arcSections

    def _get_arc_titles(self, elemIds, elements):
        """Return a list of arc titles, preceded by the short names.
        
        Positional arguments:
            elemIds -- list of element IDs.
            elements -- list of element objects.          
        """
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(f'({elements[elemId].shortName}) {elements[elemId].title}')
                except:
                    pass
        return elemTitles

    def _get_relation_id_list(self, newTitleStr, oldTitleStr, elements):
        """Return a list of valid IDs from a string containing semicolon-separated titles."""
        if newTitleStr or oldTitleStr:
            if oldTitleStr != newTitleStr:
                elemIds = []
                for elemTitle in string_to_list(newTitleStr):
                    for elemId in elements:
                        if elements[elemId].title == elemTitle:
                            elemIds.append(elemId)
                            break
                    else:
                        # No break occurred: there is no element with the specified title
                        self._ui.show_error(f'{_("Wrong name")}: "{elemTitle}"', title=_('Input rejected'))
                return elemIds

        return None

    def _go_to_arc(self, event=None):
        """Go to the arc selected in the listbox."""
        try:
            selection = self._arcCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.scArcs[selection])

    def _pick_arc(self, event=None):
        """Enter the "add arc" selection mode."""
        self._start_picking_mode()
        self._ui.tv.tree.bind('<<TreeviewSelect>>', self._add_arc)
        self._ui.tv.tree.see(AC_ROOT)

    def _remove_arc(self, event=None):
        """Remove the arc selected in the listbox from the section arcs."""
        try:
            selection = self._arcCollection.cListbox.curselection()[0]
        except:
            return

        acId = self._element.scArcs[selection]
        title = self._mdl.novel.arcs[acId].title
        if self._ui.ask_yes_no(f'{_("Remove arc")}: "{title}"?'):

            # Remove the arc from the section's list.
            arcList = self._element.scArcs
            del arcList[selection]
            self._element.scArcs = arcList

            # Remove the section from the arc's list.
            arcSections = self._mdl.novel.arcs[acId].sections
            if self._elementId in arcSections:
                arcSections.remove(self._elementId)
                self._mdl.novel.arcs[acId].sections = arcSections

                # Remove turning point assignments, if any.
                for tpId in list(self._element.scTurningPoints):
                    if self._element.scTurningPoints[tpId] == acId:
                        del(self._element.scTurningPoints[tpId])
                        # removing the arc's turning point from the section's list
                        # Note: this doesn't trigger the refreshing method
                        self._mdl.novel.turningPoints[tpId].sectionAssoc = None
                        # un-assigning the section from the arc's turning point

    def _set_action_section(self, event=None):
        self._goalLabel.config(text=_('Goal'))
        self._conflictLabel.config(text=_('Conflict'))
        self._outcomeLabel.config(text=_('Outcome'))
        self._element.scPacing = self._sectionPacingType.get()

    def _set_custom_ar_section(self, event=None):
        self._goalLabel.config(text=self._customGoal)
        self._conflictLabel.config(text=self._customConflict)
        self._outcomeLabel.config(text=self._customOutcome)
        self._element.scPacing = self._sectionPacingType.get()

    def _set_reaction_section(self, event=None):
        self._goalLabel.config(text=_('Reaction'))
        self._conflictLabel.config(text=_('Dilemma'))
        self._outcomeLabel.config(text=_('Choice'))
        self._element.scPacing = self._sectionPacingType.get()

    def _toggle_arc_frame(self, event=None):
        """Hide/show the narrative arcs frame."""
        if prefs['show_sc_arcs']:
            self._arcFrame.hide()
            prefs['show_sc_arcs'] = False
        else:
            self._arcFrame.show()
            prefs['show_sc_arcs'] = True

    def _toggle_pacing_frame(self, event=None):
        """Hide/show the 'A/R/C' frame."""
        if prefs['show_action_reaction']:
            self._pacingFrame.hide()
            prefs['show_action_reaction'] = False
        else:
            self._pacingFrame.show()
            prefs['show_action_reaction'] = True

