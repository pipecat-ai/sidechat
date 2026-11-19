# Export: exp-036-side-tt-smoke-export2

Model `side-ttsmoke-ettin-32m-s0` (ettin-32m), 259.2 MB.

- Parity with PyTorch on 283 pilot lines in mixed speaker conditions: largest probability difference 0.526657, same decision on 270/283.
- Latency on a Modal CPU, one line at a time: 9.56 ms median and 12.49 ms p95 on 4 threads; 14.8 / 18.98 ms on 1.
- Thresholds carried in config.json: {'respond': 0.85, 'wait': 0.6, 'open': 0.3, 'dev_right': 6216, 'dev_n': 8093, 'dev_wrong_now': 38, 'dev_quiet': 4460, 'max_wrong_now': 0.01, 'real_wrong_now': 2, 'real_quiet': 4186, 'max_wrong_now_real': 0.004}.
- Transformer optimizer: not shipped; {'context': {'Gelu': 10, 'LayerNormalization': 1, 'SkipLayerNormalization': 20}, 'line': {'Gelu': 12, 'LayerNormalization': 1, 'SkipLayerNormalization': 20}}; the fused graph took 16.35 ms on 1 thread.
- Two towers: the line alone (history cached) as above; both towers cold on 1 thread 54.61 ms median.

No int8 build shipped: parity too far from PyTorch: same decision on 171/283, largest probability difference 0.936673
