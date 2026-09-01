from jacobsjinjatoo import templator as jj2
from jacobsjinjatoo import stringmanip
import os
import tomllib
import shutil
import typer
from typing_extensions import Annotated
from typing import Optional, Any
from pathlib import Path
from rich import print
import importlib.resources
import re
from stingeripc.loading import parse_yaml_file
from stevedore import ExtensionManager
from stingeripc import StingerInterface, __version__, topic_util
from stingeripc.filtering import filter_by_consumer
from stingeripc.config import load_config, StingerConfig
from stingeripc.exceptions import ProtobufError
from stingeripc.protobuf_compiler import ProtobufSources


def _to_plain(value: Any) -> Any:
    """Recursively convert a jacobs-json-doc parsed document into plain Python types."""
    if isinstance(value, dict):
        return {k: _to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_plain(v) for v in value]
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return float(value)
    if isinstance(value, str):
        return str(value)
    return value


def _parse_yaml(text: str) -> Any:
    """Parse YAML text with jacobs-json-doc, resolving $ref references in place."""
    fetcher = PrepopulatedFetcher()
    fetcher.prepopulate(None, text)
    options = ParseOptions()
    options.ref_resolution_mode = RefResolutionMode.RESOLVE_REFERENCES
    return create_document(uri=None, fetcher=fetcher, options=options)


def emit_protobuf_bindings(template_dir: Path, outdir: Path, stinger, config_obj, inname: Path) -> None:
    """Copy the .proto sources into the output and compile them for this language.

    What to run is described by an optional ``partials/protoc.toml`` in the
    template tree.  Keeping the recipe beside the templates means this function
    needs no knowledge of any particular language, and a tree that ships no such
    file -- markdown, web -- simply does nothing here.

    Paths in the recipe may use ``{python_package}`` and ``{interface}``; protoc
    flags may additionally use ``{out}`` for the absolute output directory.
    """
    if not stinger.uses_protobuf():
        return
    recipe_path = template_dir / "partials" / "protoc.toml"
    if not recipe_path.is_file():
        return

    placeholders = {
        "python_package": stinger.python.package_directory,
        "interface": stringmanip.snake_case(stinger.name),
    }
    recipe = tomllib.loads(recipe_path.read_text())

    proto_src = (inname.parent / config_obj.protobuf.path).resolve()
    sources = ProtobufSources(proto_src, config_obj.protobuf.protoc)

    # The .proto files travel with the generated code, so the output is
    # self-contained and can be regenerated for another language later.
    copy_to = outdir / recipe["copy_to"].format(**placeholders)
    copy_to.mkdir(parents=True, exist_ok=True)
    for proto in sources.proto_files:
        shutil.copyfile(proto, copy_to / proto.name)
    print(f"🧬    PROTO: copied {len(sources.proto_files)} .proto file(s)")

    out_dir = outdir / recipe["out_dir"].format(**placeholders)
    out_dir.mkdir(parents=True, exist_ok=True)
    sources.run(*[flag.format(out=out_dir, **placeholders) for flag in recipe["flags"]])
    print(f"🧬    PROTO: compiled bindings into {recipe['out_dir'].format(**placeholders)}")

    # Some languages need a module file listing whatever protoc produced, which
    # protoc itself does not write because it does not know how the language
    # groups generated files.
    if "include_module" in recipe:
        module_file = outdir / recipe["include_module"].format(**placeholders)
        # prost nests its output by protobuf package, so the search recurses and the
        # include paths stay relative to the module file.
        generated = sorted(
            f.relative_to(module_file.parent).as_posix()
            for f in out_dir.rglob("*.rs")
            if f.resolve() != module_file.resolve()
        )
        header = recipe.get("include_module_header", "")
        body = "\n".join(f'include!("{name}");' for name in generated)
        module_file.write_text(f"{header}{body}\n")
        print(f"🧬    PROTO: wrote {recipe['include_module']} including {len(generated)} file(s)")

    # Some languages need a marker file beside the generated bindings -- a Python
    # package __init__ -- that protoc does not write.
    for name, content in recipe.get("write", {}).items():
        target = outdir / name.format(**placeholders)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.format(**placeholders))


