"""Provide a class with getters and factory methods for data model objects.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.basic_element import BasicElement
from nvlib.model.data.chapter import Chapter
from nvlib.model.data.character import Character
from nvlib.model.data.novel import Novel
from nvlib.model.data.nv_tree import NvTree
from nvlib.model.data.plot_line import PlotLine
from nvlib.model.data.plot_point import PlotPoint
from nvlib.model.data.section import Section
from nvlib.model.data.world_element import WorldElement
from nvlib.model.novx.novx_file import NovxFile
from nvlib.model.novx.zipped_novx_file import ZippedNovxFile
from nvlib.nv_globals import HOME_URL


class NovxService:

    def change_word_counter(self, wordCounter):
        """Change the section's strategy class for counting words."""
        Section.wordCounter = wordCounter

    def get_novelibre_home_url(self):
        return HOME_URL

    def get_novx_file_extension(self):
        return NovxFile.EXTENSION

    def get_word_counter(self):
        return Section.wordCounter

    def get_zipped_novx_file_extension(self):
        return ZippedNovxFile.EXTENSION

    def new_basic_element(self, **kwargs):
        return BasicElement(**kwargs)

    def new_chapter(self, **kwargs):
        return Chapter(**kwargs)

    def new_character(self, **kwargs):
        return Character(**kwargs)

    def new_novel(self, **kwargs):
        kwargs['tree'] = kwargs.get('tree', NvTree())
        return Novel(**kwargs)

    def new_novx_file(self, filePath, **kwargs):
        return NovxFile(filePath, **kwargs)

    def new_nv_tree(self, **kwargs):
        return NvTree(**kwargs)

    def new_plot_line(self, **kwargs):
        return PlotLine(**kwargs)

    def new_plot_point(self, **kwargs):
        return PlotPoint(**kwargs)

    def new_section(self, **kwargs):
        return Section(**kwargs)

    def new_world_element(self, **kwargs):
        return WorldElement(**kwargs)

    def new_zipped_novx_file(self, filePath, **kwargs):
        return ZippedNovxFile(filePath, **kwargs)

