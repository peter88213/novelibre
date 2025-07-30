# How to provide translations

First, you need to know your language code according to ISO 639-1.

For English, this is, for example, `en`, for German, it is `de`.

---

**Important**: The procedure described below is greatly simplified if you create a 
language pack based on the [nv_xx](https://github.com/peter88213/nv_xx) template 
and use the tools provided for this purpose. 

---

## Create a message catalog

A "message catalog" is a dictionary for novelibre's messages and menu entries.

For creating a message catalog, you download a template with all English messages 
from [here](https://github.com/peter88213/novelibre/blob/main/i18n/messages.pot). 


Rename `messages.pot` to `<your language code>.po`, then give some specific information 
in the header data by modifying the following lines:

```
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language: LANGUAGE\n"
```

**NOTE:** Be sure to use a text editor that writes utf-8 encoded text. Otherwise, it 
may not work with non-ASCII characters used in your language.

The  `<your language code>.po` dictionary is organized as a set of 
*message ID (msgid)* - *message string (msgstr)* pairs, where *msgid* 
means the English term, and *msgstr* means the translated term. 
This is an example for such a pair where the message string is still missing:

```
msgid "Cannot overwrite file"
msgstr ""
```

Now you enter all missing message strings. 
- If a message ID contains placeholders like `{}`, be sure to put them also 
into the message string.  
- If a message ID starts with `!`, the message string must also start with `!`. 

Before you distribute your translations, you can convert and install the message 
catalog for testing. 

## Convert the message catalog to binary format

The application needs the message catalog in binary format. This is easily achieved 
using the **msgfmt.py** converter script. 
You find it in your Python installation, in the **Tools/i18n** subdirectory. 
If not, you can download the code from [here](https://github.com/python/cpython/blob/main/Tools/i18n/msgfmt.py)

Name the binary file **novelibre.mo**. 


## Install your translation for testing

Add a subdirectory tree to **.novx/locale**, and place *novelibre.mo* there, like this:

```
<your home directory>
└── .novelibre/
    └── locale/
        └─ <language code>/
           └─ LC_MESSAGES/
              └─ novelibre.mo
```

Then start *novelibre* and see whether your translation works. 

**NOTE:** At startup, *novelibre* tries to load a message dictionary that fits to the system language. If it doesn't find a matching language code in the *locale* directory, it uses English as default language. 

**HINT:** *novelibre* comes with German translations. Look at the `de` directory tree, if you need an example. 


## Contribute your translations

If *novelibre* works fine with your translations, you can consider contributing it. 

An easy way may be to put a posting in the [novelibre forum](https://github.com/peter88213/novelibre/discussions), appending your  `<your language code>.po` file. 
