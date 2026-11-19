# Generation: exp-012-side-gen-0.1

Corpus `gen-0.1`: 8095 conversations, 113262 labelled lines.

| Writer | Planned | Written | Input tokens | Output tokens | Est. cost |
|---|---|---|---|---|---|
| o | 4000 | 3995 | 2,822,842 | 2,397,907 | $2.11 |
| a | 1700 | 1700 | 1,190,423 | 651,266 | $4.45 |
| c | 1700 | 1700 | 1,609,232 | 2,631,032 | $22.15 |
| b | 700 | 700 | 890,105 | 494,847 | $13.46 |

Splits: {'train': 84304, 'dev': 8398, 'test': 20560}. Labels: {'ignore': 60270, 'respond': 34631, 'wait': 13254, 'None': 5107}. Lines that keep to their brief: {'1': 110631, '0': 2631}.

**Kinds whose lines most often break their brief**

| Kind | Broken | Of |
|---|---|---|
| `about_reported` | 628 | 1283 |
| `about_judged` | 545 | 1267 |
| `relayed_invite` | 280 | 890 |
| `about_quoted` | 269 | 560 |
| `indirect_wish` | 259 | 679 |
| `about_question_to_group` | 138 | 715 |
| `about_stated` | 112 | 421 |
| `name_slip_corrected` | 82 | 406 |
| `name_word_sense` | 55 | 594 |
| `about_to_named_person` | 32 | 1272 |
| `alias_false_match` | 25 | 294 |
| `question_to_named_person` | 24 | 5161 |
| `never_mind` | 24 | 839 |
| `name_first` | 24 | 6463 |
| `similar_name_person` | 22 | 224 |

**Problems**

- does not mention the agent: 2295
- does not call the agent: 152
- word missing: 55
- calls or names the agent: 46
- alias phrase missing: 25
- does not point at the agent: 8
- does not name Ryan: 5
- misheard name missing: 5
- does not name Aoife: 4
- does not name Mac: 3
