# noveltree

*noveltree* is an organizer tool for writing novels with LibreOffice or OpenOffice Writer. It is written in Python and should run on several operating systems.

For more information, see the [project homepage](https://peter88213.github.io/noveltree) with description and download instructions.

## Feedback? Ideas? Feature requests?

You can go to the ["discussions" forum](https://github.com/peter88213/noveltree/discussions) and start a thread.

# Contributing

## How to provide translations

First, you need to know your language code according to ISO 639-1.

For English, this is, for example, `en`, for German, it is `de`.

**NOTE:** The procedure described below is greatly simplified if you create a language pack based on the [noveltree_xx](https://github.com/peter88213/noveltree_xx) template and use the tools provided for this purpose. 

### Create a message catalog

A "message catalog" is a dictionary for noveltree's messages and menu entries.

For creating a message catalog, you download a template with all English messages from [here](https://github.com/peter88213/noveltree/blob/main/i18n/messages.pot). 


Rename `messages.pot` to `<your language code>.po`, then give some specific information in the header data by modifying the following lines:

```
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language: LANGUAGE\n"
```

**NOTE:** Be sure to use a text editor that writes utf-8 encoded text. Otherwise, it may not work with non-ASCII characters used in your language.

The  `<your language code>.po` dictionary is organized as a set of *message ID (msgid)* - *message string (msgstr)* pairs, where *msgid* means the English term, and *msgstr* means the translated term. This is an example for such a pair where the message string is still missing:

```
msgid "Cannot overwrite file"
msgstr ""
```

Now you enter all missing message strings. 
- If a message ID contains placeholders like `{}`, be sure to put them also into the message string.  
- If a message ID starts with `!`, the message string must also start with `!`. 

Before you distribute your translations, you can convert and install the message catalog for testing. 

### Convert the message catalog to binary format

The application needs the message catalog in binary format. This is easily achieved using the **msgfmt.py** converter script. 
You find it in your Python installation, in the **Tools/i18n** subdirectory. If not, you can download the code from [here](https://github.com/python/cpython/blob/main/Tools/i18n/msgfmt.py)

Name the binary file **noveltree.mo**. 


### Install your translation for testing

Add a subdirectory tree to **.noveltree/locale**, and place *noveltree.mo* there, like this:

```
<your home directory>
└── .noveltree/
    └── locale/
        └─ <language code>/
           └─ LC_MESSAGES/
              └─ noveltree.mo
```

Then start *noveltree* and see whether your translation works. 

**NOTE:** At startup, *noveltree* tries to load a message dictionary that fits to the system language. If it doesn't find a matching language code in the *locale* directory, it uses English as default language. 

**HINT:** *noveltree* comes with German translations. Look at the `de` directory tree, if you need an example. 


### Contribute your translations

If *noveltree* works fine with your translations, you can consider contributing it. 

An easy way may be to put a posting in the [noveltree forum](https://github.com/peter88213/noveltree/discussions), appending your  `<your language code>.po` file. 


## Development

*noveltree* depends on the [novxlib](https://github.com/peter88213/novxlib) library which must be present in your file system. It is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Mandatory directory structure for building the application

```
.
├── novxlib/
│   └── src/
│       ├── novxlib/
│       ├── inliner.py
│       ├── pgettext.py
│       ├── translations.py
│       └── msgfmt.py
└── noveltree/
    ├── src/
    ├── test/
    └── tools/ 
        ├── build.xml
        ├── build_noveltree.py
        ├── make_pot.py
        └── translate_de.py
```

### Conventions

See https://github.com/peter88213/novxlib/blob/main/docs/conventions.md

## Development tools

- [Python](https://python.org) version 3.11.
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and *EGit*.
- Apache Ant is used for building the application.

### Documentation tools

- [Gaphor](https://gaphor.org/) for creating UML diagrams

## Plugin development

If you want to develop a noveltree plugin, you may want to start with a repository on GitHub using [noveltree_plugin](https://github.com/peter88213/noveltree_plugin) as a template repository. After setting up your new repository 
named e.g. *noveltree_yourPluginName*, just do a global search, and replace 
*noveltree_plugin* with *noveltree_yourPluginName*. 


## Credits

The icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

This is Open Source software, and *noveltree* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/noveltree/blob/main/LICENSE) file.

The modules in the *widgets* package are licenced under the [MIT License](http://www.opensource.org/licenses/mit-license.php). 
