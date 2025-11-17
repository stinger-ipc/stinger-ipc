"""
For both functions, the interface provided is the raw dictionary parsed from the Stinger YAML file, as specified in `schema/schema.yaml`.

"""
import semantic_version
from typing import Dict, Any, Set
from copy import deepcopy


def _collect_used_types(args: list[Dict[str, Any]], used_enums: Set[str], used_structs: Set[str]) -> None:
    """Recursively collect enum and struct names used in argument lists."""
    for arg in args:
        arg_type = arg.get("type")
        if arg_type == "enum":
            used_enums.add(arg["enumName"])
        elif arg_type == "struct":
            used_structs.add(arg["structName"])
        elif arg_type == "array":
            # Check the item type of arrays
            item_type = arg.get("itemType", {})
            if isinstance(item_type, dict):
                _collect_used_types([item_type], used_enums, used_structs)


def _collect_struct_dependencies(struct_spec: Dict[str, Any], used_enums: Set[str], used_structs: Set[str]) -> None:
    """Recursively collect enums and structs used by a struct's members."""
    members = struct_spec.get("members", [])
    for member in members:
        member_type = member.get("type")
        if member_type == "enum":
            used_enums.add(member["enumName"])
        elif member_type == "struct":
            struct_name = member["structName"]
            # Avoid infinite recursion if structs reference each other
            if struct_name not in used_structs:
                used_structs.add(struct_name)
        elif member_type == "array":
            item_type = member.get("itemType", {})
            if isinstance(item_type, dict):
                _collect_used_types([item_type], used_enums, used_structs)


def filter_by_consumer(interface: Dict[str, Any], consumer_name: str) -> Dict[str, Any]:
    """
    Filter a StingerInterface to only include methods, properties, signals, and events that specify the given consumer.

    Args:
        interface: The original StingerInterface.
        consumer_name: The name of the consumer to filter by.
        
    Returns:
        A new StingerInterface containing only the elements that are required for a client interface for the given consumer.

    Methodology:
        - Methods are included if they have the consumer in their consumers list.
        - Properties are included if they have the consumer in their consumers list.
        - Signals are included if they have the consumer in their consumers list

    Enums are included if they are used by any of the included methods, properties, signals, or by any structs used by those elements.

    Enums are included if they are used by any of the included methods, properties, signals, or by any structs used by those elements.
    """
    # Create a deep copy to avoid modifying the original
    filtered = deepcopy(interface)
    
    # Track which enums and structs are used
    used_enums: Set[str] = set()
    used_structs: Set[str] = set()
    
    # Filter signals
    if "signals" in filtered:
        filtered_signals = {}
        for signal_name, signal_spec in filtered["signals"].items():
            consumers = signal_spec.get("consumers", [])
            # If no consumers specified, include for all consumers
            # If consumers specified, only include if consumer_name is in the list
            if consumer_name in consumers:
                filtered_signals[signal_name] = signal_spec
                # Collect types used in payload
                payload = signal_spec.get("payload", [])
                _collect_used_types(payload, used_enums, used_structs)
        filtered["signals"] = filtered_signals
    
    # Filter properties
    if "properties" in filtered:
        filtered_properties = {}
        for prop_name, prop_spec in filtered["properties"].items():
            consumers = prop_spec.get("consumers", [])
            if consumer_name in consumers:
                filtered_properties[prop_name] = prop_spec
                # Collect types used in values
                values = prop_spec.get("values", [])
                _collect_used_types(values, used_enums, used_structs)
        filtered["properties"] = filtered_properties
    
    # Filter methods
    if "methods" in filtered:
        filtered_methods = {}
        for method_name, method_spec in filtered["methods"].items():
            consumers = method_spec.get("consumers", [])
            if consumer_name in consumers:
                filtered_methods[method_name] = method_spec
                # Collect types used in arguments
                arguments = method_spec.get("arguments", [])
                _collect_used_types(arguments, used_enums, used_structs)
                # Collect types used in return values
                return_values = method_spec.get("returnValues", [])
                _collect_used_types(return_values, used_enums, used_structs)
        filtered["methods"] = filtered_methods
    
    # Now collect dependencies from used structs
    if "structures" in interface:
        # Keep iterating until no new structs are added
        prev_struct_count = -1
        while len(used_structs) != prev_struct_count:
            prev_struct_count = len(used_structs)
            for struct_name in list(used_structs):
                if struct_name in interface["structures"]:
                    _collect_struct_dependencies(
                        interface["structures"][struct_name], 
                        used_enums, 
                        used_structs
                    )
    
    # Filter enums to only include used ones
    if "enums" in filtered:
        filtered_enums = {
            enum_name: enum_spec
            for enum_name, enum_spec in filtered["enums"].items()
            if enum_name in used_enums
        }
        filtered["enums"] = filtered_enums
    
    # Filter structs to only include used ones
    if "structures" in filtered:
        filtered_structs = {
            struct_name: struct_spec
            for struct_name, struct_spec in filtered["structures"].items()
            if struct_name in used_structs
        }
        filtered["structures"] = filtered_structs
    
    return filtered

