from jacobsjinjatoo import templator as jj2
import os
import shutil
import typer
from typing_extensions import Annotated
from pathlib import Path
from rich import print

from stingeripc import StingerInterface


def main(
    inname: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)],
    outdir: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, readable=True)],
):
    """Generate Rust output for a Stinger interface."""

    with inname.open(mode="r") as f:
        stinger = StingerInterface.from_yaml(f)

    params = {"stinger": stinger}

    if outdir.is_file():
        raise RuntimeError("Output directory is a file!")

    if not outdir.is_dir():
        os.makedirs(outdir)

    print(f"OUPUT: {outdir}")

    this_file = Path(__file__)
    this_dir = this_file.parent
    template_dir = (this_dir / "../templates" / "rust").resolve()

    t = jj2.CodeTemplator(output_dir=outdir)
    t.add_template_dir(template_dir)

    def recursive_render_templates(local_dir: str|Path):
        local_dir = Path(local_dir)
        cur_template_dir = template_dir / local_dir
        for entry in os.listdir(cur_template_dir):
            if entry == "target":
                # Do not copy 'target' dir
                continue
            entry_full_path = (cur_template_dir / entry).resolve()
            entry_local_path = (local_dir / entry)
            if entry.endswith(".jinja2"):
                destpath = str(entry_local_path)[:-len(".jinja2")]
                print(f"GENER: {entry_local_path} -> {destpath}")
                t.render_template(entry_local_path, destpath, **params)
            elif entry_full_path.is_dir():
                new_dir = outdir / entry_local_path
                print(f"MKDIR: {new_dir.resolve()}")
                if not new_dir.exists():
                    new_dir.mkdir(parents=True)
                recursive_render_templates(entry_local_path)
            elif entry_full_path.is_file():
                shutil.copyfile(entry_full_path, outdir / entry_local_path)
                print(f"COPY:  {entry_full_path}")

    recursive_render_templates(".")


def run():
    typer.run(main)


if __name__ == "__main__":
    run()