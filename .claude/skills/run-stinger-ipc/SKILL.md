---
name: run-stinger-ipc
description: Build, run, validate, and generate code with the stinger-ipc CLI, and prove the generated Python client/server pairs actually talk over a live MQTT broker. Use when asked to run stinger-ipc, generate code from a .stinger.yaml file, validate an interface, demo or integration-test the generator's output, or verify a template/generator change works end to end.
---

stinger-ipc is a CLI code generator (`stinger`/`stinger-ipc`), not a long-running
app — "running" it means invoking `stinger generate`/`validate`, and the real
proof of correctness is that the *generated* client and server code can talk to
each other over a real MQTT broker. Drive it via the CLI directly, and use
`.claude/skills/run-stinger-ipc/integration_test.sh` for the live round-trip
proof — it exercises every bundled example interface, not just one.

All paths below are relative to the repo root.

## Prerequisites

An MQTT broker reachable at `localhost:1883` (only needed for the live
integration test, not for `generate`/`validate` or the unit tests):

```bash
sudo apt-get install -y mosquitto mosquitto-clients
mosquitto -d
```

## Setup

```bash
uv sync
```

This also puts `stinger`/`stinger-ipc` on the venv's `PATH` (`uv run stinger ...`).

## Run (agent path): CLI

```bash
uv run stinger validate example_interfaces/simple/simple.stinger.yaml
# -> ✅  No validation errors found in example_interfaces/simple/simple.stinger.yaml

uv run stinger generate example_interfaces/simple/simple.stinger.yaml /tmp/out --language python
# -> ... GENER: lines for every rendered file ..., "Generation for 'python' completed."
```

`validate` on a file that violates the schema exits 2 and prints the JSON
Schema failure plus the offending path, e.g. for an arg with
`type: not_a_real_type`:

```
❌  Validation errors found in ...:
Error: {"name":"message","type":"not_a_real_type"} is not valid under any of the
schemas listed in the 'oneOf' keyword
...
Error constructing interface: unknown arg type: not_a_real_type
```

`--language` accepts `rust`, `python`, `markdown`, `cpp`, `web`, `protobuf`.
`task generate` (see [Taskfile.yml](../../../Taskfile.yml)) regenerates
[generated/](../../../generated/) for every example interface and language in
one shot — useful before comparing output, but slow; prefer the
`compare-stinger-generated-code` skill when the goal is "did my template
change do what I expected."

## Run (agent path): live integration test, every example interface

`generate` alone only proves the templates render. To prove the *output*
actually implements IPC, every generated Python project ships a
`server_integration_test.py` / `client_integration_test.py` pair: the server
exercises every signal/method/command/property once and validates what it
receives, the client does the same from the other side, and each prints
`[CHECK] <name> ... PASS|FAIL` lines plus a final `RESULT: PASS|FAIL (n/m
checks)` — self-checking and bounded, no manual inspection required.
[integration_test.sh](integration_test.sh) generates a fresh project per
interface, runs that pair over the real broker, and reports both sides:

```bash
.claude/skills/run-stinger-ipc/integration_test.sh
# === full (/tmp/stinger-integration-test.full.XXXXXX) ===
#   client: RESULT: PASS (20/20 checks)
#   server: RESULT: PASS (11/11 checks)
# === simple (...) ===
#   client: RESULT: PASS (6/6 checks)
#   server: RESULT: PASS (3/3 checks)
# ... signal_only, weather, prop-only ...
# ALL INTERFACES PASSED
```

With no arguments it runs every interface in its default list (`full`,
`simple`, `signal_only`, `weather`, `prop-only`) and exits 0 only if every one
of them passes on both sides. Pass an interface name to run just that one:

```bash
.claude/skills/run-stinger-ipc/integration_test.sh weather
```

Each interface gets its own fresh `/tmp/stinger-integration-test.<iface>.*`
project with `server.log`/`client.log` inside — left behind for inspection;
delete with `rm -rf /tmp/stinger-integration-test.*` when done. Total runtime
for the default set is well under a minute.

