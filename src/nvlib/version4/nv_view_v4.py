"""Provide a version 4 compatibility mixin class for the novelibre view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class NvView4:

    def register_view(self, client):
        """Ensure compatibility with version 4 API."""
        self.register_client(client)
        self._mdl.add_observer(client)

    def unregister_view(self, client):
        """Ensure compatibility with version 4 API."""
        self.unregister_client(client)
        self._mdl.delete_observer(client)

