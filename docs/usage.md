[Project homepage](../) > Instructions for use

--- 

The *novelibre* Python program provides a tree view for novels written with LibreOffice or OpenOffice *Writer*.

# Instructions for use


## Installation

- Unzip the downloaded zipfile.
- Move into the unzipped folder and launch **setup.pyw**. This installs the application for the local user.
- Create a shortcut on the desktop when asked.
- Optionally, you can replace the "Python" icon by the *novelibre* logo you may find in the installation's **icons** subdirectory.

---

### Windows integration

After installation, the setup script displays a button to open the installation directory. On Windows, the path is typically

`C:\Users\<username>\.novx`

There you will find some registry scripts that can help you integrate *novelibre* into Windows. They are started by double-clicking.

- **add_novelibre.reg** makes Explorer launch *novelibre* when you double-click *.novx* files. *.novx* files will be assigned the *novelibre* icon. *.novx* files will be assigned the content type "text/xml" This may be necessary if you want to view *.novx* files with a web browser. 

You can redo this:

- **remove_novelibre.reg** removes the registry entries made for the *.novx* file type. 

--- 

### Linux desktop integration

- You can configure a desktop launcher for *novelibre* and assign the *novelibre* icon you may find in the installation's **icons** subdirectory.
- You can set *novelibre* as the default application for *.novx* files.
- If you want to view *.novx* files with your web browser, it is recommended to register the *MIME type* of *.novx* files as *"text/xml"*.

Please refer to your desktop's documentation. 

---

## Launch the program

The included installation script prompts you to create a shortcut on the desktop. 

You can either

- launch the program by double-clicking on the shortcut icon, or
- launch the program by dragging and dropping a *.novx* project file to the shortcut icon.


--- 

# [Online help](https://peter88213.github.io/nvhelp-en/index.html)


You can open the online help page with **Help > Online help**.

![Online help screenshot](Screenshots/help01.png)

--- 

# License

This is Open Source software, and *novelibre* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelibre/blob/main/LICENSE) file.

