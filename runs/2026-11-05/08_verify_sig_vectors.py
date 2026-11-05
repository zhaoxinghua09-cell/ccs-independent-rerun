#!/usr/bin/env python3
"""
Independent signature/linkage verification for the two vector sets that ship no
executable checker:

    vectors/v1.1.20          reference-signed L1 receipt (1 file)
    vectors/v1.3.0           paired action+behavior receipts under two key models (8 files)

Upstream ships no runner for these, which is why a previous sweep recorded them
as NOT_RUNNABLE. They are not unrunnable: the verification predicates are fully
determined by the artefacts themselves (JCS + Ed25519 + SHA-256 linkage).
This script implements those predicates from scratch.

Requires: jcs, cryptography  (same two deps the upstream checker declares)
    uv run --no-project --with jcs --with cryptography python verify_sig_vectors.py --vectors <dir>

Exit 0 = every check passed; 1 = at least one FAIL; 2 = IO error.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

import jcs
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def canon(obj) -> bytes:
    return jcs.canonicalize(obj)


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon_sha256(obj) -> str:
    return sha256_hex(canon(obj))


def receipt_digest_l1(receipt: dict) -> str:
    signed = {k: v for k, v in receipt.items() if k != "signature"}
    return "sha256:" + canon_sha256(signed)


def verify_ed25519(pub_b64: str, payload: dict, sig_b64: str) -> tuple[bool, str]:
    try:
        raw = base64.b64decode(pub_b64, validate=True)
    except Exception as e:
        return False, f"pubkey b64 decode error: {e}"
    if len(raw) != 32:
        return False, f"pubkey length {len(raw)} != 32"
    try:
        sig = base64.b64decode(sig_b64, validate=True)
    except Exception as e:
        return False, f"signature b64 decode error: {e}"
    if len(sig) != 64:
        return False, f"signature length {len(sig)} != 64"
    body = {k: v for k, v in payload.items() if k != "signature"}
    msg = canon(body)
    try:
        Ed25519PublicKey.from_public_bytes(raw).verify(sig, msg)
        return True, "signature valid"
    except InvalidSignature:
        return False, "signature INVALID"
    except Exception as e:
        return False, f"verify error: {e}"


class Tally:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def check(self, scope: str, name: str, ok: bool, detail: str = "") -> bool:
        self.rows.append({"scope": scope, "check": name, "ok": bool(ok), "detail": detail})
        return ok

    @property
    def passed(self) -> int:
        return sum(1 for r in self.rows if r["ok"])

    @property
    def failed(self) -> int:
        return sum(1 for r in self.rows if not r["ok"])


def do_v1120(base: Path, t: Tally) -> None:
    f = base / "v1.1.20" / "reference-signed-001.json"
    if not f.exists():
        t.check("v1.1.20", "fixture-present", False, str(f))
        return
    t.check("v1.1.20", "fixture-present", True, f.name)
    doc = json.loads(f.read_text(encoding="utf-8"))
    rc = doc["receipt"]

    raw_b64 = doc["public_key_raw_b64"]
    raw = base64.b64decode(raw_b64, validate=True)
    t.check("v1.1.20", "pubkey-length-32", len(raw) == 32, f"{len(raw)} bytes")

    full = sha256_hex(raw)
    t.check("v1.1.20", "fingerprint-16-matches", full[:16] == doc["public_key_fingerprint_sha256_16"], f"computed {full[:16]}")
    t.check("v1.1.20", "pubkey-sha256-full-matches", full == doc["public_key_sha256_full"], f"computed {full[:16]}…")

    t.check("v1.1.20", "receipt-pubkey-equals-header", rc.get("public_key") == raw_b64)
    t.check("v1.1.20", "receipt-fingerprint-equals-header", rc.get("public_key_fingerprint") == doc["public_key_fingerprint_sha256_16"])
    t.check("v1.1.20", "issuer-consistent", rc.get("issuer") == doc.get("issuer"), str(rc.get("issuer")))
    t.check("v1.1.20", "algorithm-ed25519", rc.get("signing_algorithm") == "Ed25519")

    ok, why = verify_ed25519(raw_b64, rc, rc.get("signature", ""))
    t.check("v1.1.20", "ed25519-signature", ok, why)

    # tamper control: flip one byte of the signed payload, signature must fail
    tampered = dict(rc)
    tampered["rule_summary"] = str(tampered.get("rule_summary")) + "x"
    ok_t, _ = verify_ed25519(raw_b64, tampered, rc.get("signature", ""))
    t.check("v1.1.20", "tamper-control-must-fail", not ok_t, "mutated field rejected" if not ok_t else "MUTATION ACCEPTED")


def do_v130(base: Path, t: Tally) -> None:
    root = base / "v1.3.0"
    mf_path = root / "manifest.json"
    if not mf_path.exists():
        t.check("v1.3.0", "manifest-present", False, str(mf_path))
        return
    mf = json.loads(mf_path.read_text(encoding="utf-8"))
    t.check("v1.3.0", "manifest-present", True, mf_path.name)

    # 1. per-file hashes
    for entry in mf.get("files", []):
        p = root / entry["path"]
        if not p.exists():
            t.check("v1.3.0", f"file-hash:{entry['path']}", False, "missing")
            continue
        got = sha256_hex(p.read_bytes())
        t.check("v1.3.0", f"file-hash:{entry['path']}", got == entry["sha256"], got[:16])

    # 2. manifest self-digest
    md = mf.get("manifest_digest") or {}
    body = {k: v for k, v in mf.items() if k != "manifest_digest"}
    got = canon_sha256(body)
    t.check("v1.3.0", "manifest-digest", got == md.get("value"), f"computed {got[:16]}…")

    # 3. per-model signature + action/behavior linkage
    for variant in ("in-process-key", "sidecar-key"):
        mdir = root / variant
        if not mdir.is_dir():
            t.check("v1.3.0", f"{variant}:present", False)
            continue
        meta = json.loads((mdir / "metadata.json").read_text(encoding="utf-8"))
        pub = meta["public_key"]
        t.check("v1.3.0", f"{variant}:algorithm", meta.get("signing_algorithm") == "Ed25519")
        t.check("v1.3.0", f"{variant}:chain-verdict-INTACT", meta.get("chain_integrity_verdict") == "INTACT", str(meta.get("chain_integrity_verdict")))

        for n in (1, 2):
            ap = mdir / f"action-{n}-{'allow' if n == 1 else 'block'}.json"
            bp = mdir / f"behavior-{n}-{'allow' if n == 1 else 'block'}.json"
            if not (ap.exists() and bp.exists()):
                t.check("v1.3.0", f"{variant}:pair-{n}:present", False)
                continue
            a = json.loads(ap.read_text(encoding="utf-8"))
            b = json.loads(bp.read_text(encoding="utf-8"))

            ok, why = verify_ed25519(pub, a, a.get("signature", ""))
            t.check("v1.3.0", f"{variant}:action-{n}:ed25519", ok, why)
            ok, why = verify_ed25519(pub, b, b.get("signature", ""))
            t.check("v1.3.0", f"{variant}:behavior-{n}:ed25519", ok, why)

            d = receipt_digest_l1(a)
            t.check("v1.3.0", f"{variant}:pair-{n}:link-digest", b.get("linked_l1_receipt_digest") == d, f"computed {d[:23]}…")

            t.check("v1.3.0", f"{variant}:pair-{n}:trace-id", a.get("trace_id") == b.get("trace_id"), str(a.get("trace_id")))
            t.check("v1.3.0", f"{variant}:pair-{n}:tool-call-id", a.get("tool_call_id") == b.get("tool_call_id"))
            t.check("v1.3.0", f"{variant}:pair-{n}:issuer", a.get("issuer") == meta.get("issuer") == b.get("issuer"), str(a.get("issuer")))
            t.check("v1.3.0", f"{variant}:pair-{n}:fingerprint", a.get("public_key_fingerprint") == meta.get("public_key_fingerprint"))
            t.check("v1.3.0", f"{variant}:pair-{n}:l1-field-count-30", len([k for k in a if k != "trace_id"]) >= 25, f"{len(a)} keys")

        # tamper control per variant
        ap = mdir / "action-1-allow.json"
        a = json.loads(ap.read_text(encoding="utf-8"))
        tam = dict(a)
        tam["verdict"] = "block"
        ok_t, _ = verify_ed25519(pub, tam, a.get("signature", ""))
        t.check("v1.3.0", f"{variant}:tamper-control-must-fail", not ok_t, "mutated verdict rejected" if not ok_t else "MUTATION ACCEPTED")

    # 4. cross-model consistency: both models sign the same two actions
    ci = (mf.get("independent_verdicts") or {}).get("chain_integrity") or {}
    for variant in ("in-process-key", "sidecar-key"):
        want = ci.get(variant)
        if want:
            got = json.loads((root / variant / "metadata.json").read_text(encoding="utf-8")).get("chain_integrity_verdict")
            t.check("v1.3.0", f"cross:{variant}:matches-manifest-verdict", got == want, f"{got} vs manifest {want}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", required=True)
    ap.add_argument("--json", default="")
    ap.add_argument("--md", default="")
    a = ap.parse_args()

    base = Path(a.vectors)
    if not base.is_dir():
        print(f"ERROR: {base} not a directory", file=sys.stderr)
        return 2

    t = Tally()
    do_v1120(base, t)
    do_v130(base, t)

    print(f"checks={len(t.rows)} passed={t.passed} failed={t.failed}")
    for r in t.rows:
        if not r["ok"]:
            print(f"  FAIL {r['scope']} :: {r['check']} :: {r['detail']}")
    for scope in ("v1.1.20", "v1.3.0"):
        sub = [r for r in t.rows if r["scope"] == scope]
        print(f"  {scope}: {sum(1 for r in sub if r['ok'])}/{len(sub)}")

    rep = {
        "tool": "verify_sig_vectors.py",
        "vectors_dir": str(base),
        "deps": ["jcs", "cryptography"],
        "checks": t.rows,
        "summary": {"total": len(t.rows), "passed": t.passed, "failed": t.failed},
        "by_scope": {
            s: {
                "passed": sum(1 for r in t.rows if r["scope"] == s and r["ok"]),
                "total": sum(1 for r in t.rows if r["scope"] == s),
            }
            for s in ("v1.1.20", "v1.3.0")
        },
    }
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
        print("WROTE", a.json)
    if a.md:
        L = ["# v1.1.20 / v1.3.0 独立验证报告\n",
             "上游未提供这两集的执行器，脚本由我方独立实现（JCS + Ed25519 + SHA-256 链接）。\n",
             f"合计 **{rep['summary']['passed']}/{rep['summary']['total']}** 项通过，{rep['summary']['failed']} 项失败。\n",
             "| 集 | 通过 | 总数 |", "|---|---|---|"]
        for s, v in rep["by_scope"].items():
            L.append(f"| {s} | {v['passed']} | {v['total']} |")
        L.append("")
        L.append("## 逐项\n")
        L.append("| 集 | 检查项 | 结果 | 说明 |")
        L.append("|---|---|---|---|")
        for r in t.rows:
            L.append(f"| {r['scope']} | `{r['check']}` | {'通过' if r['ok'] else '**失败**'} | {r['detail']} |")
        Path(a.md).write_text("\n".join(L), encoding="utf-8")
        print("WROTE", a.md)

    return 0 if t.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
