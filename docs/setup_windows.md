![external-link](_images/external-link.png)
[Deutsch](https://peter88213.github.io/nvhelp-de/setup_windows.html)

------------------------------------------------------------------------

# Installation under Windows

> **Important**
>
> You receive *novelibre* as source code in the *Python* programming
> language. In order to execute the program, Python must be installed on
> your PC. There are several ways to obtain Python for free. In any case,
> I recommend the developers\' website:
>
> <https://www.python.org/>
> 
> Python is being continuously developed and improved. However, you don\'t
> need to update your Python installation as long as *novelibre* works
> with it.

> **Note**
>
> Files with the extensions **.py**, **.pyw**, and **.pyz** are Python
> programs ready to run. If you double-click such a file in Windows
> Explorer, the installed Python interpreter should launch, and nothing
> else. If that doesn\'t happen, you may not have Python fully installed.
> 
> If you\'re not sure, you can check the Windows Settings to see whether
> the assignment is correct. In Windows 11, go to Settings. The
> assignments should look like this:
> 
> ![Settings \> Apps \> Default apps \> Choose default apps by file type](_images/windows11.png)


The actual installation of *novelibre* is simple and straightforward.
The installation program automatically creates an installation
directory, copies everything necessary into it, and generates a start
file named **run.pyw** adapted for the respective computer, which must
be called in order to execute *novelibre*.

The necessary manual work consists of linking this start file to the
desktop and, if desired, assigning a program icon to the link. I will
also show you how to set it up under Windows so that the *novelibre*
project files have their own program icon and that the program
application is started when you double-click on them.

Unfortunately, I cannot automate this with my simple means without
causing problems with the security mechanisms of the operating system.

## Installing the application

#### Step 1

- Either launch the downloaded **novelibre_vx.x.x.pyz** file by
  double-clicking,

  ![Example (Windows Explorer)](_images/windows01.png)

- or execute `python novelibre_vx.x.x.pyz` on the command line.

  ![Example (Windows command line)](_images/windows02.png)

  *\"x.x.x\"* means the version number.

In both cases, a success message should appear.

![Example (Windows)](_images/windows03.png)

> **Important**
> 
> Many web browsers recognize the download as an executable file and
> offer to open it immedately. This allows you to start the
> installation conveniently.
>
> ![Beispiel (Chrome browser)](_images/windows04.png)
>
> However, depending on your security settings, your browser may
> initially refuse to download the executable file. In this case, your
> confirmation or an additional action is required.
>
> If this is not possible, you have the option of downloading the zip
> file. Then unpack it and execute `setup.py` by double-click.

> ![Example (Windows)](_images/windows10.png)

## Making novelibre accessible on the Desktop

#### Step 2

Open the installation folder.

![novelibre screenshot](_images/windows05.png)

#### Step 3

Drag and drop **run.pyw** to the desktop while holding down the
`Alt` key. This creates a shortcut to launch *novelibre* from the
Windows desktop. Now you can also drag and drop *.novx* project
files to this shortcut.

![novelibre screenshot](_images/windows06.png)

#### Step 4

Optionally, you can replace the \"Python\" icon with the *novelibre*
logo you may find in the installation\'s *icons* subdirectory.

To do this, right-click on the desktop shortcut and open the
**Properties** dialog. Select the **Shortcut** Tab and click on the
**Change icon** button (1). In the icon selection dialog, click on
the **Browse\...** button (2). This opens a file selection dialog.
Move to `<home>\.novx\icons` and double-click on the \"N\" logo (3).

![novelibre screenshot](_images/windows07.png)

#### Step 5

To rename the shortcut to *novelibre*, right-click on the desktop
shortcut and open the **Properties** dialog. In the first tab,
replace \"Shortcut to run.pyw\" with \"novelibre\".

![novelibre screenshot](_images/windows08.png)

## Associating .novx files with novelibre

#### Step 6

Optionally, you can associate the **.novx** file extension with the
*novelibre* application. Then the project files are displayed with
the *novelibre* icon in the Explorer, and you can open them with
*novelibre* by double-click. Further, you can display *.novx* files
with a web browser, using the [novx.css style
sheet](file_menu.html#copy-style-sheet).

Double-click on the **add_novelibre.reg** script. Windows will
display a warning and ask you for confirmation. If in doubt, you can
inspect the *add_novelibre.reg* file with a text editor or ask an
expert you trust.

![novelibre screenshot](_images/windows09.png)

> **Hint**
>
> You can undo this by executing the **remove_novelibre.reg** script.
> This removes all the *novelibre*-specific entries from the Windows
> registry while keeping the application.
>
> To uninstall the application and all its tools, plugins, and
> configuration data, just delete the `<home>\.novx` folder after
> executing the **remove_novelibre.reg** script.
    
> **Important**
>
> Executing the program under Windows by double-clicking on the *.novx*
> file works under the hood by calling the currently installed version of
> the Python interpreter.
> 
> If you update Python at a later date, you must then re-install
> *novelibre* afterwards, and execute **add_novelibre.reg** again.
> Otherwise, Windows will not be able to find the new Python version and
> will fail when trying to open *.novx* files on double-clicking.
> 
> Please keep that in mind, even if it\'s pretty unlikely that *novelibre*
> will need a Python update in the near future.

## Updating the application or a plugin

Just execute the first step as described above. If there is any further
action required, the setup script will give you a message.