`testable` and `protoweather` are deliberately not in the default list — see
Gotchas.

## Test

```bash
uv run pytest -q
```

As of this branch (`develop`, commit `ca3c86fd`): 314 passed, 1 known failure
(`tests/test_protobuf_payloads.py::...::test_signal_carries_a_protobuf_payload`,
`AttributeError: 'NoneType' object has no attribute 'mime_type'`) — matches
the in-progress "WIP content-type" work visible in recent commits, not a
regression from anything in this skill.

## Gotchas

- **`testable` is excluded from `integration_test.sh`'s default list.** It's
  an exhaustive "capture most variants of features" interface (30+ signals,
  20+ methods, every type). Its generated client decodes a `binary`-typed
  signal argument as a base64 *string* instead of `bytes` (a
  `PlainSerializer` on the payload model applies to `model_dump()`
  unconditionally, not just JSON encoding), which fails that one comparison
  and cascades: the resulting delay pushes later method/command/property
  checks past the server's default `MAX_LIFETIME_SECONDS`, so it self-exits
  before the client gets to them. Pre-existing, unrelated to this skill —
  run it explicitly (`integration_test.sh testable`) if you need to
  reproduce it, with a longer budget: `MAX_LIFETIME_SECONDS=90` on the
  server and a longer `timeout` around the client.
- **`protoweather` needs extra generator config** (`--config
  example_interfaces/protobuf-path.toml`, per `Taskfile.yml`'s
  `PROTO_CONFIG`) that `integration_test.sh` doesn't pass, so it's left out
  of the default list rather than failing.
- **`uv run <script>` doesn't exec-replace itself** — it keeps a separate
  `uv run ...` process alive as the parent of the actual `python3`
  interpreter. Killing only the launcher PID leaves the real server running.
  `integration_test.sh` kills every PID whose cmdline matches the run's own
  temp directory, which catches both.
- **The generated scripts buffer stdout when not attached to a tty.** If you
  redirect `server_integration_test.py`/`client_integration_test.py` output
  to a file yourself (rather than via `integration_test.sh`, which already
  sets this), set `PYTHONUNBUFFERED=1` or their `[CHECK]`/`RESULT` lines may
  not be flushed before the process ends.
- **`pkill` inside this sandbox aborts the whole shell command** if no
  process matches (even with `|| true` after it) — use `pgrep`+`kill`, or
  plain `kill <pid>`, instead of `pkill` for process cleanup here.
- **Retained MQTT state can outlive a run.** The interface-discovery message
  and property values are published with `retain=1`, so a service ID reused
  across two unrelated tools (e.g. testing the same interface by hand in
  Python and Rust with different `CLIENT_ID`s but the same broker) can leave
  a stale advertisement another client's wildcard discovery subscription
  picks up. `integration_test.sh` avoids this by giving each run a fresh
  temp project, but if you drive the generated scripts by hand and discovery
  finds an instance that shouldn't exist anymore, clear it with
  `mosquitto_pub -h 127.0.0.1 -p 1883 -t '<topic>' -r -n`.

## Troubleshooting

- **`stinger validate` prints a Rich traceback instead of a validation
  error**: the input isn't well-formed YAML (e.g. mismatched `:`/`[`), which
  crashes the YAML parser (`ruamel.yaml`/`jacobsjsondoc`) rather than
  producing the schema-violation message shown in "Run (agent path)" above.
  Fix the YAML syntax first; schema violations on syntactically valid YAML
  do produce the clean `❌ Validation errors found in ...` message.
- **A `[CHECK] ... FAIL` line in `integration_test.sh` output**: read the
  full `client.log`/`server.log` in the printed temp directory — the
  `[CHECK]` line's detail usually names the expected vs. actual value
  directly. Cross-check against Gotchas above before assuming it's new.
- **`No MQTT broker reachable at localhost:1883`**: nothing is listening on
  1883. Start one with `mosquitto -d` (installed via
  `apt-get install mosquitto`).
