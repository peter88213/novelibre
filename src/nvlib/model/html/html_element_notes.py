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
<title>{_('Notes')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Notes')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Title')}</td>
<td>{_('Text')}</td>
</tr>
'''
    _characterHeadingTemplate = f'''
<tr class="heading">
<td>{_("Characters")}</td>
<td />
</tr>
'''
    _locationHeadingTemplate = f'''
<tr class="heading">
<td>{_("Locations")}</td>
<td />
</tr>
'''
    _itemHeadingTemplate = f'''
<tr class="heading">
<td>{_("Items")}</td>
<td />
</tr>
'''
    _plotLineHeadingTemplate = f'''
<tr class="heading">
<td>{_("Plot lines")}</td>
<td />
</tr>
'''
    _partTemplate = '''<tr>
<td class="parttitle">$Title</td>
<td class="part">$Notes</td>
</tr>
'''
    _chapterTemplate = '''<tr>
<td class="chaptertitle">$Title</td>
<td class="chapter">$Notes</td>
</tr>
'''
    __plotLineTemplate = '''<tr>
<td class="title">$Title</td>
<td>$Notes</td>
</tr>
'''
    _sectionTemplate = _characterTemplate = _locationTemplate = _itemTemplate = _plotPointTemplate = '''<tr>
<td>$Title</td>
<td>$Notes</td>
</tr>
'''

    _stage1Template = '''<tr>
<td class="stagetitle">$Title</td>
<td class="stage">$Notes</td>
</tr>
'''

    _stage2Template = '''<tr>
<td class="stage">$Title</td>
<td class="stage">$Notes</td>
</tr>
'''
