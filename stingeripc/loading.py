from jacobsjsondoc import ParseOptions
from jacobsjsondoc.fetcher import FilesystemFetcher
from jacobsjsondoc.document import create_document
from jacobsjsondoc.options import RefResolutionMode
from typing import  Any, IO
from pathlib import Path
from uuid import uuid4

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

def parse_yaml_file(file_path: str|Path) -> Any:
    fetcher = FilesystemFetcher()
    options = ParseOptions()
    options.ref_resolution_mode = RefResolutionMode.RESOLVE_REFERENCES
    doc = create_document(uri=str(file_path), fetcher=fetcher, options=options)
    return _to_plain(doc)

def parse_yaml_io(yaml_input: IO, input_name: str|None=None) -> Any:
    fetcher = FilesystemFetcher()
    if input_name is None:
        input_name = f"input-{uuid4()}.yaml"
    fetcher.add_file_io(input_name, yaml_input)
    options = ParseOptions()
    options.ref_resolution_mode = RefResolutionMode.RESOLVE_REFERENCES
    doc = create_document(uri=input_name, fetcher=fetcher, options=options)
    return _to_plain(doc)