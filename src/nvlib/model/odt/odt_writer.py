"""Provide a generic class for ODT file export.

Other ODT file writers inherit from this class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

from nvlib.model.odf.odf_file import OdfFile
from nvlib.model.odt.novx_to_odt import NovxToOdt
from nvlib.novx_globals import Error
from nvlib.nv_locale import _


class OdtWriter(OdfFile):
    """Generic OpenDocument text templates and writer."""

    EXTENSION = '.odt'
    # overwrites Novel.EXTENSION

    _ODF_COMPONENTS = [
        'manifest.rdf',
        'META-INF',
        'content.xml',
        'meta.xml',
        'mimetype',
        'settings.xml',
        'styles.xml',
        'META-INF/manifest.xml',
    ]

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
        'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
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
        '  <style:font-face style:name="StarSymbol" '
        'svg:font-family="StarSymbol" style:font-charset="x-symbol"/>\n'
        '  <style:font-face style:name="Consolas" svg:font-family="Consolas" '
        'style:font-adornments="Standard" '
        'style:font-family-generic="modern" '
        'style:font-pitch="fixed"/>\n'
        '  <style:font-face style:name="Courier New" '
        'svg:font-family="&apos;Courier New&apos;" '
        'style:font-adornments="Standard" style:font-family-generic="modern" '
        'style:font-pitch="fixed"/>\n'
        ' </office:font-face-decls>\n'
        ' <office:automatic-styles/>\n'
        ' <office:body>\n'
        '  <office:text text:use-soft-page-breaks="true">\n\n'
    )
    _CONTENT_XML_FOOTER = (
        '  </office:text>\n'
        ' </office:body>\n'
        '</office:document-content>\n'
    )
    _META_XML = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:'
        'xmlns:office:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'office:version="1.2">\n'
        '  <office:meta>\n'
        '    <meta:generator>novelibre</meta:generator>\n'
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
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<manifest:manifest '
        'xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" '
        'manifest:version="1.2">\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/vnd.oasis.opendocument.text" '
        'manifest:full-path="/" />\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/xml" '
        'manifest:full-path="content.xml" manifest:version="1.2" />\n'
        '  <manifest:file-entry manifest:media-type="application/rdf+xml" '
        'manifest:full-path="manifest.rdf" manifest:version="1.2" />\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/xml" manifest:full-path="styles.xml" '
        'manifest:version="1.2" />\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/xml" manifest:full-path="meta.xml" '
        'manifest:version="1.2" />\n'
        '  <manifest:file-entry manifest:media-type="application/xml" '
        'manifest:full-path="settings.xml" manifest:version="1.2" />\n'
        '</manifest:manifest>\n'
    )
    _MANIFEST_RDF = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '  <rdf:Description rdf:about="styles.xml">\n'
        '    <rdf:type rdf:resource='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/odf#StylesFile"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="">\n'
        '    <ns0:hasPart xmlns:ns0='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" '
        'rdf:resource="styles.xml"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="content.xml">\n'
        '    <rdf:type rdf:resource='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="">\n'
        '    <ns0:hasPart '
        'xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" '
        'rdf:resource="content.xml"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="">\n'
        '    <rdf:type rdf:resource='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/pkg#Document"/>\n'
        '  </rdf:Description>\n'
        '</rdf:RDF>\n'
    )
    _SETTINGS_XML = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<office:document-settings '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'office:version="1.2">\n'
        ' <office:settings>\n'
        '  <config:config-item-set config:name="ooo:view-settings">\n'
        '   <config:config-item config:name="ViewAreaTop" '
        'config:type="int">0</config:config-item>\n'
        '   <config:config-item config:name="ViewAreaLeft" '
        'config:type="int">0</config:config-item>\n'
        '   <config:config-item config:name="ViewAreaWidth" '
        'config:type="int">30508</config:config-item>\n'
        '   <config:config-item config:name="ViewAreaHeight" '
        'config:type="int">27783</config:config-item>\n'
        '   <config:config-item config:name="ShowRedlineChanges" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="InBrowseMode" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item-map-indexed config:name="Views">\n'
        '    <config:config-item-map-entry>\n'
        '     <config:config-item config:name="ViewId" '
        'config:type="string">view2</config:config-item>\n'
        '     <config:config-item config:name="ViewLeft" '
        'config:type="int">8079</config:config-item>\n'
        '     <config:config-item config:name="ViewTop" '
        'config:type="int">3501</config:config-item>\n'
        '     <config:config-item config:name="VisibleLeft" '
        'config:type="int">0</config:config-item>\n'
        '     <config:config-item config:name="VisibleTop" '
        'config:type="int">0</config:config-item>\n'
        '     <config:config-item config:name="VisibleRight" '
        'config:type="int">30506</config:config-item>\n'
        '     <config:config-item config:name="VisibleBottom" '
        'config:type="int">27781</config:config-item>\n'
        '     <config:config-item config:name="ZoomType" '
        'config:type="short">0</config:config-item>\n'
        '     <config:config-item config:name="ViewLayoutColumns" '
        'config:type="short">1</config:config-item>\n'
        '     <config:config-item config:name="ZoomFactor" '
        'config:type="short">100</config:config-item>\n'
        '     <config:config-item config:name="IsSelectedFrame" '
        'config:type="boolean">false</config:config-item>\n'
        '    </config:config-item-map-entry>\n'
        '   </config:config-item-map-indexed>\n'
        '  </config:config-item-set>\n'
        '  <config:config-item-set '
        'config:name="ooo:configuration-settings">\n'
        '   <config:config-item config:name="AddParaSpacingToTableCells" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="PrintPaperFromSetup" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="IsKernAsianPunctuation" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintReversed" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="LinkUpdateMode" '
        'config:type="short">1</config:config-item>\n'
        '   <config:config-item config:name="DoNotCaptureDrawObjsOnPage" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="SaveVersionOnClose" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintEmptyPages" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="PrintSingleJobs" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="AllowPrintJobCancel" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="AddFrameOffsets" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintLeftPages" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="PrintTables" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="ProtectForm" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="ChartAutoUpdate" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="PrintControls" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="PrinterSetup" '
        'config:type="base64Binary">8gT+/0hQIExhc2VySmV0IFAyMDE0AAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAS'
        'FAgTGFzZXJKZXQgUDIwMTQAAAAAAAAAAAAAAAAAAAAWAAEAGAQAAAAAAAAEAAhSAAAEd'
        'AAAM1ROVwIACABIAFAAIABMAGEAcwBlAHIASgBlAHQAIABQADIAMAAxADQAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQQDANwANAMPnwAAAQAJAJoLNAgAAAEABwBYA'
        'gEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAU0RETQAGAAAABgAASFAgTGFzZXJKZXQgU'
        'DIwMTQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAA'
        'AEAAAAJAAAACQAAAAkAAAAJAAAACQAAAAkAAAAJAAAACQAAAAkAAAAJAAAACQAAAAkAA'
        'AAJAAAACQAAAAkAAAAJAAAACQAAAAAAAAABAAAAAQAAABoEAAAAAAAAAAAAAAAAAAAPA'
        'AAALQAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAgICAAP8AAAD//wAAAP8AAAD//wAAAP8A/'
        'wD/AAAAAAAAAAAAAAAAAAAAAAAoAAAAZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADeAwAA3gMAAAAAAAAAAAAAAIAAAAAAA'
        'AAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABrjvBgNAMAAAAAAAAAA'
        'AAABIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABIAQ09NUEFUX0RVUExFWF9NT0RFC'
        'gBEVVBMRVhfT0ZG</config:config-item>\n'
        '   <config:config-item config:name="CurrentDatabaseDataSource" '
        'config:type="string"/>\n'
        '   <config:config-item config:name="LoadReadonly" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="CurrentDatabaseCommand" '
        'config:type="string"/>\n'
        '   <config:config-item config:name="ConsiderTextWrapOnObjPos" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="ApplyUserData" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="AddParaTableSpacing" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="FieldAutoUpdate" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:'
        'name="IgnoreFirstLineIndentInNumbering" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="TabsRelativeToIndent" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:'
        'name="IgnoreTabsAndBlanksForLineCalculation" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintAnnotationMode" '
        'config:type="short">0</config:config-item>\n'
        '   <config:config-item config:name="AddParaTableSpacingAtStart" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="UseOldPrinterMetrics" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="TableRowKeep" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrinterName" '
        'config:type="string">HP LaserJet P2014</config:config-item>\n'
        '   <config:config-item config:name="PrintFaxName" '
        'config:type="string"/>\n'
        '   <config:config-item config:name="UnxForceZeroExtLeading" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintTextPlaceholder" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:'
        'name="DoNotJustifyLinesWithManualBreak" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintRightPages" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="CharacterCompressionType" '
        'config:type="short">0</config:config-item>\n'
        '   <config:config-item config:name="UseFormerTextWrapping" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="IsLabelDocument" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="AlignTabStopPosition" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="PrintHiddenText" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="DoNotResetParaAttrsForNumFont" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintPageBackground" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="CurrentDatabaseCommandType" '
        'config:type="int">0</config:config-item>\n'
        '   <config:config-item config:name="OutlineLevelYieldsNumbering" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintProspect" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintGraphics" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="SaveGlobalDocumentLinks" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintProspectRTL" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="UseFormerLineSpacing" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="AddExternalLeading" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="UseFormerObjectPositioning" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="RedlineProtectionKey" '
        'config:type="base64Binary"/>\n'
        '   <config:config-item config:name="MathBaselineAlignment" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:'
        'name="ClipAsCharacterAnchoredWriterFlyFrames" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="UseOldNumbering" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintDrawings" '
        'config:type="boolean">true</config:config-item>\n'
        '   <config:config-item config:name="PrinterIndependentLayout" '
        'config:type="string">disabled</config:config-item>\n'
        '   <config:config-item config:'
        'name="TabAtLeftIndentForParagraphsInList" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="PrintBlackFonts" '
        'config:type="boolean">false</config:config-item>\n'
        '   <config:config-item config:name="UpdateFromTemplate" '
        'config:type="boolean">true</config:config-item>\n'
        '  </config:config-item-set>\n'
        ' </office:settings>\n'
        '</office:document-settings>\n'
    )
    _STYLES_XML = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<office:document-styles '
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
        'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
        'xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" '
        'xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" '
        'xmlns:math="http://www.w3.org/1998/Math/MathML" '
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
        'xmlns:loext="urn:org:documentfoundation:names:experimental:'
        'office:xmlns:loext:1.0">\n'
        ' <office:font-face-decls>\n'
        '  <style:font-face style:name="StarSymbol" '
        'svg:font-family="StarSymbol" style:font-charset="x-symbol"/>\n'
        '  <style:font-face style:name="Calibri" '
        'svg:font-family="&apos;Calibri&apos;"/>\n'
        '  <style:font-face style:name="Courier New" '
        'svg:font-family="&apos;Courier New&apos;" '
        'style:font-adornments="Standard" style:font-family-generic="modern" '
        'style:font-pitch="fixed"/>\n'
        '  <style:font-face style:name="Consolas" '
        'svg:font-family="Consolas" style:font-adornments="Standard" '
        'style:font-family-generic="modern" style:font-pitch="fixed"/>\n'
        '  </office:font-face-decls>\n'
        ' <office:styles>\n'
        '  <style:default-style style:family="graphic">\n'
        '   <style:graphic-properties svg:stroke-color="#3465a4" '
        'draw:fill-color="#729fcf" fo:wrap-option="no-wrap" '
        'draw:shadow-offset-x="0.3cm" draw:shadow-offset-y="0.3cm" '
        'draw:start-line-spacing-horizontal="0.283cm" '
        'draw:start-line-spacing-vertical="0.283cm" '
        'draw:end-line-spacing-horizontal="0.283cm" '
        'draw:end-line-spacing-vertical="0.283cm" '
        'style:flow-with-text="true"/>\n'
        '   <style:paragraph-properties '
        'style:text-autospace="ideograph-alpha" style:line-break="strict" '
        'style:writing-mode="lr-tb" '
        'style:font-independent-line-spacing="false">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:color="#000000" '
        'fo:font-size="10pt" '
        'fo:language="$Language" fo:country="$Country" '
        'style:font-size-asian="10pt" style:language-asian="zxx" '
        'style:country-asian="none" style:font-size-complex="1pt" '
        'style:language-complex="zxx" style:country-complex="none"/>\n'
        '  </style:default-style>\n'
        '  <style:default-style style:family="paragraph">\n'
        '   <style:paragraph-properties '
        'fo:hyphenation-ladder-count="no-limit" '
        'style:text-autospace="ideograph-alpha" '
        'style:punctuation-wrap="hanging" style:line-break="strict" '
        'style:tab-stop-distance="1.251cm" style:writing-mode="lr-tb"/>\n'
        '   <style:text-properties fo:color="#000000" '
        'style:font-name="Calibri" fo:font-size="10.5pt" '
        'fo:language="$Language" fo:country="$Country" '
        'style:font-name-asian="Calibri" style:font-size-asian="10pt" '
        'style:language-asian="zxx" style:country-asian="none" '
        'style:font-name-complex="Segoe UI" style:font-size-complex="1pt" '
        'style:language-complex="zxx" style:country-complex="none" '
        'fo:hyphenate="false" fo:hyphenation-remain-char-count="2" '
        'fo:hyphenation-push-char-count="2"/>\n'
        '  </style:default-style>\n'
        '  <style:style style:name="Standard" style:family="paragraph" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties fo:line-height="0.73cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties style:font-name="Courier New" '
        'fo:font-size="12pt" fo:font-weight="normal"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Text_20_body" '
        'style:display-name="Text body" style:family="paragraph" '
        'style:parent-style-name="Standard" '
        'style:next-style-name="First_20_line_20_indent" style:class="text" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties style:page-number="auto">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="First_20_line_20_indent" '
        'style:display-name="First line indent" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0.499cm" '
        'style:auto-text-indent="false" style:page-number="auto"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Hanging_20_indent" '
        'style:display-name="Hanging indent" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" style:class="text">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="1cm" fo:margin-right="0cm" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="-0.499cm" '
        'style:auto-text-indent="false">\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="0cm"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Text_20_body_20_indent" '
        'style:display-name="Text body indent" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" style:class="text">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" '
        'style:auto-text-indent="false"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading" style:family="paragraph" '
        'style:parent-style-name="Standard" '
        'style:next-style-name="Text_20_body" style:class="text" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties fo:line-height="0.73cm" '
        'fo:text-align="center" style:justify-single-word="false" '
        'style:page-number="auto" fo:keep-with-next="always">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_1" '
        'style:display-name="Heading 1" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="1" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="1.461cm" fo:margin-bottom="0.73cm" '
        'style:page-number="auto">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:text-transform="uppercase" '
        'fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_2" '
        'style:display-name="Heading 2" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="2" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="1.461cm" fo:margin-bottom="0.73cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_3" '
        'style:display-name="Heading 3" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="3" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="0.73cm" fo:margin-bottom="0.73cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties fo:font-style="italic"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_4" '
        'style:display-name="Heading 4" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties fo:margin-top="0.73cm" '
        'fo:margin-bottom="0.73cm" style:page-number="auto"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_5" '
        'style:display-name="Heading 5" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties style:page-number="auto"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_6" '
        'style:display-name="Heading 6" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_7" '
        'style:display-name="Heading 7" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_8" '
        'style:display-name="Heading 8" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_9" '
        'style:display-name="Heading 9" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_10" '
        'style:display-name="Heading 10" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="10" style:list-style-name="" '
        'style:class="text">\n'
        '   <style:text-properties fo:font-size="75%" fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Header" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties fo:text-align="end" '
        'style:justify-single-word="false" style:page-number="auto" '
        'fo:padding="0.049cm" fo:border-left="none" fo:border-right="none" '
        'fo:border-top="none" fo:border-bottom="0.002cm solid #000000" '
        'style:shadow="none">\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" '
        'style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:font-variant="normal" '
        'fo:text-transform="none" fo:font-style="italic"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Header_20_left" '
        'style:display-name="Header left" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Header_20_right" '
        'style:display-name="Header right" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Footer" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties fo:text-align="center" '
        'style:justify-single-word="false" style:page-number="auto" '
        'text:number-lines="false" text:line-number="0">\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:font-size="11pt"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Footer_20_left" '
        'style:display-name="Footer left" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Footer_20_right" '
        'style:display-name="Footer right" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Title" style:family="paragraph" '
        'style:parent-style-name="Standard" style:next-style-name="Subtitle" '
        'style:class="chapter" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="0cm" '
        'fo:margin-right="0cm" fo:margin-top="0.000cm" '
        'fo:margin-bottom="0cm" fo:line-height="200%" '
        'fo:text-align="center" style:justify-single-word="false" '
        'fo:text-indent="0cm" style:auto-text-indent="false" '
        'style:page-number="auto" fo:background-color="transparent" '
        'fo:padding="0cm" fo:border="none" text:number-lines="false" '
        'text:line-number="0">\n'
        '    <style:tab-stops/>\n'
        '    <style:background-image/>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:text-transform="uppercase" '
        'fo:font-weight="normal" style:letter-kerning="false"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Subtitle" style:family="paragraph" '
        'style:parent-style-name="Title" style:class="chapter" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties fo:font-variant="normal" '
        'fo:text-transform="none" fo:letter-spacing="normal" '
        'fo:font-style="italic" fo:font-weight="normal"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Quotations" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" style:class="html">\n'
        '   <style:paragraph-properties fo:margin="100%" '
        'fo:margin-left="1cm" fo:margin-right="0cm" fo:margin-top="0cm" '
        'fo:margin-bottom="0cm" fo:text-indent="0cm" '
        'style:auto-text-indent="false"/>\n'
        '   <style:text-properties style:font-name="Consolas"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Emphasis" style:family="text">\n'
        '   <style:text-properties fo:font-style="italic" '
        'fo:background-color="transparent"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Strong_20_Emphasis" '
        'style:display-name="Strong Emphasis" style:family="text">\n'
        '   <style:text-properties fo:text-transform="uppercase"/>\n'
        '  </style:style>\n'
        ' </office:styles>\n'
        ' <office:automatic-styles>\n'
        '  <style:page-layout style:name="Mpm1">\n'
        '   <style:page-layout-properties fo:page-width="21.001cm" '
        'fo:page-height="29.7cm" style:num-format="1" '
        'style:paper-tray-name="[From printer settings]" '
        'style:print-orientation="portrait" fo:margin-top="3.2cm" '
        'fo:margin-bottom="2.499cm" fo:margin-left="2.701cm" '
        'fo:margin-right="3cm" style:writing-mode="lr-tb" '
        'style:layout-grid-color="#c0c0c0" style:layout-grid-lines="20" '
        'style:layout-grid-base-height="0.706cm" '
        'style:layout-grid-ruby-height="0.353cm" '
        'style:layout-grid-mode="none" style:layout-grid-ruby-below="false" '
        'style:layout-grid-print="false" style:layout-grid-display="false" '
        'style:footnote-max-height="0cm">\n'
        '    <style:columns fo:column-count="1" fo:column-gap="0cm"/>\n'
        '    <style:footnote-sep style:width="0.018cm" '
        'style:distance-before-sep="0.101cm" '
        'style:distance-after-sep="0.101cm" style:adjustment="left" '
        'style:rel-width="25%" style:color="#000000"/>\n'
        '   </style:page-layout-properties>\n'
        '   <style:header-style/>\n'
        '   <style:footer-style>\n'
        '    <style:header-footer-properties fo:min-height="1.699cm" '
        'fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="1.199cm" '
        'style:shadow="none" style:dynamic-spacing="false"/>\n'
        '   </style:footer-style>\n'
        '  </style:page-layout>\n'
        ' </office:automatic-styles>\n'
        ' <office:master-styles>\n'
        '  <style:master-page style:name="Standard" '
        'style:page-layout-name="Mpm1">\n'
        '   <style:footer>\n'
        '    <text:p text:style-name="Footer"><text:page-number '
        'text:select-page="current"/></text:p>\n'
        '   </style:footer>\n'
        '  </style:master-page>\n'
        ' </office:master-styles>\n'
        '</office:document-styles>\n'
    )
    _NOVELIBRE_STYLES = (
        f'  <style:style style:name="{_("Chapter_20_beginning")}" '
        f'style:display-name="{_("Chapter beginning")}" '
        'style:family="paragraph" style:parent-style-name="Text_20_body" '
        'style:next-style-name="First_20_line_20_indent" '
        'style:class="text">\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Epigraph")}" '
        f'style:display-name="{_("Epigraph")}" '
        'style:family="paragraph" style:parent-style-name="Quotations" '
        f'style:next-style-name="{_("Epigraph source")}" style:class="text">\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Epigraph_20_source")}" '
        f'style:display-name="{_("Epigraph source")}" '
        f'style:family="paragraph" style:parent-style-name="{_("Epigraph")}" '
        'style:next-style-name="Text_20_body" style:class="text">\n'
        '  <style:paragraph-properties fo:margin-top="0cm" '
        'fo:margin-bottom="1.46cm" fo:text-align="end"/>\n'
        '  <style:text-properties fo:language="zxx" fo:country="none" fo:font-style="italic"/>\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Section_20_mark")}" '
        f'style:display-name="{_("Section mark")}" '
        'style:family="paragraph" style:parent-style-name="Standard" '
        'style:next-style-name="Text_20_body" style:class="text">\n'
        '   <style:text-properties fo:color="#008000" '
        'fo:font-size="10pt" fo:language="zxx" fo:country="none"/>\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Heading_20_3_20_invisible")}" '
        f'style:display-name="{_("Heading 3 invisible")}" '
        'style:family="paragraph" '
        'style:parent-style-name="Heading_20_3" style:class="text">\n'
        '   <style:paragraph-properties fo:margin-top="0cm" '
        'fo:margin-bottom="0cm" fo:line-height="100%"/>\n'
        '   <style:text-properties text:display="none"/>\n'
        '  </style:style>'
    )
    _NOVELIBRE_STYLE_NAMES = (
        _('Chapter_20_beginning'),
        _('Epigraph'),
        _('Epigraph_20_source'),
        _('Section_20_mark'),
        _('Heading_20_3_20_invisible'),
    )

    _MIMETYPE = 'application/vnd.oasis.opendocument.text'

    def __init__(self, filePath, **kwargs):
        """Create a temporary directory for zipfile generation.
        
        Positional arguments:
            filePath: str -- path to the file 
                             represented by the Novel instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        Extends the superclass constructor,        
        """
        super().__init__(filePath, **kwargs)
        self._contentParser = NovxToOdt()

        self.userStylesXml = None
        # str -- Path to the user's custom styles.xml file.
        # This variable can be overwritten at runtime by the exporter class.

    @classmethod
    def add_novelibre_styles(cls, stylesXmlStr):
        """Return stylesXmlStr with the novelibre-specific styles inserted.
        
        The _NOVELIBRE_STYLES string is inserted right before the
        closing tag of the office:styles section.
        This method uses string processing instead of XML processing 
        for better performance.
        """
        success = False
        lines = stylesXmlStr.split('\n')
        newlines = []
        for line in lines:
            if '</office:styles>' in line:
                newlines.append(cls._NOVELIBRE_STYLES)
                success = True
            newlines.append(line)
        if not success:
            raise ValueError('Invalid XML Styles data')

        return '\n'.join(newlines)

    @classmethod
    def remove_novelibre_styles(cls, stylesXmlStr):
        """Return stylesXmlStr with the novelibre-specific styles removed."""
        for prefix in cls.NAMESPACES:
            ET.register_namespace(prefix, cls.NAMESPACES[prefix])
        root = ET.fromstring(stylesXmlStr)
        officeStyles = root.find('office:styles', cls.NAMESPACES)
        stylesToDiscard = []
        for officeStyle in officeStyles.iterfind(
            'style:style', cls.NAMESPACES
        ):
            officeStyleName = (
                officeStyle.attrib[f"{{{cls.NAMESPACES['style']}}}name"]
            )
            if officeStyleName in cls._NOVELIBRE_STYLE_NAMES:
                stylesToDiscard.append(officeStyle)
        for officeStyle in stylesToDiscard:
            officeStyles.remove(officeStyle)
        stylesXmlStr = ET.tostring(
            root,
            encoding='utf-8',
            xml_declaration=True
        ).decode('utf-8')
        return stylesXmlStr

    def write(self):
        """Determine the languages used in the document before writing.
        
        Extends the superclass method.
        """
        if self.novel.languages is None:
            self.novel.get_languages()
        return super().write()

    def _convert_from_novx(
            self,
            text,
            quick=False,
            append=False,
            firstInChapter=False,
            xml=False,
            linebreaks=False,
            firstParagraphStyle='Text_20_body',
            epigraph=False,
    ):
        """Return text without markup, converted to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick: bool -- if True, apply a conversion mode 
                           for one-liners without formatting.
            append: bool -- if True, indent the first paragraph.
            firstInChapter: bool: -- if True, the section begins a chapter.
            xml: bool -- if True, parse XML content. 
            linebreaks: bool -- if True and not xml, break the lines 
                                instead of creating paragraphs. 
            firstParagraphStyle: str -- The first paragraph's style, 
                                        if not xml and not append.
            epigraph: bool -- if True, use "Epigraph" paragraph styles.
        
        Overrides the superclass method.
        """
        if not text and not linebreaks:
            return ''

        if quick:
            return escape(text)

        if xml:
            self._contentParser.feed(
                text,
                self.novel.languages,
                append,
                firstInChapter,
                epigraph,
            )
            return ''.join(self._contentParser.odtLines)

        # Convert plain text into XML.
        lines = text.split('\n')
        if linebreaks or epigraph:
            # epigraph means epigraph's source
            text = '<text:line-break/>'.join(lines)
        else:
            text = (
                '</text:p><text:p text:style-name="First_20_line_20_indent">'
            ).join(lines)

        if epigraph:
            firstParagraphStyle = _('Epigraph_20_source')
        elif append:
            firstParagraphStyle = "First_20_line_20_indent"
        return (
            f'<text:p text:style-name="{firstParagraphStyle}">{text}</text:p>'
        )

    def _get_fileHeaderMapping(self):
        """Return a mapping dictionary for the project section.
        
        Extends the superclass method.
        """
        fileHeaderMapping = super()._get_fileHeaderMapping()
        filterMessage = fileHeaderMapping['Filters']
        if filterMessage:
            fileHeaderMapping['Filters'] = filterMessage.replace(
                'First_20_line_20_indent', 'Text_20_body'
            ).replace('<text:p', '\n<text:p')
        return fileHeaderMapping

    def _get_sectionMapping(
            self,
            scId,
            sectionNumber,
            wordsTotal=None,
            epigraph=None,
            **kwargs,
    ):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(
            scId,
            sectionNumber,
            wordsTotal=wordsTotal,
            epigraph=epigraph,
            **kwargs
        )
        sectionMapping['sectionTitle'] = _('Section')
        return sectionMapping

    def _get_styles_xml_str(self):
        """Return the styles.xml data as a string.
        
        Try reading the user's custom styles.xml file, if any,
        and add the novelibre-specific styles. 
        If this fails, or if there is no custom file,
        use the default styles.
        
        Extends the superclass method.
        """
        if self.userStylesXml:
            try:
                with open(self.userStylesXml, 'r', encoding='utf-8') as f:
                    stylesXmlStr = f.read()
                stylesXmlStr = self._set_document_language(stylesXmlStr)
                stylesXmlStr = self.add_novelibre_styles(stylesXmlStr)
                return stylesXmlStr

            except:
                pass
        stylesXmlStr = super()._get_styles_xml_str()
        stylesXmlStr = self.add_novelibre_styles(stylesXmlStr)
        return stylesXmlStr

    def _set_document_language(self, stylesXmlStr):
        # Return stylesXmlStr with the document language set.
        stylesXmlStr = re.sub(
            r'fo\:language=\".+?\"',
            f'fo:language="{self.novel.languageCode}"',
            stylesXmlStr
        )
        stylesXmlStr = re.sub(
            r'fo\:country=\".+?\"',
            f'fo:country="{self.novel.countryCode}"',
            stylesXmlStr
        )
        return stylesXmlStr

    def _set_up(self):
        # Helper method for ZIP file generation.
        # Add rdf manifest to the temporary directory containing
        # the internal structure of an ODF file.
        # Raise the "Error" exception in case of error.
        # Extends the superclass method.

        # Generate the common ODF components.
        super()._set_up()

        # Generate manifest.rdf
        try:
            with open(
                f'{self._tempDir}/manifest.rdf',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(self._MANIFEST_RDF)
        except:
            raise Error(f'{_("Cannot write file")}: "manifest.rdf"')

