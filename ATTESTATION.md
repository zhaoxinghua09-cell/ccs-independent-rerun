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
- 发布时间（UTC）：2026-11-05T04:45:48.867942+00:00
- 发布时间（本地）：2026-11-05T12:45:48.867959

## 5. 作品指纹（内容哈希）
- 包指纹 SHA-256：2db5d6b1b3ef8c0798cd87026d1e743c94e48cc99b7820429e4608bebbc3d00c
- 本指纹由发布包内全部文件的哈希按确定顺序合成，可作为该版本
  「于上述时间由 Xinghua Zhao (Steven Zhao) - LGD / SynomosAI initiative 发布」的完整性标识。篡改任一文件即导致指纹变化。
- 加强权属：可将本指纹锚定至可信时间戳服务（RFC3161 TSA）或区块链，
  形成不可抵赖的「在先发表」证据（该步骤需外部服务，须经确认后单独执行）。

## 6. 内锚与外锚（可核验的在先发表证据）

**内锚（本包内自证）**

- 署名：`Xinghua Zhao (Steven Zhao) — LGD / SynomosAI initiative`
- 规范仓：`https://github.com/zhaoxinghua09-cell/ccs-independent-rerun`
- 版本 / 批次：`2026.11.05`
- 包指纹：`2db5d6b1b3ef8c0798cd87026d1e743c94e48cc99b7820429e4608bebbc3d00c`
- 逐文件哈希见上方文件清单，可用 `publish_attest.py --verify` 复核

**外锚（第三方时间戳）**

- 载体：GitHub commit（由 GitHub 服务器侧记录时间，非本地可改）
- 本批次内容提交：`4da9f2a3b04dff6540da4e43e4e7688d9647a164`（2026-11-05T04:47:06Z）
- 直达：`https://github.com/zhaoxinghua09-cell/ccs-independent-rerun/commit/4da9f2a3b04dff6540da4e43e4e7688d9647a164`
- 说明：`manifest.json` 已包含在上述提交内；本 `ATTESTATION.md` 于同一日随后提交（因其自身无法被自身哈希覆盖，故不列入 manifest）。

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
| runs/2026-11-05/README.md | 675393d66d7a3c76d6b9cf94bb9df2fe6593dbe768bfbb293d1db573237cfbea |
| runs/2026-11-05/rerun_runs.json | 2a100347d3ccfcb57b1c85bd6738b01d53f3dc904d65993eab6d5598afbf943c |
