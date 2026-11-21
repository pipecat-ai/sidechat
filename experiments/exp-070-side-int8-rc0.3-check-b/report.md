# int8 against fp32 on the test sets (`side-r9-ettin-150m-s1`, exp-070-side-int8-rc0.3-check-b)

int8 at its own thresholds 0.6/0.45, fp32 at 0.6/0.4.

| Set | Rows | Same decision | Right, fp32 | Right, int8 | Others answered, fp32 | int8 | Others held, fp32 | int8 |
|---|---|---|---|---|---|---|---|---|
| ambient-bench-0.1 | 16,222 | 99.38% | 96.89% | 97.19% | 0.28% | 0.30% | 2.83% | 2.50% |
| ami-addressee-0.1 | 8,875 | 99.92% | 98.99% | 99.04% | 0.00% | 0.00% | 1.01% | 0.96% |
| ami-silent-0.1.test | 10,434 | 99.92% | 99.45% | 99.53% | 0.00% | 0.00% | 0.55% | 0.47% |
| ami-addressee-stt-0.1 | 8,202 | 99.87% | 98.87% | 98.93% | 0.01% | 0.01% | 1.12% | 1.06% |
| pilot-0.4@anonymous | 283 | 99.29% | 87.78% | 87.04% | 2.45% | 2.45% | 4.91% | 5.52% |
| slurp-in-ami-stt-keyterm-0.1 | 2,766 | 98.52% | 90.67% | 89.84% | n/a | n/a | n/a | n/a |
| tcl-wakeup-0.1@anonymous | 3,647 | 99.29% | 92.87% | 93.06% | 1.94% | 2.06% | 3.08% | 2.72% |
