#!/usr/bin/env bash
# Generates Python code for one or all bundled example interfaces, then runs
# each one's generated server_integration_test.py against
# client_integration_test.py over a live MQTT broker - the real proof that
# the generator's output actually implements IPC, not just that it renders.
#
# Both scripts are self-checking: each prints "[CHECK] <name> ... PASS|FAIL"
# per thing it verifies and a final "RESULT: PASS|FAIL (n/m checks)" line,
# and the server exits on its own once satisfied (or after a timeout) - so
# this driver only needs to launch them, wait, and report.
#
# Usage: integration_test.sh [INTERFACE]
#   INTERFACE   run just this interface (default: run every interface below)
#
# Requires an MQTT broker reachable at localhost:1883 (mosquitto).
set -uo pipefail

# testable and protoweather are deliberately excluded: testable is an
# exhaustive-type-coverage stress interface that currently trips known,
# separate bugs in binary-field (de)serialization unrelated to this skill's
# own templates, and protoweather needs extra protobuf generator config this
# driver does not pass. See SKILL.md Gotchas.
DEFAULT_INTERFACES=(full simple signal_only weather prop-only)

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

if ! mosquitto_pub -h 127.0.0.1 -p 1883 -t 'stinger-ipc/integration-test/probe' -m ping >/dev/null 2>&1; then
    echo "No MQTT broker reachable at localhost:1883. Start one with: mosquitto -d" >&2
    exit 1
fi

run_one() {
    local iface="$1"
    local iface_file="$REPO_ROOT/example_interfaces/$iface/$iface.stinger.yaml"
    if [[ ! -f "$iface_file" ]]; then
        echo "No such interface file: $iface_file" >&2
        return 1
    fi

    local outdir
    outdir="$(mktemp -d "/tmp/stinger-integration-test.${iface}.XXXXXX")"
    echo "=== $iface ($outdir) ==="

    (cd "$REPO_ROOT" && uv run stinger generate "$iface_file" "$outdir" --language python) \
        2>&1 | tail -3
    (cd "$outdir" && uv sync -q)

    (cd "$outdir" && PYTHONUNBUFFERED=1 uv run python examples/server_integration_test.py \
        > server.log 2>&1 &)
    sleep 2

    (cd "$outdir" && PYTHONUNBUFFERED=1 timeout 30 uv run python examples/client_integration_test.py \
        > client.log 2>&1)
    local client_exit=$?

    # The server exits on its own once every check it can verify has come in,
    # or after its own MAX_LIFETIME_SECONDS (default 15s) - for an interface
    # with nothing for it to verify (e.g. signal_only) that means it always
    # runs the full default 15s. Wait for its own RESULT line rather than
    # cutting it off before it reports one.
    local waited=0
    while [[ "$waited" -lt 30 ]] && ! grep -q '^RESULT:' "$outdir/server.log" 2>/dev/null; do
        sleep 1
        waited=$((waited + 1))
    done

    # `uv run` execs a child python process rather than replacing itself, so
    # the server has to be killed by matching its own directory in the
    # cmdline - the launcher PID alone leaves the real process running.
    mapfile -t server_pids < <(pgrep -f "$outdir/.*server_integration_test.py" || true)
    if [[ "${#server_pids[@]}" -gt 0 ]]; then
        kill -9 "${server_pids[@]}" 2>/dev/null || true
    fi

    local client_result server_result
    client_result="$(grep -E '^RESULT:' "$outdir/client.log" || echo 'RESULT: (client produced no result line)')"
    server_result="$(grep -E '^RESULT:' "$outdir/server.log" || echo 'RESULT: (server produced no result line)')"
    echo "  client: $client_result"
    echo "  server: $server_result"

    if [[ "$client_exit" -eq 0 ]] && [[ "$client_result" == RESULT:\ PASS* ]] && [[ "$server_result" == RESULT:\ PASS* ]]; then
        return 0
    fi
    return 1
}

if [[ $# -ge 1 ]]; then
    run_one "$1"
    exit $?
fi

overall=0
for iface in "${DEFAULT_INTERFACES[@]}"; do
    if ! run_one "$iface"; then
        overall=1
    fi
    echo
done

if [[ "$overall" -eq 0 ]]; then
    echo "ALL INTERFACES PASSED"
else
    echo "AT LEAST ONE INTERFACE FAILED - see per-interface RESULT lines above"
fi
exit "$overall"
