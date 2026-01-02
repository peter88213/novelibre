"""Provide icons for the novelibre.GUI

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path

from nvlib.nv_globals import prefs
import tkinter as tk


class Icons:

    def __init__(self):

        def new_icon(iconFile):
            try:
                return tk.PhotoImage(file=f'{iconPath}/{iconFile}')

            except:
                return None

        def get_icon_dir(size):
            try:
                homeDir = str(Path.home()).replace('\\', '/')
            except:
                return None

            iconPath = f"{homeDir}/.novx/{prefs['icon_set']}/{size}"
            if os.path.isdir(iconPath):
                return iconPath

            prefs['icon_set'] = 'icons'
            iconPath = f'{homeDir}/.novx/icons/{size}'
            if os.path.isdir(iconPath):
                return iconPath

            return None

        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16

        iconPath = get_icon_dir(size)

        self.addChildIcon = new_icon('addChild.png')

        self.addIcon = new_icon('add.png')

        self.addMultipleIcon = new_icon('add_multiple.png')

        self.addParentIcon = new_icon('addParent.png')

        self.chaptersIcon = new_icon('chapters.png')

        self.closeIcon = new_icon('close.png')

        self.collapseIcon = new_icon('collapse.png')

        self.copyIcon = new_icon('copy.png')

        self.cutIcon = new_icon('cut.png')

        self.discardManuscriptIcon = new_icon('discardManuscript.png')

        self.exitIcon = new_icon('exit.png')

        self.expandIcon = new_icon('expand.png')

        self.exportIcon = new_icon('export.png')

        self.folderIcon = new_icon('folder.png')

        self.goBackIcon = new_icon('goBack.png')

        self.goForwardIcon = new_icon('goForward.png')

        self.gotoIcon = new_icon('goto.png')

        self.gridIcon = new_icon('grid.png')

        self.helpIcon = new_icon('help.png')

        self.highlightIcon = new_icon('highlight.png')

        self.homeIcon = new_icon('home.png')

        self.importIcon = new_icon('import.png')

        self.installationFolderIcon = new_icon('installation_folder.png')

        self.levelsIcon = new_icon('levels.png')

        self.lockIcon = new_icon('lock.png')

        self.manuscriptIcon = new_icon('manuscript.png')

        self.nLogoIcon = new_icon('nLogo.png')

        self.newProjectIcon = new_icon('newProject.png')

        self.newsIcon = new_icon('smile.png')

        self.openProjectIcon = new_icon('openProject.png')

        self.pasteIcon = new_icon('paste.png')

        self.pluginsIcon = new_icon('plugins.png')

        self.povIcon = new_icon('pov.png')

        self.propertiesIcon = new_icon('properties.png')

        self.reloadIcon = new_icon('reload.png')

        self.removeIcon = new_icon('remove.png')

        self.resetHighlightIcon = new_icon('reset_highlight.png')

        self.saveAsIcon = new_icon('saveAs.png')

        self.saveIcon = new_icon('save.png')

        self.settingsIcon = new_icon('settings.png')

        self.stageIcon = new_icon('stage.png')

        self.statusIcon = new_icon('status.png')

        self.stickyNoteIcon = new_icon('sticky_note.png')

        self.tagsIcon = new_icon('tag.png')

        self.typeIcon = new_icon('type.png')

        self.unlockIcon = new_icon('unlock.png')

        self.updateFromManuscriptIcon = new_icon('updateFromManuscript.png')

        self.viewBookIcon = new_icon('viewBook.png')

        self.viewCharactersIcon = new_icon('viewCharacters.png')

        self.viewItemsIcon = new_icon('viewItems.png')

        self.viewLocationsIcon = new_icon('viewLocations.png')

        self.viewPlotLinesIcon = new_icon('viewArcs.png')

        self.viewProjectnotesIcon = new_icon('viewProjectnotes.png')

        self.viewerIcon = new_icon('viewer.png')

