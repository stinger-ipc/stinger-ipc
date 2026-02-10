

from string import Formatter
from typing import List


BUILTIN_ARGUMENTS = {"interface_name", "service_id", "signal_name", "property_name", "method_name", "client_id"}

def is_valid_topic_template(template: str, additional_arguments: List[str]) -> bool:
    """Check if a topic template is valid.
    
    A template is valid if:
    1. All arguments are from BUILTIN_ARGUMENTS or additional_arguments
    2. No argument appears more than once in the template
    
    Args:
        template: The template string to validate.
        additional_arguments: List of additional allowed argument names.
        
    Returns:
        True if the template is valid, False otherwise.
    """
    formatter = Formatter()
    allowed_arguments = BUILTIN_ARGUMENTS | set(additional_arguments)
    seen_arguments = set()
    
    for _, field_name, _, _ in formatter.parse(template):
        if field_name is not None:
            # Check if argument already appeared
            if field_name in seen_arguments:
                return False
            
            # Check if argument is allowed
            if field_name not in allowed_arguments:
                return False
            
            seen_arguments.add(field_name)
    
    return True


def topic_template_fill_in(template: str, **kwargs) -> str:
    """Fill in a topic template with the provided keyword arguments.
    
    If only some template arguments are provided, they will be replaced
    while others remain as template placeholders.
    """
    formatter = Formatter()
    result = []
    for literal_text, field_name, format_spec, conversion in formatter.parse(template):
        result.append(literal_text)
        if field_name is not None:
            if field_name in kwargs:
                value = kwargs[field_name]
                if conversion:
                    value = formatter.convert_field(value, conversion)
                if format_spec:
                    value = format(value, format_spec)
                result.append(str(value))
            else:
                # Keep the placeholder for unprovided arguments
                placeholder = '{' + field_name
                if conversion:
                    placeholder += '!' + conversion
                if format_spec:
                    placeholder += ':' + format_spec
                placeholder += '}'
                result.append(placeholder)
    return ''.join(result)


def get_topic_arguments(template: str) -> list[str]:
    """Get a list of argument names in the order they appear in the template.
    
    Args:
        template: The template string to extract arguments from.
        
    Returns:
        A list of argument names in the order they appear.
    """
    formatter = Formatter()
    arguments = []
    for _, field_name, _, _ in formatter.parse(template):
        if field_name is not None and field_name not in arguments:
            arguments.append(field_name)
    return arguments


def get_argument_position(template: str, argument: str) -> int | None:
    """Get the position of an argument in the topic when split by '/'.
    
    Args:
        template: The template string to search.
        argument: The argument name to find.
        
    Returns:
        The index of the segment containing the argument when the topic is split by '/',
        or None if the argument is not in the template.
    """
    formatter = Formatter()
    segment_index = 0
    
    for literal_text, field_name, _, _ in formatter.parse(template):
        # Count slashes in literal text before this field
        if literal_text:
            segment_index += literal_text.count('/')
        
        if field_name is not None and field_name == argument:
            return segment_index
    
    return None

