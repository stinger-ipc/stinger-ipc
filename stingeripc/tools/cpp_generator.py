from jacobsjinjatoo import templator as jj2
import os
import yaml
import typer
from typing_extensions import Annotated
from pathlib import Path
from rich import print

from stingeripc import StingerInterface
from typing import Any


def main(
    inname: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)],
    outdir: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, readable=True)],
):
    """Generate C++ output for a Stinger interface."""

    with inname.open(mode="r") as f:
        stinger = StingerInterface.from_yaml(f, placeholder="%1%")

    params: dict[str, Any] = {
        "stinger": stinger,
        "client_source_files": [],
        "server_source_files": [],
        "client_header_files": [],
        "server_header_files": [],
    }

    if outdir.is_file():
        raise RuntimeError("Output directory is a file!")

    if not outdir.is_dir():
        outdir.mkdir(parents=True)

    source_code_dir = outdir / "src"
    source_code_dir.mkdir(parents=True, exist_ok=True)

    headers_code_dir = outdir / "include"
    headers_code_dir.mkdir(parents=True, exist_ok=True)

    examples_code_dir = outdir / "examples"
    examples_code_dir.mkdir(parents=True, exist_ok=True)

    this_file = Path(__file__)
    # The templates live under the package `stingeripc/templates/cpp` next to `tools`.
    # compute that from the tools directory: tools -> parent (stingeripc) -> templates/cpp
    template_dir = (this_file.parent / ".." / "templates" / "cpp").resolve()

    if not template_dir.is_dir():
        raise RuntimeError(f"C++ template directory not found: {template_dir}")

    output_dir = outdir.resolve()
    t = jj2.CodeTemplator(output_dir=output_dir)
    t.add_template_dir(template_dir)

    headers_template_dir = template_dir / "include"
    for fname in os.listdir(headers_template_dir):
        header_code_path = Path("include") / fname
        if fname.endswith(".jinja2"):
            print(f"GENERATING HEADER: {fname}")
            header_dest_path = str(header_code_path)[:-len(".jinja2")]
            if "server" not in header_dest_path:
                params["client_header_files"].append(header_dest_path)
            if "client" not in header_dest_path:
                params["server_header_files"].append(header_dest_path)
            t.render_template(header_code_path, header_dest_path, **params)

    src_template_dir = template_dir / "src"
    for fname in os.listdir(src_template_dir):
        source_code_path = Path("src") / fname
        if fname.endswith(".jinja2"):
            print(f"GENERATING SOURCE: {fname}")
            source_dest_path = str(source_code_path)[:-len(".jinja2")]
            if "server" not in source_dest_path:
                params["client_source_files"].append(source_dest_path)
            if "client" not in source_dest_path:
                params["server_source_files"].append(source_dest_path)
            t.render_template(source_code_path, source_dest_path, **params)

    example_template_dir = template_dir / "examples"
    for fname in os.listdir(example_template_dir):
        example_code_path = Path("examples") / fname
        if fname.endswith(".jinja2"):
            print(f"GENERATING EXAMPLE: {fname}")
            example_dest_path = str(example_code_path)[:-len(".jinja2")]
            t.render_template(example_code_path, example_dest_path, **params)

    print(f"GENERATING CmakeLists")
    t.render_template("CMakeLists.txt.jinja2", "CMakeLists.txt", **params)


def run():
    typer.run(main)


if __name__ == "__main__":
    run()

