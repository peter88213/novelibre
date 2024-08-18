[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "Features" project](https://github.com/users/peter88213/projects/14).

### Version 4.9.5

- Rejecting malformed .novx files.

Based on novxlib 4.6.3

### Version 4.9.4

- Text box discarding illegal characters.
- novxlib update for safe XML reading and writing.

Based on novxlib 4.6.2

### Version 4.9.3

- Refactor for future Python versions.

Based on novxlib 4.5.9

### Version 4.9.2

- Handling novx XML parser error.
- Using raw strings for regular expressions.
- Adjusting separators in File.filePath.
- Refactor for future Python versions.

Based on novxlib 4.5.7

### Version 4.9.1

- Remove "private" tkinter imports that would not work with Linux.

Based on novxlib 4.5.3

### Version 4.9.0

- Make the right mouse button work under Mac OS.
- Extend the API, providing a global PLATFORM constant.

Based on novxlib 4.5.3

### Version 4.8.3

- Fix a regression from version 4.8.2 where project files could be mistakenly rejected as corrupted.

Based on novxlib 4.5.3

### Version 4.8.2

- Validating model object property types to prevent broken plugins from causing major damage.

Based on novxlib 4.5.2

### Version 4.8.1

- Prevent overwriting novx files with incomplete XML structures in case of conversion errors. 
- Show a popup message, if saving fails.

Based on novxlib 4.5.1

### Version 4.8.0

- Use a special paragraph style for the chapter beginnings in the manuscript and in the final document.
- Use translated names for the custom ODT styles used.

Based on novxlib 4.5.0

### Version 4.7.0

- API change: New option "localize_date".
- Make date localization optional (Closes #26).

Based on novxlib 4.4.2

### Version 4.6.2

- Fix a bug where no modification is indicated when the reference date is cleared.

Based on novxlib 4.4.1

### Version 4.6.1

- Add accelerator key to the "Online help" menu entry.

Based on novxlib 4.4.0

### Version 4.6.0

- Provide context sensitive help via F1 key and several mouse buttons.

Based on novxlib 4.4.0

### Version 4.5.2

- Update messages for wrong date/time entry.

Based on novxlib 4.4.0

### Version 4.5.0

- API update: Add register/unregister methods to NvView.

Based on novxlib 4.4.0

### Version 4.4.2

- Use the customized field titles for document export.

Based on novxlib 4.4.0

### Version 4.4.1

- Revise the "missing date/reference date" messaging.

Based on novxlib 4.3.0

### Version 4.4.0

- Show section moon phase on demand.
- Extend the API, providing a service for moonphase calculation.

Based on novxlib 4.3.0

### Version 4.3.4

novxlib update, verifying XML input:
- Check whether project notes IDs start with the correct prefix.

Based on novxlib 4.2.2

### Version 4.3.3

novxlib update, verifying XML input:
- Check whether IDs start with the correct prefix.

Based on novxlib 4.2.1

### Version 4.3.2

novxlib update, verifying XML input:
- ISO-formatted date
- ISO-formatted time
- Strings representing numbers

Based on novxlib 4.2.0

### Version 4.3.1

- Fix a bug in PluginCollection.load_file(), where the plugin's file path gets lost 
  if the plugin inherits from PluginBase.
- Refactor the nv_controller module.
- Update the PluginBase class.

Based on novxlib 4.1.0

### Version 4.3.0

Extend the API for the nv_clipboard plugin.

- Make the toolbar delegate in NvView a "public" instance variable.
- Make the Toolbar buttonBar a "public" instance variable.
- Add a service to the controller that returns the global preferences.
- Remove unused imports; update docstrings.

Based on novxlib 4.1.0

### Version 4.2.1

- Make sure that critical errors do not happen silently. 
  In case of unhandled exceptions, show a popup window with the stack trace.
  This is only part of the "run.pyw" starter script generated during setup. 

Based on novxlib 4.1.0

### Version 4.2.0

- Upgrade the plugin API by improving the *NvService* interface. 
  The service now returns *NvTreeview* instances instead of *NvView* instances. 
  This may help to avoid side effects in case of a broken plugin implementation.

Based on novxlib 4.1.0

### Version 4.1.2

- Fix a regression from version 4.1.1 where plot points cannot be created.
- Refactor: make nvService inherit from novxService.
- Refactor: use nvService factory methods for model object instantiation.
- Refactor: convert TreeViewer local functions into methods.

Based on novxlib 4.1.0

### Version 4.1.1

- Library update. Now reading and writing *.novx* version 1.4 files.
- Make the Action/Reaction scheme more general (#22).
- Refactor, changing the API.
- Provide a service class with factory methods and getters for the novxlib model.

Based on novxlib 4.0.2

### Version 3.9.2

- Make sure not to read back redundant language tags from ODT.

Based on novxlib 3.7.4

### Version 3.9.1

- Change the view settings of generated ODT documents to single page per column.
- Leave empty plot notes out when writing novx files.

Based on novxlib 3.7.3

### Version 3.9.0

- Fix a regression from version 3.8.0 where data export raises an unhandled exception due to a bug in novxlib.
- novxlib API is extended: new global function intersection().

Based on novxlib 3.7.2

### Version 3.8.0

- Improve the novx file read/write process.
- Change toolbar button positions.

Based on novxlib 3.6.0

### Version 3.7.8

- Make sure that collected values are hidden when a parent node is expanded, for whatever reason.
- Refactor the tree_viewer module.

Based on novxlib 3.5.4

### Version 3.7.7

- Fix a bug where the status bar cannot be restored with the "Esc" key after having used the pick mode.

Based on novxlib 3.5.3

### Version 3.7.6

- Improve the "pick mode".
- When updating the section view, select the last plot line.

Based on novxlib 3.5.3

### Version 3.7.5

- Section view: Terminate the "pick mode" after adding a picked element to the list. 
  This avoids problems that may occur when entering other data in "pick mode".

Based on novxlib 3.5.3

### Version 3.7.4

- Fix a bug where scenes might get lost during splitting, if split markers are not placed as intended. 

Based on novxlib 3.5.3

### Version 3.7.3

- Indent the novx files up to the content paragraph level, but not inline elements within paragraphs.

Based on novxlib 3.5.1

### Version 3.7.2

- Fix a bug where single spaces between emphasized text in section content are lost when writing novx files.

Based on novxlib 3.5.0

### Version 3.7.1

- Update plot line hyperlinks in the plotlist.
- Add plot line hyperlinks to the plot grid.

Based on novxlib 3.4.1

### Version 3.7.0

New document types:

- Story structure export and import.
- Plot line descriptions export and import.

Based on novxlib 3.4.0

### Version 3.6.3

- Fix a regression from version 3.5.0 where the book settings of the last opened project are preset in newly created projects.

Based on novxlib 3.3.0

### Version 3.6.2

- Fix a bug where the viewpoint can not be set if no character is related.

Based on novxlib 3.3.0

### Version 3.6.1

- Fix a regression from version 1.4.1 where changing the chapter type may also affect the next chapter selected.
- Fix a regression from version 3.5.0 where the chapter properties are displayed in the wrong order after selecting the "Trash bin". 

Based on novxlib 3.3.0

### Version 3.6.0

- Try to fix broken links (#17).
- API update due to the changes in novxlib.

Based on novxlib 3.3.0

## Important

For *novelibre* version 3.6, the following plugins and tools must be updated to work with the version 1.3 file format:

- [Timeline plugin](https://github.com/peter88213/nv_timeline/)
- [Aeon Timeline 2 plugin](https://github.com/peter88213/nv_aeon2/)
- [XPress tagged text export](https://github.com/peter88213/novx_xtg/)


### Version 3.5.2

- Store link paths relative to the project directory.

Based on novxlib 3.2.0

### Version 3.5.1

- Fix a regression from version 3.0.0 where plot lines and plot points cannot be deleted.

Based on novxlib 3.2.0

## Important

For *novelibre* version 3.5, the following plugins and tools must be updated to work with the version 1.2 file format:

- [Timeline plugin](https://github.com/peter88213/nv_timeline/)
- [Aeon Timeline 2 plugin](https://github.com/peter88213/nv_aeon2/)
- [XPress tagged text export](https://github.com/peter88213/novx_xtg/)


### Version 3.5.0

The DTD has been upgraded to version 1.2, due to the following changes:

#### Add "Sticky notes" to the chapters, locations, items, and plot lines (#15)

- Add notes text boxes to the properties views.
- Show collected stage note indicators for collapsed chapters.
- Show collected plot point note indicators for collapsed plot lines.

#### Add links to chapters, sections, plot lines, plot points, and project notes (#16).

- Add link frames to all properties views
- Abbreviate links in the project path.

Based on novxlib 3.2.0

### Version 3.4.1

- Fix a regression from version 3.4.0 where links cannot be added.

Based on novxlib 3.1.0

### Version 3.4.0

- Open Zim links the correct way.
- Add ODF documents to the link file types.

Based on novxlib 3.1.0

### Version 3.3.1

- Move the Plot grid export from the export menu to the Plot menu.

Based on novxlib 3.1.0

### Version 3.3.0

- Update section list structure.
- Import tags from Plot Grid even if empty.
- Refactor for novxlib update.

Based on novxlib 3.1.0

### Version 3.2.4

- Refactor: Add "Return" keybinding to the LabelEntry widget.
- Improve the "Import" dialog layout.

Based on novxlib 3.0.1

### Version 3.2.3

- Fix the "Import" dialog button activation.

Based on novxlib 3.0.1

### Version 3.2.2

- Option for importing documents even if open in OO/LO.
- Show localized file date/time instead of ISO-formatted date/time.
- Add translation to the content viewer.

Based on novxlib 3.0.1

### Version 3.1.2

- Update message.

Based on novxlib 3.0.1

### Version 3.1.1

- Display localized time in the "Show ages" title bar.
- Display localized time in the "Reference date" frame.
- Provide weekday names and month names for all languages.

Based on novxlib 3.0.1

### Version 3.1.0

- Display the localized date in the tree view.
- Display the localized date with the week day in the properties view.
- Refactor the section date/day display.

Based on novxlib 3.0.0

### Version 3.0.6

- Move the "Close" buttons of Plugin Manager and import dialog to the right.

Based on novxlib 2.0.1

### Version 3.0.5

- Make the initial value for adding multiple sections a constant and set it to 1.
- Show an error message if a new element cannot be created.

Based on novxlib 2.0.1

### Version 3.0.4

- SimpleDialog class: Instead of just focusing, activate the default button. 

Based on novxlib 2.0.1

### Version 3.0.3

- Improve the "Export document" and the "New sections" 
  dialogs with a custom dialog box. 

Based on novxlib 2.0.1

### Version 3.0.2

- Fix a bug where imported sections are split at the 
  "####" mark, but not appended as they should. 

Based on novxlib 2.0.1

### Version 3.0.1

- Refactor the code.

Based on novxlib 2.0.0

### Version 3.0.0

- Fix a regression from version 2.7.0 where faulty plot lists are generated. 
- Refactor the code, using the new "plot line/plot point" 
  wording for the variables and methods. 
- Upgrade the API to version 3 due to the DTD changes. Otherwise, plugins
  with v2.x API might not be able to read the novx files.
- Enable the online help in German.

Based on novxlib 2.0.0

### Version 2.7.0

- Rewording: Arc -> Plot line.
- Up to 20 sections can now be added at once.
- New option: Ask whether documents should be opened straight after export.
- New option: Lock the project after document export.
- Add "Export" options dialog. 
- In the section properties view, provide a text box to enter notes for the selected arc.
- Add the ODS Plot grid to the document types for export and import.
- Make the ODS Section list export-only.

Based on novxlib 1.5.0

### Version 2.6.1

- Provide translated headers for ODS export.
- Label the plugin manager exit button "Close".
- Label the view options exit button "Close".

Based on novxlib 1.4.2

### Version 2.6.0

- Add a button for creating the section duration from date/time difference.
- More robust ODS file reading.

Based on novxlib 1.4.1

### Version 2.5.0

- Add date/time information to the section list.

Based on novxlib 1.4.0

### Version 2.4.1

- Replace the "Segoe UI 10" font with "Calibri 10.5" for ODF document export.
- Fix a bug where links do not work in the ODS plot list for section titles containing false double quotes.

Based on novxlib 1.3.1

### Version 2.4.0

- Fix a bug where the plot list cannot be generated if an arc has no plot point.
- Reword/Refactor replacing "Turning point" with "Plot point" without affecting the API.

Based on novxlib 1.3.0

### Version 2.3.1

- Require changes to be saved before document export.
- Fix a bug where document import is aborted silently on error. 

Based on novxlib 1.2.1

### Version 2.3.0

- Export manuscripts and synopses optionally filtered either by viewpoint, or by arc.
- Disable several menus when locking the project.
- Lock/unlock the plugins.

Based on novxlib 1.2.0

### Version 2.2.0

- Do not ask before opening the manuscript, if the export is called by clicking on the toolbar icon.
- Modifiy the manuscript export wording in the Export menu.

Based on novxlib 1.1.0

### Version 2.1.0

**Please run the registry script "add_novelibre.reg" on Windows.** 

Rename the application.

Based on novxlib 1.1.0

### Version 2.0.0

**Please update all installed plugins. Check your program launcher/desktop shortcut, and re-run the registry script on Windows.** 
See [this message](https://github.com/peter88213/noveltree/discussions/1#discussioncomment-8526314).

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup and registry scripts.
- Rename packages that have "noveltree" in their name.
- Refactor the code for v2.0 API.

Based on novxlib 1.1.0

### Version 1.8.0

**Please update all installed plugins.** 
See [this message](https://github.com/peter88213/noveltree/discussions/1#discussioncomment-8510191).

- Re-structure the website; adjust links.

Based on novxlib 1.1.0

### Version 1.7.3

- Ask for confirmation before joining two sections.

Based on novxlib 1.1.0

### Version 1.7.2

- Split the "show_links" configuration for characters, locations, and items.

Based on novxlib 1.1.0

### Version 1.7.1

- If a section has a "day" instead of a date, calculate the age of the related characters based on the reference date, if any.
- Extend messaging.

Based on novxlib 1.1.0

### Version 1.7.0

- The age of the related characters can be called up in the section properties window. 

Based on novxlib 1.1.0

### Version 1.6.11

Fix a bug where detaching and re-docking the Properties view causes malfunction.

- Neatly reparent the Properties viewer when detaching/docking it.
- Catch all exceptions that might be raised on shutdown. 
- Never disable Text viewer and Properties buttons.

Based on novxlib 1.0.1

### Version 1.6.10

- Deactivate the detached mode for the Properties window to avoid problems
  caused by a bug yet to fix.

Based on novxlib 1.0.1

### Version 1.6.9

- Fix a bug where the writing progress is unclear because the overall word count is not provided by the model.

Based on novxlib 1.0.1

### Version 1.6.8

- Fix a bug in novxlib where turning points appear in the wrong columns
of the plot list ods export and html report.

Based on novxlib 1.0.1

### Version 1.6.7

- Fix a bug where locked documents are not highlighted in the import list.

Based on novxlib 1.0.0

### Version 1.6.6

- Mark turning points with "notes" in the tree.

Based on novxlib 1.0.0

### Version 1.6.5

- Add a "noveltree Home page" entry to the help menu.

Based on novxlib 1.0.0

### Version 1.6.4

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib 1.0.0

### Version 1.6.3

- Update icons.
. Update German translation.

Based on novxlib 1.0.0

### Version 1.6.2

- Make the context menus close under Linux when losing the focus.

Based on novxlib 1.0.0

### Version 1.6.1

- Add the short names to the section arcs view.

Based on novxlib 1.0.0

### Version 1.6.0

- Add "File > Copy style sheet" menu entry.

Based on novxlib 1.0.0

### Version 1.5.0

- Under Windows, exit the program with Alt-F4 instead of Ctrl-Q.
- No longer use the hotkeys F1..F4, F6...F12.

Based on novxlib 1.0.0

### Version 1.4.3

- When closing the project, disable the buttons introduced with v1.4.0.

Based on novxlib 1.0.0

### Version 1.4.2

- Fix a bug where property changes might be lost when pressing the F5 key.

Based on novxlib 1.0.0

### Version 1.4.1

- Add "Unused" checkboxes to the chapter/section properties view.

Based on novxlib 1.0.0

### Version 1.4.0

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

Based on novxlib 1.0.0

### Version 1.3.1

- Fix a bug where the HTML lists are not generated.

Based on novxlib 1.0.0

### Version 1.3.0

- Provide icons for the collection list buttons.
- Make the icons available for the entire GUI.

Based on novxlib 1.0.0

### Version 1.2.2

- Fix "View" menu control.
- Add "Import" menu control.
- Add "Project notes" menu control.

Based on novxlib 1.0.0

### Version 1.2.1

- Make it easier to exit the Pick Mode.

Based on novxlib 1.0.0

### Version 1.2.0

- Change the view of the arcs associated with a section into a list.
- Improve the usability by indicating the Pick Mode.
- Extend the API: NvView.set_status() takes a custom colors argument.

Based on novxlib 1.0.0

### Version 1.1.3

- Move the CollectionBox buttons to the right side.

Based on novxlib 1.0.0

### Version 1.1.2

- Fix a regression where the contents viewer is not reset on closing a project.
- Fix a bug where the stage level cannot be changed".

Based on novxlib 1.0.0

### Version 1.1.1

- Handle missing toolbar icon files.

Based on novxlib 1.0.0

### Version 1.1.0

- Integrate the toolbar. 
  If the *noveltree_toolbar* plugin is installed, please delete it with the Plugin manager.
- Refactor.

Based on novxlib 1.0.0

### Version 1.0.1

- Fix the plugin API version constant.

Based on novxlib 1.0.0

### Version 1.0.0

- Release under the GPLv3 license.

Based on noveltree-Alpha 0.10.0
Based on novxlib 1.0.0
