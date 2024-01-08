# ![N](img/nLogo32.png) noveltree

*noveltree* is an organizer tool for writing novels with *LibreOffice Writer* or *OpenOffice Writer*. The entire novel is stored in a single file with all additional information. The manuscript is exported for editing with *Writer*, and then written back so that everything is always consistent and in one place. *noveltree* uses its own XML file format. 

![Screenshot](Screenshots/screen01.png)

*noveltree* is written in Python and should run on several operating systems.


## Features

- The entire project is displayed in a tree, with branches for the book, characters, locations, items, arcs, and project notes.
- Tree elements can be added, moved, and deleted.
- There are three levels: part, chapter, and section.
- The right sidebar displays the essential properties of the selected element for editing.
- A text viewer window can be toggled on and off.
- There is a wide range of ODF-type file export for *OpenOffice* and *LibreOffice*.
- The exported ODT manuscript and several other exported documents can be re-imported to update the project.
- Several reports can be presented in list form. 
- The application is ready for internationalization with GNU gettext. A German localization is provided. 

## Plugins

*noveltree's* functionality can be extended by plugins. Here are some examples:

- [A toolbar with buttons for frequently used commands](https://peter88213.github.io/noveltree_toolbar/)
- [A yw7 file importer/exporter](https://peter88213.github.io/noveltree_yw7/)
- [An on-demand update checker](https://peter88213.github.io/noveltree_updater/)
- [A daily progress log viewer](https://peter88213.github.io/noveltree_progress/)
- [A book/series collection manager](https://peter88213.github.io/noveltree_collection/)
- [A relationship matrix](https://peter88213.github.io/noveltree_matrix/)
- [A Timeline plugin](https://peter88213.github.io/noveltree_timeline/)
- [An Aeon Timeline 2 plugin](https://peter88213.github.io/noveltree_aeon2/)
- [A theme changer](https://peter88213.github.io/noveltree_themes/)
- [A Story Template management plugin](https://peter88213.github.io/noveltree_templates/)
- [A simple "markup" section editor](https://peter88213.github.io/noveltree_editor/)

## Requirements

- [Python](https://www.python.org/) version 3.6+. 
     - For current Windows versions, use version 3.9.10 or above.
     - For Vista and Windows 7, use version 3.7.2.
- Tk support for Python. This is usually part of the Windows Python installation, but may need to be installed additionally under Linux.
- Either [LibreOffice](https://www.libreoffice.org/) or [OpenOffice](https://www.openoffice.org).

### Note for Linux users

Please make sure that your Python3 installation has the *tkinter* module. On Ubuntu, for example, it is not available out of the box and must be installed via a separate package named *python3-tk*. 

## General note about the fitness for use

At present, this program is still under active development. Therefore it is recommended to check for updates from time to time, as well as for the plugins. 

I use the program myself and fix errors immediately if I notice any. As far as I can tell, *noveltree* runs fast and reliably under Windows and Linux. It should also under other operating systems for which there is a reasonably up-to-date *Python 3* installation. However, there is a lack of a broad user base, which is why one cannot speak of real proven operation. 


## Download and install

[Download the latest release (version 1.0.0)](https://github.com/peter88213/noveltree/raw/main/dist/noveltree_v1.0.0.zip)

- Extract the "noveltree_v1.0.0" folder from the downloaded zipfile "noveltree_v1.0.0.zip".
- Move into this new folder and open "README.md" for further instructions.
- You may wish to install plugins; the [section editor](https://peter88213.github.io/noveltree_editor/) is highly recommended.

---

[Changelog](changelog)

[News](https://github.com/peter88213/noveltree/discussions/1)

[Discussions](https://github.com/peter88213/noveltree/discussions)

## Usage

See the [instructions for use](usage)

## Credits

The icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

This is Open Source software, and *noveltree* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/noveltree/blob/main/LICENSE) file.
