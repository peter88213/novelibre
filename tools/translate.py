"""Create a German translation. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import build

ab = build.ApplicationBuilder(build.VERSION)
ab.build_script()
ab.build_translation()
ab.clean_up()

