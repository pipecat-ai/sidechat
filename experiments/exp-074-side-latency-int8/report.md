# Latency on Pipecat Cloud-shaped containers (exp-074-side-latency-int8)

CPU: unknown; Modal region us-east (CLOUD_PROVIDER_AZURE). Each variant ran alone in a container with the profile's CPU and memory as hard limits. Times are the demo's `classifier_ms` (p50 / p90 / p99, ms) over its 33 sample lines: "demo" as written (0 to 2 earlier lines), "full window" after 8 earlier lines. Memory is the bench process's peak resident size (Python, Pipecat and the classifier, nothing else of the bot). A two-tower model's history is encoded first, untimed, as it would be while the person talks; its cold time (both towers) and the history encoding are shown apart. "Beats Jev" compares the full-window median with Jev's in the same profile.

Models: side-r9-ettin-150m-s1, side-r9tt-ettin-32m-s1.

## agent-1x: 0.5 vCPU, 1024 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | full window cold p50 | history encode p50 | Beats Jev | Lines |
|---|---|---|---|---|---|---|---|---|---|---|
| r9-150m-s1-fp32-t1 | 1 | 911 | 171.71 | 63184 | 206 / 315 / 427 | 991 / 1059 / 1108 |  |  |  | 198 |
| r9-150m-s1-int8-t1 | 1 | 628 | 3.06 | 127 | 123 / 200 / 388 | 672 / 696 / 724 |  |  |  | 198 |
| r9tt-32m-s1-fp32-t1 | 1 | 487 | 1.25 | 13 | 10 / 62 / 79 | 11 / 62 / 74 | 104 | 93 |  | 198 |
| r9tt-32m-s1-int8-t1 | 1 | 428 | 1.23 | 12 | 9 / 59 / 64 | 10 / 61 / 64 | 95 | 86 |  | 198 |

## agent-2x: 1.0 vCPU, 2048 MiB

| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 | full window cold p50 | history encode p50 | Beats Jev | Lines |
|---|---|---|---|---|---|---|---|---|---|---|
| r9-150m-s1-fp32-t1 | 1 | 912 | 1.64 | 122 | 104 / 148 / 180 | 465 / 490 / 504 |  |  |  | 198 |
| r9-150m-s1-int8-t1 | 1 | 628 | 1.11 | 75 | 60 / 92 / 123 | 303 / 320 / 396 |  |  |  | 198 |
| r9tt-32m-s1-fp32-t1 | 1 | 489 | 0.90 | 29 | 18 / 22 / 24 | 16 / 22 / 117 | 77 | 61 |  | 198 |
| r9tt-32m-s1-int8-t1 | 1 | 428 | 0.51 | 10 | 5 / 6 / 8 | 7 / 9 / 13 | 32 | 23 |  | 198 |

