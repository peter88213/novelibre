"""Provide a class for html element notes list representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import ELEMENT_NOTES_SUFFIX
from nvlib.nv_locale import _


class HtmlElementNotes(HtmlReport):
    """Class for HTML project notes report file representation."""
    DESCRIPTION = 'HTML element notes report'
    EXTENSION = '.html'
    SUFFIX = ELEMENT_NOTES_SUFFIX

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Project notes')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Project notes')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Title')}</td>
<td>{_('Text')}</td>
</tr>
'''

    _partTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$Notes</td>
</tr>
'''

    _chapterTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$Notes</td>
</tr>
'''
    _sectionTemplate = '''<tr>
<td>$Title</td>
<td>$Notes</td>
</tr>
'''

    _characterTemplate = '''<tr>
<td>$Title</td>
<td>$Notes</td>
</tr>
'''

    _locationTemplate = '''<tr>
<td>$Title</td>
<td>$Notes</td>
</tr>
'''

    _itemTemplate = '''<tr>
<td>$Title</td>
<td>$Notes</td>
</tr>
'''

    _stage1Template = '''<tr>
<td class="chtitle">$Title</td>
<td>$Notes</td>
</tr>
'''

    _stage2Template = '''<tr>
<td>$Title</td>
<td>$Notes</td>
</tr>
'''

    _plotLineTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$Notes</td>
</tr>
'''

    _plotPointTemplate = '''<tr>
<td>$Title</td>
<td>$Notes</td>
</tr>
'''

