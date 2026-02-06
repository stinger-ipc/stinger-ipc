from stingeripc.topic_template import topic_template_fill_in, get_topic_arguments, is_valid_topic_template

import unittest


class TestTopicTemplateFillIn(unittest.TestCase):
    def test_full_replacement(self):
        """Test when all template arguments are provided."""
        template = "hello/{name}/world/{place}"
        result = topic_template_fill_in(template, name="Alice", place="Paris")
        self.assertEqual(result, "hello/Alice/world/Paris")

    def test_partial_replacement(self):
        """Test when only some template arguments are provided."""
        template = "hello/{name}/world/{place}"
        result = topic_template_fill_in(template, name="Alice")
        self.assertEqual(result, "hello/Alice/world/{place}")

    def test_no_replacement(self):
        """Test when no template arguments are provided."""
        template = "hello/{name}/world/{place}"
        result = topic_template_fill_in(template)
        self.assertEqual(result, "hello/{name}/world/{place}")

    def test_empty_template(self):
        """Test with an empty template string."""
        result = topic_template_fill_in("")
        self.assertEqual(result, "")

    def test_no_placeholders(self):
        """Test with a template that has no placeholders."""
        template = "hello/world"
        result = topic_template_fill_in(template, name="Alice")
        self.assertEqual(result, "hello/world")

    def test_single_placeholder(self):
        """Test with a single placeholder."""
        template = "{name}"
        result = topic_template_fill_in(template, name="Bob")
        self.assertEqual(result, "Bob")

    def test_multiple_same_placeholder(self):
        """Test with the same placeholder appearing multiple times."""
        template = "{name}/test/{name}"
        result = topic_template_fill_in(template, name="Alice")
        self.assertEqual(result, "Alice/test/Alice")

    def test_partial_with_multiple_same_placeholder(self):
        """Test partial replacement with repeated placeholders."""
        template = "{name}/test/{name}/{place}"
        result = topic_template_fill_in(template, name="Alice")
        self.assertEqual(result, "Alice/test/Alice/{place}")

    def test_format_spec_provided(self):
        """Test with format specification when value is provided."""
        template = "{value:.2f}"
        result = topic_template_fill_in(template, value=3.14159)
        self.assertEqual(result, "3.14")

    def test_format_spec_not_provided(self):
        """Test that format spec is preserved when value is not provided."""
        template = "{value:.2f}"
        result = topic_template_fill_in(template)
        self.assertEqual(result, "{value:.2f}")

    def test_conversion_provided(self):
        """Test with conversion (!s, !r, !a) when value is provided."""
        template = "{name!r}"
        result = topic_template_fill_in(template, name="Alice")
        self.assertEqual(result, "'Alice'")

    def test_conversion_not_provided(self):
        """Test that conversion is preserved when value is not provided."""
        template = "{name!r}"
        result = topic_template_fill_in(template)
        self.assertEqual(result, "{name!r}")

    def test_conversion_and_format_spec(self):
        """Test with both conversion and format spec."""
        template = "{value!s:>10}"
        result = topic_template_fill_in(template, value=42)
        self.assertEqual(result, "        42")

    def test_conversion_and_format_spec_not_provided(self):
        """Test that both conversion and format spec are preserved."""
        template = "{value!s:>10}"
        result = topic_template_fill_in(template)
        self.assertEqual(result, "{value!s:>10}")

    def test_mixed_provided_and_not_provided(self):
        """Test complex case with multiple placeholders, some provided, some not."""
        template = "{service}/{version}/api/{endpoint}/{id}"
        result = topic_template_fill_in(template, service="users", endpoint="profile")
        self.assertEqual(result, "users/{version}/api/profile/{id}")

    def test_numeric_values(self):
        """Test with numeric values."""
        template = "device/{device_id}/sensor/{sensor_id}"
        result = topic_template_fill_in(template, device_id=123, sensor_id=456)
        self.assertEqual(result, "device/123/sensor/456")

    def test_extra_kwargs_ignored(self):
        """Test that extra kwargs that don't match placeholders are ignored."""
        template = "{name}"
        result = topic_template_fill_in(template, name="Alice", extra="ignored")
        self.assertEqual(result, "Alice")


