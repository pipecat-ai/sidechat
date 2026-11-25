# Size and latency: side-r3-ettin-150m-s0 beside Jev

exp-032-side-latency, 2026-11-19. Measured on a Mac (Apple M5 Max, 18 cores, 48 GB). Script:
`scripts/bench_latency.py`.

## How it was measured

Both classifiers are asked through the daily-audience demo's own gate
(`AddressingMonitor.classify`) and timed by its `classifier_ms`, which covers everything from building the
request to reading the answer. For Sidechat that is tokenising and running the ONNX model in the
bot's process. For Jev it is the HTTPS round trip to the hosted API (`jev-1.13.0`, the demo's
client and 2 s timeout, over an already open HTTP/2 connection).

There are two shapes, each over the demo's 33 sample lines:

- **demo**: the lines as written, with 0 to 2 earlier lines.
- **full window**: the same lines after 8 earlier lines, which is the demo's `history` setting and
  what a line in a running call carries.

Sidechat made 5 passes and Jev 2, after 4 warm-up lines. The passes repeat the same lines, so the
spread below is what one machine shows on these lines, not a sample of all calls. No formal
interval is given for that reason.

## Size

| | Sidechat fp32 | Sidechat int8 | Jev |
|---|---|---|---|
| Parameters | about 150M (Ettin-150M encoder plus small heads) | same | not published (hosted) |
| On disk | 598 MB model + 3.6 MB tokenizer | 267 MB + 3.6 MB | none |
| Resident memory in the bot process | about 1,020 MB | about 715 MB | about 86 MB (Pipecat and the HTTP client) |
| Load time | 0.25 s | 0.25 s | 0.26 s to connect |

Resident memory is the peak for the whole process, including about 69 MB for Python and Pipecat
before the classifier loads.

## Latency per line, ms

| | Threads | demo p50 | demo p90 | demo p99 | full window p50 | full window p90 | full window p99 | Lines |
|---|---|---|---|---|---|---|---|---|
| Sidechat fp32 | 1 | 10.1 | 17.1 | 19.3 | 51.9 | 57.1 | 58.1 | 165 + 165 |
| Sidechat fp32 | 2 (adapter default) | 9.8 | 16.0 | 17.8 | 43.5 | 47.7 | 49.0 | 165 + 165 |
| Sidechat fp32 | 4 | 8.2 | 13.3 | 14.5 | 31.3 | 35.4 | 37.1 | 165 + 165 |
| Sidechat int8 | 1 | 9.0 | 14.2 | 17.5 | 48.9 | 51.7 | 53.2 | 165 + 165 |
| Sidechat int8 | 2 | 7.7 | 11.7 | 14.3 | 35.9 | 38.0 | 39.1 | 165 + 165 |
| Sidechat int8 | 4 | 6.7 | 10.1 | 12.1 | 28.9 | 31.2 | 32.0 | 165 + 165 |
| Jev | n/a | 164.5 | 218.8 | 319.8 | 171.7 | 227.9 | 307.3 | 66 + 66 |

On the first line after loading, Sidechat took 9 to 14 ms and Jev 155 ms.

## What it means

- **On the Mac, Sidechat is much faster than Jev.** It is 16 to 25 times faster on a bare line and
  3 to 6 times faster with a full window, and its tail is far tighter: a p99 of 12 to 58 ms against
  about 310 ms.
- **Sidechat's time grows with the history; Jev's barely does.** A full 8-line window costs 3 to
  5 times a bare line, because the encoder reads every token of it. Jev's time is mostly the
  network trip. In a real call most lines carry a full window, so 30 to 50 ms is the number to
  plan on here, not 10.
- **Extra threads help only on long inputs.** Going from 1 to 4 threads saves about 2 ms on a bare line and 20 ms on
  a full window. int8 saves another 2 to 15 ms and about 300 MB.
- **The demo's deployment is the open question.** `pcc-deploy.toml` runs the bot on Pipecat Cloud
  `agent-1x`, which has 0.5 vCPU and 1 GB of memory, and Silero VAD and smart-turn already share it.
  The cloud section below measures it.

## On cloud CPUs shaped like Pipecat Cloud's profiles (exp-033)

`sidechat/pipeline/latency.py` ran the same bench on Modal: one container per variant, with the
profile's CPU and memory as hard limits. Modal us-east (Azure). Each Sidechat variant ran 198
lines and Jev 132. Median per line in ms, short history / full window.

| | agent-1x: 0.5 vCPU, 1 GiB | agent-2x: 1 vCPU, 2 GiB | agent-3x: 1.5 vCPU, 3 GiB |
|---|---|---|---|
| 150M fp32, 1 thread (910 MB) | 507 / 648; p99 21 s and 25 s | 66 / 253 | 59 / 224 |
| 150M fp32, 2 threads | 304 / 1,403; load 23 s | 120 / 604 | 71 / 327 |
| 150M int8, 1 thread (571 MB) | 103 / 532 | 51 / 271 | 46 / 248 |
| 150M int8, 2 threads | 185 / 710 | 93 / 424 | 55 / 243 |
| 68M fp32, 1 thread (round 1; 524 MB) | 89 / 397 | 33 / 116 | 45 / 193 |
| Jev (114 MB) | 53 / 56 | 144 / 149 | 74 / 76 |

- **On these CPUs Sidechat is slower than Jev.** With a full window, the 150M model takes about
  250 ms on 1 or 1.5 vCPU and 530 to 650 ms on 0.5 vCPU, against Jev's 55 to 150 ms round trip from
  the same data centre. One Modal core is 5 to 6 times slower than the Mac's on this model.
- **fp32 doesn't fit on agent-1x.** At 910 MB in a 1 GiB container it ran, but at the edge of
  memory: lines took up to 21 to 25 s, and loading took 6 to 23 s. int8 (571 MB) runs evenly. The
  real bot needs room for its transport, VAD and smart-turn as well.
- **Use 1 thread on small CPUs.** A second thread was slower everywhere below 1.5 vCPU, often by
  half again or double. The Pipecat adapter's default is 2, which suits a Mac, not `agent-1x`.
- **A smaller model or a shorter context is the way to speed.** The 68M model is about twice as
  fast as 150M. A full window costs 4 to 5 times a short history, so cutting the history in tokens
  would help most. The 32M smoke model couldn't be timed, because it predates the current input
  format.
- **Containers vary.** The same variant differed by up to 1.7 times between the 2x and 3x
  containers (68M: 116 vs 193 ms), and Jev's median ranged from 53 to 149 ms depending on the
  container. Take each number as one container's reading.
