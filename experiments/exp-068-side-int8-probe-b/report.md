# Why the default build's int8 fails parity (exp-068-side-int8-probe-b)

`side-r9-ettin-150m-s1`'s fp32 export against int8 variants on the export's 283 parity lines (pilot-0.4, mixed speaker conditions), decisions at its thresholds (respond 0.6, wait 0.4). fp32 on one thread: 315.6 ms a line (p50). Graph: {'matmuls_with_weights': 88, 'by_group': {'attn_qkv': 22, 'attn_out': 22, 'mlp_in': 22, 'mlp_out': 22}, 'layers': 22, 'sample_names': ['/m/enc/layers.0/attn/Wqkv/MatMul', '/m/enc/layers.0/attn/Wo/MatMul', '/m/enc/layers.0/mlp/Wi/MatMul', '/m/enc/layers.0/mlp/Wo/MatMul', '/m/enc/layers.1/attn/Wqkv/MatMul', '/m/enc/layers.1/attn/Wo/MatMul']}. CPU: {'model': 'unknown', 'vnni': [], 'avx512': False}.

| Variant | MatMuls in fp32 | Decisions same | Largest respond difference | Mean | MB | ms a line, 1 thread |
|---|---|---|---|---|---|---|
| per tensor | 0 | 266/283 | 0.5656 | 0.0377 | 266.5 | 181.4 |
| per tensor, reduce range | 0 | 261/283 | 0.8524 | 0.0431 | 266.5 | 183.1 |
| per tensor, no mlp_out | 22 | 280/283 | 0.2197 | 0.0119 | 324.9 | 197.7 |
| reduce range, no mlp_out | 22 | 281/283 | 0.2804 | 0.0064 | 325.4 | 193.6 |
| per tensor, reduce range, no mlp_out | 22 | 279/283 | 0.2378 | 0.0096 | 324.9 | 194.1 |
| reduce range, no mlp | 44 | 281/283 | 0.1535 | 0.0051 | 442.0 | 248.9 |
| uint8 weights, per channel | 0 | 268/283 | 0.8198 | 0.0357 | 267.2 | 217.2 |
| uint8 weights, per tensor | 0 | 269/283 | 0.5446 | 0.0378 | 266.5 | 214.7 |
