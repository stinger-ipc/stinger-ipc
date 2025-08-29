from jacobsjinjatoo import templator as jj2
from jacobsjinjatoo import stringmanip
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
    t = jj2.CodeTemplator(output_dir=os.path.dirname(outdir))
    t.add_template_dir(
        os.path.join(os.path.dirname(__file__), "../templates", "python")
    )
    for output_file in [
        "pyproject.toml",
    ]:
        print(f"[bold red]Generating:[/bold red] {output_file}")
        t.render_template(f"{output_file}.jinja2", output_file, **params)

    package_name = f"{stringmanip.lower_camel_case(stinger.name).lower()}ipc"
    generated_pkg_dir = os.path.join(outdir, package_name)
    print(f"[bold red]Making Directory:[/bold red] {generated_pkg_dir}")
    os.makedirs(generated_pkg_dir, exist_ok=True)
    for output_file in [
        "server.py",
        "client.py",
        "connection.py",
        "__init__.py",
        "method_codes.py",
    ]:
        print(f"[bold red]Generating:[/bold red] {output_file}")
        t.render_template(f"{output_file}.jinja2", output_file, **params)

    t.render_template("interface_types.py.jinja2", f"{stinger.get_enum_module_name()}.py", **params)

def run():
    typer.run(main)

if __name__ == "__main__":
    run()