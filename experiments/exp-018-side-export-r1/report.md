# Export: exp-018-side-export-r1

Model `side-r1-ettin-68m-s0` (ettin-68m), 274.2 MB.

- Parity with PyTorch on 283 pilot lines in mixed speaker conditions: largest probability difference 6e-06, same decision on 283/283.
- Latency on a Modal CPU, one line at a time: 52.66 ms median and 82.22 ms p95 on 4 threads; 131.65 / 206.78 ms on 1.
- Thresholds carried in config.json: {'respond': 0.6, 'wait': 0.45, 'open': 0.8, 'dev_right': 8549, 'dev_n': 8654, 'dev_wrong_now': 11, 'dev_quiet': 4821, 'max_wrong_now': 0.01}.

## int8 build (`model-int8.onnx`, load with `int8=True`)

- 69.2 MB. Largest probability difference from PyTorch 0.995173; same decision (fp32 thresholds) on 161/283.
- Latency: 40.82 ms median, 64.92 ms p95 on 4 threads; 76.14 / 118.84 ms on 1.
- Its own thresholds on dev (anonymous): {'respond': 0.98, 'wait': 0.2, 'open': 0.2, 'dev_right': 4821, 'dev_n': 8654, 'dev_wrong_now': 0, 'dev_quiet': 4821, 'max_wrong_now': 0.01}. Dev decision right: int8 55.7%, fp32 98.8%; answers now on lines for others: int8 0.0%, fp32 0.2%.
