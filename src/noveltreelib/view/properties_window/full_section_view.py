"""Provide a tkinter based class for viewing and editing all section properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from noveltreelib.noveltree_globals import prefs
from noveltreelib.view.properties_window.dated_section_view import DatedSectionView
from noveltreelib.widgets.folding_frame import FoldingFrame
from noveltreelib.widgets.label_combo import LabelCombo
from noveltreelib.widgets.label_entry import LabelEntry
from noveltreelib.widgets.my_string_var import MyStringVar
from noveltreelib.widgets.text_box import TextBox
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import _
from novxlib.novx_globals import list_to_string
from novxlib.novx_globals import string_to_list
import tkinter as tk


class FullSectionView(DatedSectionView):
    """Class for viewing and editing section properties.
       
    Adds to the right pane:
    - A combobox for viewpoint character selection.
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
        self._appendToPrevCheckbox.pack(anchor='w', pady=2)
        inputWidgets.append(self._appendToPrevCheckbox)

        ttk.Separator(self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for arcs and plot.
        self._arcFrame = FoldingFrame(self._sectionExtraFrame, _('Plot'), self._toggle_arc_frame)

        # 'Arcs' entry.
        self._shortNames = MyStringVar()
        self._shortNamesEntry = LabelEntry(self._arcFrame, text=_('Arcs'), textvariable=self._shortNames)
        self._shortNamesEntry.pack(anchor='w')
        inputWidgets.append(self._shortNamesEntry)
        self._shortNamesEntry.entry.bind('<Return>', self.apply_changes)

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

        #--- 'Append to previous section' checkbox.
        self._element.appendToPrev = self._appendToPrev.get()

        #--- 'Arcs' entry.
        newShortNamesStr = self._shortNames.get()
        newShortNames = string_to_list(newShortNamesStr)
        arcs = {}
        # key: short name; value: ID
        for acId in self._mdl.novel.arcs:
            arcs[self._mdl.novel.arcs[acId].shortName] = acId
        newArcs = []
        checkedShortNames = []
        for shortName in newShortNames:
            if shortName in arcs:
                checkedShortNames.append(shortName)
                newArcs.append(arcs[shortName])
            else:
                self._ui.show_error(f'{_("Wrong name")}: "{shortName}"', title=_('Input rejected'))
        if checkedShortNames != newShortNames:
            self._shortNames.set(list_to_string(checkedShortNames))
        if self._element.scArcs != newArcs:
            self._element.scArcs = newArcs
            for acId in self._mdl.novel.arcs:
                arcSections = self._mdl.novel.arcs[acId].sections
                if acId in self._element.scArcs:
                    if not self._elementId in arcSections:
                        arcSections.append(self._elementId)
                else:
                    if self._elementId in arcSections:
                        arcSections.remove(self._elementId)
                        for tpId in list(self._element.scTurningPoints):
                            if self._element.scTurningPoints[tpId] == acId:
                                self._mdl.novel.turningPoints[tpId].sectionAssoc = None
                                del(self._element.scTurningPoints[tpId])
                self._mdl.novel.arcs[acId].sections = arcSections

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

        # 'Arcs' entry (if any).
        arcShortNames = []
        turningPointTitles = []
        for acId in self._element.scArcs:
            arcShortNames.append(self._mdl.novel.arcs[acId].shortName)
        for tpId in self._element.scTurningPoints:
            turningPointTitles.append(self._mdl.novel.turningPoints[tpId].title)
        self._shortNames.set(list_to_string(arcShortNames))
        self._turningPointsDisplay.config(text=list_to_string(turningPointTitles))

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

