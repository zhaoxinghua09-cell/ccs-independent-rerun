# Independent rerun — 2026-11-05 batch

本次批次为 **外部独立复跑** 的原始转录（Windows 10 / git 2.47.1 / uv 0.12.3 / Python 3.13.12）。
全部运行 **零凭据、零 cookie、零登录态**，只访问公开仓库。

上游仓库：`https://github.com/DSHCorrectover/ccs-conformance-vectors`

> 需要直接引用或转发本批次结论时，用包根的 **[`CITATION.md`](../../CITATION.md)**（单页可引用摘要：结论、数字、链接、复现命令、边界），不必逐份拼接转录。

---

## 批次一览

| # | 文件 | 目标 | 关键结果 | exit |
|---|---|---|---|---|
| 01 | `01_stranger_effff90.log` | 陌生人视角：全新 clone → 检出 `effff90` → 按上游 README 命令跑 `vectors/v1.4.0-conformance` | `Checks: 1477/1549 passed`、`Cases: 66/66`、`ALL VECTORS PASSED` | 0 |
| 02 | `02_stranger_main_cb88218.log` | 对当前 `main`（`cb88218`，2026-11-05 08:18:56 +0800）复跑同一向量集 | `Checks: 1477/1549 passed`、`Cases: 66/66`、**`Receipts verified: 73/73 admitted by manifest`**、`ALL VECTORS PASSED` | 0 |
| 03 | `03_negative_controls_utf8.log` | 负控 NC-A（篡改被 manifest 覆盖的文件，manifest 不动）/ NC-B（篡改 receipt 并重新钉住 manifest） | NC-A：`MANIFEST VERIFICATION FAILED` / NC-B：`Manifest verified` → `SOME VECTORS FAILED` + 2 条 FAIL 行 | 0 / 1 |
| 04 | `04_allsets_sweep.log` | 6 个向量集遍历（**`core.autocrlf=true` 环境**，见「已知环境坑」） | `v1.4.0-conformance` 通过；其余见下 | 混合 |
| 05 | `05_clean_clone_autocrlf_false.log` | 干净 clone（`core.autocrlf=false`、`core.eol=lf`、`--depth 1`），逐集复跑 + `technical-fit-v1` 的 C1–C6 逐例验签 | `canonicalization-v1`：`Checks: 81/81 passed`；`v1.4.0-conformance`：`1477/1549` + `Receipts 73/73`；C1–C4/C6 `VALID`，C5（篡改）`INVALID` | 见文件 |
| 06 | `06_headline_pristine_utf8.log` | 同一命令的 UTF-8 干净捕获（对照 `鉁?` 伪影） | 与 02 判定字段逐字一致 | 0 |
| 07 | `07_admission_verifier.py` | `mustfail-v1` 的**独立 admission 裁决器**（零依赖）。上游只给向量与期望，未提供裁决器 | 15/15 裁决对上；14/14 最小修复后转 PASS；4/4 松紧度负控 | 0 |
| 08 | `08_verify_sig_vectors.py` | `v1.1.20` + `v1.3.0` 的**签名与链接验证器**（依赖 `jcs` + `cryptography`）。上游未提供执行器 | 60/60 项通过；含 3 条篡改负控（改任一字段后签名必须失败） | 0 |
| 09 | `09_mustfail_verdict.md` | 07 的逐向量裁决明细 | 见文件 | — |
| 10 | `10_sig_vectors.md` | 08 的逐项验证明细 | 见文件 | — |
| 11 | `11_R5_adm_run.log` | 07 原始运行输出（未编辑） | `verdict_match=15/15  dims_match=15/15` | 0 |
| 12 | `12_R6_sig_run.log` | 08 原始运行输出（未编辑） | `checks=60 passed=60 failed=0` | 0 |
| 13 | `13_independent_verdict_and_signature.md` | 07/08 的说明文档：为什么之前判「不可跑」是判错了 | 见文件 | — |

机器可读汇总：`rerun_runs.json`（含 `R5` / `R6` 登记与 `correction` 块）
机读明细：`mustfail_verdict.json`、`sig_vectors.json`

### 11 与 12 的编码（附 UTF-8 镜像）

`11_R5_adm_run.log`、`12_R6_sig_run.log` 是 **UTF-16LE**（Windows PowerShell 重定向的默认编码），
原样保留，未做任何改写——它们是原始转录，不动的理由就在这里。

同时提供 **逐字对应的 UTF-8 镜像**，方便直接阅读或 `curl`：

| 原始（UTF-16LE） | 镜像（UTF-8，LF） |
|---|---|
| `11_R5_adm_run.log`（3142B） | `11_R5_adm_run.utf8.log`（1546B） |
| `12_R6_sig_run.log`（356B） | `12_R6_sig_run.utf8.log`（175B） |

转换只做两件事：UTF-16LE → UTF-8、CRLF → LF。**未增删任何字符**，可用两份互校。
字节数不同是编码差异，不是内容差异。

