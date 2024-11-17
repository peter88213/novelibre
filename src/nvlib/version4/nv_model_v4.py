"""Provide a version 4 compatibility mixin class for the novelibre model.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class NvModelV4:

    def register_client(self, client):
        """Ensure compatibility with version 4 API."""
        self.add_observer(client)

    def unregister_client(self, client):
        """Ensure compatibility with version 4 API."""
        self.delete_observer(client)

