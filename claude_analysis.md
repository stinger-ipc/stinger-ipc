# stinger-ipc: codebase analysis and improvement recommendations

## Context

The user asked for an analysis of the stinger-ipc repository and a list of recommendations.
This is an assessment, not a change request. Every item below was verified against the
working tree on `develop` (2026-09-21) and carries a file reference and a concrete fix, so
any item can be picked up later as its own task.

Baseline measured locally:

| Check | Result |
|---|---|
| `uv run pytest` | 348 passed, 1 skipped, 0.65 s |
| `uv run mypy stingeripc/` | 22 errors in 5 files |
| `uv run black --check stingeripc tests` | 8 files would be reformatted |
| Local `generated/` tree | 43 GB, of which 42 GB is six separate Rust `target/` dirs |

Overall: the architecture is sound (declarative YAML, pydantic models, plugin-discovered
symbol providers, a language-agnostic template walker, per-language `protoc.toml` recipes).
The problems are mostly around the edges: packaging, CI coverage, correctness of generated
runtime code, and drift between the three language targets.

---

## P0: Ship-blocking bugs

### 1. Installed wheels are missing runtime template files
`pyproject.toml:54-57` ships only `templates/**/*.jinja2`. Ten files the generator reads or
copies at runtime are excluded from any wheel (confirmed against `dist/stinger_ipc-0.10.0a3`):
all three `partials/protoc.toml` recipes, `cpp/.clang-format`, `cpp/Taskfile.yml`,
`rust/Taskfile.yml`, `rust/.gitignore`, `cpp/examples/protolists.proto`, and the web
`{%if stinger.uses_protobuf()%}proto_bundle.js.jinja2{%endif%}` file (its name does not end
in `.jinja2`). Worst effect: `generic_generator.py:64-66` returns silently when the recipe is
missing, so **protobuf code generation is a silent no-op from pip-installed stinger-ipc**.
- Fix: `stingeripc = ["templates/**/*", "schemas/**/*"]` or `include-package-data = true` with
  a `MANIFEST.in`; add a CI step that builds the wheel and asserts these paths exist.

### 2. Schema packaging relies on a committed symlink
`stingeripc/schema -> ../schemas/` is a git symlink; `cli.py:126` locates it by `__file__`.
On a checkout with `core.symlinks=false` (Windows default) the glob matches nothing and
`stinger validate` raises `FileNotFoundError`.
- Fix: move `schemas/` under `stingeripc/`, drop the symlink, load via `importlib.resources`.

### 3. Generated clients leak pending method calls and never time out (all 3 languages)
- Python `client.py.jinja2:333`: `_pending_method_responses` entry is never evicted; the
  returned `Future` has no timeout; the dict is written from the caller thread and read/deleted
  from the MQTT thread (line 397) with no lock. Properties got both a timeout
  (`PROPERTY_VALUE_TIMEOUT_SECONDS`, line 48) and mutexes; methods got neither.
- Rust `client.rs.jinja2:476`: `receiver.await.unwrap()` with no `tokio::time::timeout`,
  panics if the sender drops. Line 405 `from_bytes(...).unwrap()` turns bad remote input into
  a panic.
- C++ `client.hpp.jinja2:129`: `_pending<Method>MethodCalls` map has no mutex (signals do,
  lines 110/118); entries are never erased; a duplicate response calls `set_value()` twice.
- Fix: add a method timeout constant per language, evict on completion or timeout, guard the
  Python dict and C++ map with the existing mutex pattern, replace the two Rust `unwrap`s.

### 4. C++ server drops method requests that have no handler
`cpp/src/server.cpp.jinja2:298-301` has `// TODO: publish an error response` and returns.
The calling client's future never resolves.
- Fix: publish a `NOT_IMPLEMENTED` return code, matching what Python and Rust do.

