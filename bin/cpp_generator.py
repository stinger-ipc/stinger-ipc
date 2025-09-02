from jacobsjinjatoo import templator as jj2
import sys
import yaml
import os
from pathlib import Path

from stingeripc import StingerInterface

if __name__ == "__main__":
    inname = sys.argv[1]
    outdir = sys.argv[2]
    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
        "source_files": [],
        "header_files": []
    }

    source_code_dir = os.path.join(outdir, "src")
    if not os.path.exists(source_code_dir):
        os.makedirs(source_code_dir)

    headers_code_dir = os.path.join(outdir, "include")
    if not os.path.exists(headers_code_dir):
        os.makedirs(headers_code_dir)

    examples_code_dir = os.path.join(outdir, "examples")
    if not os.path.exists(examples_code_dir):
        os.makedirs(examples_code_dir)

    template_dir = os.path.join(os.path.dirname(__file__), "../stingeripc", "templates", "cpp")

    output_dir = Path(outdir).resolve()
    t = jj2.CodeTemplator(output_dir=output_dir)
    t.add_template_dir(template_dir)

    headers_template_dir = os.path.join(template_dir, "include")
    for f in os.listdir(headers_template_dir):
        header_code_path = os.path.join("include", f)
        if f.endswith(".jinja2"):
            print(f"GENERATING HEADER: {f}")
            header_dest_path = header_code_path[:-len(".jinja2")]
            params['header_files'].append(header_dest_path)
            t.render_template(header_code_path, header_dest_path, **params)

    src_template_dir = os.path.join(template_dir, "src")
    for f in os.listdir(src_template_dir):
        source_code_path = os.path.join("src", f)
        if f.endswith(".jinja2"):
            print(f"GENERATING SOURCE: {f}")
            source_dest_path = source_code_path[:-len(".jinja2")]
            params['source_files'].append(source_dest_path)
            t.render_template(source_code_path, source_dest_path, **params)

    example_template_dir = os.path.join(template_dir, "examples")
    for f in os.listdir(example_template_dir):
        example_code_path = os.path.join("examples", f)
        if f.endswith(".jinja2"):
            print(f"GENERATING EXAMPLE: {f}")
            example_dest_path = example_code_path[:-len(".jinja2")]
            t.render_template(example_code_path, example_dest_path, **params)

    print(f"GENERATING CmakeLists")
    t.render_template("CMakeLists.txt.jinja2", "CMakeLists.txt", **params)

