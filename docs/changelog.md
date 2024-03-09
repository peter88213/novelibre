[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "Features" project](https://github.com/users/peter88213/projects/14).


### v3.0.5

- Make the initial value for adding multiple sections a constant and set it to 1.
- Show an error message if a new element cannot be created.

Based on novxlib v2.0.1

### v3.0.4

- SimpleDialog class: Instead of just focusing, activate the default button. 

Based on novxlib v2.0.1

### v3.0.3

- Improve the "Export document" and the "New sections" 
  dialogs with a custom dialog box. 

Based on novxlib v2.0.1

### v3.0.2

- Fix a bug where imported sections are split at the 
  "####" mark, but not appended as they should. 

Based on novxlib v2.0.1

### v3.0.1

- Refactor the code.

Based on novxlib v2.0.0

### v3.0.0

- Fix a regression from v2.7.0 where faulty plot lists are generated. 
- Refactor the code, using the new "plot line/plot point" 
  wording for the variables and methods. 
- Upgrade the API to version 3 due to the DTD changes. Otherwise, plugins
  with v2.x API might not be able to read the novx files.
- Enable the online help in German.

Based on novxlib v2.0.0

### v2.7.0

- Rewording: Arc -> Plot line.
- Up to 20 sections can now be added at once.
- New option: Ask whether documents should be opened straight after export.
- New option: Lock the project after document export.
- Add "Export" options dialog. 
- In the section properties view, provide a text box to enter notes for the selected arc.
- Add the ODS Plot grid to the document types for export and import.
- Make the ODS Section list export-only.

Based on novxlib v1.5.0

### v2.6.1

- Provide translated headers for ODS export.
- Label the plugin manager exit button "Close".
- Label the view options exit button "Close".

Based on novxlib v1.4.2

### v2.6.0

- Add a button for creating the section duration from date/time difference.
- More robust ODS file reading.

Based on novxlib v1.4.1

### v2.5.0

- Add date/time information to the section list.

Based on novxlib v1.4.0

### v2.4.1

- Replace the "Segoe UI 10" font with "Calibri 10.5" for ODF document export.
- Fix a bug where links do not work in the ODS plot list for section titles containing false double quotes.

Based on novxlib v1.3.1

### v2.4.0

- Fix a bug where the plot list cannot be generated if an arc has no plot point.
- Reword/Refactor replacing "Turning point" with "Plot point" without affecting the API.

Based on novxlib v1.3.0

### v2.3.1

- Require changes to be saved before document export.
- Fix a bug where document import is aborted silently on error. 

Based on novxlib v1.2.1

### v2.3.0

- Export manuscripts and synopses optionally filtered either by viewpoint, or by arc.
- Disable several menus when locking the project.
- Lock/unlock the plugins.

Based on novxlib v1.2.0

### v2.2.0

- Do not ask before opening the manuscript, if the export is called by clicking on the toolbar icon.
- Modifiy the manuscript export wording in the Export menu.

Based on novxlib v1.1.0

### v2.1.0

**Please run the registry script "add_novelibre.reg" on Windows.** 

Rename the application.

Based on novxlib v1.1.0

### v2.0.0

**Please update all installed plugins. Check your program launcher/desktop shortcut, and re-run the registry script on Windows.** 
See [this message](https://github.com/peter88213/noveltree/discussions/1#discussioncomment-8526314).

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup and registry scripts.
- Rename packages that have "noveltree" in their name.
- Refactor the code for v2.0 API.

Based on novxlib v1.1.0

### v1.8.0

**Please update all installed plugins.** 
See [this message](https://github.com/peter88213/noveltree/discussions/1#discussioncomment-8510191).

- Re-structure the website; adjust links.

Based on novxlib v1.1.0

### v1.7.3

- Ask for confirmation before joining two sections.

Based on novxlib v1.1.0

### v1.7.2

- Split the "show_links" configuration for characters, locations, and items.

Based on novxlib v1.1.0

### v1.7.1

- If a section has a "day" instead of a date, calculate the age of the related characters based on the reference date, if any.
- Extend messaging.

Based on novxlib v1.1.0

### v1.7.0

- The age of the related characters can be called up in the section properties window. 

Based on novxlib v1.1.0

### v1.6.11

Fix a bug where detaching and re-docking the Properties view causes malfunction.

- Neatly reparent the Properties viewer when detaching/docking it.
- Catch all exceptions that might be raised on shutdown. 
- Never disable Text viewer and Properties buttons.

Based on novxlib v1.0.1

### v1.6.10

- Deactivate the detached mode for the Properties window to avoid problems
  caused by a bug yet to fix.

Based on novxlib v1.0.1

### v1.6.9

- Fix a bug where the writing progress is unclear because the overall word count is not provided by the model.

Based on novxlib v1.0.1

### v1.6.8

- Fix a bug in novxlib where turning points appear in the wrong columns
of the plot list ods export and html report.

Based on novxlib v1.0.1

### v1.6.7

- Fix a bug where locked documents are not highlighted in the import list.

Based on novxlib v1.0.0

### v1.6.6

- Mark turning points with "notes" in the tree.

Based on novxlib v1.0.0

### v1.6.5

- Add a "noveltree Home page" entry to the help menu.

Based on novxlib v1.0.0

### v1.6.4

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib v1.0.0

### v1.6.3

- Update icons.
. Update German translation.

Based on novxlib v1.0.0

### v1.6.2

- Make the context menus close under Linux when losing the focus.

Based on novxlib v1.0.0

### v1.6.1

- Add the short names to the section arcs view.

Based on novxlib v1.0.0

### v1.6.0

- Add "File > Copy style sheet" menu entry.

Based on novxlib v1.0.0

### v1.5.0

- Under Windows, exit the program with Alt-F4 instead of Ctrl-Q.
- No longer use the hotkeys F1..F4, F6...F12.

Based on novxlib v1.0.0

### v1.4.3

- When closing the project, disable the buttons introduced with v1.4.0.

Based on novxlib v1.0.0

### v1.4.2

- Fix a bug where property changes might be lost when pressing the F5 key.

Based on novxlib v1.0.0

### v1.4.1

- Add "Unused" checkboxes to the chapter/section properties view.

Based on novxlib v1.0.0

### v1.4.0

- Fix a bug where the project structure of a newly created project is invisible until the first element is created.
- Save new empty projects right after creation.

Extend the toolbar and change key bindings:

- Ctrl-N adds an element
- Ctrl-Alt-N adds a child element
- Ctrl-Alt-Shift-N adds a parent element

Extend the API:
- NvController.add_child()
- NvController.add_parent()
- NvController.add_element(): arguments changed

Based on novxlib v1.0.0

### v1.3.1

- Fix a bug where the HTML lists are not generated.

Based on novxlib v1.0.0

### v1.3.0

- Provide icons for the collection list buttons.
- Make the icons available for the entire GUI.

Based on novxlib v1.0.0

### v1.2.2

- Fix "View" menu control.
- Add "Import" menu control.
- Add "Project notes" menu control.

Based on novxlib v1.0.0

### v1.2.1

- Make it easier to exit the Pick Mode.

Based on novxlib v1.0.0

### v1.2.0

- Change the view of the arcs associated with a section into a list.
- Improve the usability by indicating the Pick Mode.
- Extend the API: NvView.set_status() takes a custom colors argument.

Based on novxlib v1.0.0

### v1.1.3

- Move the CollectionBox buttons to the right side.

Based on novxlib v1.0.0

### v1.1.2

- Fix a regression where the contents viewer is not reset on closing a project.
- Fix a bug where the stage level cannot be changed".

Based on novxlib v1.0.0

### v1.1.1

- Handle missing toolbar icon files.

Based on novxlib v1.0.0

### v1.1.0

- Integrate the toolbar. 
  If the *noveltree_toolbar* plugin is installed, please delete it with the Plugin manager.
- Refactor.

Based on novxlib v1.0.0

### v1.0.1

- Fix the plugin API version constant.

Based on novxlib v1.0.0

### v1.0.0

- Release under the GPLv3 license.

Based on noveltree-Alpha v0.10.0
Based on novxlib v1.0.0
