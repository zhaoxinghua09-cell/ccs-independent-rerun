# Independent rerun — 2026-11-05 batch

本次批次为 **外部独立复跑** 的原始转录（Windows 10 / git 2.47.1 / uv 0.12.3 / Python 3.13.12）。
全部运行 **零凭据、零 cookie、零登录态**，只访问公开仓库。

上游仓库：`https://github.com/DSHCorrectover/ccs-conformance-vectors`

---

## 批次一览

| # | 文件 | 目标 | 关键结果 | exit |
|---|---|---|---|---|
| 01 | `01_stranger_effff90.log` | 陌生人视角：全新 clone → 检出 `effff90` → 按上游 README 命令跑 `vectors/v1.4.0-conformance` | `Checks: 1477/1549 passed`、`Cases: 66/66`、`ALL VECTORS PASSED` | 0 |
| 02 | `02_stranger_main_cb88218.log` | 对当前 `main`（`cb88218`，2026-11-05 08:18:56 +0800）复跑同一向量集 | `Checks: 1477/1549 passed`、`Cases: 66/66`、**`Receipts verified: 73/73 admitted by manifest`**、`ALL VECTORS PASSED` | 0 |
| 03 | `03_negative_controls_utf8.log` | 负控 NC-A（篡改被 manifest 覆盖的文件，manifest 不动）/ NC-B（篡改 receipt 并重新钉住 manifest） | NC-A：`MANIFEST VERIFICATION FAILED` / NC-B：`Manifest verified` → `SOME VECTORS FAILED` + 2 条 FAIL 行 | 0 / 1 |
| 04 | `04_allsets_sweep.log` | 6 个向量集遍历（**`core.autocrlf=true` 环境**，见「已知环境坑」） | `v1.4.0-conformance` 通过；其余见下 | 混合 |
| 05 | `05_clean_clone_autocrlf_false.log` | 干净 clone（`core.autocrlf=false`、`core.eol=lf`、`--depth 1`），逐集复跑 + `technical-fit-v1` 的 C1–C6 逐例验签 | `canonicalization-v1`：`Checks: 81/81 passed`；`v1.4.0-conformance`：`1477/1549` + `Receipts 73/73`；C1–C4/C6 `VALID`，C5（篡改）`INVALID` | 见文件 |

机器可读汇总：`rerun_runs.json`

---

## 已知环境坑（两份转录必须并读）

**`04_allsets_sweep.log` 里 `canonicalization-v1` 报 `MANIFEST VERIFICATION FAILED` 是伪失败。**

原因：该次运行的环境 `core.autocrlf=true`，Git 在检出时把换行转成 CRLF，导致文件 SHA-256 与 manifest 记录不一致 —— 是**我方检出配置**问题，不是上游缺陷。

**`05_clean_clone_autocrlf_false.log` 用 `core.autocrlf=false -c core.eol=lf` 重新检出后，`canonicalization-v1` 得到 `Checks: 81/81 passed`。**

保留 04 这份「失败」转录，是为了让读者能看到这个坑本身，而不是只看到修好之后的结果。

**另一处需并读**：`02_stranger_main_cb88218.log` 开头有 `FETCH_EXIT=128`（`schannel: SSL/TLS connection failed`）。
该次 `git fetch` 因本机 TLS 握手失败而中断，`git pull` 同样失败（`PULL_EXIT=1`）。
但该克隆在 clone 阶段已取得 `main` 的完整对象，`git checkout main` 后的 **HEAD 实测为 `cb88218`（与上游当前 main 一致）**，其后运行结果可信。
真正「干净的一次性 clone 后复跑」以 `05_clean_clone_autocrlf_false.log` 为准（该次 `CLONE_EXIT=0`，HEAD 同为 `cb88218`）。

---

## 结果分类（不混着说）

**通过（真跑通）**：`v1.4.0-conformance`（1477/1549）、`canonicalization-v1`（81/81，需 LF 检出）

**按设计应当失败（门禁证明有效）**：`mustfail-v1` —— 该集是 MUST-FAIL 集合，`EXIT=1` 且 `SOME VECTORS FAILED` 是**预期结果**，不是缺陷

**不可跑（上游未提供执行器或不是向量集结构，非失败）**：`v1.1.20`、`technical-fit-v1`（无 `manifest.json`，后者需走 `verify_pilot.py` 逐例验签，见 05）

---

## 转录编码说明

`01`–`05` 是在 **Windows PowerShell** 中直接捕获原生进程输出得到的，其中行首的 `✓` 记号被控制台按 GBK 解码，在转录里呈现为 `鉁?`。

**这是捕获端的显示伪影，不涉及任何判定结果**：所有判断依据字段（`Checks: n/m passed`、`EXIT_*=n`、`Receipts verified: n/n`、`MANIFEST VERIFICATION FAILED`、`SOME VECTORS FAILED`、`ALL VECTORS PASSED`）均为纯 ASCII，未受影响。

为避免读者只能看到有伪影的转录，另附 `06_headline_pristine_utf8.log` —— 该份用 **Python 子进程按 UTF-8 字节解码**捕获，`✓` 完整保留，可作为对照。

---

## 复现方式

```bash
git -c core.autocrlf=false -c core.eol=lf clone --depth 1 \
  https://github.com/DSHCorrectover/ccs-conformance-vectors.git
cd ccs-conformance-vectors
uv run --no-project --with jcs --with cryptography \
  python checkers/independent_checker.py vectors/v1.4.0-conformance
```

预期末行：`ALL VECTORS PASSED`，且 `Checks: 1477/1549 passed`。
（`1477/1549` 表示 1549 条断言中 1477 条通过；该向量集的通过判据是 `ALL VECTORS PASSED` 且 exit 0，不是断言全过。）

---

## 边界

- 本批次只证明「**在所述 commit 上、按上游 README 的命令、在干净环境中可复现**」，不构成对上游设计或安全性的评价。
- `02` 的 TLS 中断已如实记录于上，未做任何美化。
- 断言计数（如 `Cases: 66/66`）在 `effff90` 上恰好正确但无区分度 —— 这正是 issue #2 所述 checker 自证行的表现，本批次转录保留了该原始输出。
