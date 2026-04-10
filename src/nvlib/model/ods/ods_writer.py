"""Provide a generic class for ODS file export.

Other ODS file writers inherit from this class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template
from xml.sax.saxutils import escape

from nvlib.model.odf.odf_file import OdfFile


class OdsWriter(OdfFile):
    """Generic OpenDocument spreadsheet templates and writer."""
    EXTENSION = '.ods'
    _ODF_COMPONENTS = [
        'META-INF',
        'content.xml',
        'meta.xml',
        'mimetype',
        'styles.xml',
        'META-INF/manifest.xml'
    ]

    # Column width:
    # co1 2.000cm
    # co2 3.000cm
    # co3 4.000cm
    # co4 8.000cm

    _CONTENT_XML_HEADER = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<office:document-content '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
        'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
        'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
        'xmlns:fo="urn:oasis:names:tc:opendocument:'
        'xmlns:xsl-fo-compatible:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" '
        'xmlns:presentation="urn:oasis:names:tc:opendocument:'
        'xmlns:presentation:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:'
        'xmlns:svg-compatible:1.0" '
        'xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" '
        'xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" '
        'xmlns:math="http://www.w3.org/1998/Math/MathML" '
        'xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" '
        'xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:ooow="http://openoffice.org/2004/writer" '
        'xmlns:oooc="http://openoffice.org/2004/calc" '
        'xmlns:dom="http://www.w3.org/2001/xml-events" '
        'xmlns:xforms="http://www.w3.org/2002/xforms" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:rpt="http://openoffice.org/2005/report" '
        'xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'xmlns:tableooo="http://openoffice.org/2009/table" '
        'xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:'
        'xmlns:field:1.0" office:version="1.2">\n'
        ' <office:scripts/>\n'
        ' <office:font-face-decls>\n'
        '  <style:font-face style:name="Calibri" '
        'svg:font-family="&apos;Calibri&apos;" '
        'style:font-adornments="Standard" '
        'style:font-family-generic="swiss" style:font-pitch="variable"/>\n'
        ' </office:font-face-decls>\n'
        ' <office:automatic-styles>\n'
        '  <style:style style:name="co1" style:family="table-column">\n'
        '   <style:table-column-properties '
        'fo:break-before="auto" style:column-width="2.000cm"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="co2" style:family="table-column">\n'
        '   <style:table-column-properties '
        'fo:break-before="auto" style:column-width="3.000cm"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="co3" style:family="table-column">\n'
        '   <style:table-column-properties '
        'fo:break-before="auto" style:column-width="4.000cm"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="co4" style:family="table-column">\n'
        '   <style:table-column-properties '
        'fo:break-before="auto" style:column-width="8.000cm"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="ro1" style:family="table-row">\n'
        '   <style:table-row-properties style:row-height="1.157cm" '
        'fo:break-before="auto" style:use-optimal-row-height="true"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="ro2" style:family="table-row">\n'
        '   <style:table-row-properties style:row-height="2.053cm" '
        'fo:break-before="auto" style:use-optimal-row-height="true"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="ta1" style:family="table" '
        'style:master-page-name="Default">\n'
        '   <style:table-properties table:display="true" '
        'style:writing-mode="lr-tb"/>\n'
        '  </style:style>\n'
        '  <number:date-style style:name="N36" '
        'number:automatic-order="true">\n'
        '   <number:day number:style="long"/>\n'
        '   <number:text>.</number:text>\n'
        '   <number:month number:style="long"/>\n'
        '   <number:text>.</number:text>\n'
        '   <number:year number:style="long"/>\n'
        '  </number:date-style>\n'
        '  <number:time-style style:name="N40">\n'
        '   <number:hours number:style="long"/>\n'
        '   <number:text>:</number:text>\n'
        '   <number:minutes number:style="long"/>\n'
        '  </number:time-style>\n'
        '  <style:style style:name="ce1" style:family="table-cell" '
        'style:parent-style-name="Heading" style:data-style-name="N36"/>\n'
        '  <style:style style:name="ce2" style:family="table-cell" '
        'style:parent-style-name="Default" style:data-style-name="N36"/>\n'
        '  <style:style style:name="ce3" style:family="table-cell" '
        'style:parent-style-name="Heading" style:data-style-name="N40"/>\n'
        '  <style:style style:name="ce4" style:family="table-cell" '
        'style:parent-style-name="Default" style:data-style-name="N40"/>\n'
        '$Styles </office:automatic-styles>\n'
        ' <office:body>\n'
        '  <office:spreadsheet>\n'
        '   <table:table table:name="'
    )
    _CONTENT_XML_FOOTER = (
        '   </table:table>\n'
        '  </office:spreadsheet>\n'
        ' </office:body>\n'
        '</office:document-content>\n'
    )
    _META_XML = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<office:document-meta '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'office:version="1.2">\n'
        '  <office:meta>\n'
        '    <meta:generator>novxlib</meta:generator>\n'
        '    <dc:title>$Title</dc:title>\n'
        '    <dc:description>$Summary</dc:description>\n'
        '    <dc:subject></dc:subject>\n'
        '    <meta:keyword></meta:keyword>\n'
        '    <meta:initial-creator>$Author</meta:initial-creator>\n'
        '    <dc:creator></dc:creator>\n'
        '    <meta:creation-date>${Datetime}Z</meta:creation-date>\n'
        '    <dc:date></dc:date>\n'
        '  </office:meta>\n'
        '</office:document-meta>\n'
    )
    _MANIFEST_XML = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<manifest:manifest xmlns:manifest='
        '"urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" '
        'manifest:version="1.2">\n'
        ' <manifest:file-entry manifest:media-type='
        '"application/vnd.oasis.opendocument.spreadsheet" '
        'manifest:version="1.2" manifest:full-path="/"/>\n'
        ' <manifest:file-entry manifest:media-type="text/xml" '
        'manifest:full-path="content.xml"/>\n'
        ' <manifest:file-entry manifest:media-type="text/xml" '
        'manifest:full-path="styles.xml"/>\n'
        ' <manifest:file-entry manifest:media-type="text/xml" '
        'manifest:full-path="meta.xml"/>\n'
        ' <manifest:file-entry manifest:media-type="text/xml" '
        'manifest:full-path="settings.xml"/>\n'
        '</manifest:manifest>\n'
    )
    _STYLES_XML = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<office:document-styles '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
        'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
        'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
        'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:'
        'xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" '
        'xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:'
        'presentation:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:'
        'svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:'
        'xmlns:chart:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:'
        'xmlns:dr3d:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" '
        'xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" '
        'xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:ooow="http://openoffice.org/2004/writer" '
        'xmlns:oooc="http://openoffice.org/2004/calc" '
        'xmlns:dom="http://www.w3.org/2001/xml-events" '
        'xmlns:rpt="http://openoffice.org/2005/report" '
        'xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'xmlns:tableooo="http://openoffice.org/2009/table" '
        'office:version="1.2">\n'
        ' <office:font-face-decls>\n'
        '  <style:font-face style:name="Calibri" '
        'svg:font-family="&apos;Calibri&apos;" '
        'style:font-adornments="Standard" '
        'style:font-family-generic="swiss" style:font-pitch="variable"/>\n'
        ' </office:font-face-decls>\n'
        ' <office:styles>\n'
        '  <style:default-style style:family="table-cell">\n'
        '   <style:paragraph-properties style:tab-stop-distance="1.25cm"/>\n'
        '   <style:text-properties style:font-name="Arial" '
        'fo:language="$Language" fo:country="$Country" '
        'style:font-name-asian="Arial Unicode MS" style:language-asian="zh" '
        'style:country-asian="CN" style:font-name-complex="Tahoma" '
        'style:language-complex="hi" style:country-complex="IN"/>\n'
        '  </style:default-style>\n'
        '  <number:number-style style:name="N0">\n'
        '   <number:number number:min-integer-digits="1"/>\n'
        '  </number:number-style>\n'
        '  <style:style style:name="Default" style:family="table-cell">\n'
        '   <style:table-cell-properties style:text-align-source="fix" '
        'style:repeat-content="false" fo:background-color="transparent" '
        'fo:wrap-option="wrap" fo:padding="0.136cm" '
        'style:vertical-align="top"/>\n'
        '   <style:paragraph-properties fo:text-align="start"/>\n'
        '   <style:text-properties style:font-name="Calibri" '
        'fo:font-size="10.5pt" style:font-name-asian="Microsoft YaHei" '
        'style:font-name-complex="Lucida Sans"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Result" style:family="table-cell" '
        'style:parent-style-name="Default">\n'
        '   <style:text-properties fo:font-style="italic" '
        'style:text-underline-style="solid" '
        'style:text-underline-width="auto" '
        'style:text-underline-color="font-color" fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Result2" style:family="table-cell" '
        'style:parent-style-name="Result"/>\n'
        '  <style:style style:name="Heading" style:family="table-cell" '
        'style:parent-style-name="Default">\n'
        '   <style:table-cell-properties fo:background-color="#f0f0f0" '
        'style:text-align-source="fix" style:repeat-content="false"/>\n'
        '   <style:paragraph-properties fo:text-align="start"/>\n'
        '   <style:text-properties fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading1" '
        'style:family="table-cell" style:parent-style-name="Heading">\n'
        '   <style:table-cell-properties style:rotation-angle="90"/>\n'
        '  </style:style>\n'
        ' </office:styles>\n'
        ' <office:automatic-styles>\n'
        '  <style:page-layout style:name="Mpm1">\n'
        '   <style:page-layout-properties style:writing-mode="lr-tb"/>\n'
        '   <style:header-style>\n'
        '    <style:header-footer-properties fo:min-height="0.751cm" '
        'fo:margin-left="0cm" fo:margin-right="0cm" '
        'fo:margin-bottom="0.25cm"/>\n'
        '   </style:header-style>\n'
        '   <style:footer-style>\n'
        '    <style:header-footer-properties fo:min-height="0.751cm" '
        'fo:margin-left="0cm" fo:margin-right="0cm" '
        'fo:margin-top="0.25cm"/>\n'
        '   </style:footer-style>\n'
        '  </style:page-layout>\n'
        '  <style:page-layout style:name="Mpm2">\n'
        '   <style:page-layout-properties style:writing-mode="lr-tb"/>\n'
        '   <style:header-style>\n'
        '    <style:header-footer-properties fo:min-height="0.751cm" '
        'fo:margin-left="0cm" fo:margin-right="0cm" '
        'fo:margin-bottom="0.25cm" '
        'fo:border="0.088cm solid #000000" fo:padding="0.018cm" '
        'fo:background-color="#c0c0c0">\n'
        '     <style:background-image/>\n'
        '    </style:header-footer-properties>\n'
        '   </style:header-style>\n'
        '   <style:footer-style>\n'
        '    <style:header-footer-properties fo:min-height="0.751cm" '
        'fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0.25cm" '
        'fo:border="0.088cm solid #000000" fo:padding="0.018cm" '
        'fo:background-color="#c0c0c0">\n'
        '     <style:background-image/>\n'
        '    </style:header-footer-properties>\n'
        '   </style:footer-style>\n'
        '  </style:page-layout>\n'
        ' </office:automatic-styles>\n'
        ' <office:master-styles>\n'
        '  <style:master-page style:name="Default" '
        'style:page-layout-name="Mpm1">\n'
        '   <style:header>\n'
        '    <text:p><text:sheet-name>???</text:sheet-name></text:p>\n'
        '   </style:header>\n'
        '   <style:header-left style:display="false"/>\n'
        '   <style:footer>\n'
        '    <text:p>Seite <text:page-number>1</text:page-number></text:p>\n'
        '   </style:footer>\n'
        '   <style:footer-left style:display="false"/>\n'
        '  </style:master-page>\n'
        '  <style:master-page style:name="Report" '
        'style:page-layout-name="Mpm2">\n'
        '   <style:header>\n'
        '    <style:region-left>\n'
        '     <text:p><text:sheet-name>???</text:sheet-name> '
        '(<text:title>???</text:title>)</text:p>\n'
        '    </style:region-left>\n'
        '    <style:region-right>\n'
        '     <text:p><text:date style:data-style-name="N2" '
        'text:date-value="2021-03-15">15.03.2021</text:date>, '
        '<text:time>15:34:40</text:time></text:p>\n'
        '    </style:region-right>\n'
        '   </style:header>\n'
        '   <style:header-left style:display="false"/>\n'
        '   <style:footer>\n'
        '    <text:p>Seite <text:page-number>1</text:page-number> / '
        '<text:page-count>99</text:page-count></text:p>\n'
        '   </style:footer>\n'
        '   <style:footer-left style:display="false"/>\n'
        '  </style:master-page>\n'
        ' </office:master-styles>\n'
        '</office:document-styles>\n'
    )
    _MIMETYPE = 'application/vnd.oasis.opendocument.spreadsheet'

    def _convert_from_novx(self, text, **kwargs):
        """Return text, converted from novelibre markup to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            isLink: bool -- if True, 
                            avoid double quotes in the returned text. 
        
        Overrides the superclass method.
        """
        if not text:
            return ''

        return escape(text.rstrip()).replace('\n', '</text:p>\n<text:p>')

    def _get_extra_styles(self, elements):

        DEFAULT_BG_COLOR = '#f0f0f0'

        # Element name cell style.
        styleTemplate = (
            '  <style:style style:name="$Name" style:family="table-cell" '
            'style:parent-style-name="Default">\n'
            '   <style:table-cell-properties '
            'fo:border-bottom="none" '
            'fo:border-left="0.176cm solid $BgColor" '
            'fo:border-right="none" '
            'fo:border-top="none"/>\n'
            '  </style:style>'
        )

        mappings = {
            'DefaultBgColor': DEFAULT_BG_COLOR,
        }
        xmlText = []
        for elemId in elements:
            elemColor = elements[elemId].color
            if elemColor is not None:
                bgColor = elemColor
            else:
                bgColor = DEFAULT_BG_COLOR

            mappings['Name'] = elemId
            mappings['BgColor'] = bgColor
            styleXml = Template(styleTemplate)
            xmlText.append(styleXml.substitute(mappings))
        return '\n'.join(xmlText)

    def _get_fileHeaderMapping(self):
        fileHeaderMapping = super()._get_fileHeaderMapping()
        fileHeaderMapping['Styles'] = ''
        return fileHeaderMapping