### 5. A schema test that can never fail, against the wrong schema
`tests/test_examples.py:30` is `assert (len(errors), 0)`, a non-empty tuple, always truthy.
Line 9 validates against `schemas/0.2/` while every example declares `0.3.0`. Only 2 of 8
examples are checked.
- Fix: `assertEqual(len(errors), 0)`, point at 0.3, parametrize over `example_interfaces/*/`.

---

## P1: CI, tooling, and repository hygiene

### 6. CI does not run the test suite, black, or any compile step
Two workflows exist. `mypy.yml` runs mypy on `stingeripc/` only; `generate-and-publish.yml`
runs `task generate` and pushes to a sibling repo. Neither runs `pytest`, `black --check`,
`cpp:compile`, `rust:check`, or any generated-code unit tests. Both trigger only on
`main`/`master`, so day-to-day work on `develop` gets no CI. mypy is currently red (22
errors) and black is red (8 files) on `develop` without anyone being told.
- Fix: one `ci.yml` on push/PR to `develop` and `master` running pytest, mypy, black, a wheel
  build check (item 1), and at least `task python` in a matrix of 3.12/3.13. Add a
  tag-triggered publish workflow with PyPI trusted publishing instead of the manual
  `uv publish` in `.claude/skills/stinger-release/SKILL.md:121-137`.

### 7. Fix the current mypy and black failures
mypy: `asyncapi.py:121-137` redefines `prop` six times; `components.py:253,298,307` reference
names only imported under `TYPE_CHECKING`; `components.py:105-120` indexes an `Any | None`;
`generic_generator.py:44-48` is dead code with undefined names (see item 12);
`cpp_symb.py:182` has an unused ignore. Then tighten `mypy.ini` (add
`disallow_incomplete_defs`, `python_version = 3.12`, drop stale `stringcase`/`yamlloader`
stanzas) and run it over `tests/` too.

### 8. Share one Cargo target directory across the example Rust builds
Six `generated/*/rust/target` dirs total 42 GB; every dependency compiles six times.
- Fix: set `CARGO_TARGET_DIR: '{{.GENERATED_DIR}}/.cargo-target'` in the Rust tasks.

### 9. Taskfile bugs
- `Taskfile.yml:602` quotes the glob, so `task clean` removes nothing.
- Lines 171, 184, 213, 226, 251 hardcode `dir: generated/...` instead of `{{.GENERATED_DIR}}`,
  which breaks the `compare-stinger-generated-code` skill's `GENERATED_DIR=./modified` flow.
- Line 61 lists nonexistent `schemas/schema.yaml` as a source; lines 175-176 list a path from
  the old `example_interfaces/*/python` layout.
- `asyncapi:generate` (471-475) and `protobuf:check` (567-571) skip `PROTO_INTERFACES`.
- There is no `task test` for the repo's own pytest suite.

### 10. Dependency declarations
- `rich` and `typing_extensions` are imported (`cli.py:6,8`, `generic_generator.py:8,12`) but
  not declared; `rich` works only because typer happens to pull it in. Drop
  `typing_extensions` (stdlib `typing.Annotated` on 3.12) and declare `rich`.
- `go-task-bin`, `packaging`, `pydantic-asyncapi` are runtime deps that the package never
  imports. Move the first two to dev; remove the third.
- `jacobs-json-schema` (dev) is imported nowhere; remove.
- Use `[tool.setuptools.packages.find]` instead of the hand-listed `packages`.

### 11. Stale and stray files
- `.directory` (KDE folder metadata) is tracked; `.pytest_cache/` and
  `.claude/settings.local.json` are not ignored; `.vscode/` is both ignored and tracked.
- `.vscode/settings.json:15-19` points YAML validation at `schemas/schema.yaml` with glob
  `*.stingeripc`; both are wrong. `.vscode/launch.json` targets paths that no longer exist.
- `bin/asyncapi_generator.py` imports a class that no longer exists;
  `bin/clean_example_output.sh` cleans the old layout.
