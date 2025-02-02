"""Provide a converter class for novelibre universal import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.converter.converter import Converter
from nvlib.model.converter.new_project_factory import NewProjectFactory
from nvlib.model.converter.novx_conversion import NovxConversion


class NovxConverter(NovxConversion, Converter):
    """A converter for universal import and export.

    Support novelibre projects and most of the File subclasses 
    that can be read or written by OpenOffice/LibreOffice.
    """

    def __init__(self):
        """Change the newProjectFactory strategy.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self.newProjectFactory = NewProjectFactory(self.CREATE_SOURCE_CLASSES)
