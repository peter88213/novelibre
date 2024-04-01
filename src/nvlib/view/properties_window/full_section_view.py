"""Provide a tkinter based class for viewing and editing all section properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.nv_globals import prefs
from nvlib.view.properties_window.dated_section_view import DatedSectionView
from nvlib.widgets.collection_box import CollectionBox
from nvlib.widgets.folding_frame import FoldingFrame
from nvlib.widgets.label_combo import LabelCombo
from nvlib.widgets.my_string_var import MyStringVar
from nvlib.widgets.text_box import TextBox
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import PL_ROOT
from novxlib.novx_globals import PLOT_LINE_PREFIX
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
    - A "Plot" folding frame for plotLines and plot point associations.
    - An "Action/Reaction" folding frame for Goal/Reaction/Outcome.
    """

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
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

        #--- Frame for plot lines and plot.
        self._arcFrame = FoldingFrame(self._sectionExtraFrame, _('Plot'), self._toggle_arc_frame)

        # 'Plot lines' listbox.
        self._plotlineTitles = ''
        self._arcLabel = ttk.Label(self._arcFrame, text=_('Plot lines'))
        self._arcLabel.pack(anchor='w')
        self._plotlineCollection = CollectionBox(
            self._arcFrame,
            cmdAdd=self._pick_plotline,
            cmdRemove=self._remove_plotline,
            cmdOpen=self._go_to_arc,
            cmdActivate=self._activate_arc_buttons,
            cmdSelect=self._on_select_plotline,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._plotlineCollection.pack(fill='x')
        inputWidgets.extend(self._plotlineCollection.inputWidgets)
        self._selectedPlotline = None

        #--- 'Plot line notes' text box for entering self._element.plotNotes[plId],
        #    where plId is the ID of the selected plot line in the'Plot lines' listbox.
        ttk.Label(self._arcFrame, text=_('Notes on the selected plot line')).pack(anchor='w')
        self._plotNotesWindow = TextBox(
            self._arcFrame,
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
        self._plotNotesWindow.pack(fill='x')
        inputWidgets.append(self._plotNotesWindow)

        tk.Label(self._arcFrame, text=_('Plot points')).pack(anchor='w')

        #--- 'Plot points' label.
        self._plotPointsDisplay = tk.Label(self._arcFrame, anchor='w', bg='white')
        self._plotPointsDisplay.pack(anchor='w', fill='x')

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
        self._goalWindow = TextBox(
            self._pacingFrame,
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
        self._conflictWindow = TextBox(
            self._pacingFrame,
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
        self._outcomeWindow = TextBox(
            self._pacingFrame,
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

        #--- 'Plot line notes' text box.
        self._save_plot_notes()

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

        #--- 'Plot lines' listbox.
        self._plotlineTitles = self._get_plotline_titles(self._element.scPlotLines, self._mdl.novel.plotLines)
        self._plotlineCollection.cList.set(self._plotlineTitles)
        listboxSize = len(self._plotlineTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._plotlineCollection.cListbox.config(height=listboxSize)
        if not self._plotlineCollection.cListbox.curselection() or not self._plotlineCollection.cListbox.focus_get():
            self._plotlineCollection.disable_buttons()

        #--- 'Plot notes' text box.
        self._plotNotesWindow.clear()
        self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='light gray')
        if self._plotlineTitles:
            self._plotlineCollection.cListbox.select_set(0)
            self._selectedPlotline = 0
            self._on_select_plotline(0)
        else:
            self._selectedPlotline = None

        #--- "Plot points" label
        plotPointTitles = []
        for ppId in self._element.scPlotPoints:
            plId = self._element.scPlotPoints[ppId]
            plotPointTitles.append(f'{self._mdl.novel.plotLines[plId].shortName}: {self._mdl.novel.plotPoints[ppId].title}')
        self._plotPointsDisplay.config(text=list_to_string(plotPointTitles))

        #--- 'Unused' checkbox.
        if self._element.scType > 0:
            self._isUnused.set(True)
        else:
            self._isUnused.set(False)

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

        #--- Frame for plot lines.
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

    def unlock(self):
        """Enable plot line notes only if a plot line is selected."""
        super().unlock()
        if self._selectedPlotline is None:
            self._plotNotesWindow.config(state='disabled')

    def _activate_arc_buttons(self, event=None):
        if self._element.scPlotLines:
            self._plotlineCollection.enable_buttons()
        else:
            self._plotlineCollection.disable_buttons()

    def _add_plotline(self, event=None):
        # Add the selected element to the collection, if applicable.
        plotlineList = self._element.scPlotLines
        plId = self._ui.tv.tree.selection()[0]
        if not plId.startswith(PLOT_LINE_PREFIX):
            # Restore the previous section selection mode.
            self._end_picking_mode()
        elif not plId in plotlineList:
            plotlineList.append(plId)
            self._element.scPlotLines = plotlineList
            plotlineSections = self._mdl.novel.plotLines[plId].sections
            if not self._elementId in plotlineSections:
                plotlineSections.append(self._elementId)
                self._mdl.novel.plotLines[plId].sections = plotlineSections

    def _get_plotline_titles(self, elemIds, elements):
        """Return a list of plot line titles, preceded by the short names.
        
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
        """Go to the plot line selected in the listbox."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.scPlotLines[selection])

    def _on_select_plotline(self, selection):
        """Callback routine for section plot line list selection."""
        self._save_plot_notes()
        self._selectedPlotline = self._element.scPlotLines[selection]
        self._plotNotesWindow.config(state='normal')
        if self._element.plotNotes:
            self._plotNotesWindow.set_text(self._element.plotNotes.get(self._selectedPlotline, ''))
        else:
            self._plotNotesWindow.clear()
        if self._isLocked:
            self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='white')

    def _pick_plotline(self, event=None):
        """Enter the "add plot line" selection mode."""
        self._start_picking_mode()
        self._ui.tv.tree.bind('<<TreeviewSelect>>', self._add_plotline)
        self._ui.tv.tree.see(PL_ROOT)

    def _remove_plotline(self, event=None):
        """Remove the plot line selected in the listbox from the section associations."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        plId = self._element.scPlotLines[selection]
        title = self._mdl.novel.plotLines[plId].title
        if not self._ui.ask_yes_no(f'{_("Remove plot line")}: "{title}"?'):
            return

        # Remove the plot line from the section's list.
        arcList = self._element.scPlotLines
        del arcList[selection]
        self._element.scPlotLines = arcList

        # Remove the section from the plot line's list.
        arcSections = self._mdl.novel.plotLines[plId].sections
        if self._elementId in arcSections:
            arcSections.remove(self._elementId)
            self._mdl.novel.plotLines[plId].sections = arcSections

            # Remove plot point assignments, if any.
            for ppId in list(self._element.scPlotPoints):
                if self._element.scPlotPoints[ppId] == plId:
                    del(self._element.scPlotPoints[ppId])
                    # removing the plot line's plot point from the section's list
                    # Note: this doesn't trigger the refreshing method
                    self._mdl.novel.plotPoints[ppId].sectionAssoc = None
                    # un-assigning the section from the plot line's plot point

    def _save_plot_notes(self):
        if self._selectedPlotline and self._plotNotesWindow.hasChanged:
            plotNotes = self._element.plotNotes
            if plotNotes is None:
                plotNotes = {}
            plotNotes[self._selectedPlotline] = self._plotNotesWindow.get_text()
            self.doNotUpdate = True
            self._element.plotNotes = plotNotes
            self.doNotUpdate = False

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
        """Hide/show the plot lines frame."""
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

