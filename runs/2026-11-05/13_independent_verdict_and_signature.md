# S5-补 · 独立裁决与签名验证（对 `08_全量实跑矩阵.md` 的更正）

**日期**：2026-11-05
**上游快照**：`cb88218f449c5bc184f0f487a2760eb9953da25a`（今日 main）
**零凭据**：是（无 PAT、无 token，仅匿名 HTTPS 克隆）
**动机**：用户问「他找我们，我们给了他最大的价值吗」。复核时发现「3 集不可跑」这个结论是我方判据不足，
不是上游缺陷——这是本件最大的价值缺口，必须自己先修掉。

---

## 一句话

> **上游 6 个向量集，6 个都能验，且全部通过。**
> 之前记的「3 集不可跑」，是把「上游没给执行器」误当成了「不可验证」。
> 执行器可以由独立验证方自己写——只要判定式由工件本身完全决定。

---

## 一、之前为什么判错

`08` 第一节的写法是：

| 集 | 当时的理由 | 问题在哪 |
|---|---|---|
| `v1.3.0` | 「非 `expected.json` case 结构」 | 它是 `action+behavior` 成对 receipt，本来就不该用 case 检查器跑 |
| `mustfail-v1` | 「上游未提供 admission 判定器」 | 判定器可以从 `policy` 块 + 向量字段写出来；没有判定器 ≠ 没有判定式 |
| `v1.1.20` | 「仅 1 个参考签名样本」 | 样本正是用来验签的，公钥就在文件里 |

共同错误：**把「上游缺工具」当成「工件缺可验证性」。** 这两件事完全不同。
独立验证人的职责恰恰是自己把缺的那一环补上，而不是记一笔「不可跑」就结束。

---

## 二、R5 · `mustfail-v1` 独立 admission 裁决器

**执行器**：`admission_verifier.py`（零依赖，仅 Python 标准库）
**输入白名单**：`policy` / `tool_call` / `workflow` / `observed_response` / `data_flow` / `response_data_labels`
**物理上读不到答案**：`expectation` / `expectation_detail` / `dimensions_violated` / `why_must_fail` / `title` / `id`
全部被排除在 `whitelist()` 之外，脚本内有断言守这道门。

### 结果

| 项目 | 结果 |
|---|---|
| 向量总数 | 15（14 MUST-FAIL + 1 MUST-PASS，与 README 声称**逐数核对一致**） |
| 裁决与期望一致 | **15 / 15** |
| 违规维度与声明一致 | **15 / 15** |
| 最小修复后翻转为 PASS | **14 / 14** |
| 松紧度负控 | **4 / 4** |

### 为什么「最小修复」这一栏最值钱

对 14 条 MUST-FAIL 逐条**只改唯一违规定点**（S01 补 `tool_call_id`、S02 把 `"9999"` 改成 `9999`、
S06 换 nonce、S10 换成授权工具、S11 把金额降到阈值内并带 ticket……），改完**全部转 PASS**。

这条证明了两件事：

1. 裁决器不是无脑拒——它放行修好的向量；
2. 每条向量的拦点是**必要且充分**的——拦住它的就是那一处，不多不少。

只报「14/14 全部拒绝」是没有信息量的，因为一个 `return FAIL` 也能做到 14/14。

### 松紧度负控

| 场景 | 期望 | 实测 |
|---|---|---|
| `C01` 原样 | PASS | PASS |
| `C01` 把 `path` 改成 `../../etc/passwd` | FAIL | FAIL（`X8-path-traversal`） |
| `C01` 把 `caller.issuer` 改成 `ccs-verifier/self-asserted` | FAIL | FAIL（`I5-caller-issuer`） |
| `C01` 把 `tool` 改成 `admin.emergency_revoke_all_sessions` | FAIL | FAIL（`X1/X2-tool-not-authorised`） |

---

## 三、R6 · `v1.1.20` + `v1.3.0` 签名与链接验证

**执行器**：`verify_sig_vectors.py`（依赖 `jcs` + `cryptography`，与上游 checker 同两个依赖）

**签名口径与上游一致**：`Ed25519` over `JCS(receipt − signature)`，
即 `independent_checker.py::receipt_digest_l1` 的定义，不是我方自创口径。

