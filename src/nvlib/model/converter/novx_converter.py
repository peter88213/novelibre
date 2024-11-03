"""Provide a converter class for novelibre universal import and export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.converter.converter_ff import ConverterFf
from nvlib.model.converter.new_project_factory import NewProjectFactory
from nvlib.model.novx.novx_file import NovxFile
from nvlib.model.ods.ods_r_charlist import OdsRCharList
from nvlib.model.ods.ods_r_grid import OdsRGrid
from nvlib.model.ods.ods_r_itemlist import OdsRItemList
from nvlib.model.ods.ods_r_loclist import OdsRLocList
from nvlib.model.ods.ods_w_charlist import OdsWCharList
from nvlib.model.ods.ods_w_grid import OdsWGrid
from nvlib.model.ods.ods_w_itemlist import OdsWItemList
from nvlib.model.ods.ods_w_loclist import OdsWLocList
from nvlib.model.ods.ods_w_plot_list import OdsWPlotList
from nvlib.model.ods.ods_w_sectionlist import OdsWSectionList
from nvlib.model.odt.odt_r_chapterdesc import OdtRChapterDesc
from nvlib.model.odt.odt_r_characters import OdtRCharacters
from nvlib.model.odt.odt_r_items import OdtRItems
from nvlib.model.odt.odt_r_locations import OdtRLocations
from nvlib.model.odt.odt_r_manuscript import OdtRManuscript
from nvlib.model.odt.odt_r_partdesc import OdtRPartDesc
from nvlib.model.odt.odt_r_plotlines import OdtRPlotlines
from nvlib.model.odt.odt_r_proof import OdtRProof
from nvlib.model.odt.odt_r_sectiondesc import OdtRSectionDesc
from nvlib.model.odt.odt_r_stages import OdtRStages
from nvlib.model.odt.odt_w_brief_synopsis import OdtWBriefSynopsis
from nvlib.model.odt.odt_w_chapterdesc import OdtWChapterDesc
from nvlib.model.odt.odt_w_characters import OdtWCharacters
from nvlib.model.odt.odt_w_export import OdtWExport
from nvlib.model.odt.odt_w_items import OdtWItems
from nvlib.model.odt.odt_w_locations import OdtWLocations
from nvlib.model.odt.odt_w_manuscript import OdtWManuscript
from nvlib.model.odt.odt_w_partdesc import OdtWPartDesc
from nvlib.model.odt.odt_w_plotlines import OdtWPlotlines
from nvlib.model.odt.odt_w_proof import OdtWProof
from nvlib.model.odt.odt_w_sectiondesc import OdtWSectionDesc
from nvlib.model.odt.odt_w_stages import OdtWStages
from nvlib.model.odt.odt_w_xref import OdtWXref


class NovxConverter(ConverterFf):
    """A converter for universal import and export.

    Support novelibre projects and most of the File subclasses 
    that can be read or written by OpenOffice/LibreOffice.

    Overrides the superclass constants EXPORT_SOURCE_CLASSES,
    EXPORT_TARGET_CLASSES, IMPORT_SOURCE_CLASSES, IMPORT_TARGET_CLASSES.

    Class constants:
        CREATE_SOURCE_CLASSES -- list of classes that - additional to HtmlImport
                        and HtmlOutline - can be exported to a new novelibre project.
    """
    EXPORT_SOURCE_CLASSES = [NovxFile]
    EXPORT_TARGET_CLASSES = [
        OdsWCharList,
        OdsWGrid,
        OdsWItemList,
        OdsWLocList,
        OdsWPlotList,
        OdsWSectionList,
        OdtWBriefSynopsis,
        OdtWChapterDesc,
        OdtWCharacters,
        OdtWExport,
        OdtWItems,
        OdtWLocations,
        OdtWManuscript,
        OdtWPartDesc,
        OdtWPlotlines,
        OdtWProof,
        OdtWSectionDesc,
        OdtWStages,
        OdtWXref,
    ]
    IMPORT_SOURCE_CLASSES = [
        OdsRCharList,
        OdsRGrid,
        OdsRItemList,
        OdsRLocList,
        OdtRChapterDesc,
        OdtRCharacters,
        OdtRItems,
        OdtRLocations,
        OdtRManuscript,
        OdtRPartDesc,
        OdtRPlotlines,
        OdtRProof,
        OdtRSectionDesc,
        OdtRStages,
    ]
    IMPORT_TARGET_CLASSES = [NovxFile]
    CREATE_SOURCE_CLASSES = []

    def __init__(self):
        """Change the newProjectFactory strategy.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self.newProjectFactory = NewProjectFactory(self.CREATE_SOURCE_CLASSES)
