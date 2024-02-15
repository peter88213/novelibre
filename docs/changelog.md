[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "Features" project](https://github.com/users/peter88213/projects/14).

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
