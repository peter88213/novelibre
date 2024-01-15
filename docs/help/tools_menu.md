[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Command reference: Tools menu

--- 

# Tools menu 

**Miscellaneous functions**

**Note:** The *Tools* menu can be extended by plugins to add more features.

--- 

## Plugin manager

**Display and manage installed plugins**

- Successfully installed plugins are displayed black on white by default.
- Outdated plugins are grayed out.
- Plugins that cannot run are displayed in red, with an error message.

### About version compatibility

On the window frame, you see the *noveltree* version, consisting of three numbers that are separated by points.

`<major version number>.<minor version number>.<patch level>`

In the **noveltree API** column, you see the plugin's compatibility information, consisting of two numbers that are separated by points.

`<major version number>.<minor version number>`

#### The rule for compatibility 

- The plugin's *noveltree API* major version number must be the same as *noveltree's* major version number. 
- The plugin's *noveltree API* minor version number must be less than or equal to *noveltree's* minor version number.

#### Fix incompatibilities

- If the plugin's *noveltree API* major version number is greater than *noveltree's* major version number, *noveltree* needs to be updated.
- If the plugin's *noveltree API* major version number is less than *noveltree's* major version number, the plugin needs to be updated.
- If the plugin's *noveltree API* minor version number is greater than *noveltree's* minor version number, *noveltree* needs to be updated.

#### Update plugins

Select the plugin you want to update. If the "Home page" button is activated, you can click on it, and your system browser opens the plugin home page. Otherwise, you have to know the source of the plugin yourself. 

Go to the plugin home page and download the latest release. Install it according to the instructions. 

If the plugin is a *noveltree* add-on, reinstall it from your latest *noveltree* release files.

### Uninstall a plugin

Select the plugin, and click on the **Delete** button. 

--- 

## Open installation folder

**Launch the file manager**

- You can launch the file manager with the *noveltree* installation folder with **File > Open installation folder**. This might be helpful, if you wish to edit configuration files, or install your own plugins.

---

[<< Previous](export_menu) -- [Next >>](tree_context_menu)