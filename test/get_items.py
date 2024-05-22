"""Read items from an XML data file.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import sys
from novxlib.model.novel import Novel
from novxlib.model.nv_tree import NvTree
from novxlib.novx.item_data_reader import ItemDataReader

filePath = sys.argv[1]
dataSet = ItemDataReader(filePath)
dataSet.novel = Novel(tree=NvTree)
dataSet.read()
for itId in dataSet.novel.items:
    print(dataSet.novel.items[itId].title)

