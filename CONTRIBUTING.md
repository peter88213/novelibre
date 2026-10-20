# Contributing

## General

- Unless you use *novelibre* yourself, it seems rather unlikely to me 
  that you could contribute anything meaningful.

- Before contributing to this project, consider going to the 
  [novelibre "Discussions" forum](https://github.com/peter88213/novelibre/discussions) 
  first to discuss your idea. 
  If you're considering implementing a new feature, the preferred approach is to create a plugin. 

- If you want to pick up an issue, please contact me before creating a pull request. 
  To do so, just leave a comment on the relevant issue.

- The proper way to contribute code is forking the repository 
  and implementing your solution in a thread other than `main`.  
  Then create a pull request. 
  Any code sent via email attachments etc. may be considered as spam and rejected.

- Offers of code in exchange for payment will be discarded as spam. 
 
- Before you start coding, familiarize yourself with the design of *novelibre*, 
  particularly the implementation of the MVC pattern and the plugin API. 
  User interaction should be handled through this API and use the notification 
  mechanisms of the novelibre GUI. 


## AI policy

I consider code to be creative work, and I have a strong preference for 
contributions designed by actual humans over the average and 
mediocre output of agentic and generative AI.

In general, so-called vibe coding does not meet my code quality requirements, 
so this project is not suitable for such contributions in any case. 
The licensing implications around generated code are also unclear, 
as AI models are trained on material without consent or concern for original licensing.

No AI automation or agentic tools are used anywhere in this project. 
Do not use your AI agents on your contributions either. 
Commits listed in any way as authored by, signed off by, or assisted by, 
AI tools are explicitly not allowed. 
Pull requests containing such commits will be rejected. 
You should also not commit AI-specific files into the code repository. 


## How to provide translations

Translation files are distributed as language packs and maintained in their own repositories. 
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
[novelibre discussion page](https://github.com/peter88213/novelibre/discussions/71)
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


