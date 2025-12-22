from pydantic import BaseModel
from .interface_types import *


class TestableInitialPropertyValues(BaseModel):

    read_write_integer: int
    read_write_integer_version: int = 0

    read_only_integer: int
    read_only_integer_version: int = 0

    read_write_optional_integer: Optional[int]
    read_write_optional_integer_version: int = 0

    read_write_two_integers: ReadWriteTwoIntegersProperty
    read_write_two_integers_version: int = 0

    read_only_string: str
    read_only_string_version: int = 0

    read_write_string: str
    read_write_string_version: int = 0

    read_write_optional_string: Optional[str]
    read_write_optional_string_version: int = 0

    read_write_two_strings: ReadWriteTwoStringsProperty
    read_write_two_strings_version: int = 0

    read_write_struct: AllTypes
    read_write_struct_version: int = 0

    read_write_optional_struct: AllTypes
    read_write_optional_struct_version: int = 0

    read_write_two_structs: ReadWriteTwoStructsProperty
    read_write_two_structs_version: int = 0

    read_only_enum: Numbers
    read_only_enum_version: int = 0

    read_write_enum: Numbers
    read_write_enum_version: int = 0

    read_write_optional_enum: Optional[Numbers]
    read_write_optional_enum_version: int = 0

    read_write_two_enums: ReadWriteTwoEnumsProperty
    read_write_two_enums_version: int = 0

    read_write_datetime: datetime
    read_write_datetime_version: int = 0

    read_write_optional_datetime: Optional[datetime]
    read_write_optional_datetime_version: int = 0

    read_write_two_datetimes: ReadWriteTwoDatetimesProperty
    read_write_two_datetimes_version: int = 0

    read_write_duration: timedelta
    read_write_duration_version: int = 0

    read_write_optional_duration: Optional[timedelta]
    read_write_optional_duration_version: int = 0

    read_write_two_durations: ReadWriteTwoDurationsProperty
    read_write_two_durations_version: int = 0

    read_write_binary: bytes
    read_write_binary_version: int = 0

    read_write_optional_binary: bytes
    read_write_optional_binary_version: int = 0

    read_write_two_binaries: ReadWriteTwoBinariesProperty
    read_write_two_binaries_version: int = 0

    read_write_list_of_strings: List[str]
    read_write_list_of_strings_version: int = 0

    read_write_lists: ReadWriteListsProperty
    read_write_lists_version: int = 0
