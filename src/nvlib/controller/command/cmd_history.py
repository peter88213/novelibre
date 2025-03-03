"""Provide a command stack for the novelibre controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class CmdHistory(list):

    def execute(self, command):
        self.append(command)
        command.execute()

    def undo(self):
        self.pop().undo()

