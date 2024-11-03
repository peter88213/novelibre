"""Provide a class for html plot list representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import _
from nvlib.novx_globals import list_to_string


class HtmlPlotList(HtmlReport):
    """html plot list representation."""
    DESCRIPTION = _('HTML Plot list')
    SUFFIX = PLOTLIST_SUFFIX

    def write(self):
        """Create a HTML table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """

        def create_cell(text, attr=''):
            """Return the markup for a table cell with text and attributes."""
            return f'<td {attr}>{self._convert_from_novx(text)}</td>'

        htmlText = [self._fileHeader]
        htmlText.append(f'''<title>{self.novel.title}</title>
</head>
<body>
<p class=title>{self.novel.title} - {_("Plot")}</p>
<table>''')
        plotLineColors = (
            'LightSteelBlue',
            'Gold',
            'Coral',
            'YellowGreen',
            'MediumTurquoise',
            'Plum',
            )

        # Get plot lines.
        if self.novel.tree.get_children(PL_ROOT) is not None:
            plotLines = self.novel.tree.get_children(PL_ROOT)
        else:
            plotLines = []

        # Title row.
        htmlText.append('<tr class="heading">')
        htmlText.append(create_cell(''))
        for i, plId in enumerate(plotLines):
            colorIndex = i % len(plotLineColors)
            htmlText.append(create_cell(self.novel.plotLines[plId].title, attr=f'style="background: {plotLineColors[colorIndex]}"'))
        htmlText.append('</tr>')

        # Section rows.
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                # Section row
                if self.novel.sections[scId].scType == 0:
                    htmlText.append(f'<tr>')
                    htmlText.append(create_cell(self.novel.sections[scId].title))
                    for i, plId in enumerate(plotLines):
                        colorIndex = i % len(plotLineColors)
                        if scId in self.novel.plotLines[plId].sections:
                            plotPoints = []
                            for ppId in self.novel.tree.get_children(plId):
                                if scId == self.novel.plotPoints[ppId].sectionAssoc:
                                    plotPoints.append(self.novel.plotPoints[ppId].title)
                            htmlText.append(create_cell(list_to_string(plotPoints), attr=f'style="background: {plotLineColors[colorIndex]}"'))
                        else:
                            htmlText.append(create_cell(''))
                    htmlText.append(f'</tr>')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))
