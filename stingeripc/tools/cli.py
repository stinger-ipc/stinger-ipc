
import os
import sys
from wsgiref.validate import validator
from rich import print
from pathlib import Path
import typer
from typing_extensions import Annotated
from typing import Optional
from jacobsjinjatoo import templator as jj2
import jsonschema_rs
import yaml
import yamlloader
from stingeripc.interface import StingerInterface

from . import cpp_generator
from . import generic_generator

app = typer.Typer(help="stinger-ipc generator CLI")


@app.command()
def generate(
    input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)],
    output_dir: Annotated[Path, typer.Argument(..., file_okay=False, dir_okay=True, writable=True, readable=True)],
    language: Annotated[Optional[str], typer.Option("--language", "-l", help="Language to generate: rust, python, markdown, cpp, web, protobuf")] = None,
    template_pkg: Annotated[Optional[list[str]], typer.Option("--template-pkg", help="Python package(s) containing templates")] = None,
    template_path: Annotated[Optional[list[Path]], typer.Option("--template-path", help="Filesystem path(s) to template directories")] = None,
    consumer: Annotated[Optional[str], typer.Option("--consumer", help="Consumer name/identifier")] = None,
    config: Annotated[Optional[Path], typer.Option("--config", help="TOML configuration file", exists=True, file_okay=True, dir_okay=False, readable=True)] = None,
):
    """Generate code for a Stinger interface.

    INPUT_FILE is the .stinger.yaml file
    OUTPUT_DIR is the directory that will receive generated files
    
    At least one of --language, --template-pkg, or --template-path must be provided.
    """

    # Check if at least one template source is provided
    if not language and not template_pkg and not template_path:
        raise typer.BadParameter(
            "At least one of: --language, --template-pkg, or --template-path must be provided"
        )
    
    # If language is provided, validate and use specialized generators
    if language:
        lang = language.lower()
        if lang not in ("rust", "python", "markdown", "cpp", "web", "protobuf"):
            raise typer.BadParameter("language must be one of: rust, python, markdown, cpp, web, protobuf")

        if lang in ["markdown", "rust", "html", "protobuf", "python", "web"]:
            generic_generator.main(input_file, output_dir, lang, template_pkg, template_path, consumer, config)
        elif lang == "cpp":
            cpp_generator.main(input_file, output_dir)
        
        print(f"Generation for '{lang}' completed.")
    
    # Use generic generator if template-pkg or template-path is provided
    if template_pkg or template_path:
        generic_generator.main(input_file, output_dir, language, template_pkg, template_path, consumer, config)
        print(f"Generation from custom templates completed.")

@app.command()
def validate(input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)]):
    """Validate a Stinger interface YAML file.

    INPUT_FILE is the .stinger.yaml file
    """
    schema_file = Path(__file__).parent.parent / "schema" / "schema.yaml"
    schema_obj = yaml.load(schema_file.open("r"), Loader=yamlloader.ordereddict.Loader)
    validator = jsonschema_rs.validator_for(schema_obj)
    
    input_obj = yaml.load(input_file.open("r"), Loader=yamlloader.ordereddict.Loader)

    for error in validator.iter_errors(input_obj):
        print(f"Error: {error}")
        print(f"Location: {error.instance_path}")
    sys.exit(0)

@app.command()
def hello():
    print("Hello world")

def run():
    app()

if __name__ == "__main__":
    run()

