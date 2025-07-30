# Contributing

## How to provide translations

First, you need to know your language code according to ISO 639-1.

For English, this is, for example, `en`, for German, it is `de`.

Now you can create a language pack based on the [nv_xx](https://github.com/peter88213/nv_xx) 
template and use the tools provided for this purpose. 

Anyway, the nuts and bolts of the translations system are described [here](TRANSLATE-md).



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


