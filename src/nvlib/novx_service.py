"""Provide a class with getters and factory methods for novxlib model objects.

Copyright (c) 2024 Peter Triesberger
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


class NovxService:
    """Getters and factory methods for model elements."""

    def get_novx_file_extension(self):
        return NovxFile.EXTENSION

    def make_basic_element(self, **kwargs):
        return BasicElement(**kwargs)

    def make_chapter(self, **kwargs):
        return Chapter(**kwargs)

    def make_character(self, **kwargs):
        return Character(**kwargs)

    def make_novel(self, **kwargs):
        kwargs['tree'] = kwargs.get('tree', NvTree())
        return Novel(**kwargs)

    def make_nv_tree(self, **kwargs):
        return NvTree(**kwargs)

    def make_plot_line(self, **kwargs):
        return PlotLine(**kwargs)

    def make_plot_point(self, **kwargs):
        return PlotPoint(**kwargs)

    def make_section(self, **kwargs):
        return Section(**kwargs)

    def make_world_element(self, **kwargs):
        return WorldElement(**kwargs)

    def make_novx_file(self, filePath, **kwargs):
        return NovxFile(filePath, **kwargs)

