from typing import Optional
from enum import IntEnum


class MethodReturnCode(IntEnum):
    SUCCESS = 0
    CLIENT_ERROR = 1
    SERVER_ERROR = 2
    TRANSPORT_ERROR = 3
    PAYLOAD_ERROR = 4
    TIMEOUT = 5
    UNKNOWN_ERROR = 6
    NOT_IMPLEMENTED = 7


class StingerMethodException(Exception):

    def __init__(self, result_code: MethodReturnCode, message: str):
        super().__init__(message)
        self._result_code = result_code

    @property
    def result_code(self) -> MethodReturnCode:
        return self._result_code


class SuccessStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.SUCCESS, message)


class ClientErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.CLIENT_ERROR, message)


class ServerErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.SERVER_ERROR, message)


class TransportErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.TRANSPORT_ERROR, message)


class PayloadErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.PAYLOAD_ERROR, message)


class TimeoutStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.TIMEOUT, message)


class UnknownErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.UNKNOWN_ERROR, message)


class NotImplementedStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.NOT_IMPLEMENTED, message)


def stinger_exception_factory(result_code: int, message: Optional[str] = None):
    exc_classes = {
        0: SuccessStingerMethodException,
        1: ClientErrorStingerMethodException,
        2: ServerErrorStingerMethodException,
        3: TransportErrorStingerMethodException,
        4: PayloadErrorStingerMethodException,
        5: TimeoutStingerMethodException,
        6: UnknownErrorStingerMethodException,
        7: NotImplementedStingerMethodException,
    }
    exc_class = exc_classes[result_code]
    return exc_class(message or "")
