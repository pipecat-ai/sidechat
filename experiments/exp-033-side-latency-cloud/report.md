# Latency on Pipecat Cloud-shaped containers (exp-033-side-latency-cloud)

CPU: unknown; Modal region us-east (CLOUD_PROVIDER_AWS). Each variant ran alone in a container with the profile's CPU and memory as hard limits. Times are the demo's `classifier_ms` (p50 / p90 / p99, ms) over its 33 sample lines: "demo" as written (0 to 2 earlier lines), "full window" after 8 earlier lines. Memory is the bench process's peak resident size (Python, Pipecat and the classifier, nothing else of the bot).

Models: side-r3-ettin-150m-s0, side-r1-ettin-68m-s0, side-smoke-ettin-32m-s0. `smoke` is a 32M trial model, here for its speed only.

## agent-1x: 0.5 vCPU, 1024 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | Lines |
|---|---|---|---|---|---|---|---|
| r3-150m-fp32-t1 | 1 | 910 | 5.76 | 453 | 507 / 1538 / 21344 | 648 / 880 / 25408 | 198 |
| r3-150m-fp32-t2 | 2 | 910 | 22.88 | 1787 | 304 / 2294 / 5088 | 1403 / 2223 / 4302 | 198 |
| r3-150m-int8-t1 | 1 | 571 | 2.20 | 188 | 103 / 180 / 262 | 532 / 589 / 656 | 198 |
| r3-150m-int8-t2 | 2 | 573 | 2.32 | 175 | 185 / 286 / 302 | 710 / 801 / 993 | 198 |
| r1-68m-fp32-t1 | 1 | 524 | 2.12 | 104 | 89 / 113 / 217 | 397 / 409 / 473 | 198 |
| r1-68m-fp32-t2 | 2 | 524 | 2.32 | 174 | 186 / 278 / 499 | 604 / 702 / 784 | 198 |
| smoke-32m-fp32-t1 | 1 | failed (exit 1) | | | | | |
| smoke-32m-fp32-t2 | 2 | failed (exit 1) | | | | | |
| jev |  | 114 | 0.62 | 47 | 53 / 82 / 105 | 56 / 80 / 119 | 132 |

## agent-2x: 1.0 vCPU, 2048 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | Lines |
|---|---|---|---|---|---|---|---|
| r3-150m-fp32-t1 | 1 | 910 | 1.79 | 88 | 66 / 90 / 116 | 253 / 266 / 305 | 198 |
| r3-150m-fp32-t2 | 2 | 911 | 1.47 | 150 | 120 / 202 / 276 | 604 / 681 / 719 | 198 |
| r3-150m-int8-t1 | 1 | 571 | 1.10 | 67 | 51 / 78 / 94 | 271 / 291 / 325 | 198 |
| r3-150m-int8-t2 | 2 | 573 | 1.39 | 143 | 93 / 116 / 186 | 424 / 500 / 562 | 198 |
| r1-68m-fp32-t1 | 1 | 524 | 1.08 | 43 | 33 / 45 / 58 | 116 / 123 / 128 | 198 |
| r1-68m-fp32-t2 | 2 | 524 | 1.29 | 21 | 17 / 70 / 75 | 117 / 168 / 175 | 198 |
| smoke-32m-fp32-t1 | 1 | failed (exit 1) | | | | | |
| smoke-32m-fp32-t2 | 2 | failed (exit 1) | | | | | |
| jev |  | 114 | 0.43 | 120 | 144 / 171 / 236 | 149 / 180 / 310 | 132 |

## agent-3x: 1.5 vCPU, 3072 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | Lines |
|---|---|---|---|---|---|---|---|
| r3-150m-fp32-t1 | 1 | 911 | 1.63 | 73 | 59 / 80 / 94 | 224 / 239 / 258 | 198 |
| r3-150m-fp32-t2 | 2 | 885 | 1.28 | 65 | 71 / 102 / 142 | 327 / 358 / 374 | 198 |
| r3-150m-int8-t1 | 1 | 571 | 1.20 | 60 | 46 / 72 / 128 | 248 / 258 / 272 | 198 |
| r3-150m-int8-t2 | 2 | 573 | 1.05 | 49 | 55 / 77 / 151 | 243 / 287 / 308 | 198 |
| r1-68m-fp32-t1 | 1 | 524 | 0.97 | 52 | 45 / 67 / 80 | 193 / 201 / 213 | 198 |
| r1-68m-fp32-t2 | 2 | 525 | 0.97 | 88 | 25 / 57 / 85 | 161 / 189 / 202 | 198 |
| smoke-32m-fp32-t1 | 1 | failed (exit 1) | | | | | |
| smoke-32m-fp32-t2 | 2 | failed (exit 1) | | | | | |
| jev |  | 114 | 0.37 | 66 | 74 / 94 / 145 | 76 / 93 / 126 | 132 |

