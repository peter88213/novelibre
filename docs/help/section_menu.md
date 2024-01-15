[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Command reference: Section menu

--- 

# Section menu 

**Section operation**

--- 

## Add

**Add a new section**

You can add a section to the tree with **Section > Add**.
- The new section is placed at the next free position after the selection, if possible.
- Otherwise, no new section is generated.  
- The new section has an auto-generated title. You can change it in the right pane.

### Properties of a new section

- *Normal* type
- *Outline* completion status
- No viewpoint character assigned
- No arc or tag assigned
- No date/time set

--- 

## Set Type

**Set the [type](basic_concepts) of the selected section**

This can be *Normal* or *Unused*.

### Type change for multiple sections

Either select multiple sections, or select a chapter.

--- 

## Set Status

**Set the [section completion status](basic_concepts)**

This can be *Outline*, *Draft*, *1st Edit*, *2nd Edit*, or *Done*.

### Status change for multiple sections

- Either select multiple sections, or
- select a parent node (chapter or Book)

--- 

## Export section descriptions for editing 

**Export an ODT document**

This will generate a new OpenDocument text document (odt) containing a
**full synopsis** with part/chapter headings and section descriptions that can
be edited and written back to project format. File name suffix is
`_sections_tmp`.

--- 

## Export section list (spreadsheet) 

**Export an ODS document**

This will generate a new OpenDocument spreadsheet (ods) listing the following:

- Hyperlink to the section in the manuscript (if any)
- Section title
- Section description
- Tags
- Section notes
- A/R
- Goal
- Conflict
- Outcome
- Sequential section number
- Words total
- Word count
- Characters
- Locations
- Items

Only "normal" sections get a row in the section list. Sections of the "Unused" type are omitted.

File name suffix is `_sectionlist_tmp`.

--- 

[<< Previous](chapter_menu) -- [Next >>](characters_menu)