# Export: exp-023-side-export-r1b

Model `side-r1-ettin-68m-s0` (ettin-68m), 274.2 MB.

- Parity with PyTorch on 283 pilot lines in mixed speaker conditions: largest probability difference 6e-06, same decision on 283/283.
- Latency on a Modal CPU, one line at a time: 86.0 ms median and 138.04 ms p95 on 4 threads; 185.47 / 314.75 ms on 1.
- Thresholds carried in config.json: {'respond': 0.6, 'wait': 0.45, 'open': 0.8, 'dev_right': 8551, 'dev_n': 8733, 'dev_wrong_now': 11, 'dev_quiet': 4821, 'max_wrong_now': 0.01, 'real_wrong_now': 4, 'real_quiet': 4186, 'max_wrong_now_real': 0.004}.

No int8 build shipped: parity too far from PyTorch: same decision on 161/283, largest probability difference 0.999989
