"""Provide a class for a history list for the novelibre tree. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class HistoryList:
    """A browsing history of nodes in a Treeview."""

    def __init__(self):
        self._historyList = []
        self._pointer = None
        self._lock = False

    def append_node(self, node):
        """Append a node to the browsing history list, if not locked.
        
        Set the browsing pointer to the appended node.
        """
        if not self._lock:
            try:
                del self._historyList[self._pointer + 1:]
            except:
                pass
            if self._pointer is None or self._historyList[self._pointer] != node:
                self._historyList.append(node)
                self._pointer = len(self._historyList) - 1
        self._lock = False
        # print(self._historyList)

    def go_back(self):
        """Return a node back in the tree browsing history."""
        if self._pointer is None:
            return None

        if self._pointer > 0:
            self._pointer -= 1
        return self._historyList[self._pointer]

    def go_forward(self):
        """Return a node back in the tree browsing history."""
        if self._pointer is None:
            return None

        if self._pointer + 1 < len(self._historyList):
            self._pointer += 1
        return self._historyList[self._pointer]

    def lock(self):
        """Prevent the history list from being extended.
        
        This may be necessary when going back or forward.
        """
        self._lock = True

    def reset(self):
        """Clear the browsing history."""
        self._historyList = []
        self._pointer = None
        self._lock = False

