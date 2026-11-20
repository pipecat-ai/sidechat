# Phase 8 notes: how much is left to gain

2026-11-20, after rc0.3. Jon asked whether the data we have, or can find, could still improve the
model significantly. Two free or near-free checks answered the two biggest measured gaps, and an
independent test showed where rc0.3 stands on data made by others. Read this, then
[TODO.md](../TODO.md).

## What was done

- **Duplex-MPE's unnamed requests**
  ([report](../reports/2026-11-20-side-duplex-implicit.md); no cost, stored predictions and tags
  only):
  - They are three quarters of rc0.3's errors there.
  - The model reads them confidently as said to a person.
  - A lower threshold costs about three times the holds on people's lines everywhere.
  - Duplex-MPE writes requests to its assistant with "you" 74% of the time. Real speech is the
    reverse: assistants 7% (SLURP), people asking each other 37% (AMI).
  - So it is mostly the benchmark's style, and training on it would teach the wrong lesson.
- **The name as heard** ([report](../reports/2026-11-20-side-names-as-heard.md), exp-062, about
  $0.90):
  - A dev set of SLURP's train and devel recordings that say "Olly" (1,234 recordings), heard by
    Deepgram plain and with the keyterm.
  - With the keyterm, the name survives in 81.5% of headset recordings and 68.8% of far-field ones.
  - The misses are mostly the name dropped, or common words. A rule restoring one-letter-off words
    recovers 0.2 points safely, or 3 to 5 points while answering about 0.2% of people's lines. No
    rule shipped.
- **An independent test: TCL's Intelligent Wakeup**
  ([report](../reports/2026-11-20-side-tcl-wakeup.md), exp-063, about $0.40; SD-27). People with a
  voice assistant, Sigma, in the room; 3,647 lines, text only, labelled by TCL (for Sigma when
  Sigma speaks next).
  - **Named requests:** every build answers 98.7% at once, the same as Jev.
  - **On answering now, rc0.3 ties Jev** (F1 0.725 against 0.717; paired +0.05 points, -0.47 to
    +0.58), while holding 3% of people's lines to Jev's 37%. rc0.3 and rc0.2 are the same here,
    apart from the known extra holds.
  - **TCL's own audio model, trained on TCL's train split, is well ahead** (F1 0.890). It answers
    76% of unnamed follow-ups (rc0.3 36%) and 0.57% of people's lines outright (rc0.3 1.94%).
  - **The gap is in one place: the line right after the agent answers.** When the other person
    speaks next, rc0.3 separates follow-ups to Sigma from talk to the partner poorly (AUROC 0.67,
    against 0.995 before Sigma has spoken). Half its false accepts are there.
  - **It is not the thresholds.** A threshold chosen on this test gives the same F1.
  - **Part of the false-accept gap is the label.** A quarter of rc0.3's false accepts are lines Sigma
    answers one turn later. Four are questions to Sigma by name, and four a named thanks.
- **Code:**
  - `stt_slurp.run --split dev`, with downloads that resume and recordings cached in R2.
  - The `names-dev*` sets in `build.py`.
  - `sidechat/sources/tcl_wakeup.py` (the converter and TCL's measures) and
    `sidechat/pipeline/tcl.py`. The latter fetches the test split's text columns into R2, then runs
    Jev, scores rc0.3 and rc0.2, and writes the summary.

## Things learned

- **rc0.3 is close to what text can do on the measures we have.** The remaining gaps are:
  - a benchmark's style (Duplex-MPE);
  - information that never reaches the text (a dropped name);
  - real ambiguity in text (nameless questions between people, SD-19).
- **On data made by others, rc0.3 is level with Jev on answering, and much quieter.** It is not
  level with a model trained on that data's own distribution. The remaining loss is who the line
  after the agent's answer is for, which the text barely says.
- **Check before spending.** The three checks cost about $1.30 together and ruled out options that
  would have cost $20 to $60 and taught the wrong thing.

## Loose ends

- Nothing committed. The dev set's transcripts and audio cache live in R2 only (SD-23), and so does
  TCL's text (SD-27).
- TCL's timings are turn onsets only, so this test cannot measure timing input.

## Where the next phase picks up

Options, none urgent:

1. **Timing input** (the pause before the line, overlap with the agent). TCL's test points straight
   at it: the hard line is the one right after the agent stops. Pipecat has the timings, and AMI has
   real ones. It needs a schema and model change, and it is the next real step past text.
2. **Generated follow-ups, now specific.** Three kinds of conversation:
   - the other person following up to the agent without its name;
   - people reacting among themselves to the agent's answer;
   - a person returning to the agent several turns later.

   Measure on TCL's test, which is never trained on. A modest expected gain; TCL's own ranking
   right after Sigma (AUROC 0.67) suggests the text holds little more.
