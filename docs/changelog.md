[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "Features" project](https://github.com/users/peter88213/projects/14).

---


### Version 5.25.0

- Enable opening an existing manuscript if the project is locked.


### Version 5.24.5

- Fixed a regression from version 5.24.2 where an unhandled ZeroDivisionError occurs when creating an empty project.


### Version 5.24.4

- Fixed a regression from version 5.24.2 where a message box pops up every time a folding frame is toggled while the project is locked.


### Version 5.24.3

- Refactored the code for better maintainability.


### Version 5.24.2

- Displaying previews on collapsed property frames.
- Fixed a bug where the word target and word count start values cannot be reset properly.
- Fixed a bug where the age is displayed as zero if the character has been
  dead for less than a year.
- Improved and extended the age display.
- Added a duration display to the section properties.
- Changed the API of PyCalendar.age().


### Version 5.23.5

- Changed icon colors for better display in dark mode.


### Version 5.23.4

- Changed icon colors for better display in dark mode.


### Version 5.23.3

Updated the css style sheet for better display of epigraphs.

Refactored the code according to PEP 8

- Mentioned specific exceptions.
- Shortened long lines.
- Replaced docstrings of "non-publlic' methods with comments.
- Removed redundant comments.


### Version 5.23.2

- Changed icon colors for better display in dark mode.


### Version 5.23.1

- Fixed a bug where the localized name of the month is not exported correctly.


### Version 5.23.0

- Providing an optional export template for appended sections: 
  `FileExport._appendedSectionTemplate`.


### Version 5.22.0

Enhancements for the *nv_custom_export* plugin (#59):

- Providing a service method to get the final document export class.
- The main controller and sub controllers get an `on_open()` method 
  that is called after a project has been opened.  


### Version 5.21.0

The file format has been upgraded to version 1.6.
*.novx* files created with *novelibre* version 5.21+ 
cannot be read with older *novelibre* versions.

- Chapters can be prefaced with epigraphs.
- Swapped main menu position of "Import" and "Export"
- Providing a chapter/part list export to edit the epigraphs with Calc.
- Fixed character notes reimport.
- Fixed a bug where chapter templates are applied to parts if no part
  template exists.
- Simplified the section description document by removing the ODT part
  and chapter sections which are not needed for reimport.
- Added a "Notes" column to the location list and to the item list.
- Added a chapter number column to the chapter list.
- Hiding the ID columns of the character/location/item lists.


### Version 5.20.2 (no build)

Fixed the UiCmd class intended for external programs. 


### Version 5.20.1

- Improved automatic time generation if previous section has no date/day.

Refactored the code for better maintainability:
- All date/time related operations on the model are combined as class methods in the PyCalendar class.
- New: Moon class containing the moon phase calculations.
- Moved duplicate html auxiliary methods to the superclass.


### Version 5.19.1

- Refactored the code for better performance.


### Version 5.19.0

- Fixed a regression from 5.18.1, where picking mode doesn't open the branch to pick from.
- When going to a category, close others.
- When picking from a category, close others.

API change:
- Added TreeViewer methods for saving and restoring the opening status of the branches.


### Version 5.18.2

- Bugfixes for document reimport.


### Version 5.18.1

- No longer expanding the whole tree in "picking mode".


### Version 5.18.0

- Fixed a bug where the **File > New > Create from ODT...** command cannot be properly aborted.
- API upgrade: `FileManager.create_project()` returns `True` on success.


### Version 5.17.7

- Fixed a bug where an exception is raised when aborting **File > New > Empty project**.
- Fixed a bug where the **File > Open...** command cannot be properly aborted.


### Version 5.17.6

- Minor Refactoring: Moved some actions from `MainController.on_close()` to  `MainView.on_close()`.


### Version 5.17.5

- Reset the change notification after closing a project without saving changes. 


### Version 5.17.4

- Refactored the code for better maintainability.


### Version 5.17.3

- Fixed a bug where no error message appears when trying to open a broken link.
- Revised the messaging for a better look under Linux.
- Refactored the code for better maintainability.


### Version 5.16.3

- Set a minimum plugin manager window height.


### Version 5.16.2

- Updated the Window title of "About novelibre".


### Version 5.16.1

- Improved message for unexpected errors.
- Refactored the code for better maintainability.


### Version 5.16.0

- API upgrade: Implemented NvTree.parent()


### Version 5.15.2

- Displaying a message if there is no manuscript to discard. 


### Version 5.15.1

- Refactored the code for better performance, reverting to the string processing variant of OdtWriter.add_novelibre_styles().
- Removed OdfFile.add_novelibre_styles()

### Version 5.15.0

Refactored the code for better maintainability.

#### API changes

- New: OdfFile.NAMESPACES
- New: OdtWriter.add_novelibre_styles() and OdtWriter.remove_novelibre_styles()
- New: FileManager.set_user_styles() and FileManager.restore_default_styles()


### Version 5.14.0

- Added new settings to the **Export/Options** dialog, allowing users to provide their own document templates (#51).


### Version 5.13.5

- Reworked HTML timetable timestamp generation to avoid exception for section dates outside POSIX range.
- Added the days of the week to the HTML timetable.


### Version 5.13.4

- Exporting a section time table. Closes #50.
- Do not show HTML lists if there are no list items.


### Version 5.12.3

- Refactored the code for better maintainability, replacing NovxConverter by the NovxConversion mixin.


### Version 5.12.2

- Refactored the code for better maintainability, simplifying the class hierarchy of the converter.


### Version 5.12.1

- Refactored the code for better maintainability, simplifying the class hierarchy of the main view.


### Version 5.12.0

- Refactored the code for better maintainability, abandoning the mvclib package.


### Version 5.11.2

- Fixed a regression from version 5.9.0 where success messages may not be shown on the status bar after reimporting a document.


### Version 5.11.1

- Refactored the code for better maintainability.


### Version 5.11.0

- Changed the confirmation requests for the "Restore backup" command.
- API update: New FileManager methods.


### Version 5.10.0

- Added a "Show notes" HTML report.
- Refactored the code for better maintainability.


### Version 5.9.2

- Making a backup copy immediately after creating a new project by ODF import (#46).
- Handling exceptions that may be raised when open_document() fails.
- Restoring the status bar before executing file related commands.


### Version 5.9.1

- Integrating the online help with the "Backup options" dialog (#46).
- Refactored the use of the install/home path (#44).


### Version 5.9.0

- Every time, *novelibre* saves the project, 
  it also saves a copy to a user-defined directory, if any.
  The file name of the copy gets the suffix `#`.
  Closes #46.


### Version 5.8.0

- Fixed a bug in OdsRGrid where the grid cannot be re-imported repeatedly.
- Added the section duration to the Plot Grid. Closes #49.
- OdsReader no longer checking the number of fields in each row.


### Version 5.7.1

Enhanced keyboard navigation.
- `Alt`-`Left`: Go back in history.
- `Alt`-`Right`: Go forward in history.
- `Alt`-`Up`: Go to the previous node of the same kind.
- `Alt`-`Down`: Go to the next node of the same kind. 

Refactoring for this:
- Moved BasicViewCtrl.load_next() to TreeViewerCtrl.load_next().
- Moved BasicViewCtrl.load_prev() to TreeViewerCtrl.load_prev().


### Version 5.6.0

- ContentsViewer using a service to get the preferences (#31).
- Generating an event when changing the selection.


### Version 5.5.0

- Copy/Cut/Paste included.
- If the nv_clipboard plugin is installed, it will be removed during installation.


### Version 5.4.1

- Setting the user's home directory as default for new projects. Closes #40.
- Revised the installation routine in order not to delete files that
  aren't part of the release package.


### Version 5.4.0

- To better support themes, the RichTextNv "tag" colors are configurable now. 


### Version 5.3.0

- Skipping the configuration in case of error.
- To better support themes, the background color of the stages is no longer configurable.


### Version 5.2.1

- Adjust the wording in the context menu.


### Version 5.2.0

- New feature: Change the type of all sections assigned to a plot line.


### Version 5.1.4

- No longer count unused sections for plot line properties (#39).


### Version 5.1.3

- Added a legal notice to the user interface.


### Version 5.1.2

- Making sure to save the error log file in the installation directory.


### Version 5.1.1

- Making sure not to change the character status accidentally when reading back the character list. 


### Version 5.1.0

- Localized the character status in the character list.


### Version 5.0.28

#### New features
- Via the context menu, you can export a manuscript containing only the selected chapter.
- New Chapter menu entry: **Move selected chapters to new project**. 
  This creates a new project containing the moved chapters/sections 
  and all related elements and plot lines/plot points.
- Added a **Major character** checkbox to the character properties view. 
- Importing and exporting plot lines with plot points via XML data files. 
- Making it easier to delete multiple elements.
- Added a **Cut** command to the *nv_clipboard* plugin.
- Updated the sample templates included with the *nv_templates* plugin.
- The *nv_collection* plugin now always asks before saving.
- In case of program errors, a log file is created that can be used for bug reporting. 
- Added birth and death dates to the ODS character list.
- Added birth and death dates to the HTML character list.

#### Bugfixes
- Fixed a bug where the project is not updated from ODT location and item descriptions.
- Fixed a bug where an exception is raised when trying to delete chapters that contain stages.
- Fixed a regression from version 4.17.1 where the root element titles are invisible when creating a project without saving it immediately.
- Preventing setting a section in an unused chapter "normal" via the properties checkbox.
- Changed the menu title for exporting the final document.
- Creating multiple sections always in ascending order.
- Preventing loading templates with the *nv_templates* plugin while the project is locked.
- No longer auto-fix broken links while the project is locked. 
- Fixed a bug where the cover image may not be displayed when opening an existing project after discarding a new project.
- Fixed a bug where the editor window is not closed when the corresponding section is deleted. 

#### Other
- novx file format update to version 1.5: Added a "Field" element for custom data.
- Changed the menu title for exporting the final document.
- Creating multiple sections always in ascending order.
- Refactored the code for better maintainability.
- The API is updated to version 5.0, so all plugins must be updated.
- Allowing arbitrary link openers to be added to the link processor.
- Moved the Zim Wiki page link processing to the *nv_zim* plugin.
- Finished the *nv_statistics* plugin.
- Improved the cross reference export.
- Extended and improved the user guide.


### Version 4.17.2

Preparations for the upcoming version 5

- Refactored the code for better maintainability.

### Version 4.17.1

Preparations for the upcoming version 5

- Making the stage background color configurable.
- Refactored and revise the code for better maintainability.
- Release the dependency on the novxlib and apptk libraries.

### Version 4.16.1

- If an element title is empty, replace it with the element ID.

Based on novxlib 5.0.0
Based on apptk 2.3.0

### Version 4.16.0

- Added a "Cancel" option to the quit/close dialog.
- Do not close a project if saving fails.

Based on novxlib 5.0.0
Based on apptk 2.3.0

### Version 4.15.6

- Fixed a bug where an exception is raised when closing a project
while a property view widget still has the focus. 

Based on novxlib 5.0.0
Based on apptk 2.2.0

### Version 4.15.5

- Fixed a bug where an exception is raised when closing a project
immediately after deleting a section.
- Assign the correct type when moving a section to the "trash bin".

Based on novxlib 5.0.0
Based on apptk 2.2.0

### Version 4.15.4

Refactored the code for better maintainability

- Removed the isLocked property from the NvController class.

Based on novxlib 5.0.0
Based on apptk 2.2.0

### Version 4.15.3

Refactored the code for better maintainability

- PropertiesViewer now using the new ViewComponentBase methods of apptk 2.1.0.
- Updated docstrings and code comments.

Based on novxlib 4.8.0
Based on apptk 2.1.0

### Version 4.15.2

- Restore the plugin_manager module from version 4.14.1.

Based on novxlib 4.8.0
Based on apptk 1.1.0

### Version 4.15.1

- Changed the pop-up window titles.

Based on novxlib 4.8.0
Based on apptk 1.1.0

### Version 4.15.0

- Refactored the MVC implementation for better maintainability.

Based on novxlib 4.8.0
Based on apptk 1.0.0

### Version 4.14.1

Refactored the code for better maintainability:
- Simplified the PopUpBase API.

Based on novxlib 4.8.0

### Version 4.14.0

Refactored the code for better maintainability:
- Providing an abstract base class for pop-up windows.
- Made ExportOptionsWindow, ViewOptionsWindow, PluginManager, and PrjUpdater PopUpBase subclasses.
- Moved and renamed the update_project method.
- Moved and renamed the manage_plugins method.

Based on novxlib 4.8.0

### Version 4.13.1

- Fixed a regression from version 4.13.0 where plugins cannot add toolbar buttons.
- Extended the PluginBase constructor.

Based on novxlib 4.8.0

### Version 4.13.0

- Made the status bar colors configurable.

Refactored the code for better maintainability:
- Providing an abstract base class for the view components.
- Made the tree viewer, contents viewer, toolbar, and properties viewer ViewComponentBase subclasses.
- Renamed local variables.
- Updated docstrings.

Based on novxlib 4.8.0

### Version 4.12.0

- Added a notification mode to the status bar (yellow).
- Showing a notification instead of an error, if the user opens an existing document instead of exporting.
- Showing a notification if the document export is canceled due to unsaved changes.
- Providing a specific error message if an odt import document contains an unknown model element (novxlib).

Based on novxlib 4.8.0

### Version 4.11.11

- Refactored: Use the view's API instead of tkinter imports.
- Refactored: Move the project-specific tk.Toplevel subclasses to the new view.pop_up package.
- Updated docstrings.

Based on novxlib 4.7.3

### Version 4.11.10

- Fixed the 'Plot points' label to enable theming.

Based on novxlib 4.7.3

### Version 4.11.9

- Fixed a bug where the project notes are displayed in the HTML report without linebreaks.

Based on novxlib 4.7.3

### Version 4.11.8

- Fixed a bug where an exception is raised when trying to add a parent element to the tree while the project is locked. 

Based on novxlib 4.7.2

### Version 4.11.7

- Fixed HTML report title display.

Based on novxlib 4.7.2

### Version 4.11.6

- Added accelerators to hovertips.
- Fixed typo in German translation.

Based on novxlib 4.7.1

### Version 4.11.5

- Updated UI text.
- Refactored: defensive programming and re-structuring of packages.

Based on novxlib 4.6.7

### Version 4.11.4

- Fixed a bug where an unhandled exception is raised when trying to open the project folder while no project is open.

Based on novxlib 4.6.7

### Version 4.11.3

- Fixed a bug where an unhandled exception is raised when trying automatically unlock an unnamed new project.
- Refactored the error messaging system.

Based on novxlib 4.6.7

### Version 4.11.2

- Handling formatted headings when importing work-in-progress or outline.

Based on novxlib 4.6.7

### Version 4.11.1

- No longer displaying empty "stage" paragraphs in the content viewer.

Based on novxlib 4.6.5

### Version 4.11.0

- Added tooltips.
- Fixed a regression from version 4.10.1 where the "F1" key does not work with the import dialog.

Refactor:
- Separate keyboard settings and mouse operation settings.
- Put everything in the new platform_settings module.

Based on novxlib 4.6.4

### Version 4.10.3

- Refactored the event bindings.

Based on novxlib 4.6.4

### Version 4.10.2

- Restore the "Quit" menu command for the Mac (#28).

Based on novxlib 4.6.4

### Version 4.10.1

- Translate accelerators.

Refactor:
- Added right-click event to the key definitions.
- Using the NvView.key definitions instead of hard-coded key bindings.
- Define mouse operations with the NvView.key definitions.

Based on novxlib 4.6.3

### Version 4.10.0

- Providing shortcuts and key bindings for Mac OS.
- The zipfile setup script is now generated by the PackageBuilder class.
- Added/update docstrings.

Based on novxlib 4.6.3

### Version 4.9.6

- Set limits for the application's window size.
- Refactored: Replace global constants with class constants.

Based on novxlib 4.6.3

### Version 4.9.5

- Rejecting malformed .novx files.

Based on novxlib 4.6.3

### Version 4.9.4

- Text box discarding illegal characters.
- novxlib update for safe XML reading and writing.

Based on novxlib 4.6.2

### Version 4.9.3

- Refactored for future Python versions.

Based on novxlib 4.5.9

### Version 4.9.2

- Handling novx XML parser error.
- Using raw strings for regular expressions.
- Adjusting separators in File.filePath.
- Refactored for future Python versions.

Based on novxlib 4.5.7

### Version 4.9.1

- Removed "private" tkinter imports that would not work with Linux.

Based on novxlib 4.5.3

### Version 4.9.0

- Made the right mouse button work under Mac OS.
- Extended the API, providing a global PLATFORM constant.

Based on novxlib 4.5.3

### Version 4.8.3

- Fixed a regression from version 4.8.2 where project files could be mistakenly rejected as corrupted.

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
- Made date localization optional.

Based on novxlib 4.4.2

### Version 4.6.2

- Fixed a bug where no modification is indicated when the reference date is cleared.

Based on novxlib 4.4.1

### Version 4.6.1

- Added accelerator key to the "Online help" menu entry.

Based on novxlib 4.4.0

### Version 4.6.0

- Providing context sensitive help via F1 key and several mouse buttons.

Based on novxlib 4.4.0

### Version 4.5.2

- Updated messages for wrong date/time entry.

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
- Extended the API, providing a service for moonphase calculation.

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

- Fixed a bug in PluginCollection.load_file(), where the plugin's file path gets lost 
  if the plugin inherits from PluginBase.
- Refactored the nv_controller module.
- Updated the PluginBase class.

Based on novxlib 4.1.0

### Version 4.3.0

Extend the API for the nv_clipboard plugin.

- Made the toolbar delegate in NvView a "public" instance variable.
- Made the Toolbar buttonBar a "public" instance variable.
- Added a service to the controller that returns the global preferences.
- Removed unused imports; update docstrings.

Based on novxlib 4.1.0

### Version 4.2.1

- Made sure that critical errors do not happen silently. 
  In case of unhandled exceptions, show a popup window with the stack trace.
  This is only part of the "run.pyw" starter script generated during setup. 

Based on novxlib 4.1.0

### Version 4.2.0

- Upgrade the plugin API by improving the *NvService* interface. 
  The service now returns *NvTreeview* instances instead of *NvView* instances. 
  This may help to avoid side effects in case of a broken plugin implementation.

Based on novxlib 4.1.0

### Version 4.1.2

- Fixed a regression from version 4.1.1 where plot points cannot be created.
- Refactored: make nvService inherit from novxService.
- Refactored: use nvService factory methods for model object instantiation.
- Refactored: convert TreeViewer local functions into methods.

Based on novxlib 4.1.0

### Version 4.1.1

- Library update. Now reading and writing *.novx* version 1.4 files.
- Made the Action/Reaction scheme more general (#22).
- Refactored, changing the API.
- Providing a service class with factory methods and getters for the novxlib model.

Based on novxlib 4.0.2

### Version 3.9.2

- Made sure not to read back redundant language tags from ODT.

Based on novxlib 3.7.4

### Version 3.9.1

- Changing the view settings of generated ODT documents to single page per column.
- Leaving empty plot notes out when writing novx files.

Based on novxlib 3.7.3

### Version 3.9.0

- Fixed a regression from version 3.8.0 where data export raises an unhandled exception due to a bug in novxlib.
- novxlib API is extended: new global function intersection().

Based on novxlib 3.7.2

### Version 3.8.0

- Improved the novx file read/write process.
- Changed toolbar button positions.

Based on novxlib 3.6.0

### Version 3.7.8

- Made sure that collected values are hidden when a parent node is expanded, for whatever reason.
- Refactored the tree_viewer module.

Based on novxlib 3.5.4

### Version 3.7.7

- Fixed a bug where the status bar cannot be restored with the "Esc" key after having used the pick mode.

Based on novxlib 3.5.3

### Version 3.7.6

- Improved the "pick mode".
- When updating the section view, select the last plot line.

Based on novxlib 3.5.3

### Version 3.7.5

- Section view: Terminate the "pick mode" after adding a picked element to the list. 
  This avoids problems that may occur when entering other data in "pick mode".

Based on novxlib 3.5.3

### Version 3.7.4

- Fixed a bug where scenes might get lost during splitting, if split markers are not placed as intended. 

Based on novxlib 3.5.3

### Version 3.7.3

- Indent the novx files up to the content paragraph level, but not inline elements within paragraphs.

Based on novxlib 3.5.1

### Version 3.7.2

- Fixed a bug where single spaces between emphasized text in section content are lost when writing novx files.

Based on novxlib 3.5.0

### Version 3.7.1

- Updated plot line hyperlinks in the plotlist.
- Added plot line hyperlinks to the plot grid.

Based on novxlib 3.4.1

### Version 3.7.0

New document types:

- Story structure export and import.
- Plot line descriptions export and import.

Based on novxlib 3.4.0

### Version 3.6.3

- Fixed a regression from version 3.5.0 where the book settings of the last opened project are preset in newly created projects.

Based on novxlib 3.3.0

### Version 3.6.2

- Fixed a bug where the viewpoint can not be set if no character is related.

Based on novxlib 3.3.0

### Version 3.6.1

- Fixed a regression from version 1.4.1 where changing the chapter type may also affect the next chapter selected.
- Fixed a regression from version 3.5.0 where the chapter properties are displayed in the wrong order after selecting the "Trash bin". 

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

- Fixed a regression from version 3.0.0 where plot lines and plot points cannot be deleted.

Based on novxlib 3.2.0

## Important

For *novelibre* version 3.5, the following plugins and tools must be updated to work with the version 1.2 file format:

- [Timeline plugin](https://github.com/peter88213/nv_timeline/)
- [Aeon Timeline 2 plugin](https://github.com/peter88213/nv_aeon2/)
- [XPress tagged text export](https://github.com/peter88213/novx_xtg/)


### Version 3.5.0

The DTD has been upgraded to version 1.2, due to the following changes:

#### Add "Sticky notes" to the chapters, locations, items, and plot lines (#15)

- Added notes text boxes to the properties views.
- Show collected stage note indicators for collapsed chapters.
- Show collected plot point note indicators for collapsed plot lines.

#### Add links to chapters, sections, plot lines, plot points, and project notes (#16).

- Added link frames to all properties views
- Abbreviate links in the project path.

Based on novxlib 3.2.0

### Version 3.4.1

- Fixed a regression from version 3.4.0 where links cannot be added.

Based on novxlib 3.1.0

### Version 3.4.0

- Open Zim links the correct way.
- Added ODF documents to the link file types.

Based on novxlib 3.1.0

### Version 3.3.1

- Move the Plot grid export from the export menu to the Plot menu.

Based on novxlib 3.1.0

### Version 3.3.0

- Updated section list structure.
- Import tags from Plot Grid even if empty.
- Refactored for novxlib update.

Based on novxlib 3.1.0

### Version 3.2.4

- Refactored: Add "Return" keybinding to the LabelEntry widget.
- Improved the "Import" dialog layout.

Based on novxlib 3.0.1

### Version 3.2.3

- Fixed the "Import" dialog button activation.

Based on novxlib 3.0.1

### Version 3.2.2

- Option for importing documents even if open in OO/LO.
- Show localized file date/time instead of ISO-formatted date/time.
- Added translation to the content viewer.

Based on novxlib 3.0.1

### Version 3.1.2

- Updated message.

Based on novxlib 3.0.1

### Version 3.1.1

- Display localized time in the "Show ages" title bar.
- Display localized time in the "Reference date" frame.
- Providing weekday names and month names for all languages.

Based on novxlib 3.0.1

### Version 3.1.0

- Display the localized date in the tree view.
- Display the localized date with the week day in the properties view.
- Refactored the section date/day display.

Based on novxlib 3.0.0

### Version 3.0.6

- Move the "Close" buttons of Plugin Manager and import dialog to the right.

Based on novxlib 2.0.1

### Version 3.0.5

- Made the initial value for adding multiple sections a constant and set it to 1.
- Show an error message if a new element cannot be created.

Based on novxlib 2.0.1

### Version 3.0.4

- SimpleDialog class: Instead of just focusing, activate the default button. 

Based on novxlib 2.0.1

### Version 3.0.3

- Improved the "Export document" and the "New sections" 
  dialogs with a custom dialog box. 

Based on novxlib 2.0.1

### Version 3.0.2

- Fixed a bug where imported sections are split at the 
  "####" mark, but not appended as they should. 

Based on novxlib 2.0.1

### Version 3.0.1

- Refactored the code.

Based on novxlib 2.0.0

### Version 3.0.0

- Fixed a regression from version 2.7.0 where faulty plot lists are generated. 
- Refactored the code, using the new "plot line/plot point" 
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
- Added "Export" options dialog. 
- In the section properties view, provide a text box to enter notes for the selected arc.
- Added the ODS Plot grid to the document types for export and import.
- Made the ODS Section list export-only.

Based on novxlib 1.5.0

### Version 2.6.1

- Providing translated headers for ODS export.
- Label the plugin manager exit button "Close".
- Label the view options exit button "Close".

Based on novxlib 1.4.2

### Version 2.6.0

- Added a button for creating the section duration from date/time difference.
- More robust ODS file reading.

Based on novxlib 1.4.1

### Version 2.5.0

- Added date/time information to the section list.

Based on novxlib 1.4.0

### Version 2.4.1

- Replace the "Segoe UI 10" font with "Calibri 10.5" for ODF document export.
- Fixed a bug where links do not work in the ODS plot list for section titles containing false double quotes.

Based on novxlib 1.3.1

### Version 2.4.0

- Fixed a bug where the plot list cannot be generated if an arc has no plot point.
- Reword/Refactor replacing "Turning point" with "Plot point" without affecting the API.

Based on novxlib 1.3.0

### Version 2.3.1

- Require changes to be saved before document export.
- Fixed a bug where document import is aborted silently on error. 

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
- Refactored the code for v2.0 API.
- Changed the installation directory in the setup and registry scripts.
- Renamed packages that have "noveltree" in their name.
- Refactored the code for v2.0 API.

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
- Extended messaging.

Based on novxlib 1.1.0

### Version 1.7.0

- The age of the related characters can be called up in the section properties window. 

Based on novxlib 1.1.0

### Version 1.6.11

Fix a bug where detaching and re-docking the Properties view causes malfunction.

- Neatly reparenting the Properties viewer when detaching/docking it.
- Catching all exceptions that might be raised on shutdown. 
- Never disabling Text viewer and Properties buttons.

Based on novxlib 1.0.1

### Version 1.6.10

- Deactivated the detached mode for the Properties window to avoid problems caused by a bug yet to fix.

Based on novxlib 1.0.1

### Version 1.6.9

- Fixed a bug where the writing progress is unclear because the overall word count is not provided by the model.

Based on novxlib 1.0.1

### Version 1.6.8

- Fixed a bug in novxlib where turning points appear in the wrong columns of the plot list ods export and html report.

Based on novxlib 1.0.1

### Version 1.6.7

- Fixed a bug where locked documents are not highlighted in the import list.

Based on novxlib 1.0.0

### Version 1.6.6

- Marked turning points with "notes" in the tree.

Based on novxlib 1.0.0

### Version 1.6.5

- Added a "noveltree Home page" entry to the help menu.

Based on novxlib 1.0.0

### Version 1.6.4

- Switched the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib 1.0.0

### Version 1.6.3

- Updated icons.
- Updated German translation.

Based on novxlib 1.0.0

### Version 1.6.2

- Made the context menus close under Linux when losing the focus.

Based on novxlib 1.0.0

### Version 1.6.1

- Added the short names to the section arcs view.

Based on novxlib 1.0.0

### Version 1.6.0

- Added "File > Copy style sheet" menu entry.

Based on novxlib 1.0.0

### Version 1.5.0

- Under Windows, exit the program with Alt-F4 instead of Ctrl-Q.
- No longer using the hotkeys F1..F4, F6...F12.

Based on novxlib 1.0.0

### Version 1.4.3

- When closing the project, disable the buttons introduced with v1.4.0.

Based on novxlib 1.0.0

### Version 1.4.2

- Fixed a bug where property changes might be lost when pressing the F5 key.

Based on novxlib 1.0.0

### Version 1.4.1

- Added "Unused" checkboxes to the chapter/section properties view.

Based on novxlib 1.0.0

### Version 1.4.0

- Fixed a bug where the project structure of a newly created project is invisible until the first element is created.
- Saving new empty projects right after creation.

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

- Fixed a bug where the HTML lists are not generated.

Based on novxlib 1.0.0

### Version 1.3.0

- Providing icons for the collection list buttons.
- Made the icons available for the entire GUI.

Based on novxlib 1.0.0

### Version 1.2.2

- Fixed "View" menu control.
- Added "Import" menu control.
- Added "Project notes" menu control.

Based on novxlib 1.0.0

### Version 1.2.1

- Making it easier to exit the Pick Mode.

Based on novxlib 1.0.0

### Version 1.2.0

- Changed the view of the arcs associated with a section into a list.
- Improved the usability by indicating the Pick Mode.
- Extended the API: NvView.set_status() takes a custom colors argument.

Based on novxlib 1.0.0

### Version 1.1.3

- Move the CollectionBox buttons to the right side.

Based on novxlib 1.0.0

### Version 1.1.2

- Fixed a regression where the contents viewer is not reset on closing a project.
- Fixed a bug where the stage level cannot be changed".

Based on novxlib 1.0.0

### Version 1.1.1

- Handling missing toolbar icon files.

Based on novxlib 1.0.0

### Version 1.1.0

- Integrated the toolbar. 
  If the *noveltree_toolbar* plugin is installed, please delete it with the Plugin manager.
- Refactored.

Based on novxlib 1.0.0

### Version 1.0.1

- Fixed the plugin API version constant.

Based on novxlib 1.0.0

### Version 1.0.0

- Release under the GPLv3 license.

Based on noveltree-Alpha 0.10.0
Based on novxlib 1.0.0