def resolve_protobuf_messages(stinger, config_obj, inname: Path) -> None:
    """Match every protobuf message the interface names against the .proto sources.

    Done once, before any template runs, so a message that does not exist fails
    here with a name and a suggestion rather than surfacing later as a compile
    error in generated code.  An interface that names no protobuf messages needs
    no protobuf configuration and does nothing here.
    """
    refs = stinger.all_protobuf_refs()
    if not refs:
        return

    # Relative to the interface file, so a .stinger.yaml and its .proto files
    # travel together regardless of where the generator is invoked from.
    proto_dir = (inname.parent / config_obj.protobuf.path).resolve()
    print(f"🧬 [bold cyan]PROTOS:[/bold cyan] {proto_dir}")
    sources = ProtobufSources(proto_dir, config_obj.protobuf.protoc)
    sources.resolve_all(refs)
    for ref in stinger.protobuf_messages():
        print(f"🧬    MSG: {ref.full_name} ({ref.proto_file})")


def main(
    inname: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)],
    outdir: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, readable=True)],
    language: Annotated[Optional[str], typer.Argument(help="Shortcut for internally provided templates")] = None,
    template_pkg: Annotated[Optional[list[str]], typer.Option(help="Python package(s) containing templates")] = None,
    template_path: Annotated[Optional[list[Path]], typer.Option(help="Filesystem path(s) to template directories")] = None,
    consumer: Annotated[Optional[str], typer.Option("--consumer", help="Consumer name/identifier")] = None,
    config: Annotated[list[Path], typer.Option("--config", help="TOML configuration file(s) - later files override earlier ones", exists=True, file_okay=True, dir_okay=False, readable=True)] = [],
):
    """Generate output for a Stinger interface.

    At least one of --language, --template-pkg, or --template-path must be provided.
    """
    print(f"▶️ [bold cyan]VERSION:[/bold cyan] {__version__}")

    # Validate that at least one template source is provided
    if not language and not template_pkg and not template_path:
        raise typer.BadParameter("At least one of: --language, --template-pkg, or --template-path must be provided")

    # Load and merge configuration files
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

    print(f"🟢   [bold cyan]LOAD:[/bold cyan] {inname}")
    yaml_obj = parse_yaml_file(inname)
    if consumer:
        print(f"💠 CONSUMER {consumer}")
        stinger_yaml = filter_by_consumer(yaml_obj, consumer)
        stinger = StingerInterface.from_dict(stinger_yaml, config_obj)
    else:
        stinger = StingerInterface.from_dict(yaml_obj, config_obj)

    resolve_protobuf_messages(stinger, config_obj, inname)

    print(f"🚥 [bold cyan]SIGNALS:[/bold cyan] {len(stinger.signals)}")
    print(f"💠 [bold cyan]METHODS:[/bold cyan] {len(stinger.methods)}")
    print(f"📣 [bold cyan]COMMANDS:[/bold cyan] {len(stinger.commands)}")
    print(f"🍌   [bold cyan]PROPS:[/bold cyan] {len(stinger.properties)}")

    params: dict[str, Any] = {
        "stinger": stinger,
        "config": config_obj,
        "consumer": consumer,
        "generator": {
            "version": __version__,
        },
        "templates": dict(),
        "utils": {
            "topic_template_placeholder_index": topic_util.get_argument_position,
            "get_topic_arguments": topic_util.get_topic_arguments,
            "template_topic_fill_in": topic_util.topic_template_fill_in,
            "topic_template_to_js": topic_util.topic_template_to_js,
        },
    }

    if outdir.is_file():
        raise RuntimeError("Output directory is a file!")

    print(f"📁 [bold cyan]OUTPUT:[/bold cyan] {outdir}")

    mgr: ExtensionManager = ExtensionManager(
        namespace="stinger_symbols",
        invoke_on_load=False,
        on_load_failure_callback=lambda mgr, ext, exc: print(f"❌[bold red]EXTFAIL:[/bold red] {ext.name} : {exc}"),
    )
    for ext in mgr:
        print(f"🔌    EXT: {ext.name:7} : {ext.entry_point_target}")

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
            web_templator.add_template_dir(real_path)
            template_dirs.append(real_path)

    # Add template packages
    if template_pkg:
        for pkg_name in template_pkg:
            pattern = r"^([a-zA-Z0-9_\-]+)\.([a-zA-Z0-9_\-.]+)"
            match = re.search(pattern, pkg_name)
            if match:
                package_name = match.group(1)
                template_subdir = match.group(2).replace(".", "/")
            else:
                package_name = pkg_name
                template_subdir = ""
            try:
                print(f"[bold cyan]TEMPLATES:[/bold cyan] {package_name} {template_subdir}")
                code_templator.add_template_package(package_name, template_subdir)
                web_templator.add_template_package(package_name, template_subdir)
                pkg_path = importlib.resources.files(package_name)
                template_dirs.append(Path(str(pkg_path)) / Path(template_subdir))

                # Try to import package and get version
                try:
                    pkg_module = importlib.import_module(package_name)
                    if hasattr(pkg_module, "__version__"):
                        if package_name not in params["templates"]:
                            params["templates"][package_name] = {}
                        params["templates"][package_name]["version"] = pkg_module.__version__
                except Exception:
                    pass  # Silently ignore if we can't get version

            except ModuleNotFoundError as e:
                raise RuntimeError(f"Template package not found: {package_name}") from e

    # Add language-based template directory if language is specified
    if language:
        this_file = Path(__file__)
        this_dir = this_file.parent
        template_dir = (this_dir / "../templates" / language).resolve()
        print(f"[bold cyan]TEMPLATES:[/bold cyan] {template_dir}")
        if not template_dir.exists():
            raise RuntimeError(f"Template directory does not exist: {template_dir}")
        code_templator.add_template_dir(template_dir)
        web_templator.add_template_dir(template_dir)
        template_dirs.append(template_dir)

    def recursive_find_output_files(src_walker: Path, dest_walker: Path) -> list[str]:
        found_files = []
        for entry in os.listdir(src_walker):
            src_entry = src_walker / entry
            dest_entry = dest_walker / entry
            if ("{{" in entry and "}}" in entry) or ("{%" in entry and "%}" in entry):
                rendered_entry_name = code_templator.render_string(entry, **params)
                if len(rendered_entry_name) > 0:
                    dest_entry = dest_walker / rendered_entry_name
                else:
                    continue
            if entry.endswith(".jinja2"):
                dest_path_str = str(dest_entry)[: -len(".jinja2")]
                dest_path = Path(dest_path_str).relative_to(outdir)
                found_files.append(str(dest_path))
            elif src_entry.is_dir():
                found_files.extend(recursive_find_output_files(src_entry, dest_entry))
            elif src_entry.is_file():
                dest_path = Path(dest_entry).relative_to(outdir)
                found_files.append(str(dest_path))
        return found_files

    output_file_list = set()
    for template_dir in template_dirs:
        output_file_list.update(recursive_find_output_files(Path(template_dir), Path(outdir)))
    params["output_files"] = list(output_file_list)

    def recursive_render_templates(template_dir, src_walker: Path, dest_walker: Path):
        print(f"🚶   [green]WALK[/green]: {src_walker}")
        for entry in os.listdir(src_walker):
            if entry.endswith("partials"):
                continue
            src_entry = src_walker / entry
            dest_entry = dest_walker / entry
            print(f"🚶  [white]ENTRY[/white]: {src_entry.relative_to(template_dir)}")
            if ("{{" in entry and "}}" in entry) or ("{%" in entry and "%}" in entry):
                rendered_entry_name = code_templator.render_string(entry, **params)
                if len(rendered_entry_name) == 0:
                    print(f"👓   [grey]NAME[/grey]: {entry} -> [excluded]")
                    continue
                dest_entry = dest_walker / rendered_entry_name
                print(f"👓   [grey]NAME[/grey]: {entry} -> {rendered_entry_name}")
            if str(dest_entry).endswith(".jinja2") and ".jinja2" in str(src_entry):
                dest_path_str = str(dest_entry)[: -len(".jinja2")]
                template = str(src_entry.relative_to(template_dir))
                dest_path = Path(dest_path_str).relative_to(outdir)
                print(f"✨  [green]GENER[/green]: {dest_path}")
                if dest_path_str.endswith(".html") or dest_path_str.endswith(".htm"):
                    web_templator.render_template(template, dest_path, **params)
                else:
                    code_templator.render_template(template, dest_path, **params)
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

    for template_dir in template_dirs:
        emit_protobuf_bindings(Path(template_dir), Path(outdir), stinger, config_obj, inname)


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
