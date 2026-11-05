# Independent verification — citable summary

Prepared so that the result can be quoted or forwarded without reassembly.
Everything below is either a number from a run transcript in this repository, or a link that resolves to one.

## One line

> An independent verification was performed on `DSHCorrectover/ccs-conformance-vectors` by a party with no affiliation to Correctover or MolTrust, using no credentials and no privileged access. All six vector sets were verifiable; all six passed. Three of the six ship without an executor upstream and were exercised with independently written harnesses.

## Who

Xinghua Zhao (Steven Zhao) — independent researcher, LGD (Lifecycle Governance Doctrine) / SynomosAI initiative — ORCID 0009-0001-0512-1237.
No affiliation with Correctover or MolTrust. No funding, no employment, no advisory relationship.

## What was verified

| Vector set | Harness used | Result |
|---|---|---|
| `v1.4.0-conformance` | upstream `conformance_checker` | `ALL VECTORS PASSED`; 1477/1549 assertions at `effff90`, and again at `cb88218` where the fixed checker additionally reports `Receipts verified: 73/73` |
| `canonicalization-v1` | upstream checker | `Checks: 81/81 passed` (requires an LF checkout; CRLF gives a false mismatch) |
| `mustfail-v1` | **independent harness** (upstream ships none) | 15/15 verdicts match the declared expectation; 15/15 violated dimensions match; **14/14 minimal-repair cases flip to PASS**; 4/4 looseness negative controls behave |
| `v1.3.0` (`in-process-key`) | **independent harness** | 50/50 checks, including 2 tamper controls that must fail and do |
| `v1.1.20` (`reference-signed-001`) | **independent harness** | 10/10 checks, including 1 tamper control that must fail and does |
| `technical-fit-v1` | `verify_pilot.py` | C1–C6 signature checks; C5 (tampered) `INVALID` as required |

93 judgments in total, 0 failures.

The number that carries the most weight is `14/14`. For each of the 14 MUST-FAIL vectors, correcting only the single violating field — the amount `"9999"` becoming `9999`, one stale nonce replaced, one unpermitted tool swapped for a permitted one — turned the verdict to PASS. A gate that rejects everything scores 14/14 on rejection alone; only a gate whose rejection is *necessary and sufficient* scores 14/14 on repair.

## Two findings returned upstream

1. The checker's summary line reported `Cases: len/len`, a self-proof line that cannot fail. Reported as issue #2 and fixed in `c848fae`.
2. `mustfail-v1/README.md` states that a verifier scoring one call at a time will wrongly admit all three workflow traces. That holds for `W01` and `W02`. It does not hold for `W03`, whose tainted instruction origin is recorded in the per-call `instruction_provenance` field, where a single-call verifier can see it. A suggested clarification was offered; the vectors themselves are not wrong.

## Evidence

- Repository: <https://github.com/zhaoxinghua09-cell/ccs-independent-rerun>
- Run batch: <https://github.com/zhaoxinghua09-cell/ccs-independent-rerun/tree/main/runs/2026-11-05>
- Per-file SHA-256 manifest: <https://github.com/zhaoxinghua09-cell/ccs-independent-rerun/blob/main/manifest.json>
- Attestation and authorship, with external anchor: <https://github.com/zhaoxinghua09-cell/ccs-independent-rerun/blob/main/ATTESTATION.md>
- Upstream issue filed: <https://github.com/DSHCorrectover/ccs-conformance-vectors/issues/2>
- Upstream fix commit: <https://github.com/DSHCorrectover/ccs-conformance-vectors/commit/c848faeade7a2ad9d211cf065e0e1ef415b4a3e7>

Raw run transcripts are included unedited, including one run that aborted on a TLS failure and was rerun from a clean clone. The failed attempt was not deleted.

## Reproducing it

```
git -c core.autocrlf=false -c core.eol=lf clone --depth 1 \
  https://github.com/DSHCorrectover/ccs-conformance-vectors.git

python admission_verifier.py --vectors ccs-conformance-vectors/vectors/mustfail-v1
uv run --no-project --with jcs --with cryptography \
  python verify_sig_vectors.py --vectors ccs-conformance-vectors/vectors
```

Neither command needs a token, a key, or a network path other than public HTTPS.

## Boundaries

- This is a verification of **reproducibility and conformance to the vectors' own declared criteria**. It is not a security review of the protocol, an evaluation of the design, or a statement about fitness for any particular deployment.
- Three of the six sets were exercised with harnesses written here, not by upstream. They are published alongside their results so the criteria can be checked, and any disagreement with upstream's intent should be read as a question, not a verdict.
- The counts above are tied to the commits named. Upstream was still receiving pushes on the day of the run; a later commit is a different object and would need its own run.
- This document was prepared by the verifier. It is not an endorsement of Correctover, MolTrust, or the applicant beyond the specific artifacts listed.
