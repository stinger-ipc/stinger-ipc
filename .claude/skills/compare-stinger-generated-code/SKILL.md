---
name: compare-stinger-generated-code
description: |
  Validates that stinger-ipc code generation changes are intentional by diffing output before and after a code change. Stashes current changes, runs `GENERATED_DIR=./original task generate`, pops the stash, runs `GENERATED_DIR=./modified task generate`, diffs the two trees, and reports which changes are intentional (expected from what the agent changed) versus unintentional (surprises). Use this skill whenever the user wants to verify, audit, or check what changed in generated output — e.g. "did my template change only affect what I expected?", "check the generated output", "validate generated files", "make sure nothing unexpected changed", or "diff generated code before and after my change".
---

# Compare Stinger Generated Code

You are validating that a stinger-ipc code change only affected the generated output the user intended. The workflow runs the generator twice — against the original code and the modified code — then compares the results.

---

## Step 1 — Understand the intent

Before running anything, check the conversation for context: **what did the user change, and what generated output should that affect?**

If it's already clear from the conversation, note it and proceed. If not, ask one short question: "What did you change and what output were you expecting to affect?"

You'll use this in Step 5 to classify each diff hunk as intentional or unintentional.

---

## Step 2 — Stash all current changes

```bash
git stash
```

Confirm the stash succeeded and the working tree is clean:

```bash
git status --porcelain
```

If there's nothing to stash (no uncommitted changes), stop and tell the user — there's nothing to compare.

If the stash fails, stop and report the error before proceeding.

---

## Step 3 — Generate the baseline into `./original`

First, remove any stale output trees from previous runs so old artifacts cannot pollute the comparison:

```bash
rm -rf ./original ./modified
```

```bash
GENERATED_DIR=./original task generate
```

This runs the generator against the *pre-change* (stashed) code. Output lands in `./original/`.

If this command fails, pop the stash before reporting the error:

```bash
git stash pop
```

---

## Step 4 — Restore changes and generate the modified output

```bash
git stash pop
```

If the pop produces merge conflicts, stop immediately — don't proceed with a conflicted working tree.

Then regenerate with the user's changes applied:

```bash
GENERATED_DIR=./modified task generate
```

Output lands in `./modified/`.

---

## Step 5 — Diff the two trees

```bash
diff -r --unified=3 ./original ./modified > /tmp/stinger_gen_diff.txt 2>&1
wc -l /tmp/stinger_gen_diff.txt
```

Read the diff file. If it's large (hundreds of lines), work through it by file/directory.

Classify each changed file into one of two buckets based on the user's stated intent:

**Intentional** — A direct, expected consequence of the change. Examples:
- User updated a Python template → the rendered `.py` files changed accordingly
- User added a field to an interface → all generated languages now include that field
- User changed a filter or transformer → output reflects the new transformation

**Unintentional** — Present but not expected. Common causes:
- A collateral change in a language/format the user didn't intend to touch
- Non-determinism in the generator (ordering, timestamps)
- A bug introduced by the change that affected more than it should have

**Ignore / do not report** — Known noise that is neither intentional nor worth surfacing:
- Differences in generated *example* files (e.g. `server_demo.py`, `*_demo.*`, `example_*`). These contain random example values produced by `get_random_example_value()` which uses a non-deterministic seed, so they vary between runs and are meaningless for comparison purposes.

When in doubt, surface it as unintentional — better to over-report than to silently miss something.

---

## Step 6 — Report to the user

```
## Stinger Generated Code Comparison

### ✅ Intentional changes
- <file or pattern>: <why this was expected>

### ⚠️ Unintentional changes — review needed
- <file>: <what changed and why it's surprising>
  <relevant diff hunk>

### No differences
<only mention if useful context>
```

If everything looks intentional, say so clearly. If there are unintentional changes, paste the relevant diff hunks inline so the user doesn't have to go dig through `/tmp/stinger_gen_diff.txt` themselves.

---

## Step 7 — Offer to clean up

Ask the user whether to remove the temporary directories:

```bash
rm -rf ./original ./modified
```

Don't do this automatically — they may want to inspect the output further.
