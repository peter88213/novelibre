[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Command reference: Export menu

--- 

**NOTE:** This help page applies to *novelyst* and is not yet updated for *noveltree*.

# Export menu 

**File export**

---

## Manuscript for editing

This will write parts, chapters, and sections into a new OpenDocument
text document (odt) with invisible chapter and section sections (to be
seen in the Navigator). File name suffix is `_manuscript`.

-   Only "normal" chapters and sections are exported. Chapters and
    sections marked "unused", "todo" or "notes" are not exported.
-   Comments within sections are written back as section titles 
    if surrounded by `~`.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Chapters and sections can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split sections by inserting headings or a section divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Section divider. Optionally, you can append the 
       section title to the section divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split sections from *Writer* to *noveltree* not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.


---

## Notes chapters for editing

This will write "Notes" parts and chapters with child sections into a new 
OpenDocument text document (odt) with invisible chapter and section 
sections (to be seen in the Navigator). File name suffix is `_notes`.

-   Comments within sections are written back as section titles
    if surrounded by `~`.
-   Chapters and sections can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split sections by inserting headings or a section divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Section divider. Optionally, you can append the 
       section title to the section divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split sections from *Writer* to *noveltree* not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Todo chapters for editing

This will write "Todo" parts and chapters with child sections into a new 
OpenDocument text document (odt) with invisible chapter and section 
sections (to be seen in the Navigator). File name suffix is `_todo`.

-   Comments within sections are written back as section titles
    if surrounded by `~`.
-   Chapters and sections can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split sections by inserting headings or a section divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Section divider. Optionally, you can append the 
       section title to the section divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split sections from *Writer* to *noveltree* not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Manuscript with visible structure tags for proof reading

This will write parts, chapters, and sections into a new OpenDocument
text document (odt) with visible section markers. File name suffix is
`_proof`.

-   Only "normal" chapters and sections are exported. Chapters and
    sections marked "unused", "todo" or "notes" are not exported.
-   Sections beginning with `<HTML>` or `<TEX>` are not exported.
-   The document contains chapter and section headings. However, changes will not be written back.
-   The document contains section `[ScID:x]` markers.
    **Do not touch lines containing the markers** if you want to
    be able to write the document back to *noveltree* format.
-   Chapters and sections can neither be rearranged nor deleted.
-   When editing the document, you can split sections by inserting headings or a section divider:
    -   *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -   *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -   `###` → Section divider. Optionally, you can append the 
        section title to the section divider. You can also add a description, separated by `|`.
    -   **Note:** Export documents with split sections from *Writer* to *noveltree* not more than once.      
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Manuscript without tags (export only)

This will write parts, chapters, and sections into a new OpenDocument
text document (odt).

-   The document is placed in the same folder as the project.
-   Document's **filename**: `<project name>.odt`.
-   Only "normal" chapters and sections are exported. Chapters and
    sections marked "unused", "todo" or "notes" are not exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Comments with special marks (like `/*@en this is an endnote. */`) 
    are converted into footnotes or endnotes. Markup:
    - `@fn*` -- simple footnote, marked with an astersik
    - `@fn` -- numbered footnote
    - `@en` -- numbered endnote   
-   Gobal variables and project variables are not resolved.
-   Part titles appear as first level heading.
-   Chapter titles appear as second level heading.
-   Section titles appear as navigable comments pinned to the beginning of
    the section.
-   Sections are separated by `* * *`. The first line is not
    indented.
-   Starting from the second paragraph, paragraphs begin with
    indentation of the first line.
-   Sections marked "attach to previous section" appear like
    continuous paragraphs.
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Brief synopsis (export only)

This will write a brief synopsis with part, chapter, and sections titles into a new 
OpenDocument text document.  File name suffix is `_brf_synopsis`.
 
-   Only "normal" chapters and sections are exported. Chapters and
    sections marked "unused", "todo" or "notes" are not exported.
-   Titles of sections beginning with `<HTML>` or `<TEX>` are not exported.
-   Part titles appear as first level heading.
-   Chapter titles appear as second level heading.
-   Section titles appear as plain paragraphs.

---

## Cross references (export only)

This will generate a new OpenDocument text document (odt) containing
navigable cross references. File name suffix is `_xref`. The cross
references are:

-   Sections per character,
-   sections per location,
-   sections per item,
-   sections per tag,
-   characters per tag,
-   locations per tag,
-   items per tag.

---

## Obfuscated text for word count

This will generate a text file (txt) containing all "normal" sections 
(without headings), where the characters are replaced with "x". 
It generates the same word count as you see displayed in *noveltree*. 

---

## Characters/locations/items data files

This will create a set of XML files containing the project's characters, 
locations, and items with all their properties. 
These files can be used to export the characters, locations, 
and items to another project (also with noveltree).

To import XML data files from another project, use the **Import** command
in the **Characters**, **Locations**, or **Items** menu. 

---

## Plot description (export only)

This will write plot-defining "Todo" parts and chapters into a new 
OpenDocument text document (odt). File name suffix is `_plot`.

The document contains:

- "Todo" chapters within the narrative part (titles and descriptions).
- Part titles (first level heading, only if the part's first chapter defines an arc)
- Arc titles (second level heading)
- Arc descriptions
- Point titles (third level heading)
- Links to the associated section, if any
- Point descrptions.
- Point contents.


---

## Plot spreadsheet (export only)

**Export an ODS document**

This will generate a new OpenDocument spreadsheet (ods) containing sections, 
arcs, plot structure, and plot points. File name suffix is `_plotlist`.
The spreadsheet is not meant to be written back to *noveltree*.

- There are hyperlinks to the sections in the manuscript, and to the chapters in the plot description.

---

## Show Plot list

Show sections, arcs, plot structure, and plot points.
This will generate a list-formatted HTML file, and launch your system's web browser for displaying it. 

- The Report is a temporary file, auto-deleted on program exit.
- If needed, you can have your web browser save or print it.

---

[<< Previous](project_notes_menu) -- [Next >>](import_menu)