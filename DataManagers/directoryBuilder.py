import logging
from pathlib import Path

class DirectoryBuilder:
    def __init__(self, root_dir):
        self._root_dir = Path(root_dir)