> 附带说明一个实测现象：GitHub 匿名 Contents API 对 UTF-16 文件会在 `content` 字段里做转码返回
> （`size` 报 356，解开 base64 只得 180 字节），所以**拿 API 的字节数去比对 manifest 会得到假失败**。
> 核对字节数请走 `raw.githubusercontent.com`。

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

**这里有一处更正，先讲清楚**：本 README 的早期版本把 `mustfail-v1` 写成「按设计应当失败」。
这个说法**不成立**——用上游 `independent_checker.py` 跑 `mustfail-v1`，输出是
`No case directories with expected.json found`（exit 1），这不是「应有的拒绝」，而是**跑错了执行器**：
该集是 `case.json` 结构，判定的是 admission 决策，而 `independent_checker.py` 只认 `expected.json` 的向量集。
把「跑错了」记成「应当失败」，是给自己发一枚假绿。

### 更正后的分类

**上游自带执行器，跑通**：`v1.4.0-conformance`（1477/1549）、`canonicalization-v1`（81/81，须 LF 检出）、`technical-fit-v1`（6/6，走自带 `verify_pilot.py`）

**上游未提供执行器，由本包独立实现执行器后跑通**：

| 集 | 执行器 | 结果 |
|---|---|---|
| `mustfail-v1` | `07_admission_verifier.py`（零依赖） | 15/15 裁决与期望一致；14/14 最小修复后转 PASS；4/4 松紧度负控 |
| `v1.3.0` | `08_verify_sig_vectors.py` | 50/50（含 2 条篡改负控） |
| `v1.1.20` | `08_verify_sig_vectors.py` | 10/10（含 1 条篡改负控） |

**全量口径：6 个向量集，6 个可验，6 个通过；0 不可跑，0 失败。**

> 口径纪律：**不得**表述为「全部向量集用上游执行器通过」——其中 3 集用的是本包自写执行器，这句话必须说明。
> 可以说的是：「6 集全部通过；其中 3 集上游无执行器，由本包独立实现。」

### 裁决器为什么可信（这两条比「14/14 全拒」有信息量）

1. **最小修复**：对 14 条 MUST-FAIL 逐条只改**唯一**违规定点（补 `tool_call_id`、把 `"9999"` 改成 `9999`、换 nonce、换回授权工具……），改完 **14/14 全部转 PASS**。这说明拦点必要且充分，而不是无脑拒。
2. **松紧度负控**：`C01` 原样必须 PASS（实测 PASS）；把 `path` 改成 `../../etc/passwd`、把 `caller.issuer` 改成自证颁发者、把 `tool` 改成管理员工具，三种篡改必须 FAIL（实测全 FAIL）。

裁决器的输入白名单只有 `policy` / `tool_call` / `workflow` / `observed_response` / `data_flow` / `response_data_labels`；
`expectation` / `expectation_detail` / `dimensions_violated` / `why_must_fail` 被 `whitelist()` 排除，脚本内有断言守门。

### 顺带一条对上游的反馈（不是挑刺）

`mustfail-v1/README.md` 称「逐调用打分的裁决器会把三条 workflow 全部误放行」。
实测：`W01`、`W02` 成立；**`W03` 不成立**——它的注入来源写在 step 2 `tool_call.instruction_provenance` 里，
一个读该字段的单调用裁决器即可拦截。详见 `13_independent_verdict_and_signature.md` 第四节。

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

另外 3 个上游没有执行器的集，用本包自带的执行器跑（同样零凭据）：

```bash
# mustfail-v1：独立的 admission 裁决器（零依赖，不需要 uv）
python 07_admission_verifier.py --vectors ../ccs-conformance-vectors/vectors/mustfail-v1

# v1.1.20 + v1.3.0：签名与链接验证
uv run --no-project --with jcs --with cryptography \
  python 08_verify_sig_vectors.py --vectors ../ccs-conformance-vectors/vectors
```

预期：`verdict_match=15/15  dims_match=15/15  minimal_fix_flipped=14/14  controls_ok=4/4`
与 `checks=60 passed=60 failed=0`。

---

## 边界

- 本批次只证明「**在所述 commit 上、按上游 README 的命令、在干净环境中可复现**」，不构成对上游设计或安全性的评价。
- **其中 3 集（`mustfail-v1` / `v1.3.0` / `v1.1.20`）的执行器是本包自写的，不是上游的。** 这一点必须随结果一起说，不能省。
- 自写执行器的判据取自工件本身（`policy` 块、`manifest` 声明、`JCS` + `Ed25519`），未参考上游期望值文件作为输入；比对在裁决之后进行，不一致即报，未做调参凑齐。
- `02` 的 TLS 中断已如实记录于上，未做任何美化。
- 断言计数（如 `Cases: 66/66`）在 `effff90` 上恰好正确但无区分度 —— 这正是 issue #2 所述 checker 自证行的表现，本批次转录保留了该原始输出。
- README 早期版本关于 `mustfail-v1`「按设计应当失败」的表述已作废并更正，更正理由写在「结果分类」一节。
