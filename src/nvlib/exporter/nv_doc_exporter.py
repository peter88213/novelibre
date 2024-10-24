"""Provide a converter class for document export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os

from novxlib.converter.export_target_factory import ExportTargetFactory
from novxlib.file.doc_open import open_document
from novxlib.novx.data_writer import DataWriter
from novxlib.novx_globals import Error
from novxlib.novx_globals import _
from novxlib.novx_globals import norm_path
from novxlib.ods.ods_w_charlist import OdsWCharList
from novxlib.ods.ods_w_grid import OdsWGrid
from novxlib.ods.ods_w_itemlist import OdsWItemList
from novxlib.ods.ods_w_loclist import OdsWLocList
from novxlib.ods.ods_w_plot_list import OdsWPlotList
from novxlib.ods.ods_w_sectionlist import OdsWSectionList
from novxlib.odt.odt_w_brief_synopsis import OdtWBriefSynopsis
from novxlib.odt.odt_w_chapterdesc import OdtWChapterDesc
from novxlib.odt.odt_w_characters import OdtWCharacters
from novxlib.odt.odt_w_export import OdtWExport
from novxlib.odt.odt_w_items import OdtWItems
from novxlib.odt.odt_w_locations import OdtWLocations
from novxlib.odt.odt_w_manuscript import OdtWManuscript
from novxlib.odt.odt_w_partdesc import OdtWPartDesc
from novxlib.odt.odt_w_plotlines import OdtWPlotlines
from novxlib.odt.odt_w_proof import OdtWProof
from novxlib.odt.odt_w_sectiondesc import OdtWSectionDesc
from novxlib.odt.odt_w_stages import OdtWStages
from novxlib.odt.odt_w_xref import OdtWXref
from nvlib.exporter.filter_factory import FilterFactory
from nvlib.nv_globals import prefs
from nvlib.widgets.nv_simpledialog import SimpleDialog


class NvDocExporter:
    """Converter class for document export."""
    EXPORT_TARGET_CLASSES = [
        DataWriter,
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

    def __init__(self, ui):
        """Create strategy class instances."""
        self._ui = ui
        self.exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)
        self._source = None
        self._target = None

    def run(self, source, suffix, **kwargs):
        """Create a target object and run conversion.
        
        Keyword arguments:
            show: Boolean -- If True, open the exported document after creation.
            ask: Boolean -- If True, ask before opening the created document.

        Positional arguments: 
            source -- NovxFile instance.
            suffix: str -- Target file name suffix.
            
        On success, return a message. Otherwise raise the Error exception.
        """
        self._source = source
        self._isNewer = False
        __, self._target = self.exportTargetFactory.make_file_objects(self._source.filePath, suffix=suffix)
        if os.path.isfile(self._target.filePath):
            targetTimestamp = os.path.getmtime(self._target.filePath)
            try:
                if  targetTimestamp > self._source.timestamp:
                    timeStatus = _('Newer than the project file')
                    self._isNewer = True
                    defaultButton = 1
                else:
                    timeStatus = _('Older than the project file')
                    defaultButton = 0
            except:
                timeStatus = ''
                defaultButton = 0
            self._targetFileDate = datetime.fromtimestamp(targetTimestamp).strftime('%c')
            title = _('Export document')
            message = _('{0} already exists.\n(last saved on {2})\n{1}.\n\nOpen this document instead of overwriting it?').format(
                        norm_path(self._target.DESCRIPTION), timeStatus, self._targetFileDate)
            askOverwrite = SimpleDialog(
                None,
                text=message,
                buttons=[_('Overwrite'), _('Open existing'), _('Cancel')],
                default=defaultButton,
                cancel=2,
                title=title
                )
            values = [False, True, None]
            openExisting = values[askOverwrite.go()]
            if openExisting is None:
                raise Error(f'{_("Action canceled by user")}.')

            elif openExisting:
                open_document(self._target.filePath)
                if self._isNewer:
                    prefix = ''
                else:
                    prefix = '!'
                    # warn the user, if a document is open that might be outdated
                return f'{prefix}{_("Opened existing {0} (last saved on {1})").format(self._target.DESCRIPTION, self._targetFileDate)}.'

        # Generate a new document. Overwrite the existing document, if any.
        filterElementId = kwargs.get('filter', '')
        self._target.sectionFilter = FilterFactory.get_section_filter(filterElementId)
        self._target.chapterFilter = FilterFactory.get_chapter_filter(filterElementId)
        self._target.novel = self._source.novel
        self._target.write()
        self._targetFileDate = datetime.now().replace(microsecond=0).isoformat(sep=' ')
        if kwargs.get('show', True):
            askOpen = kwargs.get('ask', True) and prefs['ask_doc_open']
            if not askOpen or self._ui.ask_yes_no(
                _('{} created.\n\nOpen now?').format(norm_path(self._target.DESCRIPTION)),
                title=self._target.novel.title,
                ):
                open_document(self._target.filePath)
        return _('Created {0} on {1}.').format(self._target.DESCRIPTION, self._targetFileDate)

