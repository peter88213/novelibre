"""Provide a class for ODS plot grid import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.id_generator import new_id
from nvlib.model.data.section import Section
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import GRID_SUFFIX, CH_ROOT
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class OdsRGrid(OdsReader):
    """ODS section list reader. """
    DESCRIPTION = _('Plot grid')
    SUFFIX = GRID_SUFFIX
    COLUMN_TITLES = [
        'ID',
        'Section',
        'Date',
        'Time',
        'Day',
        'Duration',
        'Title',
        'Description',
        'Viewpoint',
        'Tags',
        'Scene',
        'Goal',
        'Conflict',
        'Outcome',
        'Notes',
    ]
    _idPrefix = SECTION_PREFIX,

    def add_new_element(self, prevId, row):
        """Add a new section to the tree.
        
        Positional arguments:
            prevId : str -- previous tree element, 
                            None if the new element is at the first place.
            row : List of the new element's properties. 
                  Used to determine whether a title is given.
        
        If a title is given:
            Create a Section instance,
            place its ID it after prevId in the tree,
            Return the section ID.
        Otherwise, return an empty string.
        """
        if not row[6]:
            return ''

        newId = new_id(self.novel.sections, prefix=SECTION_PREFIX)
        self.novel.sections[newId] = Section(
            scType=0,
            status=1,
            appendToPrev=False,
        )
        if prevId:
            chId = self.novel.tree.parent(prevId)
            index = self.novel.tree.get_children(chId).index(prevId) + 1
        else:
            chId = self.novel.tree.get_children(CH_ROOT)[0]
            index = 0
        self.novel.tree.insert(chId, index, newId)
        self.projectStructureModified = True
        return newId

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the Section attributes contained.
        Extends the superclass method.
        """
        self._columnTitles = self.COLUMN_TITLES[:]
        for plId in self.novel.plotLines:
            self._columnTitles.append(plId)
        super().read()
        self._read_sections()

        #--- plot line titles
        for i, column in enumerate(self._rows[0]):
            if column.startswith(PLOT_LINE_PREFIX):
                self.novel.plotLines[column].title = self._rows[1][i]

