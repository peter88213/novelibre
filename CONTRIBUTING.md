# Contributing

## General

- If you don't use *novelibre* yourself, it seems rather unlikely to me 
  that you could contribute anything meaningful.

- Any constructive feedback and any sharing of user experiences on the 
  [novelibre "Discussions" forum](https://github.com/peter88213/novelibre/discussions)
  is a useful contribution to the maintenance and improvement of *novelibre*, 
  even if it merely serves as an encouragement to continue providing the software. 

- Contributions to the documentation in the form of best practices on the 
  [novelibre Wiki](https://github.com/peter88213/novelibre/wiki) are greatly appreciated. 

- Also, contributions to the translation into your language—if it is not English or 
  German—are very welcome (see below). 

- If the program does not behave as described in the user guide, 
  there may be a bug. In that case, an issue report might help. 
  If it is obvious that the bug is in a plugin, please file the issue report 
  in the repository for that plugin. Otherwise, use the *Issues* page of 
  the *novelibre* repository.

- If you'd like to suggest an improvement for *novelibre* or its plugins, the 
  [novelibre "Discussions" forum](https://github.com/peter88213/novelibre/discussions)
  is the place to go. 
  Please do not submit a feature request as an issue before your idea 
  has been discussed in the discussion forum. 

- If you want to pick up an existing issue, contact the maintainer by
  leaving a comment on the relevant issue before you start coding.

- If you want to contribute code, keep in mind that *novelibre* users 
  entrust the application with their work—which may span many years—and 
  must therefore rely on your expertise and diligence.
  If you need AI assistance while coding, it may be that you don't really 
  understand the output you're trying to produce. 
  In that case, you should refrain from contributing code to the *novelibre* project. 
   
- The proper way to contribute code is forking the repository 
  and implementing your solution in a new branch other than `main`. 
  Then create a pull request. 
  Pull requests—with the exception of translations—are only accepted 
  if they are related to an issue to which you are assigned as a contributor.  
  Code sent via email will be classified as spam and rejected.

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

- [Python](https://python.org) version 3.15.
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


