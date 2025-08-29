
import sys
from pathlib import Path
import typer
from typing_extensions import Annotated

from . import markdown_generator
from . import python_generator
from . import rust_generator


app = typer.Typer(help="stinger-ipc generator CLI")


@app.command()
def generate(
    language: Annotated[str, typer.Argument(...)],
    input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)],
    output_dir: Annotated[Path, typer.Argument(..., file_okay=False, dir_okay=True, writable=True, readable=True)],
):
    """Generate code for a Stinger interface.

    LANGUAGE must be one of: rust, python, markdown
    INPUT_FILE is the .stinger.yaml file
    OUTPUT_DIR is the directory that will receive generated files
    """
    lang = language.lower()
    if lang not in ("rust", "python", "markdown"):
        raise typer.BadParameter("language must be one of: rust, python, markdown")

    if lang == "python":
        # python_generator.main expects Path arguments via typer
        python_generator.main(input_file, output_dir)
    elif lang == "markdown":
        # markdown_generator.main expects Path arguments via typer
        markdown_generator.main(input_file, output_dir)
    else:  # rust
        rust_generator.main(input_file, output_dir)

    typer.echo(f"Generation for '{lang}' completed.")

@app.command()
def hello():
    print("Hello world")

def run():
    app()

if __name__ == "__main__":
    run()