class TestGetTopicArguments(unittest.TestCase):
    def test_single_argument(self):
        """Test extracting a single argument."""
        template = "{name}"
        result = get_topic_arguments(template)
        self.assertEqual(result, ["name"])

    def test_multiple_arguments(self):
        """Test extracting multiple arguments in order."""
        template = "{service}/{version}/api/{endpoint}/{id}"
        result = get_topic_arguments(template)
        self.assertEqual(result, ["service", "version", "endpoint", "id"])

    def test_no_arguments(self):
        """Test template with no arguments."""
        template = "hello/world"
        result = get_topic_arguments(template)
        self.assertEqual(result, [])

    def test_empty_template(self):
        """Test with empty template."""
        template = ""
        result = get_topic_arguments(template)
        self.assertEqual(result, [])

    def test_repeated_arguments(self):
        """Test that repeated arguments only appear once."""
        template = "{name}/test/{name}/{place}"
        result = get_topic_arguments(template)
        self.assertEqual(result, ["name", "place"])

    def test_arguments_with_format_spec(self):
        """Test that arguments with format specs are extracted correctly."""
        template = "{value:.2f}/{count:>5}"
        result = get_topic_arguments(template)
        self.assertEqual(result, ["value", "count"])

    def test_arguments_with_conversion(self):
        """Test that arguments with conversions are extracted correctly."""
        template = "{name!r}/{value!s}"
        result = get_topic_arguments(template)
        self.assertEqual(result, ["name", "value"])

    def test_complex_template(self):
        """Test with a complex template."""
        template = "device/{device_id}/sensor/{sensor_id}/data/{timestamp}"
        result = get_topic_arguments(template)
        self.assertEqual(result, ["device_id", "sensor_id", "timestamp"])


class TestIsValidTopicTemplate(unittest.TestCase):
    def test_valid_builtin_arguments(self):
        """Test template with only builtin arguments is valid."""
        template = "{interface_name}/signal/{signal_name}"
        result = is_valid_topic_template(template, [])
        self.assertTrue(result)

    def test_valid_additional_arguments(self):
        """Test template with additional arguments is valid."""
        template = "{interface_name}/custom/{custom_arg}"
        result = is_valid_topic_template(template, ["custom_arg"])
        self.assertTrue(result)

    def test_valid_mixed_arguments(self):
        """Test template with both builtin and additional arguments."""
        template = "{interface_name}/{service_id}/data/{sensor_id}"
        result = is_valid_topic_template(template, ["sensor_id"])
        self.assertTrue(result)

    def test_invalid_unknown_argument(self):
        """Test template with unknown argument is invalid."""
        template = "{interface_name}/test/{unknown_arg}"
        result = is_valid_topic_template(template, [])
        self.assertFalse(result)

    def test_invalid_duplicate_argument(self):
        """Test template with duplicate argument is invalid."""
        template = "{interface_name}/test/{interface_name}"
        result = is_valid_topic_template(template, [])
        self.assertFalse(result)

    def test_invalid_duplicate_additional_argument(self):
        """Test template with duplicate additional argument is invalid."""
        template = "{custom_arg}/test/{custom_arg}"
        result = is_valid_topic_template(template, ["custom_arg"])
        self.assertFalse(result)

    def test_valid_empty_template(self):
        """Test empty template is valid."""
        template = ""
        result = is_valid_topic_template(template, [])
        self.assertTrue(result)

    def test_valid_no_arguments(self):
        """Test template with no arguments is valid."""
        template = "static/topic/path"
        result = is_valid_topic_template(template, [])
        self.assertTrue(result)

    def test_valid_all_builtin_arguments(self):
        """Test template using all builtin arguments."""
        template = "{interface_name}/{service_id}/{signal_name}/{property_name}/{method_name}/{client_id}"
        result = is_valid_topic_template(template, [])
        self.assertTrue(result)

    def test_invalid_partial_match(self):
        """Test that partial matching doesn't work - argument must be exact."""
        template = "{interface_name_extra}"
        result = is_valid_topic_template(template, [])
        self.assertFalse(result)

    def test_valid_with_format_spec(self):
        """Test that format specs don't affect validation."""
        template = "{interface_name}/{service_id:.5}"
        result = is_valid_topic_template(template, [])
        self.assertTrue(result)

    def test_valid_with_conversion(self):
        """Test that conversions don't affect validation."""
        template = "{interface_name!r}/{signal_name!s}"
        result = is_valid_topic_template(template, [])
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