def check_version_consistency(interface: Dict[str, Any]) -> None:
    """
    Anywhere there is a structVersion or enumVersion specified in an argument list, make sure that there is a version specified on the corresponding struct or enum.
    Also make sure the two versions are compatible, which means the major and minor versions must match.

    Raises:
        ValueError: If any method, property, signal, or event specifies consumers but does not specify a version.
    """
    def check_args(args: list[Dict[str, Any]], component_name: str, component_type: str) -> None:
        """Check version consistency for a list of arguments."""
        for arg in args:
            arg_type = arg.get("type")
            
            # Check enum version consistency
            if arg_type == "enum":
                enum_name = arg.get("enumName")
                enum_version_in_arg = arg.get("enumVersion")
                
                if enum_version_in_arg:
                    # Get the enum definition
                    if "enums" not in interface or enum_name not in interface["enums"]:
                        raise ValueError(
                            f"{component_type} '{component_name}' references enum '{enum_name}' "
                            f"which is not defined in the interface"
                        )
                    
                    enum_spec = interface["enums"][enum_name]
                    enum_version_in_def = enum_spec.get("version")
                    
                    if not enum_version_in_def:
                        raise ValueError(
                            f"{component_type} '{component_name}' specifies enumVersion '{enum_version_in_arg}' "
                            f"for enum '{enum_name}', but the enum definition does not have a version"
                        )
                    
                    # Check semantic version compatibility (major.minor must match)
                    arg_ver = semantic_version.Version(enum_version_in_arg)
                    def_ver = semantic_version.Version(enum_version_in_def)
                    
                    if arg_ver.major != def_ver.major or arg_ver.minor != def_ver.minor:
                        raise ValueError(
                            f"{component_type} '{component_name}' requires enum '{enum_name}' "
                            f"version {enum_version_in_arg} (major.minor: {arg_ver.major}.{arg_ver.minor}), "
                            f"but the enum is defined with version {enum_version_in_def} "
                            f"(major.minor: {def_ver.major}.{def_ver.minor})"
                        )
            
            # Check struct version consistency
            elif arg_type == "struct":
                struct_name = arg.get("structName")
                struct_version_in_arg = arg.get("structVersion")
                
                if struct_version_in_arg:
                    # Get the struct definition
                    if "structures" not in interface or struct_name not in interface["structures"]:
                        raise ValueError(
                            f"{component_type} '{component_name}' references struct '{struct_name}' "
                            f"which is not defined in the interface"
                        )
                    
                    struct_spec = interface["structures"][struct_name]
                    struct_version_in_def = struct_spec.get("version")
                    
                    if not struct_version_in_def:
                        raise ValueError(
                            f"{component_type} '{component_name}' specifies structVersion '{struct_version_in_arg}' "
                            f"for struct '{struct_name}', but the struct definition does not have a version"
                        )
                    
                    # Check semantic version compatibility (major.minor must match)
                    arg_ver = semantic_version.Version(struct_version_in_arg)
                    def_ver = semantic_version.Version(struct_version_in_def)
                    
                    if arg_ver.major != def_ver.major or arg_ver.minor != def_ver.minor:
                        raise ValueError(
                            f"{component_type} '{component_name}' requires struct '{struct_name}' "
                            f"version {struct_version_in_arg} (major.minor: {arg_ver.major}.{arg_ver.minor}), "
                            f"but the struct is defined with version {struct_version_in_def} "
                            f"(major.minor: {def_ver.major}.{def_ver.minor})"
                        )
            
            # Recursively check array item types
            elif arg_type == "array":
                item_type = arg.get("itemType")
                if isinstance(item_type, dict):
                    check_args([item_type], component_name, component_type)
    
    # Check signals
    if "signals" in interface:
        for signal_name, signal_spec in interface["signals"].items():
            # Check if consumers specified but version is missing
            if signal_spec.get("consumers") and not signal_spec.get("version"):
                raise ValueError(
                    f"Signal '{signal_name}' specifies consumers but does not specify a version"
                )
            
            # Check payload arguments
            payload = signal_spec.get("payload", [])
            check_args(payload, signal_name, "Signal")
    
    # Check properties
    if "properties" in interface:
        for prop_name, prop_spec in interface["properties"].items():
            # Check if consumers specified but version is missing
            if prop_spec.get("consumers") and not prop_spec.get("version"):
                raise ValueError(
                    f"Property '{prop_name}' specifies consumers but does not specify a version"
                )
            
            # Check values arguments
            values = prop_spec.get("values", [])
            check_args(values, prop_name, "Property")
    
    # Check methods
    if "methods" in interface:
        for method_name, method_spec in interface["methods"].items():
            # Check if consumers specified but version is missing
            if method_spec.get("consumers") and not method_spec.get("version"):
                raise ValueError(
                    f"Method '{method_name}' specifies consumers but does not specify a version"
                )
            
            # Check arguments
            arguments = method_spec.get("arguments", [])
            check_args(arguments, method_name, "Method")
            
            # Check return values
            return_values = method_spec.get("returnValues", [])
            check_args(return_values, method_name, "Method")
    
    # Check struct members recursively
    if "structures" in interface:
        for struct_name, struct_spec in interface["structures"].items():
            members = struct_spec.get("members", [])
            check_args(members, struct_name, "Struct")
