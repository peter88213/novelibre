"""Provide a class for ODT invisibly tagged project notes export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import PROJECTNOTES_SUFFIX
from nvlib.nv_locale import _


class OdtWProjectNotes(OdtWriter):
    """ODT project notes templates.

    Export project notes with invisible tags.
    """
    DESCRIPTION = _('Project notes')
    SUFFIX = PROJECTNOTES_SUFFIX

    _fileHeader = (
        f'{OdtWriter._CONTENT_XML_HEADER}<text:p text:style-name="Title">'
        '$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>\n'
        f'<text:h text:style-name="Heading_20_1">{_("Project notes")}</text:h>\n'
    )
    _projectNoteTemplate = (
        '<text:h text:style-name="Heading_20_2" '
        'text:outline-level="2">$Title</text:h>\n'
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$Desc\n'
        '</text:section>\n'
    )
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

