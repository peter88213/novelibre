"""Read characters from an XML data file.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import sys
from novxlib.model.novel import Novel
from novxlib.model.nv_tree import NvTree
from novxlib.novx.character_data_reader import CharacterDataReader

filePath = sys.argv[1]
dataSet = CharacterDataReader(filePath)
dataSet.novel = Novel(tree=NvTree)
dataSet.read()
for crId in dataSet.novel.characters:
    print(dataSet.novel.characters[crId].title)

