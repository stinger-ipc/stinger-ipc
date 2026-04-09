---
name: stinger-release
description: |
  Full release workflow for the stinger-ipc Python package: bump the version in pyproject.toml, run the task suite, build with uv, create and push a git tag, and publish to PyPI with uv publish. Use this skill whenever the user wants to release, publish, cut a version, ship, or bump stinger-ipc — even if they just say "release it" or "push a new version".
---

# Stinger-IPC Release Workflow

Work through the steps below in order. Pause only when a decision can't be inferred (e.g. which version component to bump).

---

## Step 1 — Determine the new version

Read the `version` field from `pyproject.toml` (it follows semver: MAJOR.MINOR.PATCH, with optional `.postN` suffix).

Ask the user which component to bump **only if they haven't already told you**:
- Bug-fix / maintenance → bump **patch** (most common)
- New backwards-compatible feature → bump **minor**
- Breaking changes → bump **major**

Confirm the new version before proceeding (e.g. "I'll bump from 0.7.6.post1 → 0.7.7. Shall I proceed?").

---

## Step 2 — Check for uncommitted changes

```bash
git status --porcelain
```

If there are uncommitted changes, **stop and tell the user**. A release tag should point at a clean, committed tree.

---

## Step 3 — Bump the version in pyproject.toml

Edit the `version = "..."` line under `[project]` in `pyproject.toml`. Be precise — don't touch version strings in dependency declarations.

---

## Step 4 — Synchronize `schemas/README.md` with the schema

Compare `schemas/schema.yaml` against `schemas/README.md`. Update the README so that every feature, type, field, and constraint documented in the README accurately reflects the schema. In particular, watch for:

- Argument types (the valid `type` enum values in the schema)
- Argument fields (`index`, `example`, `schema`, `optional`, `enumVersion`, `structVersion`, etc.)
- Top-level sections (`enums`, `structures`, `constants`, `signals`, `methods`, `properties`)
- Component fields (`version`, `consumers`, `readOnly`, `documentation`, etc.)
- The `stingeripc` key and its allowed version values
- Interface metadata fields (`name`, `version`, `title`, `summary`, `license`, `documentation`)

If the README is already up to date, skip this step. If changes are made, stage them:

```bash
git add schemas/README.md
```

---

## Step 5 — Run the task suite

```bash
task
```

This runs generate + tests + compile checks across all language targets. If anything fails, stop and report the errors. Do not proceed with a broken build.

---

## Step 6 — Build the package

```bash
uv build
```

Fix any build errors before continuing.

---

## Step 7 — Commit the version bump

```bash
git add pyproject.toml
git commit -m "chore: bump version to <new_version>"
```

If `schemas/README.md` was updated in Step 4, include it in the commit (or make a separate commit):
```bash
git add schemas/README.md
git commit -m "docs: sync schemas/README.md with schema.yaml"
```

---

## Step 8 — Create and push a git tag

```bash
git tag v<new_version>
git push origin v<new_version>
```

Also push the commit if the branch hasn't been pushed yet:
```bash
git push
```

---

## Step 9 — Publish to PyPI

Check for the publish token:

```bash
echo $UV_PUBLISH_TOKEN
```

If `UV_PUBLISH_TOKEN` is set, publish directly:
```bash
uv publish
```

If it is **not** set, ask the user for the token, then run:
```bash
uv publish --token <token>
```

Do not log or display the token value in output.

---

## Done

Confirm the release is complete: report the new version, tag name, and PyPI publish status. If anything failed at any step, clearly describe the failure and what the user should do next.
