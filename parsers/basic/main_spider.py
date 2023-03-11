from typing import Optional
from parsers.basic.headers_preparator import HeadersPreparatorInterface


class Spider:
    def __init__(self, headers_behavior: Optional[HeadersPreparatorInterface] = None):
        if headers_behavior:
            self._headers = headers_behavior.get_headers()
        else:
            self._headers = None

    def get_result(self):
        pass
