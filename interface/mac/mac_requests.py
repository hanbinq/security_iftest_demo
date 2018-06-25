import requests
try:
    from .mac import *
except SystemError:
    from mac import *


class MACRequests:

    def __init__(self):
        self.timestamp = get_timstamp()


