
from enum import Enum

class MethodResultCode(Enum):
    SUCCESS = 0
    CLIENT_ERROR = 1
    SERVER_ERROR = 2
    TRANSPORT_ERROR = 3

class StingerMethodException(Exception):
    
    def __init__(self, result_code: MethodResultCode):
        super().__init__()
        self._result_code = result_code

    @property
    def result_code(self) -> MethodResultCode:
        return self._result_code

class SuccessStingerMethodException(StingerMethodException):
    def __init__(self):
        super().__init__(0)

class ClientErrorStingerMethodException(StingerMethodException):
    def __init__(self):
        super().__init__(1)

class ServerErrorStingerMethodException(StingerMethodException):
    def __init__(self):
        super().__init__(2)

class TransportErrorStingerMethodException(StingerMethodException):
    def __init__(self):
        super().__init__(3)