| 集 | 通过 | 总数 | 验了什么 | 篡改负控 |
|---|---|---|---|---|
| `v1.1.20` | 10 | 10 | 验签；`public_key_raw_b64` → SHA-256 的前 16 位与全长两个指纹字段自洽；receipt 内公钥/指纹/颁发者与文件头一致 | 1 条：改 `rule_summary` → 签名必须失败 → **已失败** |
| `v1.3.0` | 50 | 50 | `manifest.files[]` 逐件 SHA-256；`manifest_digest` = SHA-256(JCS(manifest − manifest_digest))；8 个 receipt 逐个验签；`behavior.linked_l1_receipt_digest` 与 action 的 `receipt_digest_l1` 对齐；两套密钥模型的 `chain_integrity_verdict` 与 manifest 声明一致 | 2 条：改 `verdict` → 签名必须失败 → **均已失败** |

**结论：两集都是 `PASS (own harness)`。**

---

## 四、顺带抓到上游一处断言不精确（这是我们能回馈的东西）

`mustfail-v1/README.md` 第 56-59 行称：

> *"A verifier that scores one call at a time will wrongly admit all three traces."*

实测（`admission_verifier.py` 的 `shallow_per_call_check`，逐 step 单独裁决）：

| 向量 | 步数 | 逐步单独裁决是否全 PASS | 该声称 |
|---|---|---|---|
| `W01` | 2 | 是 | 成立 |
| `W02` | 3 | 是 | 成立 |
| `W03` | 3 | **否**（step 2 命中 `X11-untrusted-instruction`） | **不成立** |

**原因**：`W03` 的注入来源写在 step 2 的 `tool_call.instruction_provenance.source_trust = "untrusted-external-content"`，
一个读取该字段的单调用裁决器即可拦截，不需要跨步推理。
而 `W01`（PHI 流向 scope 不符的 webhook）、`W02`（allowlist 主机 302 到 metadata）的恶意性确实**只存在于链上**，单步不可见。

**建议**（可选）：把 `W03` 的 provenance 提到 workflow 层，或在 README 中注明
「逐调用拦截依赖裁决器读取 `instruction_provenance`」。
这样这句断言在任何单调用裁决器上都严格成立。

> 这条不是挑刺。它是「独立验证人」这个角色唯一能给出的、别处拿不到的东西：
> 我照你的说明写了裁决器，跑出来发现有一处你说的话，在我这种实现下不成立。

---

## 五、陌生人复现方法

```bash
git -c core.autocrlf=false -c core.eol=lf clone --depth 1 \
  https://github.com/DSHCorrectover/ccs-conformance-vectors.git
cd ccs-conformance-vectors

cd <本仓>
uv run --no-project --with jcs --with cryptography python verify_sig_vectors.py --vectors ../ccs-conformance-vectors/vectors

python admission_verifier.py --vectors ../ccs-conformance-vectors/vectors
```

两条命令都不需要任何凭据。

---

## 六、证据文件

| 文件 | 内容 |
|---|---|
| `admission_verifier.py` | 裁决器源码（零依赖）+ 最小修复表 + 松紧度负控 |
| `verify_sig_vectors.py` | 签名/链接验证器源码 |
| `mustfail_verdict.json` / `.md` | R5 逐向量裁决明细、14 条最小修复结果、4 条负控结果 |
| `sig_vectors.json` / `.md` | R6 60 项逐项结果 |
| `R5_adm_run.log` / `R6_sig_run.log` | 原始运行输出（未编辑） |
| `rerun_runs.json` | `R5` / `R6` 登记 + `coverage_matrix` 更正 + `correction` 块 |
| `08_全量实跑矩阵.md` | 旧结论（第 1-4 节）保留，第五节为本次更正 |

---

## 七、更正后的总账

| 口径 | 旧（v1） | 新（v2） |
|---|---|---|
| 全量 6 集 | 3 PASS / 3 NOT_RUNNABLE / 0 FAIL | **6 PASS / 0 NOT_RUNNABLE / 0 FAIL** |
| 上游自带执行器 | 3 | 3 |
| 我方独立实现执行器 | 0 | 3 |
| 断言层覆盖（v5 仅声称 `v1.4.0-conformance @ effff90`） | 1/1 | 1/1（不变） |

> 口径纪律不变：**仍不得表述为「全部向量集用上游执行器通过」**——
> 其中 3 集用的是我方自写执行器，这句话必须在正文里说清楚。
> 可以说的是：**上游 6 集，6 集都能验，6 集都过；其中 3 集上游无执行器，由我方独立实现。**
