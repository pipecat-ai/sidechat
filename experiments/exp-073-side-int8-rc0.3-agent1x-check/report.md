# int8 against fp32 on the test sets (`side-r9tt-ettin-32m-s1`, exp-073-side-int8-rc0.3-agent1x-check)

int8 at its own thresholds 0.55/0.45, fp32 at 0.55/0.45.

| Set | Rows | Same decision | Right, fp32 | Right, int8 | Others answered, fp32 | int8 | Others held, fp32 | int8 |
|---|---|---|---|---|---|---|---|---|
| duplex-mpe-0.1 | 52,364 | 99.72% | 95.67% | 95.67% | 0.33% | 0.33% | 0.70% | 0.69% |
