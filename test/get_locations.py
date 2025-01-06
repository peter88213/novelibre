"""Read locations from an XML data file.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import sys
from nvlib.model.data.novel import Novel
from nvlib.model.data.nv_tree import NvTree
from nvlib.model.novx.location_data_reader import LocationDataReader

filePath = sys.argv[1]
dataSet = LocationDataReader(filePath)
dataSet.novel = Novel(tree=NvTree)
dataSet.read()
for lcId in dataSet.novel.locations:
    print(dataSet.novel.locations[lcId].title)

