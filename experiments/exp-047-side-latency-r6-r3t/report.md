# Latency on Pipecat Cloud-shaped containers (exp-047-side-latency-r6-r3t)

CPU: unknown; Modal region uk (CLOUD_PROVIDER_AWS). Each variant ran alone in a container with the profile's CPU and memory as hard limits. Times are the demo's `classifier_ms` (p50 / p90 / p99, ms) over its 33 sample lines: "demo" as written (0 to 2 earlier lines), "full window" after 8 earlier lines. Memory is the bench process's peak resident size (Python, Pipecat and the classifier, nothing else of the bot). A two-tower model's history is encoded first, untimed, as it would be while the person talks; its cold time (both towers) and the history encoding are shown apart. "Beats Jev" compares the full-window median with Jev's in the same profile.

Models: side-r6ttr3t-ettin-32m-s0, side-r6ttr3t-ettin-68m-s0.

## agent-1x: 0.5 vCPU, 1024 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | full window cold p50 | history encode p50 | Beats Jev | Lines |
|---|---|---|---|---|---|---|---|---|---|---|
| r6ttr3t-32m-fp32-t1 | 1 | 488 | 1.58 | 13 | 7 / 58 / 64 | 10 / 62 / 65 | 88 | 76 | yes | 198 |
| r6ttr3t-68m-fp32-t1 | 1 | 818 | 5.03 | 90 | 83 / 92 / 116 | 83 / 91 / 96 | 380 | 300 | yes | 198 |
| r6ttr3t-68m-int8-t1 | 1 | 557 | 2.07 | 80 | 21 / 72 / 79 | 23 / 74 / 77 | 211 | 190 | yes | 198 |
| jev |  | 114 | 0.70 | 163 | 159 / 183 / 216 | 163 / 179 / 223 |  |  |  | 132 |

## agent-2x: 1.0 vCPU, 2048 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | full window cold p50 | history encode p50 | Beats Jev | Lines |
|---|---|---|---|---|---|---|---|---|---|---|
| r6ttr3t-32m-fp32-t1 | 1 | 488 | 0.97 | 14 | 7 / 8 / 9 | 9 / 10 / 11 | 35 | 27 | yes | 198 |
| r6ttr3t-68m-fp32-t1 | 1 | 803 | 1.73 | 63 | 52 / 69 / 156 | 49 / 60 / 75 | 237 | 182 | yes | 198 |
| r6ttr3t-68m-int8-t1 | 1 | 556 | 1.02 | 27 | 22 / 26 / 29 | 25 / 29 / 41 | 121 | 101 | yes | 198 |
| jev |  | 114 | 0.36 | 34 | 61 / 104 / 202 | 58 / 104 / 153 |  |  |  | 132 |

