# Contributing

## How to provide translations

Translation files are distributed as language packs. 
This makes it easier to provide translations for all plugins, 
and also to offer online help that uses the translated terms.
The main advantage of this method is that separate language packs 
can be added and updated without requiring new versions of the application. 


### Updating existing language packs 

Anyone who would like to contribute to the further development and updating 
of the existing language packs should fork the relevant plugin repository 
and make a pull request after creating or revising the *.po and/or *.md files. 
The maintainer of *novelibre* can then 
create the new release after merging the changes. 


### Creating new language packs

New language packs are created using the 
[nv_xx](https://github.com/peter88213/nv_xx) 
template repository. 
If you don't feel confident doing this yourself, you can post on the 
[novelibre discussion page](https://github.com/peter88213/novelibre/discussions)
to request a language pack, whose translation files and help pages you can then edit. 




## Development

*novelibre* is organized as an Eclipse PyDev project. 
The official release branch on GitHub is *main*.

### Mandatory directory structure for building the application package

```
.
└── novelibre/
    ├── i18n/
    ├── src/
    └── tools/ 
        ├── build.py
        ├── inliner.py
        ├── msgfmt.py
        ├── package_builder.py
        ├── pgettext.py
        ├── translate_de.py
        └── translations.py
```

### Conventions

See the [coding conventions page](docs/conventions.md)

## Development tools

- [Python](https://python.org) version 3.12.
- **build.py** starts the building and packaging process.

### Optional IDE
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and *EGit*.
- Apache Ant can be used for starting the **build.py** script.

### Documentation tools
- [Gaphor](https://gaphor.org/) UML modeler. 
- [Sphinx](https://www.sphinx-doc.org) website generator for the online documentation.

## Plugin development

If you want to develop a novelibre plugin, you may want to start with a repository on GitHub using [nv_plugin](https://github.com/peter88213/nv_plugin) as a template repository. After setting up your new repository 
named e.g. *novelibre_yourPluginName*, just do a global search, and replace 
*nv_plugin* with *novelibre_yourPluginName*, and *nv_plugin* with *nv_yourPluginName*. 


