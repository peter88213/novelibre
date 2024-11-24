"""Provide a converter class for report generation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.model.converter.export_target_factory import ExportTargetFactory
from nvlib.model.file.doc_open import open_document
from nvlib.model.html.html_characters import HtmlCharacters
from nvlib.model.html.html_items import HtmlItems
from nvlib.model.html.html_locations import HtmlLocations
from nvlib.model.html.html_plot_list import HtmlPlotList
from nvlib.model.html.html_project_notes import HtmlProjectNotes


class NvHtmlReporter:
    """Converter class for report generation.
    
    The HTML files are placed in a temporary directory 
    specified by the user interface's tempDir attribute, if any. 
    Otherwise, the project directory is used. 
    """
    EXPORT_TARGET_CLASSES = [
        HtmlCharacters,
        HtmlLocations,
        HtmlItems,
        HtmlPlotList,
        HtmlProjectNotes,
        ]

    def __init__(self):
        """Create strategy class instances.
        
        Extends the superclass constructor.
        """
        self._exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)

    def run(self, source, suffix, tempdir='.'):
        """Create a target object and run conversion.

        Positional arguments: 
            source -- NovxFile instance.
            suffix: str -- Target file name suffix.
            
        Optional arguments:
            tempdir: str -- Path to the directory where the HTML file is created.
        """
        kwargs = {'suffix':suffix}
        __, target = self._exportTargetFactory.new_file_objects(source.filePath, **kwargs)
        # Adjust HTML file path to the temp directory, if any
        # (the target factory sets the project directory; this is overridden here).
        __, filename = os.path.split(target.filePath)
        target.filePath = f'{tempdir}/{filename}'
        target.novel = source.novel
        target.write()
        open_document(target.filePath)

