import sys
import subprocess
from ruamel.yaml import YAML
from packaging.version import Version, InvalidVersion
import io
import logging

logger = logging.getLogger("CompatibilityChecks")
logging.basicConfig(level=logging.DEBUG)

def get_yaml_content_from_commit(commit_ref, file_path):
    """
    Fetches the content of a file from a specific git commit.
    Returns the content as a string, or None if the file doesn't exist
    in that commit.
    """
    try:
        # Use git show to get the file content without checking it out
        # This is a safe way to get the content from the previous commit
        result = subprocess.run(
            ['git', 'show', f'{commit_ref}:{file_path}'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        # File doesn't exist in the specified commit
        return None

def convert_payload_list(payload):
    if not isinstance(payload, list):
        return payload
    ret_dict = dict()
    for arg in payload:
        ret_dict[arg["name"]] = arg
    return ret_dict

def compare_payloads(cur_arr, prev_arr, allow_new_properties=True) -> tuple[bool, str]:
    cur = convert_payload_list(cur_arr)
    prev = convert_payload_list(prev_arr)
    if prev and (prev_compat := prev.get("compatibility")):
        prev_ver = Version(prev_compat)
        if cur:
            if cur_compat := cur.get("compatibility"):
                cur_ver = Version(cur_compat)
                if cur == prev:
                    return True, "Both definitions are the same, including version"
                elif cur_ver < prev_ver:
                    return False, f"The current definition has an earlier version {cur_ver} than the previous definition {prev_ver}."
                elif cur_ver > prev_ver:
                    keys_in_prev_that_no_longer_exist = set(prev.keys()) - set(cur.keys())
                    if len(keys_in_prev_that_no_longer_exist) > 0:
                        return False, f"Newer definition version {cur_ver} does not have properties [{keys_in_prev_that_no_longer_exist}] that previously existed."
                    else:
                        new_keys_in_cur = set(cur.keys()) - set(prev.keys())
                        if len(keys_in_prev_that_no_longer_exist) == 0 and len(new_keys_in_cur) == 0:
                            return True, f"Properties in newer version {cur_ver} are the same as previous properties"
                        elif allow_new_properties:
                            return True, f"New version {cur_ver} provides new properties as allowed"
                        else:
                            return False, f"New version {cur_ver} provides new properties which is not allowed"
                else:
                    return False, "Was not able to compare definitions."
            else:
                return False, f"A previous definition exists at version {prev_ver}, but the current definition does not provide compatibility."
        else:
            return False, f"A previous definition exists at version {prev_ver}, but not a current one"
    else:
        return True, "No previous definition exists."

def main(yaml_file: str):
    """
    Main function to compare the YAML file.
    """

    # Get the content of the current version of the YAML file
    try:
        with open(yaml_file, 'r') as f:
            current_yaml_content = f.read()
    except FileNotFoundError:
        print(f"Error: YAML file '{yaml_file}' not found.")
        sys.exit(1)

    # Get the content of the previous version of the YAML file
    previous_yaml_content = get_yaml_content_from_commit('HEAD^', yaml_file)

    if not previous_yaml_content:
        print(f"Info: '{yaml_file}' did not exist in the previous commit. No version check needed.")
        sys.exit(0)

    # Parse both YAML versions
    yaml = YAML(typ='safe')
    current_data = yaml.load(io.StringIO(current_yaml_content))
    previous_data = yaml.load(io.StringIO(previous_yaml_content))

    # Check for the 'signals' key
    if 'signals' not in current_data or 'signals' not in previous_data:
        print("Error: 'signals' key not found in one of the YAML files.")
        sys.exit(1)

    exit_code = 1

    # Perform the comparison

    for signal_name, current_signal in current_data['signals'].items():
        # Check if the signal existed in the previous version
        previous_signal = previous_data['signals'].get(signal_name, dict())
        cur_payload = current_signal.get('payload', dict())
        prev_payload = previous_signal.get('payload', dict())
        result, comment = compare_payloads(cur_payload, prev_payload)
        if result:
            logger.info("Signal %s OK: %s", signal_name, comment)
        else:
            logger.error("Signal %s ERR: %s", signal_name, comment)
            exit_code = 1

    print("All checks passed.")
    sys.exit(exit_code)

if __name__ == '__main__':
    main(sys.argv[1])
