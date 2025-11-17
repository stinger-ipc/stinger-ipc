from jacobsjinjatoo import templator as jj2
import os
import shutil
import typer
from typing_extensions import Annotated
from typing import Optional
from pathlib import Path
from rich import print
import importlib.resources

from stingeripc import StingerInterface


def main(
    inname: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)],
    outdir: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, readable=True)],
    language: Annotated[Optional[str], typer.Argument()] = None,
    template_pkg: Annotated[Optional[list[str]], typer.Option(help="Python package(s) containing templates")] = None,
    template_path: Annotated[Optional[list[Path]], typer.Option(help="Filesystem path(s) to template directories")] = None,
):
    """Generate output for a Stinger interface.
    
    At least one of language, --template-pkg, or --template-path must be provided.
    """
    
    # Validate that at least one template source is provided
    if not language and not template_pkg and not template_path:
        raise typer.BadParameter(
            "At least one of: language argument, --template-pkg, or --template-path must be provided"
        )

    with inname.open(mode="r") as f:
        stinger = StingerInterface.from_yaml(f)

    params = {"stinger": stinger}

    if outdir.is_file():
        raise RuntimeError("Output directory is a file!")

    if not outdir.is_dir():
        os.makedirs(outdir)

    print(f"OUPUT: {outdir}")

    # Collect all template directories
    template_dirs = []
    
    # Add language-based template directory if language is specified
    if language:
        this_file = Path(__file__)
        this_dir = this_file.parent
        template_dir = (this_dir / "../templates" / language).resolve()

        if not template_dir.exists():
            raise RuntimeError(f"Template directory does not exist: {template_dir}")
        
        template_dirs.append(template_dir)
    
    # Add template packages
    if template_pkg:
        for pkg_name in template_pkg:
            try:
                # Try to get the package path
                pkg = importlib.import_module(pkg_name)
                if hasattr(pkg, '__path__'):
                    # It's a package, use the first path
                    pkg_path = Path(pkg.__path__[0])
                    template_dirs.append(pkg_path)
                elif pkg.__file__:
                    # It's a module, use its parent directory
                    pkg_path = Path(pkg.__file__).parent
                    template_dirs.append(pkg_path)
                else:
                    raise RuntimeError(f"Could not determine path for package '{pkg_name}'")
            except ImportError as e:
                raise RuntimeError(f"Could not import template package '{pkg_name}': {e}")
    
    # Add template paths
    if template_path:
        for path in template_path:
            if not path.exists():
                raise RuntimeError(f"Template path does not exist: {path}")
            if not path.is_dir():
                raise RuntimeError(f"Template path is not a directory: {path}")
            template_dirs.append(path.resolve())

    t = jj2.CodeTemplator(output_dir=outdir)
    
    # Add all template directories to the templator
    for template_dir in template_dirs:
        t.add_template_dir(template_dir)

    def recursive_render_templates(local_dir: str|Path, current_template_dir: Path):
        local_dir = Path(local_dir)
        cur_template_dir = current_template_dir / local_dir
        for entry in os.listdir(cur_template_dir):
            if '{{' in entry and '}}' in entry:
                entry = t.render_template(str(entry), None, **params)
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
                recursive_render_templates(entry_local_path, current_template_dir)
            elif entry_full_path.is_file():
                shutil.copyfile(entry_full_path, outdir / entry_local_path)
                print(f"COPY:  {entry_full_path}")

    # Process templates from all template directories
    for template_dir in template_dirs:
        print(f"Processing templates from: {template_dir}")
        recursive_render_templates(".", template_dir)


def run():
    typer.run(main)


if __name__ == "__main__":
    run()