- `example_interfaces/prop_only/` is a byte-identical duplicate of `prop-only/`;
  `no-version-tracking.toml` is referenced by nothing.
- `.readthedocs.yaml:19` installs `.[dev]`, an extra that does not exist (the project uses
  PEP 735 dependency groups), so Read the Docs builds without Sphinx extensions.
- `.devcontainer` has no `postCreateCommand` and no C++ toolchain, so `task` cannot run in it.
- `stinger-release/SKILL.md:55,67` reference `schemas/schema.yaml`, which no longer exists.

---

## P2: Generator code quality

### 12. Dead code
- `stingeripc/models.py` (168 lines): imported by nothing; its `.rust/.python/.cpp` properties
  import `stingeripc.symbols.rust` etc., which do not exist; defines a second `StingerSpec`.
- `stingeripc/connection.py`: unused.
- `generic_generator.py:24-48`: `_to_plain` (duplicate of `loading.py:9`) and `_parse_yaml`
  (uses four undefined names) are never called.
- `cli.py:176-178`: `hello` subcommand shipped on both console scripts.
- `interface.py:8 VERSIONS_SUPPORTED` is never read; the real check is `components.py:504`.
- `config.py:50 CppConfig.package_suffix` is read nowhere; `cpp_symb.py` never sees config.
- `tests/mock_connection.py` (imports `stinger.connection`, would fail) and
  `tests/context.py` are imported by no test.
- `cpp/examples/protolists.proto` is referenced by nothing yet copied into every C++ tree.

### 13. Duplicated logic
- Five `for_model` if/elif ladders over the same ~17 class names (`python_symb.py:17-49`,
  `rust_symb.py:17-50`, `cpp_symb.py:14-47`, `markdown_symb.py:12-29`,
  `symbols/protobuf.py:14-33`). Replace with a dict registry on `ISymbolsProvider`.
