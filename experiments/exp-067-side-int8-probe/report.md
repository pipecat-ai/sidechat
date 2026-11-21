# Why the default build's int8 fails parity (exp-067-side-int8-probe)

`side-r9-ettin-150m-s1`'s fp32 export against int8 variants on the export's 283 parity lines (pilot-0.4, mixed speaker conditions), decisions at its thresholds (respond 0.6, wait 0.4). fp32 on one thread: 304.8 ms a line (p50). Graph: {'matmuls_with_weights': 88, 'by_group': {'attn_qkv': 22, 'attn_out': 22, 'mlp_in': 22, 'mlp_out': 22}, 'layers': 22, 'sample_names': ['/m/enc/layers.0/attn/Wqkv/MatMul', '/m/enc/layers.0/attn/Wo/MatMul', '/m/enc/layers.0/mlp/Wi/MatMul', '/m/enc/layers.0/mlp/Wo/MatMul', '/m/enc/layers.1/attn/Wqkv/MatMul', '/m/enc/layers.1/attn/Wo/MatMul']}.

| Variant | MatMuls in fp32 | Decisions same | Largest respond difference | Mean | MB | ms a line, 1 thread |
|---|---|---|---|---|---|---|
| all (as shipped before) | 0 | 176/283 | 0.9997 | 0.3168 | 267.2 | 174.4 |
| all but the heads | 0 | 176/283 | 0.9997 | 0.3168 | 267.2 | 174.1 |
| no mlp_out | 22 | 230/283 | 0.995 | 0.1635 | 325.4 | 197.1 |
| no mlp | 44 | 230/283 | 0.9936 | 0.1648 | 442.0 | 246.1 |
| no attention | 44 | 182/283 | 0.9983 | 0.3068 | 422.5 | 232.2 |
| no first and last two layers | 12 | 176/283 | 0.9994 | 0.3162 | 312.2 | 199.8 |
| no mlp_out, no heads | 22 | 230/283 | 0.995 | 0.1635 | 325.4 | 201.3 |
| per tensor | 0 | 266/283 | 0.5656 | 0.0377 | 266.5 | 173.7 |
| reduce range | 0 | 264/283 | 0.5281 | 0.0353 | 267.2 | 173.0 |
| uint8 weights, reduce range | 0 | 266/283 | 0.6422 | 0.0357 | 267.2 | 222.7 |
| no mlp_out in layer 0 | 1 | 173/283 | 0.9997 | 0.3271 | 269.8 | 183.7 |
| no mlp_out in layer 1 | 1 | 176/283 | 0.9993 | 0.3101 | 269.8 | 183.8 |
| no mlp_out in layer 2 | 1 | 173/283 | 0.9996 | 0.322 | 269.8 | 183.3 |
| no mlp_out in layer 3 | 1 | 177/283 | 0.9997 | 0.3178 | 269.8 | 180.2 |
| no mlp_out in layer 4 | 1 | 183/283 | 0.9992 | 0.302 | 269.8 | 183.8 |
| no mlp_out in layer 5 | 1 | 175/283 | 0.9996 | 0.3205 | 269.8 | 185.9 |
| no mlp_out in layer 6 | 1 | 173/283 | 0.9998 | 0.323 | 269.8 | 184.2 |
| no mlp_out in layer 7 | 1 | 177/283 | 0.9986 | 0.3108 | 269.8 | 175.5 |
| no mlp_out in layer 8 | 1 | 175/283 | 0.9996 | 0.3217 | 269.8 | 183.9 |
| no mlp_out in layer 9 | 1 | 176/283 | 0.9997 | 0.3177 | 269.8 | 175.9 |
| no mlp_out in layer 10 | 1 | 175/283 | 0.9997 | 0.3193 | 269.8 | 177.2 |
| no mlp_out in layer 11 | 1 | 186/283 | 0.9982 | 0.2886 | 269.8 | 179.9 |
| no mlp_out in layer 12 | 1 | 174/283 | 0.9998 | 0.3236 | 269.8 | 178.2 |
| no mlp_out in layer 13 | 1 | 177/283 | 0.9995 | 0.3153 | 269.8 | 178.2 |
| no mlp_out in layer 14 | 1 | 177/283 | 0.9993 | 0.3125 | 269.8 | 181.8 |
| no mlp_out in layer 15 | 1 | 176/283 | 0.9998 | 0.3201 | 269.8 | 180.3 |
| no mlp_out in layer 16 | 1 | 176/283 | 0.9997 | 0.3162 | 269.8 | 181.8 |
| no mlp_out in layer 17 | 1 | 176/283 | 0.9997 | 0.3175 | 269.8 | 186.7 |
| no mlp_out in layer 18 | 1 | 176/283 | 0.9997 | 0.3166 | 269.8 | 182.3 |
| no mlp_out in layer 19 | 1 | 176/283 | 0.9997 | 0.3167 | 269.8 | 182.5 |
| no mlp_out in layer 20 | 1 | 176/283 | 0.9997 | 0.3167 | 269.8 | 180.4 |
| no mlp_out in layer 21 | 1 | 176/283 | 0.9997 | 0.3169 | 269.8 | 179.1 |
