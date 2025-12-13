"""Provide icons for the novelibre.GUI

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_globals import PROGRAM_DIR
from nvlib.nv_globals import prefs
import tkinter as tk


class Icons:

    def __init__(self):
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            iconPath = f'{PROGRAM_DIR}/icons/{size}'
        except:
            iconPath = None
        try:
            self.addIcon = tk.PhotoImage(
                file=f'{iconPath}/add.png'
            )
        except:
            self.addIcon = None
        try:
            self.addChildIcon = tk.PhotoImage(
                file=f'{iconPath}/addChild.png'
            )
        except:
            self.addChildIcon = None
        try:
            self.addParentIcon = tk.PhotoImage(
                file=f'{iconPath}/addParent.png'
            )
        except:
            self.addParentIcon = None
        try:
            self.goBackIcon = tk.PhotoImage(
                file=f'{iconPath}/goBack.png'
            )
        except:
            self.goBackIcon = None
        try:
            self.goForwardIcon = tk.PhotoImage(
                file=f'{iconPath}/goForward.png'
            )
        except:
            self.goForwardIcon = None
        try:
            self.gotoIcon = tk.PhotoImage(
                file=f'{iconPath}/goto.png'
            )
        except:
            self.gotoIcon = None
        try:
            self.lockIcon = tk.PhotoImage(
                file=f'{iconPath}/lock.png'
            )
        except:
            self.lockIcon = None
        try:
            self.manuscriptIcon = tk.PhotoImage(
                file=f'{iconPath}/manuscript.png'
            )
        except:
            self.manuscriptIcon = None
        try:
            self.propertiesIcon = tk.PhotoImage(
                file=f'{iconPath}/properties.png'
            )
        except:
            self.propertiesIcon = None
        try:
            self.removeIcon = tk.PhotoImage(
                file=f'{iconPath}/remove.png'
            )
        except:
            self.removeIcon = None
        try:
            self.saveIcon = tk.PhotoImage(
                file=f'{iconPath}/save.png'
            )
        except:
            self.saveIcon = None
        try:
            self.updateFromManuscriptIcon = tk.PhotoImage(
                file=f'{iconPath}/updateFromManuscript.png'
            )
        except:
            self.updateFromManuscriptIcon = None
        try:
            self.viewPlotLinesIcon = tk.PhotoImage(
                file=f'{iconPath}/viewArcs.png'
            )
        except:
            self.viewPlotLinesIcon = None
        try:
            self.viewBookIcon = tk.PhotoImage(
                file=f'{iconPath}/viewBook.png'
            )
        except:
            self.viewBookIcon = None
        try:
            self.viewCharactersIcon = tk.PhotoImage(
                file=f'{iconPath}/viewCharacters.png'
            )
        except:
            self.viewCharactersIcon = None
        try:
            self.viewItemsIcon = tk.PhotoImage(
                file=f'{iconPath}/viewItems.png'
            )
        except:
            self.viewItemsIcon = None
        try:
            self.viewLocationsIcon = tk.PhotoImage(
                file=f'{iconPath}/viewLocations.png'
            )
        except:
            self.viewLocationsIcon = None
        try:
            self.viewProjectnotesIcon = tk.PhotoImage(
                file=f'{iconPath}/viewProjectnotes.png'
            )
        except:
            self.viewProjectnotesIcon = None
        try:
            self.viewerIcon = tk.PhotoImage(
                file=f'{iconPath}/viewer.png'
            )
        except:
            self.viewerIcon = None
        try:
            self.cutIcon = tk.PhotoImage(
                file=f'{iconPath}/cut.png'
            )
        except:
            self.cutIcon = None
        try:
            self.copyIcon = tk.PhotoImage(
                file=f'{iconPath}/copy.png'
            )
        except:
            self.copyIcon = None
        try:
            self.pasteIcon = tk.PhotoImage(
                file=f'{iconPath}/paste.png'
            )
        except:
            self.pasteIcon = None
        try:
            self.resetHighlightIcon = tk.PhotoImage(
                file=f'{iconPath}/reset_highlight.png'
            )
        except:
            self.resetHighlightIcon = None
        try:
            self.tagsIcon = tk.PhotoImage(
                file=f'{iconPath}/tag.png'
            )
        except:
            self.tagsIcon = None
        try:
            self.highlightIcon = tk.PhotoImage(
                file=f'{iconPath}/highlight.png'
            )
        except:
            self.highlightIcon = None
        try:
            self.exitIcon = tk.PhotoImage(
                file=f'{iconPath}/exit.png'
            )
        except:
            self.exitIcon = None
        try:
            self.expandIcon = tk.PhotoImage(
                file=f'{iconPath}/expand.png'
            )
        except:
            self.expandIcon = None
        try:
            self.collapseIcon = tk.PhotoImage(
                file=f'{iconPath}/collapse.png'
            )
        except:
            self.collapseIcon = None
        try:
            self.unlockIcon = tk.PhotoImage(
                file=f'{iconPath}/unlock.png'
            )
        except:
            self.unlockIcon = None
        try:
            self.reloadIcon = tk.PhotoImage(
                file=f'{iconPath}/reload.png'
            )
        except:
            self.reloadIcon = None
        try:
            self.closeIcon = tk.PhotoImage(
                file=f'{iconPath}/close.png'
            )
        except:
            self.closeIcon = None
        try:
            self.settingsIcon = tk.PhotoImage(
                file=f'{iconPath}/settings.png'
            )
        except:
            self.settingsIcon = None
        try:
            self.gridIcon = tk.PhotoImage(
                file=f'{iconPath}/grid.png'
            )
        except:
            self.gridIcon = None
        try:
            self.levelsIcon = tk.PhotoImage(
                file=f'{iconPath}/levels.png'
            )
        except:
            self.levelsIcon = None
        try:
            self.stageIcon = tk.PhotoImage(
                file=f'{iconPath}/stage.png'
            )
        except:
            self.stageIcon = None
        try:
            self.importIcon = tk.PhotoImage(
                file=f'{iconPath}/import.png'
            )
        except:
            self.importIcon = None
        try:
            self.exportIcon = tk.PhotoImage(
                file=f'{iconPath}/export.png'
            )
        except:
            self.exportIcon = None
        try:
            self.povIcon = tk.PhotoImage(
                file=f'{iconPath}/pov.png'
            )
        except:
            self.povIcon = None
        try:
            self.statusIcon = tk.PhotoImage(
                file=f'{iconPath}/status.png'
            )
        except:
            self.statusIcon = None
        try:
            self.typeIcon = tk.PhotoImage(
                file=f'{iconPath}/type.png'
            )
        except:
            self.typeIcon = None
        try:
            self.chaptersIcon = tk.PhotoImage(
                file=f'{iconPath}/chapters.png'
            )
        except:
            self.chaptersIcon = None
        try:
            self.pluginsIcon = tk.PhotoImage(
                file=f'{iconPath}/plugins.png'
            )
        except:
            self.pluginsIcon = None
        try:
            self.installationFolderIcon = tk.PhotoImage(
                file=f'{iconPath}/installation_folder.png'
            )
        except:
            self.installationFolderIcon = None
        try:
            self.folderIcon = tk.PhotoImage(
                file=f'{iconPath}/folder.png'
            )
        except:
            self.folderIcon = None
        try:
            self.stickyNoteIcon = tk.PhotoImage(
                file=f'{iconPath}/sticky_note.png'
            )
        except:
            self.stickyNoteIcon = None
