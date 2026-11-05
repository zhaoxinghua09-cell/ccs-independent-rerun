# v1.1.20 / v1.3.0 独立验证报告

上游未提供这两集的执行器，脚本由我方独立实现（JCS + Ed25519 + SHA-256 链接）。

合计 **60/60** 项通过，0 项失败。

| 集 | 通过 | 总数 |
|---|---|---|
| v1.1.20 | 10 | 10 |
| v1.3.0 | 50 | 50 |

## 逐项

| 集 | 检查项 | 结果 | 说明 |
|---|---|---|---|
| v1.1.20 | `fixture-present` | 通过 | reference-signed-001.json |
| v1.1.20 | `pubkey-length-32` | 通过 | 32 bytes |
| v1.1.20 | `fingerprint-16-matches` | 通过 | computed 889d3f5bd86f5ff2 |
| v1.1.20 | `pubkey-sha256-full-matches` | 通过 | computed 889d3f5bd86f5ff2… |
| v1.1.20 | `receipt-pubkey-equals-header` | 通过 |  |
| v1.1.20 | `receipt-fingerprint-equals-header` | 通过 |  |
| v1.1.20 | `issuer-consistent` | 通过 | ccs-verifier/reference |
| v1.1.20 | `algorithm-ed25519` | 通过 |  |
| v1.1.20 | `ed25519-signature` | 通过 | signature valid |
| v1.1.20 | `tamper-control-must-fail` | 通过 | mutated field rejected |
| v1.3.0 | `manifest-present` | 通过 | manifest.json |
| v1.3.0 | `file-hash:in-process-key/action-1-allow.json` | 通过 | 13ca960f631b8be3 |
| v1.3.0 | `file-hash:in-process-key/action-2-block.json` | 通过 | 1410e30b163ca746 |
| v1.3.0 | `file-hash:in-process-key/behavior-1-allow.json` | 通过 | a6c2133fafeaa43e |
| v1.3.0 | `file-hash:in-process-key/behavior-2-block.json` | 通过 | 76b7b1043196a40a |
| v1.3.0 | `file-hash:in-process-key/metadata.json` | 通过 | d9834ae063c47dfd |
| v1.3.0 | `file-hash:sidecar-key/action-1-allow.json` | 通过 | 947220246a00d2e1 |
| v1.3.0 | `file-hash:sidecar-key/action-2-block.json` | 通过 | 481fb913eb3bc36c |
| v1.3.0 | `file-hash:sidecar-key/behavior-1-allow.json` | 通过 | 3b935048ff948f66 |
| v1.3.0 | `file-hash:sidecar-key/behavior-2-block.json` | 通过 | 87b8d59a1d7b29f3 |
| v1.3.0 | `file-hash:sidecar-key/metadata.json` | 通过 | 0efb30badb3e65bc |
| v1.3.0 | `manifest-digest` | 通过 | computed 42126c2436720213… |
| v1.3.0 | `in-process-key:algorithm` | 通过 |  |
| v1.3.0 | `in-process-key:chain-verdict-INTACT` | 通过 | INTACT |
| v1.3.0 | `in-process-key:action-1:ed25519` | 通过 | signature valid |
| v1.3.0 | `in-process-key:behavior-1:ed25519` | 通过 | signature valid |
| v1.3.0 | `in-process-key:pair-1:link-digest` | 通过 | computed sha256:53c2be53d8817670… |
| v1.3.0 | `in-process-key:pair-1:trace-id` | 通过 | paired-vector-001 |
| v1.3.0 | `in-process-key:pair-1:tool-call-id` | 通过 |  |
| v1.3.0 | `in-process-key:pair-1:issuer` | 通过 | ccs-verifier/in-process-test |
| v1.3.0 | `in-process-key:pair-1:fingerprint` | 通过 |  |
| v1.3.0 | `in-process-key:pair-1:l1-field-count-30` | 通过 | 30 keys |
| v1.3.0 | `in-process-key:action-2:ed25519` | 通过 | signature valid |
| v1.3.0 | `in-process-key:behavior-2:ed25519` | 通过 | signature valid |
| v1.3.0 | `in-process-key:pair-2:link-digest` | 通过 | computed sha256:c1b88d1b3e14139b… |
| v1.3.0 | `in-process-key:pair-2:trace-id` | 通过 | paired-vector-001 |
| v1.3.0 | `in-process-key:pair-2:tool-call-id` | 通过 |  |
| v1.3.0 | `in-process-key:pair-2:issuer` | 通过 | ccs-verifier/in-process-test |
| v1.3.0 | `in-process-key:pair-2:fingerprint` | 通过 |  |
| v1.3.0 | `in-process-key:pair-2:l1-field-count-30` | 通过 | 30 keys |
| v1.3.0 | `in-process-key:tamper-control-must-fail` | 通过 | mutated verdict rejected |
| v1.3.0 | `sidecar-key:algorithm` | 通过 |  |
| v1.3.0 | `sidecar-key:chain-verdict-INTACT` | 通过 | INTACT |
| v1.3.0 | `sidecar-key:action-1:ed25519` | 通过 | signature valid |
| v1.3.0 | `sidecar-key:behavior-1:ed25519` | 通过 | signature valid |
| v1.3.0 | `sidecar-key:pair-1:link-digest` | 通过 | computed sha256:9a79fe800698b08c… |
| v1.3.0 | `sidecar-key:pair-1:trace-id` | 通过 | paired-vector-001 |
| v1.3.0 | `sidecar-key:pair-1:tool-call-id` | 通过 |  |
| v1.3.0 | `sidecar-key:pair-1:issuer` | 通过 | ccs-verifier/sidecar-test |
| v1.3.0 | `sidecar-key:pair-1:fingerprint` | 通过 |  |
| v1.3.0 | `sidecar-key:pair-1:l1-field-count-30` | 通过 | 30 keys |
| v1.3.0 | `sidecar-key:action-2:ed25519` | 通过 | signature valid |
| v1.3.0 | `sidecar-key:behavior-2:ed25519` | 通过 | signature valid |
| v1.3.0 | `sidecar-key:pair-2:link-digest` | 通过 | computed sha256:7dc05a589d5eb7fa… |
| v1.3.0 | `sidecar-key:pair-2:trace-id` | 通过 | paired-vector-001 |
| v1.3.0 | `sidecar-key:pair-2:tool-call-id` | 通过 |  |
| v1.3.0 | `sidecar-key:pair-2:issuer` | 通过 | ccs-verifier/sidecar-test |
| v1.3.0 | `sidecar-key:pair-2:fingerprint` | 通过 |  |
| v1.3.0 | `sidecar-key:pair-2:l1-field-count-30` | 通过 | 30 keys |
| v1.3.0 | `sidecar-key:tamper-control-must-fail` | 通过 | mutated verdict rejected |