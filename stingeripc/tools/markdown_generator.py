import os
import sys
from jacobsjinjatoo import templator as jj2
import os.path
import typer
from typing_extensions import Annotated
from stingeripc import StingerInterface
from rich import print
from pathlib import Path

def main(inname: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)], outdir: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, readable=True)]):
    print(f"[bold green]Reading:[/bold green] {inname}")
    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
    }
    output_dir = Path(outdir).resolve()
    print(f"[bold green]Output directory:[/bold green] {output_dir}")
    t = jj2.MarkdownTemplator(output_dir=output_dir)
    t.add_template_dir(
        os.path.join(os.path.dirname(__file__), "../templates", "markdown")
    )
    for output_file in [
        "index.md",
    ]:
        print(f"[bold red]GENERATING:[/bold red] {os.path.join(outdir, output_file)}")
        t.render_template(f"{output_file}.jinja2", output_file, **params)

def run():
    typer.run(main)

if __name__ == "__main__":
    run()