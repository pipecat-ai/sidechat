# Export: exp-027-side-export-r3

Model `side-r3-ettin-150m-s0` (ettin-150m), 598.3 MB.

- Parity with PyTorch on 283 pilot lines in mixed speaker conditions: largest probability difference 7e-06, same decision on 283/283.
- Latency on a Modal CPU, one line at a time: 106.31 ms median and 153.98 ms p95 on 4 threads; 247.39 / 375.07 ms on 1.
- Thresholds carried in config.json: {'respond': 0.6, 'wait': 0.4, 'open': 0.3, 'dev_right': 20625, 'dev_n': 20841, 'dev_wrong_now': 30, 'dev_quiet': 12767, 'max_wrong_now': 0.01, 'real_wrong_now': 0, 'real_quiet': 4186, 'max_wrong_now_real': 0.004}.

## int8 build (`model-int8.onnx`, load with `int8=True`)

- 267.2 MB. Largest probability difference from PyTorch 0.896356; same decision (fp32 thresholds) on 269/283.
- Latency: 63.35 ms median, 104.18 ms p95 on 4 threads; 86.26 / 137.0 ms on 1.
- Its own thresholds on dev (anonymous): {'respond': 0.55, 'wait': 0.4, 'open': 0.3, 'dev_right': 20544, 'dev_n': 20841, 'dev_wrong_now': 33, 'dev_quiet': 12767, 'max_wrong_now': 0.01, 'real_wrong_now': 0, 'real_quiet': 4186, 'max_wrong_now_real': 0.004}. Dev decision right: int8 98.6%, fp32 99.0%; answers now on lines for others: int8 0.3%, fp32 0.2%.
