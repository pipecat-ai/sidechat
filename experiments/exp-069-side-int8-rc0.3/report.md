# int8 for `side-r9-ettin-150m-s1` (exp-069-side-int8-rc0.3)

Recipe: per channel, reduce_range, MatMul with constant B only, each layer's mlp.Wo left in fp32. Parity against fp32 on 283 pilot lines: 281 decisions the same, largest respond difference 0.2804, mean 0.0064.

Dev (anonymous): fp32 98.97% right at its thresholds, int8 98.95% at its own ({'respond': 0.6, 'wait': 0.45, 'open': 0.5, 'dev_right': 21611, 'dev_n': 21841, 'dev_wrong_now': 24, 'dev_quiet': 13074, 'max_wrong_now': 0.01, 'real_wrong_now': 0, 'real_held': 5, 'real_quiet': 4186, 'max_wrong_now_real': 0.004, 'max_held_real': 0.002}); gap 0.02 points (bar 1).

One thread: fp32 298.3 ms a line, int8 191.2 ms (p50). 325.4 MB.

**Passes** the export's gate. Written to `models/side/side-r9-ettin-150m-s1/export-int8`.
