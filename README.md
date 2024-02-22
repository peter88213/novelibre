[![Download the latest release](docs/img/download-button.png)](https://github.com/peter88213/noveltree/raw/main/dist/noveltree_v2.0.0.zip)
[![Changelog](docs/img/changelog-button.png)](docs/changelog.md)
[![News](docs/img/news-button.png)](https://github.com/peter88213/noveltree/discussions/1)
[![Online help](docs/img/help-button.png)](https://peter88213.github.io/nvhelp-en/)


# ![N](docs/img/nLogo32.png) noveltree

*noveltree* is a computer program for novelists who prefer to write with LibreOffice or OpenOffice, 
but need additional features for the organization of their work. 

![Screenshot](docs/Screenshots/screen01.png)

## Features

- With *noveltree*, extensive novels can be broken down into **parts, chapters, and sections**. 
- You can store data on **characters, locations, and items** that are important for the story.  
- All of this appears as a clear and editable **tree** structure with listed information. 
- Summaries can be entered at all these levels, from which **synopses** and lists can be generated. 
- If you choose a **narrative structure**, *novelibre* can display stages (e.g. acts or steps) in the tree.
  When plotting, descriptions of these stages can be entered, from which *noveltree* can generate 
  its own documentation. Prefabricated structural models can also be imported from templates.
- *noveltree* also allows you to create and document an **underlying structure of arcs** 
  (character arcs or storylines) apart from the chapters and sections. This can then be linked 
  to the sections of the novel text.
- To keep track of progress, the **word count** and the **completion status** of the sections are displayed. 
- Individual chapters and sections can be flagged as "unused" to exclude them from document export.
- You can add information about the **narrative time** and duration to each section. If you enter a date, 
  the day of the week is displayed. You can also call up the age of characters that are assigned to
  a section. The date and time information can be synchronised with dedicated timeline software.
- For the **actual writing work**, *noveltree* starts the word processor of LibreOffice or OpenOffice with 
  a structured manuscript in *Open Document* format (*.odt*). At the end of a work cycle, *noveltree* 
  reimports the manuscript and updates the writing project. New chapters and sections can also be 
  created in the process.
- For **printing**, *noveltree* exports a neatly designed novel manuscript that can be formatted as 
  you wish applying LibreOffice/OpenOffice document templates. 
- *noveltree* saves its data in a well-documented file format (XML), which can also be read as 
  plain text and displayed with a standard web browser.
- *noveltree* is written in Python and should run on several operating systems, like Windows and Linux.
- The application is ready for internationalization with GNU gettext. A German localization is provided. 

## Plugins

*noveltree's* functionality can be extended by plugins. Here are some examples:

- [A yw7 file importer/exporter](https://github.com/peter88213/nv_yw7/)
- [An on-demand update checker](https://github.com/peter88213/nv_updater/)
- [A daily progress log viewer](https://github.com/peter88213/nv_progress/)
- [A book/series collection manager](https://github.com/peter88213/nv_collection/)
- [A relationship matrix](https://github.com/peter88213/nv_matrix/)
- [A Timeline plugin](https://github.com/peter88213/nv_timeline/)
- [An Aeon Timeline 2 plugin](https://github.com/peter88213/nv_aeon2/)
- [A theme changer](https://github.com/peter88213/nv_themes/)
- [A Story Template management plugin](https://github.com/peter88213/nv_templates/)
- [A simple "markup" section editor](https://github.com/peter88213/nv_editor/)

## Tools

Stand-alone Python scripts for *novx* file conversion.

- [scap_novx](https://github.com/peter88213/scap_novx/): Generate a *noveltree* project from a *Scapple* outline.
- [novx_xtg](https://github.com/peter88213/novx_xtg/): XPress tagged text export from *noveltree* projects.

## Requirements

- [Python](https://www.python.org/) version 3.6+. 
     - For current Windows versions, use version 3.9.10 or above.
     - For Vista and Windows 7, use version 3.7.2.
     - Linux users: Make sure you have the *python3-tk* package installed.
- Either [LibreOffice](https://www.libreoffice.org/) or [OpenOffice](https://www.openoffice.org).

## General note about the fitness for use

At present, this program is still under active development. Therefore it is recommended to check for updates from time to time, as well as for the plugins. 

I use the program myself and fix errors immediately if I notice any. As far as I can tell, *noveltree* runs fast and reliably under Windows and Linux. It should also under other operating systems for which there is a reasonably up-to-date *Python 3* installation. However, there is a lack of a broad user base, which is why one cannot speak of real proven operation. 

## A note for novelyst users

*noveltree* is to replace the [novelyst](https://peter88213.github.io/novelyst/) application. 
The main differences are an improved workflow that doesn't require a LibreOffice/OpenOffice extension, and the use of a new file format instead of the *.yw7* format. For more details see the [comparison between noveltree and novelyst](https://github.com/peter88213/noveltree/discussions/2).

If you are considering switching from *novelyst* to *noveltree*, the 
[nv_yw7 plugin](https://github.com/peter88213/nv_yw7/) will help you to
create *.novx* files from your existing projects. To migrate entire collections or larger amounts of project files,
you might want to take a look at the [yw_novx conversion tools](https://github.com/peter88213/yw_novx).

## Download and install

[Download the latest release (version 2.0.0)](https://github.com/peter88213/noveltree/raw/main/dist/noveltree_v2.0.0.zip)

- Extract the "noveltree_v2.0.0" folder from the downloaded zipfile "noveltree_v2.0.0.zip".
- Move into this new folder and open "README.md" for further instructions.
- You may wish to install plugins; the [section editor](https://github.com/peter88213/nv_editor/) is highly recommended.

---

[Changelog](docs/changelog.md)

[News](https://github.com/peter88213/noveltree/discussions/1)

[Discussions](https://github.com/peter88213/noveltree/discussions)

## Usage

See the [instructions for use](docs/usage.md)

## Credits

The app icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).
The toolbar icons are based on the [Eva Icons](https://akveo.github.io/eva-icons/#/), published under the [MIT License](http://www.opensource.org/licenses/mit-license.php). The original black and white icons were colored for this plugin by the maintainer. 


## License

This is Open Source software, and *noveltree* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/noveltree/blob/main/LICENSE) file.

The modules in the *widgets* package are licenced under the [MIT License](http://www.opensource.org/licenses/mit-license.php). 
