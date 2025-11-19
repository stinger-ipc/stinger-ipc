#[allow(unused_imports)]
use crate::payloads::*;
use derive_builder::Builder;

#[derive(Clone, Builder, Debug)]
pub struct TestableInitialPropertyValues {
    pub read_write_integer: i32,
    pub read_write_integer_version: u32,

    pub read_only_integer: i32,
    pub read_only_integer_version: u32,

    #[builder(default = "None")]
    pub read_write_optional_integer: Option<i32>,
    pub read_write_optional_integer_version: u32,

    pub read_write_two_integers: ReadWriteTwoIntegersProperty,
    pub read_write_two_integers_version: u32,

    pub read_only_string: String,
    pub read_only_string_version: u32,

    pub read_write_string: String,
    pub read_write_string_version: u32,

    #[builder(default = "None")]
    pub read_write_optional_string: Option<String>,
    pub read_write_optional_string_version: u32,

    pub read_write_two_strings: ReadWriteTwoStringsProperty,
    pub read_write_two_strings_version: u32,

    pub read_write_struct: AllTypes,
    pub read_write_struct_version: u32,

    #[builder(default = "None")]
    pub read_write_optional_struct: Option<AllTypes>,
    pub read_write_optional_struct_version: u32,

    pub read_write_two_structs: ReadWriteTwoStructsProperty,
    pub read_write_two_structs_version: u32,

    pub read_only_enum: Numbers,
    pub read_only_enum_version: u32,

    pub read_write_enum: Numbers,
    pub read_write_enum_version: u32,

    #[builder(default = "None")]
    pub read_write_optional_enum: Option<Numbers>,
    pub read_write_optional_enum_version: u32,

    pub read_write_two_enums: ReadWriteTwoEnumsProperty,
    pub read_write_two_enums_version: u32,

    pub read_write_datetime: chrono::DateTime<chrono::Utc>,
    pub read_write_datetime_version: u32,

    #[builder(default = "None")]
    pub read_write_optional_datetime: Option<chrono::DateTime<chrono::Utc>>,
    pub read_write_optional_datetime_version: u32,

    pub read_write_two_datetimes: ReadWriteTwoDatetimesProperty,
    pub read_write_two_datetimes_version: u32,

    pub read_write_duration: chrono::Duration,
    pub read_write_duration_version: u32,

    #[builder(default = "None")]
    pub read_write_optional_duration: Option<chrono::Duration>,
    pub read_write_optional_duration_version: u32,

    pub read_write_two_durations: ReadWriteTwoDurationsProperty,
    pub read_write_two_durations_version: u32,

    pub read_write_binary: Vec<u8>,
    pub read_write_binary_version: u32,

    #[builder(default = "None")]
    pub read_write_optional_binary: Option<Vec<u8>>,
    pub read_write_optional_binary_version: u32,

    pub read_write_two_binaries: ReadWriteTwoBinariesProperty,
    pub read_write_two_binaries_version: u32,

    pub read_write_list_of_strings: Vec<String>,
    pub read_write_list_of_strings_version: u32,

    pub read_write_lists: ReadWriteListsProperty,
    pub read_write_lists_version: u32,
}
