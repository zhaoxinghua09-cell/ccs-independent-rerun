# 权属证明与许可声明

> 本声明置于每个对外发布物的显著位置（SKILL.md 末尾 / 文档头部 / 包根）。
> 署名口径统一为「Xinghua Zhao (Steven Zhao) — LGD / SynomosAI initiative」，即本仓对外使用的品牌署名；不披露在职公司、客户信息或本机内部路径。

## 1. 著作权 ©
© 2026 Xinghua Zhao (Steven Zhao) - LGD / SynomosAI initiative. 保留所有权利。
本作品（含软件代码与文档）的著作权归 Xinghua Zhao (Steven Zhao) - LGD / SynomosAI initiative 所有。

## 2. 知识版权声明
本作品所汇集的方法论、对比分析、结构化知识与合成内容（"知识内容"），
其编排与原创表达归 Xinghua Zhao (Steven Zhao) - LGD / SynomosAI initiative 所有。未经书面许可，不得复制、转载、摘编、转售，
或用于训练任何模型 / 商业系统。
（软件代码依随附 LICENSE 的许可条款使用；本知识版权声明不限制 LICENSE 已授予的权利。）

## 3. 免责声明（AS IS）
本作品按「现状」提供，不提供任何明示或暗示的担保，包括但不限于适销性、
特定用途适用性及非侵权担保。使用风险由使用者自行承担，因使用本作品所致
任何直接或间接损失，作者不承担责任。

## 4. 发布时间戳
- 发布时间（UTC）：2026-11-05T05:02:48.865851+00:00
- 发布时间（本地）：2026-11-05T13:02:48.865867
- 内容版本：`2026.11.05.v2`

## 5. 作品指纹（内容哈希）
- 包指纹 SHA-256：dd2153c27ca07f0e9c7b638c247229e8b205ef7cf4f0f2c118494beb6406a4da
- 本指纹由发布包内全部文件的哈希按确定顺序合成，可作为该版本
  「于上述时间由 Xinghua Zhao (Steven Zhao) - LGD / SynomosAI initiative 发布」的完整性标识。篡改任一文件即导致指纹变化。
- 合成算法：对 `manifest.json` 的 `files[]`（按 `path` 升序）依次累加 `path` + `0x00` + `sha256(path)`，取 SHA-256。
  `ATTESTATION.md` 与 `manifest.json` 自身不入哈希（无法自我覆盖）。
  可用 `publish_attest.py <包目录> --verify` 逐件复核。
- 加强权属：可将本指纹锚定至可信时间戳服务（RFC3161 TSA）或区块链，
  形成不可抵赖的「在先发表」证据（该步骤需外部服务，须经确认后单独执行）。

## 6. 内锚与外锚（可核验的在先发表证据）

**内锚（本包内自证）**

- 署名：`Xinghua Zhao (Steven Zhao) — LGD / SynomosAI initiative`
- 规范仓：`https://github.com/zhaoxinghua09-cell/ccs-independent-rerun`
- 版本 / 批次：`2026.11.05.v2`
- 包指纹：`dd2153c27ca07f0e9c7b638c247229e8b205ef7cf4f0f2c118494beb6406a4da`
- 逐文件哈希见下方文件清单

**外锚（第三方时间戳，GitHub 服务器侧记录）**

| 内容版本 | 包指纹 | commit | 时间 |
|---|---|---|---|
| v1（6 份转录 + README + rerun_runs.json） | `2db5d6b1b3ef8c0798cd87026d1e743c94e48cc99b7820429e4608bebbc3d00c` | `4da9f2a3b04dff6540da4e43e4e7688d9647a164` | 2026-11-05T04:47:06Z |
| v2（本版，17 件，含独立裁决器与签名验证器） | `dd2153c27ca07f0e9c7b638c247229e8b205ef7cf4f0f2c118494beb6406a4da` | 待本版提交后回填 | — |

> **不预填未发生的事**：v2 的 commit 号在本文件写就时尚未产生，故留「待回填」。
> 回填前，v2 只有内锚（自证），没有外锚（第三方时间戳）。这个区别必须保留，不能混说。

**加强（未执行）**

如需不可抵赖级证据，可将包指纹锚定至 RFC3161 可信时间戳服务（TSA）或 Zenodo DOI。该步骤需调用外部付费/注册服务，**本批次未执行，不作已执行表述**。

---

## 附：文件清单与逐文件哈希

| 文件 | SHA-256 |
|---|---|
| runs/2026-11-05/01_stranger_effff90.log | 56113d2211b77118a54f0b419ce90dcc87eb4346c4afc53eadf34652cf22431f |
| runs/2026-11-05/02_stranger_main_cb88218.log | eca1663f6ce5c11ec10a5667b0bc2782516c6a06dfc824812d413abc58dfa1db |
| runs/2026-11-05/03_negative_controls_utf8.log | 6f3ff6a2e0e4a0adfa69892bedb4c50a90e5eb306e651d5e0fe65a29812b8287 |
| runs/2026-11-05/04_allsets_sweep.log | d911746daba86af6ca423c831c5f06dd32e5b715b0acffe6396b7d2f4de837a0 |
| runs/2026-11-05/05_clean_clone_autocrlf_false.log | c0092f7dda315debf1761e882774ec1601c0112e109887505be4ee9bdc1a9d28 |
| runs/2026-11-05/06_headline_pristine_utf8.log | f6e5d02fd1c74cddc2c99c3503f98d478e887422f05973d05ae0ed6d90f469e7 |
| runs/2026-11-05/07_admission_verifier.py | 50a3abda937b5a610c8419ef5082f4d79beb8799f325992bcabd31fad338d519 |
| runs/2026-11-05/08_verify_sig_vectors.py | e8e1b861137afe7d7aa77d6373b2bb9121b0b32ad6380edf6ad7f49e411dc9e0 |
| runs/2026-11-05/09_mustfail_verdict.md | 8abf022dcc9ed9edda5db6c4caa33529530d9f975292699f9d1c0c7749d6205b |
| runs/2026-11-05/10_sig_vectors.md | 4732e414a2b42983e37e2711167b6e0ba381d22cc240bdfa14516fa57dbe493d |
| runs/2026-11-05/11_R5_adm_run.log | fed9fb3ce83f4ce6273819ba5a9ce8cdb693436c13fc2f0ab2f2f7f26ab3ef36 |
| runs/2026-11-05/12_R6_sig_run.log | b5bf2425d97ddd4f6ee088780aa2c38bc684e299de4755394ce6e064e7f7509c |
| runs/2026-11-05/13_independent_verdict_and_signature.md | 3dc290ada7fbe856e2af9a2f28be85f1430b19fb6a212a92292d86736c37d2fd |
| runs/2026-11-05/README.md | 9a7975491b2da92e598be1ad027f653612c638aa329bba410e475b070e334710 |
| runs/2026-11-05/mustfail_verdict.json | bf90e237c571357010d3786d7127f4196e637b62f72858fbd5b7ef836b10617b |
| runs/2026-11-05/rerun_runs.json | 2a100347d3ccfcb57b1c85bd6738b01d53f3dc904d65993eab6d5598afbf943c |
| runs/2026-11-05/sig_vectors.json | 74c6d64260211ef0e0d2930763c59825e53c5d4632eb6d4e6bbcf6bddbcd860d |

**文件数：17**
