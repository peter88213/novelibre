"""Provide a class that provides novxlib features for plugins.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novxlib.config.configuration import Configuration
from novxlib.file.file import File
from novxlib.model.chapter import Chapter
from novxlib.model.character import Character
from novxlib.model.id_generator import create_id
from novxlib.model.novel import Novel
from novxlib.model.nv_tree import NvTree
from novxlib.model.plot_line import PlotLine
from novxlib.model.section import Section
from novxlib.model.world_element import WorldElement
from novxlib.novx.novx_file import NovxFile
from novxlib.novx_globals import CHAPTER_PREFIX
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import Error
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import PLOT_LINE_PREFIX
from novxlib.novx_globals import PL_ROOT
from novxlib.novx_globals import SECTION_PREFIX


class NvFacade:

    def get_novx_file_extension(self):
        return NovxFile.EXTENSION

    def make_chapter(self, **kwargs):
        return Chapter(**kwargs)

    def make_character(self, **kwargs):
        return Character(**kwargs)

    def make_id(self, elements, prefix=''):
        return create_id(elements, prefix=prefix)

    def make_plot_line(self, **kwargs):
        return PlotLine(**kwargs)

    def make_novel(self, **kwargs):
        kwargs['tree'] = kwargs.get('tree', NvTree())
        return Novel(self, **kwargs)

    def make_nv_tree(self, **kwargs):
        return NvTree(self, **kwargs)

    def make_section(self, **kwargs):
        return Section(**kwargs)

    def make_configuration(self, **kwargs):
        return Configuration(**kwargs)

    def make_world_element(self, **kwargs):
        return WorldElement(**kwargs)

    def make_novx_file(self, filePath, **kwargs):
        return NovxFile(filePath, **kwargs)

