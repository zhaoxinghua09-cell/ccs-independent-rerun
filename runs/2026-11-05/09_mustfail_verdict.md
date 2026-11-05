# mustfail-v1 独立 admission 裁决报告

由 `admission_verifier.py` 生成（零依赖，仅标准库）。

> 裁决器输入白名单：`policy` / `tool_call` / `workflow` / `observed_response` / `data_flow` / `response_data_labels`
> 裁决器**不读取**：`expectation` / `expectation_detail` / `dimensions_violated` / `why_must_fail` / `title` / `id`

## 总览

| 项目 | 结果 |
|---|---|
| 向量总数 | 15（MUST-FAIL 14 + MUST-PASS 1） |
| 裁决与期望一致 | **15/15** |
| 违规维度与声明一致 | **15/15** |
| 最小修复后翻转为 PASS | **14/14** |
| 松紧度负控通过 | **4/4** |
| 总计不符项 | 0 |

## 逐向量

| 向量 | 期望 | 裁决 | 一致 | 违规维度（实测） | 命中规则 |
|---|---|---|---|---|---|
| `MF-C01` | MUST-PASS | **PASS** | 是 | — | — |
| `MF-S01` | MUST-FAIL | **FAIL** | 是 | Structure | S1-required-field |
| `MF-S02` | MUST-FAIL | **FAIL** | 是 | Schema | SC1-strict-arg-type |
| `MF-S03` | MUST-FAIL | **FAIL** | 是 | Latency | L1-no-deadline |
| `MF-S04` | MUST-FAIL | **FAIL** | 是 | Cost | C1-per-call-budget, C2-per-trace-budget, C3-token-ceiling |
| `MF-S05` | MUST-FAIL | **FAIL** | 是 | Identity | I1-untrusted-issuer, I2-untrusted-algorithm, I3-empty-signature, I4-unknown-fingerprint |
| `MF-S06` | MUST-FAIL | **FAIL** | 是 | Integrity | G1-nonce-replay |
| `MF-S07` | MUST-FAIL | **FAIL** | 是 | Security | X3-shell-metachar, X4-fetch-and-execute |
| `MF-S08` | MUST-FAIL | **FAIL** | 是 | Security | X6-ssrf-target, X7-egress-not-allowlisted |
| `MF-S09` | MUST-FAIL | **FAIL** | 是 | Security | X5-credential-material |
| `MF-S10` | MUST-FAIL | **FAIL** | 是 | Security | X1-tool-not-allowlisted, X2-tool-not-granted |
| `MF-S11` | MUST-FAIL | **FAIL** | 是 | Security | X10-refund-over-cap, X11-untrusted-instruction |
| `MF-W01` | MUST-FAIL | **FAIL** | 是 | Integrity, Security | Y2-sensitive-egress-unregistered, Y3-label-scope-mismatch |
| `MF-W02` | MUST-FAIL | **FAIL** | 是 | Identity, Security | Y1-redirect-landed-on-blocked, Y2-sensitive-egress-unregistered, Y4-identity-credential-egress |
| `MF-W03` | MUST-FAIL | **FAIL** | 是 | Integrity, Security | Y2-sensitive-egress-unregistered, Y4-secret-crossed-boundary, Y5-untrusted-instruction-chain |

## 最小修复负控（证明拦点唯一且必要）

| 向量 | 修复后裁决 | 已翻转 | 残余规则 |
|---|---|---|---|
| `MF-S01` | PASS | 是 | — |
| `MF-S02` | PASS | 是 | — |
| `MF-S03` | PASS | 是 | — |
| `MF-S04` | PASS | 是 | — |
| `MF-S05` | PASS | 是 | — |
| `MF-S06` | PASS | 是 | — |
| `MF-S07` | PASS | 是 | — |
| `MF-S08` | PASS | 是 | — |
| `MF-S09` | PASS | 是 | — |
| `MF-S10` | PASS | 是 | — |
| `MF-S11` | PASS | 是 | — |
| `MF-W01` | PASS | 是 | — |
| `MF-W02` | PASS | 是 | — |
| `MF-W03` | PASS | 是 | — |

## 松紧度负控（证明不是无脑拒）

| 场景 | 期望 | 裁决 | 通过 |
|---|---|---|---|
| control-unmodified | PASS | PASS | 是 |
| control-path-traversal | FAIL | FAIL | 是 |
| control-untrusted-issuer | FAIL | FAIL | 是 |
| control-tool-not-granted | FAIL | FAIL | 是 |

## 逐调用浅裁决 vs 全链深裁决

上游 README 声称：只按单次调用打分的裁决器会把三条 workflow 全部误放行。实测结果：

| 向量 | 步数 | 逐步单独裁决是否全 PASS |
|---|---|---|
| `MF-W01` | 2 | 是（印证该声称） |
| `MF-W02` | 3 | 是（印证该声称） |
| `MF-W03` | 3 | 否 |
