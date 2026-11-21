# int8 against fp32 on the test sets (`side-r9tt-ettin-32m-s1`, exp-073-side-int8-rc0.3-agent1x-check-b)

int8 at its own thresholds 0.55/0.45, fp32 at 0.55/0.45.

| Set | Rows | Same decision | Right, fp32 | Right, int8 | Others answered, fp32 | int8 | Others held, fp32 | int8 |
|---|---|---|---|---|---|---|---|---|
| ambient-bench-0.1 | 16,222 | 99.55% | 97.49% | 97.68% | 0.42% | 0.45% | 2.10% | 1.87% |
| ami-addressee-0.1 | 8,875 | 99.82% | 98.67% | 98.76% | 0.00% | 0.00% | 1.33% | 1.24% |
| ami-silent-0.1.test | 10,434 | 99.91% | 99.21% | 99.28% | 0.00% | 0.00% | 0.79% | 0.72% |
| ami-addressee-stt-0.1 | 8,202 | 99.80% | 98.57% | 98.70% | 0.00% | 0.00% | 1.43% | 1.30% |
| pilot-0.4@anonymous | 283 | 98.59% | 86.67% | 86.30% | 3.68% | 4.29% | 6.13% | 5.52% |
| slurp-in-ami-stt-keyterm-0.1 | 2,766 | 98.55% | 86.41% | 86.33% | n/a | n/a | n/a | n/a |
| tcl-wakeup-0.1@anonymous | 3,647 | 99.23% | 92.95% | 93.20% | 2.24% | 2.21% | 2.66% | 2.42% |
