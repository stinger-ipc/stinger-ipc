import logging
import os
import sys
from pathlib import Path

from rich import print
from ruamel.yaml import YAML
from typing_extensions import Annotated
from typing import Optional
import jsonschema_rs
import typer
from stingeripc.loading import parse_yaml_file

from stingeripc import filtering
from stingeripc.asyncapi import stinger_to_asyncapi
from stingeripc.config import StingerConfig, load_config
from stingeripc.interface import StingerInterface

from . import generic_generator

app = typer.Typer(help="Stinger-IPC Tool")


@app.command()
def generate(
    input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)],
    output_dir: Annotated[Path, typer.Argument(..., file_okay=False, dir_okay=True, writable=True, readable=True)],
    language: Annotated[Optional[str], typer.Option("--language", "-l", help="Language to generate: rust, python, markdown, cpp, web, protobuf")] = None,
    template_pkg: Annotated[Optional[list[str]], typer.Option("--template-pkg", help="Python package(s) containing templates")] = None,
    template_path: Annotated[Optional[list[Path]], typer.Option("--template-path", help="Filesystem path(s) to template directories")] = None,
    consumer: Annotated[Optional[str], typer.Option("--consumer", help="Consumer name/identifier")] = None,
    config: Annotated[list[Path], typer.Option("--config", help="TOML configuration file(s) - later files override earlier ones", exists=True, file_okay=True, dir_okay=False, readable=True)] = [],
):
    """Generate code for a Stinger interface.

    INPUT_FILE is the .stinger.yaml file
    OUTPUT_DIR is the directory that will receive generated files

    At least one of --language, --template-pkg, or --template-path must be provided.
    """

    # Check if at least one template source is provided
    if not language and not template_pkg and not template_path:
        raise typer.BadParameter("At least one of: --language, --template-pkg, or --template-path must be provided")

    # If language is provided, validate and use specialized generators
    if language:
        lang = language.lower()
        if lang not in ("rust", "python", "markdown", "cpp", "web", "protobuf"):
            raise typer.BadParameter("language must be one of: rust, python, markdown, cpp, web, protobuf")

        generic_generator.main(input_file, output_dir, lang, template_pkg, template_path, consumer, config)
        print(f"Generation for '{lang}' completed.")

    # Use generic generator if template-pkg or template-path is provided
    if template_pkg or template_path:
        generic_generator.main(input_file, output_dir, language, template_pkg, template_path, consumer, config)
        print(f"Generation from custom templates completed.")


@app.command()
def asyncapi(
    input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)],
    output_dir: Annotated[Path, typer.Argument(..., file_okay=False, dir_okay=True, writable=True, readable=True)],
    consumer: Annotated[Optional[str], typer.Option("--consumer", help="Consumer name/identifier")] = None,
    config: Annotated[list[Path], typer.Option("--config", help="TOML configuration file(s) - later files override earlier ones", exists=True, file_okay=True, dir_okay=False, readable=True)] = [],
):
    """Generate an AsyncAPI specification from a Stinger interface.

    INPUT_FILE is the .stinger.yaml file
    OUTPUT_DIR is the directory that will receive the generated asyncapi.yaml
    """
    input_obj = parse_yaml_file(input_file)

    config_obj = StingerConfig()
    if config:
        for config_file in config:
            print(f"⚙️  [bold cyan]CONFIG:[/bold cyan] {config_file}")
            file_config = load_config(config_file)
            # Merge configs - later files override earlier ones
            # Use model_validate to ensure nested models are properly instantiated
            merged_dict = config_obj.model_dump(exclude_unset=True)
            merged_dict.update(file_config.model_dump(exclude_unset=True))
            config_obj = StingerConfig.model_validate(merged_dict)
    assert isinstance(config_obj, StingerConfig), "Config not a Stinger Config"
    for k, v in config_obj.model_dump().items():
        print(f"🔧{k:>10.10}: {v}")

    print(f"🟢   [bold cyan]LOAD:[/bold cyan] {input_file}")
    if consumer:
        print(f"💠 CONSUMER {consumer}")
        stinger_yaml = filtering.filter_by_consumer(input_obj, consumer)
    else:
        stinger_yaml = input_obj
    stinger = StingerInterface.from_dict(stinger_yaml, config_obj)

    result = stinger_to_asyncapi(stinger, config_obj)

    if not output_dir.is_dir():
        os.makedirs(output_dir)

    output_file = output_dir / "asyncapi.yaml"
    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.allow_unicode = True
    with output_file.open("w") as f:
        yaml.dump(result, f)

    print(f"✅  [bold green]AsyncAPI specification written to {output_file}[/bold green]")


@app.command()
def validate(
    input_file: Annotated[Path, typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)],
    config: Annotated[Optional[list[Path]], typer.Option("--config", "-c", exists=True, file_okay=True, dir_okay=False, readable=True, help="TOML configuration file; needed to check protobuf message names against your .proto sources")] = None,
):
    """Validate a Stinger interface YAML file.

    INPUT_FILE is the .stinger.yaml file
    """
    input_obj = parse_yaml_file(input_file)
    stingeripc_version = (input_obj.get("stingeripc") or {}).get("version")
    if not stingeripc_version:
        print(f"❌  [bold red]Missing required 'stingeripc.version' field in {input_file}[/bold red]")
        sys.exit(1)
    schema_dir = Path(__file__).parent.parent / "schema"
    # Each schema directory validates one minor version of the format; anything
    # older than 0.2 is covered by the 0.1 schema.
    schema_compat = next((v for v in ("0.3", "0.2") if stingeripc_version.startswith(v)), "0.1")
    schema_file = schema_dir / schema_compat / "schema.yaml"
    yaml = YAML(typ="safe")
    with schema_file.open("r") as f:
        schema_obj = yaml.load(f)
    validator = jsonschema_rs.validator_for(schema_obj)

    error_count = 0
    for error in validator.iter_errors(input_obj):
        if error_count == 0:
            print(f"❌  [bold red]Validation errors found in {input_file}:[/bold red]")
        error_count += 1
        print(f"Error: {error}")
        print(f"Location: {error.instance_path}")
    config_obj = StingerConfig()
    for config_file in config or []:
        merged = config_obj.model_dump(exclude_unset=True)
        merged.update(load_config(config_file).model_dump(exclude_unset=True))
        config_obj = StingerConfig.model_validate(merged)

    try:
        # from_dict parses the whole interface -- signals, methods, commands and
        # properties -- where the plain constructor reads only the 'interface' block
        # and so would not catch a malformed element.
        interface = StingerInterface.from_dict(input_obj, config_obj)
        # Only checkable when a [protobuf] path was configured; without one the
        # interface file is still validated, just not against the .proto sources.
        if interface.uses_protobuf() and config_obj.protobuf is not None:
            generic_generator.resolve_protobuf_messages(interface, config_obj, input_file)
    except Exception as e:
        if error_count == 0:
            print(f"❌  [bold red]Validation errors found in {input_file}:[/bold red]")
        error_count += 1
        print(f"Error constructing interface: {e}")

    try:
        filtering.check_version_consistency(input_obj)
    except ValueError as e:
        if error_count == 0:
            print(f"❌  [bold red]Validation errors found in {input_file}:[/bold red]")
        error_count += 1
        print(f"Version consistency error: {e}")

    if error_count == 0:
        print(f"✅  [bold green]No validation errors found in {input_file}[/bold green]")
    sys.exit(error_count)


@app.command()
def hello():
    print("Hello world")


def run():
    logging.getLogger("stevedore").setLevel(logging.WARNING)
    app()


if __name__ == "__main__":
    run()
