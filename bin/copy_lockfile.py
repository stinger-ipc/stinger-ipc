#!/usr/bin/env python3
"""
Copy example Cargo.lock to template and convert the simple_ipc package
name and version to Jinja2 template placeholders.
"""

from pathlib import Path
import re


def main():
    # Get paths relative to script location
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    src = root_dir / "example_interfaces/simple/output/rust/Cargo.lock"
    dst = root_dir / "stingeripc/templates/rust/Cargo.lock.jinja2"
    
    if not src.exists():
        print(f"Source lockfile not found: {src}", file=__import__('sys').stderr)
        return 2
    
    # Read the source file
    text = src.read_text()
    lines = text.splitlines(keepends=True)
    
    # Process the file line by line
    output_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a [[package]] line
        if line.strip() == "[[package]]":
            # Start of a package block - look ahead to check the name
            output_lines.append(line)
            i += 1
            
            # Look for the name field in the next few lines
            package_start = len(output_lines) - 1
            found_simple_ipc = False
            
            # Scan ahead to find the name field (usually within next 5 lines)
            for j in range(i, min(i + 10, len(lines))):
                check_line = lines[j]
                name_match = re.match(r'^name\s*=\s*"([^"]+)"', check_line.strip())
                if name_match:
                    if name_match.group(1) == "simple_ipc":
                        found_simple_ipc = True
                    break
            
            # Process the package block
            if found_simple_ipc:
                # Replace name and version for simple_ipc package
                while i < len(lines):
                    line = lines[i]
                    stripped = line.strip()
                    
                    # Check for name field
                    name_match = re.match(r'^name\s*=\s*"[^"]+"', stripped)
                    if name_match:
                        # Replace with template
                        indent = line[:len(line) - len(line.lstrip())]
                        output_lines.append(f'{indent}name = "{{{{stinger.name|snake_case}}}}_ipc"\n')
                        i += 1
                        continue
                    
                    # Check for version field
                    version_match = re.match(r'^version\s*=\s*"[^"]+"', stripped)
                    if version_match:
                        # Replace with template
                        indent = line[:len(line) - len(line.lstrip())]
                        output_lines.append(f'{indent}version = "{{{{stinger.version}}}}"\n')
                        i += 1
                        continue
                    
                    # End of package block
                    if stripped == "" or stripped.startswith("[["):
                        break
                    
                    # Regular line in the package block
                    output_lines.append(line)
                    i += 1
            else:
                # Not the simple_ipc package, copy as-is until end of block
                while i < len(lines):
                    line = lines[i]
                    stripped = line.strip()
                    
                    # End of package block
                    if stripped == "" or stripped.startswith("[["):
                        break
                    
                    output_lines.append(line)
                    i += 1
        else:
            # Not a package block, copy as-is
            output_lines.append(line)
            i += 1
    
    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the output
    dst.write_text(''.join(output_lines))
    print(f"Wrote templated lockfile to {dst}")
    return 0


if __name__ == "__main__":
    exit(main())
