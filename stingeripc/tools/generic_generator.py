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
    
    code_templator = jj2.CodeTemplator(output_dir=outdir)
    web_templator = jj2.WebTemplator(output_dir=outdir)

    # Add template paths
    if template_path:
        for path in template_path:
            if not path.exists():
                raise RuntimeError(f"Template path does not exist: {path}")
            if not path.is_dir():
                raise RuntimeError(f"Template path is not a directory: {path}")
            real_path = path.resolve()
            print(f"[bold cyan]TEMPLATES:[/bold cyan] {real_path}")
            code_templator.add_template_dir(real_path)
            template_dirs.append(real_path)

    # Add template packages
    if template_pkg:
        for pkg_name in template_pkg:
            try:
                print(f"[bold cyan]TEMPLATES:[/bold cyan] {pkg_name}")
                code_templator.add_template_package(pkg_name)
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
        code_templator.add_template_dir(template_dir)
        template_dirs.append(template_dir)

    def recursive_render_templates(template_dir, src_walker: Path, dest_walker: Path):
        print(f"🚶   [green]WALK[/green]: {src_walker}")
        for entry in os.listdir(src_walker):
            src_entry = src_walker / entry
            dest_entry = dest_walker / entry
            print(f"🚶   [white]ENTRY[/white]: {entry}")
            if '{{' in entry and '}}' in entry:
                rendered_entry_name = code_templator.render_string(entry, **params)
                dest_entry = dest_walker / rendered_entry_name
                print(f"👓   [grey]NAME[/grey]: {entry} -> {rendered_entry_name}")
            if entry.endswith(".jinja2"):
                dest_path_str = str(dest_entry)[:-len(".jinja2")]
                print(f"✨  [green]GENER[/green]: {dest_path_str}")
                if dest_path_str.endswith(".html") or dest_path_str.endswith(".htm"):
                    web_templator.render_template(src_entry.relative_to(template_dir), dest_path_str, **params)
                else:
                    code_templator.render_template(src_entry.relative_to(template_dir), dest_path_str, **params)
            elif src_entry.is_dir():
                print(f"📁  [green]MKDIR[/green]: {dest_entry.resolve()}")
                if not dest_entry.exists():
                    dest_entry.mkdir(parents=True)
                recursive_render_templates(template_dir, src_entry, dest_entry)
            elif src_entry.is_file():
                shutil.copyfile(src_entry, dest_entry)
                print(f"📄   [green]COPY[/green]: {src_entry}")
            else:
                print(f"⚠️    [red]SKIP[/red]: {src_entry} (unknown type)")

    # Process templates from all template directories
    for template_dir in template_dirs:
        src = Path(template_dir)
        recursive_render_templates(template_dir, src, Path(outdir))

def run():
    typer.run(main)


if __name__ == "__main__":
    run()