"""Provide a class for novelibre cross reference generation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.novel import Novel
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT


class CrossReferences:
    """Dictionaries containing a novel's cross references."""

    def __init__(self):
        # Cross reference dictionaries:

        self.scnPerChr = {}
        # key = character ID, value: list of section IDs
        # Sections per character
        self.scnPerLoc = {}
        # key = location ID, value: list of section IDs
        # Sections per location
        self.scnPerItm = {}
        # key = item ID, value: list of section IDs
        # Sections per item
        self.scnPerTag = {}
        # key = tag, value: list of section IDs
        # Sections per tag
        self.chrPerTag = {}
        # key = tag, value: list of character IDs
        # Characters per tag
        self.locPerTag = {}
        # key = tag, value: list of location IDs
        # Locations per tag
        self.itmPerTag = {}
        # key = tag, value: list of item IDs
        # Items per tag
        self.chpPerScn = {}
        # key = section ID, value: chapter ID
        # Chapter to which the section belongs
        self.srtSections = None
        # Section IDs in the overall order

    def generate_xref(self, novel: Novel):
        """Generate cross references for a novel.
        
        Positional argument:
            novel -- Novel instance to process.
        """
        self.scnPerChr = {}
        self.scnPerLoc = {}
        self.scnPerItm = {}
        self.scnPerTag = {}
        self.chrPerTag = {}
        self.locPerTag = {}
        self.itmPerTag = {}
        self.chpPerScn = {}
        self.srtSections = []

        #--- Characters per tag.
        for crId in novel.tree.get_children(CR_ROOT):
            self.scnPerChr[crId] = []
            if novel.characters[crId].tags:
                for tag in novel.characters[crId].tags:
                    if not tag in self.chrPerTag:
                        self.chrPerTag[tag] = []
                    self.chrPerTag[tag].append(crId)

        #--- Locations per tag.
        for lcId in novel.tree.get_children(LC_ROOT):
            self.scnPerLoc[lcId] = []
            if novel.locations[lcId].tags:
                for tag in novel.locations[lcId].tags:
                    if not tag in self.locPerTag:
                        self.locPerTag[tag] = []
                    self.locPerTag[tag].append(lcId)

        #--- Items per tag.
        for itId in novel.tree.get_children(IT_ROOT):
            self.scnPerItm[itId] = []
            if novel.items[itId].tags:
                for tag in novel.items[itId].tags:
                    if not tag in self.itmPerTag:
                        self.itmPerTag[tag] = []
                    self.itmPerTag[tag].append(itId)

        #--- Process chapters and sections.
        for chId in novel.tree.get_children(CH_ROOT):

            for scId in novel.tree.get_children(chId):
                self.srtSections.append(scId)
                self.chpPerScn[scId] = chId

                #--- Sections per character.
                if novel.sections[scId].characters:
                    for crId in novel.sections[scId].characters:
                        self.scnPerChr[crId].append(scId)

                #--- Sections per location.
                if novel.sections[scId].locations:
                    for lcId in novel.sections[scId].locations:
                        self.scnPerLoc[lcId].append(scId)

                #--- Sections per item.
                if novel.sections[scId].items:
                    for itId in novel.sections[scId].items:
                        self.scnPerItm[itId].append(scId)

                #--- Sections per tag.
                if novel.sections[scId].tags:
                    for tag in novel.sections[scId].tags:
                        if not tag in self.scnPerTag:
                            self.scnPerTag[tag] = []
                        self.scnPerTag[tag].append(scId)
