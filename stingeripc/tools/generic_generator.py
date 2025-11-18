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
import tomllib


def main(
    inname: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)],
    outdir: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, readable=True)],
    language: Annotated[Optional[str], typer.Argument(help="Shortcut for internally provided templates")] = None,
    template_pkg: Annotated[Optional[list[str]], typer.Option(help="Python package(s) containing templates")] = None,
    template_path: Annotated[Optional[list[Path]], typer.Option(help="Filesystem path(s) to template directories")] = None,
    config: Annotated[Optional[Path], typer.Option("--config", help="TOML configuration file", exists=True, file_okay=True, dir_okay=False, readable=True)] = None,
):
    """Generate output for a Stinger interface.
    
    At least one of --language, --template-pkg, or --template-path must be provided.
    """
    
    # Validate that at least one template source is provided
    if not language and not template_pkg and not template_path:
        raise typer.BadParameter(
            "At least one of: --language, --template-pkg, or --template-path must be provided"
        )

    config_obj = None
    if config:
        with config.open("rb") as f:
            config_obj = tomllib.load(f)

    with inname.open(mode="r") as f:
        stinger = StingerInterface.from_yaml(f)

    params = {"stinger": stinger, "config": config_obj}

    if outdir.is_file():
        raise RuntimeError("Output directory is a file!")
    
    print(f"📁 [bold cyan]OUTPUT:[/bold cyan] {outdir}")
    
    if not outdir.is_dir():
        print(f"📁  [green]MKDIR[/green]: {outdir}")
        os.makedirs(outdir)

    

    # Collect all template directories
    template_dirs = []
    
    templator = jj2.CodeTemplator(output_dir=outdir)

    # Add template paths
    if template_path:
        for path in template_path:
            if not path.exists():
                raise RuntimeError(f"Template path does not exist: {path}")
            if not path.is_dir():
                raise RuntimeError(f"Template path is not a directory: {path}")
            real_path = path.resolve()
            print(f"[bold cyan]TEMPLATES:[/bold cyan] {real_path}")
            templator.add_template_dir(real_path)
            template_dirs.append(real_path)

    # Add template packages
    if template_pkg:
        for pkg_name in template_pkg:
            try:
                print(f"[bold cyan]TEMPLATES:[/bold cyan] {pkg_name}")
                templator.add_template_package(pkg_name)
                pkg_path = importlib.resources.files(pkg_name)
                template_dirs.append(Path(pkg_path))
            except ModuleNotFoundError as e:
                raise RuntimeError(f"Template package not found: {pkg_name}") from e
    
    # Add language-based template directory if language is specified
    if language:
        this_file = Path(__file__)
        this_dir = this_file.parent
        template_dir = (this_dir / "../templates" / language).resolve()
        print(f"[bold cyan]TEMPLATES:[/bold cyan] {template_dir}")
        if not template_dir.exists():
            raise RuntimeError(f"Template directory does not exist: {template_dir}")
        templator.add_template_dir(template_dir)
        template_dirs.append(template_dir)

    def recursive_render_templates(local_dir: str|Path, current_template_dir: Path):
        local_dir = Path(local_dir)
        cur_template_dir = current_template_dir / local_dir
        for entry in os.listdir(cur_template_dir):
            if '{{' in entry and '}}' in entry:
                entry = templator.render_template(str(entry), None, **params)
            if entry == "target":
                # Do not copy 'target' dir
                continue
            entry_full_path = (cur_template_dir / entry).resolve()
            entry_local_path = (local_dir / entry)
            if entry.endswith(".jinja2"):
                destpath = str(entry_local_path)[:-len(".jinja2")]
                print(f"✨  [green]GENER[/green]: {destpath}")
                templator.render_template(entry_local_path, destpath, **params)
            elif entry_full_path.is_dir():
                new_dir = outdir / entry_local_path
                print(f"📁  [green]MKDIR[/green]: {new_dir.resolve()}")
                if not new_dir.exists():
                    new_dir.mkdir(parents=True)
                recursive_render_templates(entry_local_path, current_template_dir)
            elif entry_full_path.is_file():
                shutil.copyfile(entry_full_path, outdir / entry_local_path)
                print(f"📄   [green]COPY[/green]: {entry_full_path}")

    # Process templates from all template directories
    for template_dir in template_dirs:
        recursive_render_templates(".", template_dir)

def run():
    typer.run(main)


if __name__ == "__main__":
    run()