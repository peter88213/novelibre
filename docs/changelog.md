[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "Features" project](https://github.com/users/peter88213/projects/14).

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
