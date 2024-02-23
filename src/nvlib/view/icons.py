"""Provide icons for the novelibre.GUI

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

from nvlib.nv_globals import prefs
import tkinter as tk


class Icons:

    def __init__(self):
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            iconPath = f'{os.path.dirname(sys.argv[0])}/icons/{size}'
        except:
            iconPath = None
        try:
            self.addIcon = tk.PhotoImage(file=f'{iconPath}/add.png')
        except:
            self.addIcon = None
        try:
            self.addChildIcon = tk.PhotoImage(file=f'{iconPath}/addChild.png')
        except:
            self.addChildIcon = None
        try:
            self.addParentIcon = tk.PhotoImage(file=f'{iconPath}/addParent.png')
        except:
            self.addParentIcon = None
        try:
            self.goBackIcon = tk.PhotoImage(file=f'{iconPath}/goBack.png')
        except:
            self.goBackIcon = None
        try:
            self.goForwardIcon = tk.PhotoImage(file=f'{iconPath}/goForward.png')
        except:
            self.goForwardIcon = None
        try:
            self.gotoIcon = tk.PhotoImage(file=f'{iconPath}/goto.png')
        except:
            self.gotoIcon = None
        try:
            self.lockIcon = tk.PhotoImage(file=f'{iconPath}/lock.png')
        except:
            self.lockIcon = None
        try:
            self.manuscriptIcon = tk.PhotoImage(file=f'{iconPath}/manuscript.png')
        except:
            self.manuscriptIcon = None
        try:
            self.propertiesIcon = tk.PhotoImage(file=f'{iconPath}/properties.png')
        except:
            self.propertiesIcon = None
        try:
            self.removeIcon = tk.PhotoImage(file=f'{iconPath}/remove.png')
        except:
            self.removeIcon = None
        try:
            self.saveIcon = tk.PhotoImage(file=f'{iconPath}/save.png')
        except:
            self.saveIcon = None
        try:
            self.updateFromManuscriptIcon = tk.PhotoImage(file=f'{iconPath}/updateFromManuscript.png')
        except:
            self.updateFromManuscriptIcon = None
        try:
            self.viewArcsIcon = tk.PhotoImage(file=f'{iconPath}/viewArcs.png')
        except:
            self.viewArcsIcon = None
        try:
            self.viewBookIcon = tk.PhotoImage(file=f'{iconPath}/viewBook.png')
        except:
            self.viewBookIcon = None
        try:
            self.viewCharactersIcon = tk.PhotoImage(file=f'{iconPath}/viewCharacters.png')
        except:
            self.viewCharactersIcon = None
        try:
            self.viewItemsIcon = tk.PhotoImage(file=f'{iconPath}/viewItems.png')
        except:
            self.viewItemsIcon = None
        try:
            self.viewLocationsIcon = tk.PhotoImage(file=f'{iconPath}/viewLocations.png')
        except:
            self.viewLocationsIcon = None
        try:
            self.viewProjectnotesIcon = tk.PhotoImage(file=f'{iconPath}/viewProjectnotes.png')
        except:
            self.viewProjectnotesIcon = None
        try:
            self.viewerIcon = tk.PhotoImage(file=f'{iconPath}/viewer.png')
        except:
            self.viewerIcon = None
