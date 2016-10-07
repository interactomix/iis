import logging

import multiprocessing


class LockingFileHandler(logging.FileHandler):
    """
    Allow concurrent logging to the same file from mutliple processes.

    """
    def __init__(self, *args, **kwargs) -> None:
        self._lock = multiprocessing.Lock()
        super().__init__(*args, **kwargs)

    def emit(self, *args, **kwargs):
        with self._lock:
            super().emit(*args, **kwargs)
