# novelibre Conventions


### Coding conventions

- The code must be compatible with Python version 3.6. 
- The Python source code formatting follows widely the [PEP 8](https://peps.python.org/pep-0008/) style guide, except the maximum line length, which is 120 characters here.
- The code commenting follows the [PEP 257](https://peps.python.org/pep-0257) convention. [pydoc](https://docs.python.org/3/library/pydoc.html) can be used to display documentation for the *novelibre* modules and classes.
- Instead of inserting inline comments, append block comments.
- Type hints are not used.
- Strings are preferably enclosed in single quotes. Double quotes should only be used if nesting with single quotes is unavoidable.
- Strings should not be concatenated with the `+` operator, but with f-strings. See [PEP 498](https://peps.python.org/pep-0498/).
- All strings that appear on the user interface must be prepared for translation with GNU gettext, like: `_('See this message.')`.
- A package's **__init__.py** must not contain executable code.
- Each novelibre class is implemented in its own module.
- novelibre classes are imported with `from <module> import <class>`.

#### Method naming conventions

- `new_...`: Create an instance and return the object reference.
- `add_new_...`: Create an instance and add it to the novel. Return the element ID.
- `create_...`: Create anything.

## How to use the library with plugins and other applications

The *nvlib* package is not intended to be installed by the user, e.g. via *pip*. 
Instead, applications based on novelibre shall be self contained. That means, they contain all the code in a single script.

An application is built using the *inliner.py* script, which copies the code of all modules imported from the *nvlib* package.
The inliner script is called from an application-specific build script that passes the project-specific paths as parameters.

This is the directory structure required for building an application:

```
.
├── novelibre/
│   └── src/
│       ├── nvlib/
│       └── inliner.py
└── application/
    ├── src/
    ├── test/
    └── tools/ 
        ├── build.xml
        └── build_application.py
```

**IMPORTANT**

The *inliner.py* packager tool discards docstrings of imported modules in order to save memory. 

Docstrings are considered to be all strings that begin and end with three double quotes.

Thus, multiline strings not to be discarded during building *must* start and end with three single quotes. 



