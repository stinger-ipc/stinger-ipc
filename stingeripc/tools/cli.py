
import os
import sys
from wsgiref.validate import validator
from rich import print
from pathlib import Path
import typer
from typing_extensions import Annotated
from jacobsjinjatoo import templator as jj2
from jacobsjsonschema.draft7 import Validator
import yaml
import yamlloader
from stingeripc.interface import StingerInterface

from . import markdown_generator
from . import python_generator
from . import rust_generator
from . import cpp_generator

app = typer.Typer(help="stinger-ipc generator CLI")


@app.command()
def generate(
    language: Annotated[str, typer.Argument(...)],
    input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)],
    output_dir: Annotated[Path, typer.Argument(..., file_okay=False, dir_okay=True, writable=True, readable=True)],
):
    """Generate code for a Stinger interface.

    LANGUAGE must be one of: rust, python, markdown, cpp, web
    INPUT_FILE is the .stinger.yaml file
    OUTPUT_DIR is the directory that will receive generated files
    """
    lang = language.lower()
    if lang not in ("rust", "python", "markdown", "cpp", "web"):
        raise typer.BadParameter("language must be one of: rust, python, markdown, cpp, web")

    if lang == "python":
        # python_generator.main expects Path arguments via typer
        python_generator.main(input_file, output_dir)
    elif lang == "markdown":
        # markdown_generator.main expects Path arguments via typer
        markdown_generator.main(input_file, output_dir)
    elif lang == "web":
        wt = jj2.WebTemplator(output_dir=output_dir)
        ct = jj2.CodeTemplator(output_dir=output_dir)
        wt.add_template_dir(
            os.path.join(os.path.dirname(__file__), "../templates", "html")
        )
        ct.add_template_dir(
            os.path.join(os.path.dirname(__file__), "../templates", "html")
        )
        with open(input_file, "r") as f:
            stinger = StingerInterface.from_yaml(f)
        for output_file in [
            "app.js",
            "styles.css",
        ]:
            ct.render_template(f"{output_file}.jinja2", output_file, stinger=stinger)
        wt.render_template("index.html.jinja2", "index.html", stinger=stinger)
    elif lang == "cpp":
        cpp_generator.main(input_file, output_dir)
    elif lang == "rust":
        rust_generator.main(input_file, output_dir)
    else:
        raise RuntimeError("Unreachable code reached")

    print(f"Generation for '{lang}' completed.")

@app.command()
def validate(input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)]):
    """Validate a Stinger interface YAML file.

    INPUT_FILE is the .stinger.yaml file
    """
    schema_file = Path(__file__).parent.parent / "schema" / "schema.yaml"
    schema_obj = yaml.load(schema_file.open("r"), Loader=yamlloader.ordereddict.Loader)
    validator = Validator(schema_obj, lazy_error_reporting=False)

    input_obj = yaml.load(input_file.open("r"), Loader=yamlloader.ordereddict.Loader)
    if result := validator.validate(input_obj):
        print("Validated: ", result)
    else:
        for error in validator.get_errors():
            print(error)
        sys.exit(1)
    sys.exit(0)

@app.command()
def hello():
    print("Hello world")

def run():
    app()

if __name__ == "__main__":
    run()

