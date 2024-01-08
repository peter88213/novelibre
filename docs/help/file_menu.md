[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Command reference: File menu

--- 

**NOTE:** This help page applies to *novelyst* and is not yet updated for *noveltree*.

# File menu 

**File operation**

--- 

## New 

**Create a new novel project**

- You can create a new project with **File > New** or **Ctrl-N**. This will close the current project
  and open a file dialog asking for the location and file name of the project to create.
- Once you specified a valid file path, a blank project appears. Be aware, it's not saved on disk yet.

--- 

## Open... 

**Open a novel project**

- If no novel project is specified by dragging and dropping on the program icon,
  the latest project selected is preset. You can change it with **File > Open** or **Ctrl-O**.

--- 

## Reload

**Reload the novel project**

- You can reload the project with **File > Reload** or **Ctrl-R**.
- If the project has changed on disk since last opened, you will get a warning.

--- 

## Restore backup

**Restore the latest backup file**

- You can restore the latest backup file with **File > Restore backup** or **Ctrl-B**.
- You will get a warning.
- After restoring the backup, the backup copy is no longer available.
- You can create a backup copy by saving the project.

--- 

## Refresh tree

**Update the project structure after making changes**

You can synchronize the tree with the project structure with **File > Refresh tree** or **F5**.
This ensures for instance, 
that sections within a "Notes", "Unused", or "To do" chapter are of the same type after moving them there.
- Refreshing the tree may trigger the "Modified" flag.
- When refreshing the tree, "Normal type" chapters in the *Research* tree are moved to the *Book* tree.
- When refreshing the tree, parts and chapters are renumbered according to the settings. 
- When refreshing the tree, the tree view is reset and the browsing history is cleared.

--- 

## Lock 

**Protect the project while edited outsides**

You can lock the project, so that no changes can be made with *noveltree* while parts of the project are
edited "outsides", e.g. with OpenOffice. In locked status, the window footer displaying the project path
is displayed in reversed colors. 
 
- You can lock the project with **File > Lock** or **Ctrl-L**. The project is saved when modified.

The project lock status is persistent. This is achieved by automatically creating a lock file 
named `.LOCK.<project name>.novx#`. If you delete this file while *noveltree* is not running, the project 
will be unlocked upon next start.  

--- 

## Unlock

**Make the project editable**

- You can unlock the project with **File > Unlock** or **Ctrl-U**. 

--- 

## Open Project folder

**Launch the file manager**

- You can launch the file manager with the current project folder with **File > Open Project folder** or **Ctrl-P**. 
This might be helpful, if you wish to delete export files, open your project with another application, and so on. 
In case you edit the project "outsides", consider locking it before.

---

## Discard manuscript

**Discard the current manuscript by renaming it**

- You can add the *.bak* extension to the current manuscript with **File > Discard manuscript**. 
This may help to avoid confusion about changes made with *noveltree* and OpenOffice/LibreOffice. 
It is recommended in any case if new sections or chapters were created by splitting during the 
last export from OpenOffice/LibreOffice. 

--- 

## Save

**Save the project**

- You can save the project with **File > Save** or **Ctrl-S**.
- If the project has changed on disk since last opened, you will get a warning.
- It is recommended to refresh the tree (see above) before saving. So you can see how 
  it will look after reloading. 

--- 

## Save as...

**Save the project with another file name/at another place**

- You can save the project with another file name/at another place with **File > Save as...** or **Ctrl-Shift-S**. Then a file select dialog opens.
- Your current project remains as saved the last time. Changes since then go to the new project.

--- 

## Close

**Close the novel project**

- You can close the project without exiting the program with **File > Close**.
- When closing the project, you will be asked for saving the project, if it has changed.
- If you open another project, the current project is automatically closed.

--- 

## Exit

**Exit the program**

- You can exit with **File > Exit** of **Ctrl-Q**.
- When exiting the program, you will be asked for saving the project, if it has changed.

--- 

[<< Last](tree_context_menu) -- [Next >>](view_menu)