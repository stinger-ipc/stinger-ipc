from typing import Optional
from enum import IntEnum


class MethodReturnCode(IntEnum):
    SUCCESS = 0
    CLIENT_ERROR = 1
    SERVER_ERROR = 2
    TRANSPORT_ERROR = 3
    PAYLOAD_ERROR = 4
    SERIALIZATION_ERROR = 5
    DESERIALIZATION_ERROR = 6
    UNAUTHORIZED = 7
    TIMEOUT = 8
    OUT_OF_SYNC = 9
    UNKNOWN_ERROR = 10
    NOT_IMPLEMENTED = 11
    SERVICE_UNAVAILABLE = 12


class StingerMethodException(Exception):

    def __init__(self, return_code: MethodReturnCode, message: str):
        super().__init__(message)
        self._return_code = return_code

    @property
    def return_code(self) -> MethodReturnCode:
        return self._return_code


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


class SerializationErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.SERIALIZATION_ERROR, message)


class DeserializationErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.DESERIALIZATION_ERROR, message)


class UnauthorizedStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.UNAUTHORIZED, message)


class TimeoutStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.TIMEOUT, message)


class OutOfSyncStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.OUT_OF_SYNC, message)


class UnknownErrorStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.UNKNOWN_ERROR, message)


class NotImplementedStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.NOT_IMPLEMENTED, message)


class ServiceUnavailableStingerMethodException(StingerMethodException):
    def __init__(self, message: str):
        super().__init__(MethodReturnCode.SERVICE_UNAVAILABLE, message)


def stinger_exception_factory(return_code: int, message: Optional[str] = None):
    exc_classes = {
        0: SuccessStingerMethodException,
        1: ClientErrorStingerMethodException,
        2: ServerErrorStingerMethodException,
        3: TransportErrorStingerMethodException,
        4: PayloadErrorStingerMethodException,
        5: SerializationErrorStingerMethodException,
        6: DeserializationErrorStingerMethodException,
        7: UnauthorizedStingerMethodException,
        8: TimeoutStingerMethodException,
        9: OutOfSyncStingerMethodException,
        10: UnknownErrorStingerMethodException,
        11: NotImplementedStingerMethodException,
        12: ServiceUnavailableStingerMethodException,
    }
    exc_class = exc_classes[return_code]
    return exc_class(message or "")
