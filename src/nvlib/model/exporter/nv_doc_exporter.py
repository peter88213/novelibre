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

    def run(self,
            source,
            suffix,
            filterElementId='',
            show=True,
            ask=True,
            overwrite=False,
            doNotExport=False,
    ):
        """Create a target object and run conversion.
        
        Positional arguments: 
            source -- NovxFile instance.
            suffix: str -- Target file name suffix.
                        
        Keyword arguments:
            filterElementId: str -- element ID for filtering chapters and sections.
            show: Boolean -- If True, open the exported document after creation.
            ask: Boolean -- If True, ask before opening the created document.
            overwrite: Boolean -- Overwrite existing files without confirmation.
            doNotExport: Boolean -- Open existing, if any. Do not export.

        Return a message. 
        """
        self._source = source
        self._isNewer = False
        __, self._target = self.exportTargetFactory.new_file_objects(self._source.filePath, suffix=suffix)

        if doNotExport:
            return self._open_document_if_up_to_date()

        # Set the user's custom styles.xml path.
        if os.path.isfile(USER_STYLES_XML):
            self._target.userStylesXml = USER_STYLES_XML

        if os.path.isfile(self._target.filePath) and not overwrite:
            targetTimestamp = os.path.getmtime(self._target.filePath)
            targetIsUpToDate = False
            try:
                if  targetTimestamp > self._source.timestamp:
                    timeStatus = _('Newer than the project file')
                    targetIsUpToDate = True
                    defaultChoice = 1
                else:
                    timeStatus = _('Older than the project file')
                    defaultChoice = 0
            except Exception:
                timeStatus = ''
                defaultChoice = 0
            self._targetFileDate = datetime.fromtimestamp(targetTimestamp).strftime('%c')
            message = _('{0} already exists.\n(last saved on {2})\n{1}.\n\nOpen this document instead of overwriting it?').format(
                self._target.DESCRIPTION, timeStatus, self._targetFileDate
            )
            result = self._ui.ask_overwrite_open_cancel(
                text=f"\n\n{message}\n\n",
                default=defaultChoice,
                title=_('Export document')
            )
            if result == 2:
                raise Notification(f'{_("Action canceled by user")}.')
                # raising the exception prevents project lock

            elif result == 1:
                return self._open_existing_document(targetIsUpToDate)

        # Generate a new document. Overwrite the existing document, if any.
        self._target.sectionFilter = FilterFactory.get_section_filter(filterElementId)
        self._target.chapterFilter = FilterFactory.get_chapter_filter(filterElementId)
        self._target.novel = self._source.novel
        self._target.write()
        self._targetFileDate = datetime.now().replace(microsecond=0).isoformat(sep=' ')
        if show and (not ask or not prefs['ask_doc_open'] or self._ui.ask_yes_no(
            message=_('Open the created document?'),
            detail=f"{self._target.novel.title} - {norm_path(self._target.DESCRIPTION)}")
        ):
            open_document(self._target.filePath)
        return _('Created {0} on {1}.').format(self._target.DESCRIPTION, self._targetFileDate)

    def _open_existing_document(self, isUpToDate):
        open_document(self._target.filePath)
        if isUpToDate:
            prefix = ''
        else:
            prefix = '#'
            # warning the user, if a document is open that might be outdated
        return f'{prefix}{_("Opened existing {0} (last saved on {1})").format(self._target.DESCRIPTION, self._targetFileDate)}.'

    def _open_document_if_up_to_date(self):
        if os.path.isfile(self._target.filePath):
            targetTimestamp = os.path.getmtime(self._target.filePath)
            if  targetTimestamp > self._source.timestamp:
                self._targetFileDate = datetime.fromtimestamp(targetTimestamp).strftime('%c')
                return self._open_existing_document(True)

            else:
                message = _('{0} is not up to date.').format(self._target.DESCRIPTION)
        else:
            message = _('{0} does not exist.').format(self._target.DESCRIPTION)
        return f'!{message}'