- Four private base classes for symbols (`PythonSymbols`, `RustSymbols`, `CppSymbols`,
  markdown's) instead of the shared `lang_symb.ModelSymbols`; the wrapped model is named
  `_model`, `_arg`, `_iface`, `_prop`, `_payload`... depending on file. `CppSymbols.__init__`
  takes no config while the others do.
- The 13-line config-merge loop appears three times (`cli.py:73-86`, `cli.py:143-147`,
  `generic_generator.py:230-243`). Extract `merge_configs(paths) -> StingerConfig`.
- `components.py:17,19` imports the same two exceptions twice; line 18 is a wildcard import.
- `LanguageSymbolMixin.enhance` (`lang_symb.py:21`) constructs a new stevedore
  `ExtensionManager` (entry-point scan) for every model object; cache it at module level.

### 14. Error handling
- `stinger generate` has no try/except anywhere (`cli.py:25-58`): malformed YAML, a schema
  violation, or a typo in a TOML config key all exit with a raw traceback. `generate` never
  runs the JSON-schema validator at all; only `validate` does.
- `components.py:519-592`: seven copy-pasted `except TypeError` blocks that omit the element
  name from the message, do not `raise ... from e`, and catch only `TypeError`. The enums
  block at line 523 says "Signal specification appears to be invalid".
- `cli.py:158` catches bare `Exception` and reports internal bugs as validation errors with no
  traceback and no `--debug` flag.
- Input validation via `assert` (`components.py:112,519...`, `cli.py:86`) is stripped by `-O`.
- `cli.py:126-130` accepts 0.1/0.2 version prefixes for schema selection while
  `components.py:504` rejects anything but exactly `0.3.0`, so an old file passes stage one
  and fails stage two with a generic message.
- `asyncapi.py:184`: docstring contains `\}`; compiling with `-W error` fails.

### 15. CLI ergonomics
- No `--version`, no `--dry-run` (the output file list is already computed at
  `generic_generator.py:377-381` before anything is written), no `--quiet`; every run dumps
  the full merged config and one line per template entry.
- `cli.py:50-58` calls `generic_generator.main` twice when both `--language` and
  `--template-path` are given, rendering everything twice.
- Valid languages are hardcoded in three places (`cli.py:28,49`); derive from the templates
  directory or a typer `Enum`.
- `generic_generator.py:413` uses `shutil.copyfile`, which drops the executable bit.
- The `partials` skip is `entry.endswith("partials")` (line 386), applied in the render walk
  but not in `recursive_find_output_files` (356-376), so `output_files` lists phantom paths.

### 16. Test coverage gaps
Well covered: the four `ipc_*` models, topic utilities, protobuf resolution, example values.
Untested: `asyncapi.py` (875 lines, the largest module), `filtering.py` (301 lines of pure
dict functions), `markdown_symb.py`, `symbols/protobuf.py`, `topics.py` validators, `cli.py`
(no `CliRunner` tests, no exit-code assertions), `lang_symb.py`. The ~50 name/type properties
per language symbol provider have no direct tests. Generation is never invoked end to end
from pytest; that lives only in the Taskfile, which needs Rust, CMake, protoc, and Docker.
- Fix: a pytest that runs `generic_generator.main` for each example into a tmp dir for each
  built-in language and asserts it completes; golden-file tests for `markdown` and `asyncapi`
  output, which need no toolchain.

---

## P3: Templates and language parity

### 17. Rust ignores interface-declared QoS
Python, C++, web, and markdown render `stinger.*_qos`; `grep _qos stingeripc/templates/rust`
returns nothing. Rust hardcodes `QoS::ExactlyOnce`/`AtLeastOnce` in `message.rs.jinja2`,
`client.rs.jinja2:195,214,301,558`, `server.rs.jinja2:188-200`. The four targets disagree on
the wire.

### 18. Generated Python library misbehaves as a library
- `client.py.jinja2:31` and `server.py.jinja2:25`: `logging.basicConfig(level=DEBUG)` at
  import time forces DEBUG on the host application's root logger.
- `server.py.jinja2:153`: `signal.signal(SIGTERM, ...)` in the constructor; raises off the main
  thread and steals SIGTERM from the host.
- `server.py.jinja2:159`: `__del__` calls `shutdown()`; prefer a context manager.
- `server.py.jinja2:121`: unbounded `queue.Queue()`.
- Unconditional imports of `isodate`, `timedelta`, `asyncio`, `Future` that are unused unless
  the interface uses durations; `stinger.uses_duration()` already exists for gating.
- `client.py.jinja2:395` references `{{method_name}}` after its `endfor`; renders as
  `Handle '' method response.`

### 19. `rust/Cargo.lock.jinja2` should not exist as a template
1398 lines, two of them Jinja. It omits `jsonschema`, `prost`, `prost-types`, and
`jsonpath-rust`, which `Cargo.toml.jinja2` conditionally adds, so cargo rewrites it on first
build for nearly every interface. It provides no reproducibility and must be hand-edited on
every dependency bump.
- Fix: delete it and either ignore `Cargo.lock` for the library crate or run
  `cargo generate-lockfile` as a post-render step, the way `protoc` already runs.

### 20. Feature parity gaps
| Gap | Evidence |
|---|---|
| C++ has no LWT/presence helper | Python `lwt.py.jinja2`, Rust `lwt.rs.jinja2`; nothing in cpp |
| C++ has no docs target | Python has Sphinx, Rust has `docs/*.md` |
| C++ demos hardcode `localhost:1883` | Python and Rust demos read `MQTT_HOSTNAME` |
| Web target: no tests, no LWT, browser-only, `ws://` hardcoded to `/ws` (`app.js.jinja2:454`), AngularJS 1.8 (EOL 2022) from three CDNs with no integrity hashes, `// TODO: support all the topic params` (line 403) | last commit "wip protoweb" |
| `python/docs/api.rst.jinja2` emits an empty file for py37 | use the conditional-filename trick the web target uses |
| Rust `discovery.rs.jinja2:290` "TODO: semantically match the versions" | Python has `semver.py` |

### 21. Template maintainability
- No `trim_blocks`/`lstrip_blocks` anywhere, so whitespace `-` markers are applied by hand
  with ratios from 1.64 markers per tag (`python/partials/codec.jinja2`) to 0.21
  (`web/index.html.jinja2`). Python output is readable only because black runs afterward;
  Rust and C++ have no post-format step in the generate task.
- Rust `client.rs.jinja2` + `server.rs.jinja2` are 2105 lines with two partials; C++ has six.
  The topic-params block repeats 6x in C++ client, 5x in Rust client, 11x in Python client.
- Four independent `codec.jinja2` partials implement overlapping macro sets (22/16/6/6
  macros). Hoist payload-shape decisions into Python symbol objects so codecs only format.
- The conditional-filename convention (`{%if ...%}name.jinja2{%endif%}`) works but is
  documented nowhere; the name is rendered twice by two walkers. Add `templates/README.md`.
- Generated Python pins nothing (`pydantic>=2.11.7` admits 3.0); the four first-party runtime
  libraries (`pyqttier`, `py-stinger-conn-iface`, `stinger-python-utils`, `stinger-rwlock-watch`)
  move in lockstep with the generator and should get `~=` constraints keyed off
  `generator.version`.

---

## P4: Documentation

- README: no mention of the `asyncapi` subcommand, no description of what `web`, `markdown`,
  `protobuf` outputs are, says "C++11" while CMake sets 17, Rust example uses
  `set_signal_recv_callbacks_for_foo` and `register_add_numbers_handler` which do not match
  generated names, typo `.singeripc`. Link the `stinger-ipc/example-generated-code` repo so
  contributors know where generated output lives.
- `schemas/README.md` (349 lines, good) is not in the Sphinx toctree and has no Commands
  section. `example_interfaces/protoweather/README.md` is linked from nowhere. The `--config`
  TOML keys (`[properties] stinger_owned_values`, `version_tracking`, `[protobuf] path`,
  `[python] python37`) are documented nowhere.
- No CHANGELOG (621 commits, 7 tags, last tag `v0.9.6` on 2026-07-03 while pyproject is
  `0.11.0.dev2`; `v0.10.0a3` predates `v0.9.0a1`). No CONTRIBUTING.
- `glossary.md` has empty stubs for `interface` and `arg`.
- `CLAUDE.md` is accurate and useful; keep it in sync when items 1-2 move `schemas/`.

---

## Suggested order of work

1. Items 1, 2, 5, 6, 7 together as one "make the repo honest" PR: packaging fix, wheel check,
   CI running pytest/mypy/black on `develop`, fix the red checks.
2. Item 3 and 4 as one "method call lifecycle" PR across the three client templates plus the
   C++ server, verified with the existing generated integration tests.
3. Items 8-11 as a tooling cleanup PR.
4. Items 12-16 incrementally; item 13's registry refactor first since it unblocks typing the
   symbol providers.
5. Items 17-21 per language as separate PRs, each validated with the
   `compare-stinger-generated-code` skill.

## Verification

- Packaging: `uv build && unzip -l dist/*.whl | grep -E 'protoc.toml|clang-format|schemas/0.3'`.
- Repo health: `uv run pytest && uv run mypy stingeripc tests && uv run black --check stingeripc tests`.
- Generated code: `task python`, `task cpp`, `task rust` after each template change, then
  the `compare-stinger-generated-code` skill to confirm only intended diffs. The memory note
  says `rust:generate:protoweather` needs `protoc-gen-prost` locally; that is environmental.
- Method timeout fix: extend `python/tests/test_client.py.jinja2` and the Rust inline tests
  with a "no response" case that asserts a timeout error and an empty pending map.
