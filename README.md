# Independent re-run of the CCS conformance vectors

An unrelated-party re-run record for the CC0 conformance vectors published by
Correctover at `DSHCorrectover/ccs-conformance-vectors`, contributed as input
to the W3C `public-agent-conformance` discussion on intake criteria for
submitted reference suites.

Maintainer: Steven Zhao (China), ORCID 0009-0001-0512-1237.
No affiliation with Correctover or MolTrust, and no economic interest in
either corpus. Prepared with AI assistance.

## What was run

| | |
|---|---|
| Corpus | `DSHCorrectover/ccs-conformance-vectors` (CC0 1.0; checker under MIT) |
| Corpus commit | `effff90f231d11bb3be93d3d0d0792f36934cc78` (2026-09-30) |
| Clone command | `git -c core.autocrlf=false clone https://github.com/DSHCorrectover/ccs-conformance-vectors.git` |
| Why `-c core.autocrlf=false` | the corpus pins file bytes by digest; line-ending conversion changes every digest |
| Runtime | Windows 11; Python with `jcs` + `cryptography` (ephemeral env via `uv run --with jcs --with cryptography`) |
| Date of run | 2026-10-12 (UTC+8) |

## Commands and results

Result codes follow the CSSWG implementation-report convention
(`pass` / `fail` / `uncertain` / `invalid` / `na`).

```
target / result / command-or-note

vectors/v1.4.0-conformance / pass /
  uv run --no-project --with jcs --with cryptography \
    python checkers/independent_checker.py vectors/v1.4.0-conformance
  exit code 0; "Checks: 1477/1549 passed" (the 72 non-passing checks are
  the expected negatives); "ALL VECTORS PASSED". Full log:
  run_v1.4.0-conformance.txt

vectors/mustfail-v1 / na /
  same checker, same environment; output:
  "No case directories with expected.json found", preceded by
  "Manifest verified (mustfail-v1/manifest.json)". Full log:
  run_mustfail-v1.txt
```

Note on the summary line `Cases: N/N matched expected outcome`: in the
checker at this commit the numerator and the denominator are the same
expression, so that line carries no matching information. The signals this
record relies on are the exit code, the `Checks:` line, and the
`ALL VECTORS PASSED` / `SOME VECTORS FAILED` banner, which are computed
from distinct counters.

## Negative controls

Two deliberate faults, each in a fresh directory (no file is deleted or
mutated in place); script: `negative_controls.py`, captured output:
`negative_controls_output.txt`.

```
control / result / expected and observed

NC-A / pass /
  tamper a manifest-covered file, leave the manifest untouched.
  expected: exit 1 and the manifest gate fires.
  observed: exit 1; "MANIFEST VERIFICATION FAILED:" with a hash mismatch
  on 01-allow/receipt.json.

NC-B / pass /
  tamper the receipt AND re-pin the manifest so the manifest gate passes.
  expected: exit 1 with the manifest gate passing and a case verdict
  failing.
  observed: exit 1; first line "Manifest verified (_ncB/manifest.json)",
  then "FAIL 01-allow", "Checks: 1476/1549 passed",
  "SOME VECTORS FAILED".
```

Together these two show the two gates the suite ships can each fail on a
fault built for it, and that a fault which satisfies the digest gate is
still caught by the verdict gate.

## What this record establishes and what it leaves open

Established by this run, at the receipt-evidence layer
(`vectors/v1.4.0-conformance`): the shipped checker reproduces on an
unrelated machine, all 66 cases resolve to their expected outcomes, and
both deliberate faults above are caught.

Left open, at the admission-decision layer (`vectors/mustfail-v1`): the 15
vectors carry expectations inside `vectors.jsonl` and each `case.json`
(14 MUST-FAIL, 1 MUST-PASS control), but the release ships no runnable
adjudicator for that layer, so an unrelated party cannot produce a
machine-adjudicated result there; the documented workflow is to supply
one's own verifier and self-report. This record makes no claim about that
layer, and none about the usability or soundness of the corpus, which the
upstream README already describes accurately.

## Files

| file | content |
|---|---|
| `run_v1.4.0-conformance.txt` | full checker log, receipt-evidence layer |
| `run_mustfail-v1.txt` | full checker log, admission-decision layer |
| `negative_controls.py` | the two deliberate-fault controls (no in-place mutation) |
| `negative_controls_output.txt` | captured output and exit codes of both controls |

## License

MIT for this record (see `LICENSE`). The upstream corpus and its checker
carry their own licences; nothing from them is redistributed here beyond
the command output shown above.
