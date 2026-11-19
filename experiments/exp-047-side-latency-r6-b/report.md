# Latency on Pipecat Cloud-shaped containers (exp-047-side-latency-r6-b)

CPU: unknown; Modal region us-east (CLOUD_PROVIDER_AWS). Each variant ran alone in a container with the profile's CPU and memory as hard limits. Times are the demo's `classifier_ms` (p50 / p90 / p99, ms) over its 33 sample lines: "demo" as written (0 to 2 earlier lines), "full window" after 8 earlier lines. Memory is the bench process's peak resident size (Python, Pipecat and the classifier, nothing else of the bot). A two-tower model's history is encoded first, untimed, as it would be while the person talks; its cold time (both towers) and the history encoding are shown apart. "Beats Jev" compares the full-window median with Jev's in the same profile.

Models: side-r6-ettin-150m-s1, side-r6tt-ettin-32m-s0, side-r6tt-ettin-68m-s0, side-r6s-ettin-32m-s0.

## agent-1x: 0.5 vCPU, 1024 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | full window cold p50 | history encode p50 | Beats Jev | Lines |
|---|---|---|---|---|---|---|---|---|---|---|
| r6-150m-fp32-t1 | 1 | 910 | 6.30 | 217076 | 286 / 562 / 1045 | 486 / 526 / 1815 |  |  | no | 198 |
| r6-150m-int8-t1 | 1 | 573 | 2.47 | 117 | 97 / 164 / 186 | 508 / 570 / 599 |  |  | no | 198 |
| r6tt-32m-fp32-t1 | 1 | 488 | 1.69 | 70 | 16 / 67 / 71 | 21 / 70 / 76 | 128 | 109 | yes | 198 |
| r6tt-32m-int8-t1 | 1 | 416 | 1.36 | 37 | 8 / 60 / 65 | 11 / 63 / 73 | 97 | 90 | yes | 198 |
| r6tt-68m-fp32-t1 | 1 | 802 | 7.51 | 111 | 92 / 104 / 217 | 96 / 107 / 177 | 488 | 396 | no | 198 |
| r6s-32m-fp32-t1 | 1 | 357 | 1.48 | 130 | 23 / 83 / 112 | 100 / 125 / 194 |  |  | no | 198 |
| jev |  | 114 | 0.64 | 53 | 60 / 80 / 123 | 66 / 91 / 135 |  |  |  | 132 |

## agent-2x: 1.0 vCPU, 2048 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | full window cold p50 | history encode p50 | Beats Jev | Lines |
|---|---|---|---|---|---|---|---|---|---|---|
| r6-150m-fp32-t1 | 1 | 911 | 2.27 | 84 | 70 / 95 / 113 | 266 / 284 / 295 |  |  | no | 198 |
| r6-150m-int8-t1 | 1 | 571 | 0.98 | 31 | 18 / 27 / 35 | 108 / 117 / 125 |  |  | yes | 198 |
| r6tt-32m-fp32-t1 | 1 | 487 | 0.77 | 21 | 13 / 15 / 18 | 14 / 16 / 21 | 65 | 51 | yes | 198 |
| r6tt-32m-int8-t1 | 1 | 414 | 0.66 | 13 | 9 / 10 / 11 | 10 / 13 / 29 | 44 | 35 | yes | 198 |
| r6tt-68m-fp32-t1 | 1 | 795 | 1.48 | 50 | 39 / 51 / 98 | 49 / 57 / 60 | 218 | 174 | yes | 198 |
| r6s-32m-fp32-t1 | 1 | 357 | 0.80 | 24 | 16 / 24 / 32 | 43 / 50 / 137 |  |  | yes | 198 |
| jev |  | 114 | 0.46 | 158 | 148 / 174 / 203 | 145 / 176 / 187 |  |  |  | 132 |

