
from typing import Optional
from enum import Enum

class MethodResultCode(Enum):
    SUCCESS = 0
    CLIENT_ERROR = 1
    SERVER_ERROR = 2
    TRANSPORT_ERROR = 3
    PAYLOAD_ERROR = 4

class StingerMethodException(Exception):
    
    def __init__(self, result_code: MethodResultCode, message: str):
        super().__init__(message)
        self._result_code = result_code

    @property
    def result_code(self) -> MethodResultCode:
        return self._result_code

class SuccessStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(0, message)

class ClientErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(1, message)

class ServerErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(2, message)

class TransportErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(3, message)

class PayloadErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(4, message)


def stinger_exception_factory(result_code: int, message: Optional[str]=None):
    exc_classes = { 
        0: SuccessStingerMethodException,
        
        1: ClientErrorStingerMethodException,
        
        2: ServerErrorStingerMethodException,
        
        3: TransportErrorStingerMethodException,
        
        4: PayloadErrorStingerMethodException,
        
    }
    exc_class = exc_classes[result_code]
    return exc_class(message or "")