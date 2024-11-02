"""Provide a tkinter based class for viewing and editing section properties with relationships and tags.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.widgets.folding_frame import FoldingFrame
from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from novxlib.model.date_time_tools import get_age
from novxlib.model.date_time_tools import get_specific_date
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import _
from novxlib.novx_globals import list_to_string
from novxlib.novx_globals import string_to_list
from nvlib.nv_globals import datestr
from nvlib.nv_globals import prefs
from nvlib.view.properties_window.basic_view import BasicView
from nvlib.widgets.collection_box import CollectionBox


class RelatedSectionView(BasicView):
    """Class for viewing and editing section properties with relationships and tags.
       
    Adds to the right pane:
    - A "Tags" entry.
    - A folding frame for relationships (characters/locations/items)
    """
    _HEIGHT_LIMIT = 10

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Tags' entry.
        self._tags = MyStringVar()
        self._tagsEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Tags'),
            textvariable=self._tags,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._tagsEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._tagsEntry)

        #--- Frame for section specific properties.
        self._sectionExtraFrame = ttk.Frame(self._elementInfoWindow)
        self._sectionExtraFrame.pack(anchor='w', fill='x')

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- Frame for 'Relationships'.
        self._relationFrame = FoldingFrame(self._elementInfoWindow, _('Relationships'), self._toggle_relation_frame)

        # 'Characters' listbox.
        self._crTitles = ''
        crHeading = ttk.Frame(self._relationFrame)
        self._characterLabel = ttk.Label(crHeading, text=_('Characters'))
        self._characterLabel.pack(anchor='w', side='left')
        ttk.Button(crHeading, text=_('Show ages'), command=self._show_ages).pack(anchor='e')
        crHeading.pack(fill='x')
        self._characterCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self._pick_character,
            cmdRemove=self._remove_character,
            cmdOpen=self._go_to_character,
            cmdActivate=self._activate_character_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._characterCollection.pack(fill='x')
        inputWidgets.extend(self._characterCollection.inputWidgets)

        # 'Locations' listbox.
        self._lcTitles = ''
        self._locationLabel = ttk.Label(self._relationFrame, text=_('Locations'))
        self._locationLabel.pack(anchor='w')
        self._locationCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self._pick_location,
            cmdRemove=self._remove_location,
            cmdOpen=self._go_to_location,
            cmdActivate=self._activate_location_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._locationCollection.pack(fill='x')
        inputWidgets.extend(self._locationCollection.inputWidgets)

        # 'Items' listbox.
        self._itTitles = ''
        self._itemLabel = ttk.Label(self._relationFrame, text=_('Items'))
        self._itemLabel.pack(anchor='w')
        self._itemCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self._pick_item,
            cmdRemove=self._remove_item,
            cmdOpen=self._go_to_item,
            cmdActivate=self._activate_item_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._itemCollection.pack(fill='x')
        inputWidgets.extend(self._itemCollection.inputWidgets)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

        self._prefsShowLinks = 'show_sc_links'

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        super().apply_changes()

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            self._element.tags = string_to_list(newTags)

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

        # 'Tags' entry.
        self._tagsStr = list_to_string(self._element.tags)
        self._tags.set(self._tagsStr)

        #--- Frame for 'Relationships'.
        if prefs['show_relationships']:
            self._relationFrame.show()
        else:
            self._relationFrame.hide()

        # 'Characters' window.
        self._crTitles = self._get_element_titles(self._element.characters, self._mdl.novel.characters)
        self._characterCollection.cList.set(self._crTitles)
        listboxSize = len(self._crTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._characterCollection.cListbox.config(height=listboxSize)
        if not self._characterCollection.cListbox.curselection() or not self._characterCollection.cListbox.focus_get():
            self._characterCollection.disable_buttons()

        # 'Locations' window.
        self._lcTitles = self._get_element_titles(self._element.locations, self._mdl.novel.locations)
        self._locationCollection.cList.set(self._lcTitles)
        listboxSize = len(self._lcTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._locationCollection.cListbox.config(height=listboxSize)
        if not self._locationCollection.cListbox.curselection() or not self._locationCollection.cListbox.focus_get():
            self._locationCollection.disable_buttons()

        # 'Items' window.
        self._itTitles = self._get_element_titles(self._element.items, self._mdl.novel.items)
        self._itemCollection.cList.set(self._itTitles)
        listboxSize = len(self._itTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._itemCollection.cListbox.config(height=listboxSize)
        if not self._itemCollection.cListbox.curselection() or not self._itemCollection.cListbox.focus_get():
            self._itemCollection.disable_buttons()

    def _activate_character_buttons(self, event=None):
        if self._element.characters:
            self._characterCollection.enable_buttons()
        else:
            self._characterCollection.disable_buttons()

    def _activate_location_buttons(self, event=None):
        if self._element.locations:
            self._locationCollection.enable_buttons()
        else:
            self._locationCollection.disable_buttons()

    def _activate_item_buttons(self, event=None):
        if self._element.items:
            self._itemCollection.enable_buttons()
        else:
            self._itemCollection.disable_buttons()

    def _add_character(self, event=None):
        # Add the selected element to the collection, if applicable.
        crList = self._element.characters
        crId = self._ui.tv.tree.selection()[0]
        if crId.startswith(CHARACTER_PREFIX) and not crId in crList:
            crList.append(crId)
            self._element.characters = crList

    def _add_location(self, event=None):
        # Add the selected element to the collection, if applicable.
        lcList = self._element.locations
        lcId = self._ui.tv.tree.selection()[0]
        if lcId.startswith(LOCATION_PREFIX)and not lcId in lcList:
            lcList.append(lcId)
            self._element.locations = lcList

    def _add_item(self, event=None):
        # Add the selected element to the collection, if applicable.
        itList = self._element.items
        itId = self._ui.tv.tree.selection()[0]
        if itId.startswith(ITEM_PREFIX)and not itId in itList:
            itList.append(itId)
            self._element.items = itList

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

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

    def _get_element_titles(self, elemIds, elements):
        """Return a list of element titles.
        
        Positional arguments:
            elemIds -- list of element IDs.
            elements -- list of element objects.          
        """
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(elements[elemId].title)
                except:
                    pass
        return elemTitles

    def _go_to_character(self, event=None):
        """Go to the character selected in the listbox."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.characters[selection])

    def _go_to_location(self, event=None):
        """Go to the location selected in the listbox."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.locations[selection])

    def _go_to_item(self, event=None):
        """Go to the item selected in the listbox."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.items[selection])

    def _pick_character(self, event=None):
        """Enter the "add character" selection mode."""
        self._start_picking_mode(command=self._add_character)
        self._ui.tv.see_node(CR_ROOT)

    def _pick_location(self, event=None):
        """Enter the "add location" selection mode."""
        self._start_picking_mode(command=self._add_location)
        self._ui.tv.see_node(LC_ROOT)

    def _pick_item(self, event=None):
        """Enter the "add item" selection mode."""
        self._start_picking_mode(command=self._add_item)
        self._ui.tv.see_node(IT_ROOT)

    def _remove_character(self, event=None):
        """Remove the character selected in the listbox from the section characters."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        crId = self._element.characters[selection]
        title = self._mdl.novel.characters[crId].title
        if self._ui.ask_yes_no(f'{_("Remove character")}: "{title}"?'):
            crList = self._element.characters
            del crList[selection]
            self._element.characters = crList

    def _remove_location(self, event=None):
        """Remove the location selected in the listbox from the section locations."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        lcId = self._element.locations[selection]
        title = self._mdl.novel.locations[lcId].title
        if self._ui.ask_yes_no(f'{_("Remove location")}: "{title}"?'):
            lcList = self._element.locations
            del lcList[selection]
            self._element.locations = lcList

    def _remove_item(self, event=None):
        """Remove the item selected in the listbox from the section items."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        itId = self._element.items[selection]
        title = self._mdl.novel.items[itId].title
        if self._ui.ask_yes_no(f'{_("Remove item")}: "{title}"?'):
            itList = self._element.items
            del itList[selection]
            self._element.items = itList

    def _show_ages(self, event=None):
        """Display the ages of the related characters."""
        if self._element.date is not None:
            now = self._element.date
        else:
            try:
                now = get_specific_date(
                    self._element.day,
                    self._mdl.novel.referenceDate
                    )
            except:
                self._show_missing_date_message()
                return

        charList = []
        for crId in self._element.characters:
            birthDate = self._mdl.novel.characters[crId].birthDate
            deathDate = self._mdl.novel.characters[crId].deathDate
            try:
                years = get_age(now, birthDate, deathDate)
                if years < 0:
                    years *= -1
                    suffix = _('years after death')
                else:
                    suffix = _('years old')
                charList.append(f'{self._mdl.novel.characters[crId].title}: {years} {suffix}')
            except:
                charList.append(f'{self._mdl.novel.characters[crId].title}: ({_("no data")})')

        if charList:
            self._ui.show_info(
                '\n'.join(charList),
                title=f'{_("Date")}: {datestr(now)}'
                )

    def _toggle_relation_frame(self, event=None):
        """Hide/show the 'Relationships' frame."""
        if prefs['show_relationships']:
            self._relationFrame.hide()
            prefs['show_relationships'] = False
        else:
            self._relationFrame.show()
            prefs['show_relationships'] = True

