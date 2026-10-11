#!/usr/bin/env python3
"""Negative controls for the CCS conformance suite.

NC-A: tamper a manifest-covered file, leave manifest alone
      -> EXPECT manifest gate to fire (exit 1, "MANIFEST VERIFICATION FAILED")
NC-B: tamper a receipt AND re-pin the manifest to match
      -> EXPECT manifest gate to PASS but a case verdict to FAIL (exit 1)

No deletion is performed: each control gets a fresh directory name.
"""
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys

REPO = os.getcwd()
PY = sys.executable
SRC = os.path.join(REPO, "vectors", "v1.4.0-conformance")
CHECKER = os.path.join(REPO, "checkers", "independent_checker.py")


def fresh_copy(dst):
    if os.path.exists(dst):
        print("  (dest exists, reusing name with suffix)")
        dst = dst + "-b"
    shutil.copytree(SRC, dst)
    return dst


def run_checker(target):
    p = subprocess.run([PY, CHECKER, target], capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    print("=" * 70)
    print("NC-A : tamper a manifest-covered file, manifest untouched")
    print("=" * 70)
    a = fresh_copy("_ncA")
    target = os.path.join(a, "01-allow", "receipt.json")
    raw = open(target, "rb").read()
    open(target, "wb").write(raw + b"\n")
    rc, out = run_checker(a)
    print("  exit =", rc)
    print("  first line:", out.strip().splitlines()[0] if out.strip() else "(none)")
    print("  => EXPECTED: exit 1 + MANIFEST VERIFICATION FAILED")
    print("  => NC-A", "WORKS (gate can fail)" if rc == 1 and "MANIFEST VERIFICATION FAILED" in out else "DID NOT FIRE")

    print()
    print("=" * 70)
    print("NC-B : tamper receipt AND re-pin manifest so manifest gate passes")
    print("=" * 70)
    b = fresh_copy("_ncB")
    target = os.path.join(b, "01-allow", "receipt.json")
    obj = json.load(open(target, encoding="utf-8"))
    before = obj.get("signature")
    obj["signature"] = base64.b64encode(b"\x00" * 64).decode()
    with open(target, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    new_digest = hashlib.sha256(open(target, "rb").read()).hexdigest()
    mpath = os.path.join(b, "manifest.json")
    man = json.load(open(mpath, encoding="utf-8"))
    man["files"]["01-allow/receipt.json"] = new_digest
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2)
    print("  signature before:", (before or "")[:24], "...")
    print("  signature after :", obj["signature"][:24], "...")
    print("  re-pinned digest applied to manifest")
    rc, out = run_checker(b)
    print("  exit =", rc)
    manifest_line = out.strip().splitlines()[0] if out.strip() else "(none)"
    print("  first line:", manifest_line)
    last = [l for l in out.strip().splitlines() if l.strip()][-1]
    print("  last line :", last)
    fails = [l for l in out.splitlines() if "FAIL" in l]
    print("  FAIL lines:", len(fails))
    for l in fails[:6]:
        print("   ", l.strip())
    ok = rc == 1 and "MANIFEST VERIFICATION FAILED" not in out
    print("  => NC-B", "WORKS (verdict gate can fail, manifest gate passed)" if ok else "UNEXPECTED")


if __name__ == "__main__":
    main()
