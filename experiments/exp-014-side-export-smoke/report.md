# Export: exp-014-side-export-smoke

Model `side-smoke-ettin-32m-s0` (ettin-32m), 128.6 MB.

- Parity with PyTorch on 283 pilot lines in mixed speaker conditions: largest probability difference 6e-06, same decision on 283/283.
- Latency on a Modal CPU, one line at a time: 20.79 ms median and 34.87 ms p95 on 4 threads; 43.32 / 67.85 ms on 1.
- Thresholds carried in config.json: {'respond': 0.6, 'wait': 0.55, 'open': 0.5, 'dev_right': 519, 'dev_n': 633}.
