from jacobsjinjatoo import templator as jj2
from jacobsjinjatoo import stringmanip
import os.path
import typer
from typing_extensions import Annotated
from stingeripc import StingerInterface
from rich import print
from pathlib import Path

def main(inname: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)], outdir: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, readable=True)]):

    print(f"[bold]Reading:[/bold] {inname}")
    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
    }
    output_dir = Path(outdir).resolve()
    print(f"[bold]Output directory:[/bold] {output_dir}")
    t = jj2.CodeTemplator(output_dir=output_dir)
    t.add_template_dir(
        os.path.join(os.path.dirname(__file__), "../templates", "python")
    )
    for output_file in [
        "pyproject.toml",
    ]:
        print(f"[bold green]Generating:[/bold green] {output_file}")
        t.render_template(f"{output_file}.jinja2", output_file, **params)

    package_name = f"{stringmanip.lower_camel_case(stinger.name).lower()}ipc"
    generated_pkg_dir = output_dir / package_name
    print(f"[bold]Making Directory:[/bold] {generated_pkg_dir}")
    os.makedirs(generated_pkg_dir, exist_ok=True)
    for output_file in [
        "server.py",
        "client.py",
        "connection.py",
        "__init__.py",
        "method_codes.py",
    ]:
        of = generated_pkg_dir / output_file
        print(f"[bold green]Generating:[/bold green] {of}")
        output = t.render_template(f"{output_file}.jinja2", of, **params)

    t.render_template("interface_types.py.jinja2", f"{generated_pkg_dir}/{stinger.get_enum_module_name()}.py", **params)

def run():
    typer.run(main)

if __name__ == "__main__":
    run()