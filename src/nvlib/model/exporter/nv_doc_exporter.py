"""Provide a converter class for document export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os

from nvlib.model.converter.export_target_factory import ExportTargetFactory
from nvlib.model.converter.novx_conversion import NovxConversion
from nvlib.model.exporter.filter_factory import FilterFactory
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import Notification
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import USER_STYLES_XML
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class NvDocExporter(NovxConversion):
    """Converter class for document export."""

    def __init__(self, ui):
        """Create strategy class instances."""
        self._ui = ui
        self.exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)
        self._source = None
        self._target = None

    def run(self, source, suffix, **kwargs):
        """Create a target object and run conversion.
        
        Keyword arguments:
            filter: str -- element ID for filtering chapters and sections.
            show: Boolean -- If True, open the exported document after creation.
            ask: Boolean -- If True, ask before opening the created document.

        Positional arguments: 
            source -- NovxFile instance.
            suffix: str -- Target file name suffix.
            overwrite: Boolean --Overwrite existing files without confirmation. 
            ask: Boolean -- Ask before opening the document.
                        
        On success, return a message. Otherwise raise an Error or Notification exception.
        """
        self._source = source
        self._isNewer = False
        overwrite = kwargs.get('overwrite', False)
        __, self._target = self.exportTargetFactory.new_file_objects(self._source.filePath, suffix=suffix)

        # Set the user's custom styles.xml path.
        if os.path.isfile(USER_STYLES_XML):
            self._target.userStylesXml = USER_STYLES_XML

        if os.path.isfile(self._target.filePath) and not overwrite:
            targetTimestamp = os.path.getmtime(self._target.filePath)
            try:
                if  targetTimestamp > self._source.timestamp:
                    timeStatus = _('Newer than the project file')
                    self._isNewer = True
                    defaultChoice = 1
                else:
                    timeStatus = _('Older than the project file')
                    defaultChoice = 0
            except:
                timeStatus = ''
                defaultChoice = 0
            self._targetFileDate = datetime.fromtimestamp(targetTimestamp).strftime('%c')
            message = _('{0} already exists.\n(last saved on {2})\n{1}.\n\nOpen this document instead of overwriting it?').format(
                        norm_path(self._target.DESCRIPTION), timeStatus, self._targetFileDate)
            result = self._ui.ask_overwrite_open_cancel(
                text=f"\n\n{message}\n\n",
                default=defaultChoice,
                title=_('Export document')
                )
            if result == 2:
                raise Notification(f'{_("Action canceled by user")}.')

            elif result == 1:
                open_document(self._target.filePath)
                if self._isNewer:
                    prefix = ''
                else:
                    prefix = '#'
                    # warning the user, if a document is open that might be outdated
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
                message=_('Open the created document?'),
                detail=f"{self._target.novel.title} - {norm_path(self._target.DESCRIPTION)}",
                ):
                open_document(self._target.filePath)
        return _('Created {0} on {1}.').format(self._target.DESCRIPTION, self._targetFileDate)

