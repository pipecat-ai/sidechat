# int8 for `side-r9tt-ettin-32m-s1` (exp-072-side-int8-rc0.3-agent1x)

Recipe: per channel, reduce_range, MatMul with constant B only, each layer's mlp.Wo left in fp32. Parity against fp32 on 283 pilot lines: 279 decisions the same, largest respond difference 0.2732, mean 0.0069.

Dev (anonymous): fp32 98.55% right at its thresholds, int8 98.55% at its own ({'respond': 0.55, 'wait': 0.45, 'open': 0.6, 'dev_right': 38794, 'dev_n': 39366, 'dev_wrong_now': 40, 'dev_quiet': 23309, 'max_wrong_now': 0.01, 'real_wrong_now': 0, 'real_held': 6, 'real_quiet': 4186, 'max_wrong_now_real': 0.004, 'max_held_real': 0.002}); gap 0.0 points (bar 1).

One thread: fp32 25.1 ms a line, int8 14.2 ms (p50). 195.1 MB.

**Passes** the export's gate. Written to `models/side/side-r9tt-ettin-32m-s1/export-int8`.
