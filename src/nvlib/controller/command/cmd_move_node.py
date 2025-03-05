"""Provide an abstract command base class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.command.command import Command


class CmdMoveNode(Command):

    def __init__(self, model, node, targetNode):
        self._mdl = model
        self._node = node
        self._targetNode = targetNode
        self._prevPos = self._mdl.tree.prev(self._node)
        if not self._prevPos:
            self._prevPos = self._mdl.tree.parent(self._node)

    def execute(self):
        self._mdl.move_node(self._node, self._targetNode)

    def undo(self):
        self._mdl.move_node(self._node, self._prevPos)
