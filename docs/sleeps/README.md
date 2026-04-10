# docs/days — Production Notes

## Purpose

Each day gets one MD and one MP3. The MD is clean narration text for TTS with no formatting. The MP3 is the final audio artifact. The file loops as a continuous 90-minute sleep-cycle-aligned track.

---

## Sleep Architecture and Loop Timing

Standard 90-minute sleep cycle model (Walker, Littlehales). Cycles are uniform at 90 minutes. N3 (deep/slow-wave sleep) dominates early cycles. REM dominates later cycles. The non-REM portion of each cycle shrinks by 10 minutes per cycle as REM expands by 10 minutes.

| Cycle | Non-REM (min) | REM onset from sleep onset | REM window |
|-------|--------------|--------------------------|------------|
| 1     | 80           | t = 80 min               | 80–90 min  |
| 2     | 70           | t = 160 min              | 160–180 min|
| 3     | 60           | t = 240 min              | 240–270 min|
| 4     | 50           | t = 320 min              | 320–360 min|
| 5     | 40           | t = 400 min              | 400–450 min|

6 hours of sleep = 4 complete cycles (360 min). 7.5 hours of sleep = 5 complete cycles (450 min).

---

## Loop Design

The full narration is exactly 90 minutes (~11,700 words at 130 wpm). The entire loop is spoken narration. There is no ambient filler segment. The loop restarts immediately at the end of the 90-minute file.

```
[NARRATION: 90 min — full structured arc]
```

The loop restarts at: t = 0, 90, 180, 270, 360 min from sleep onset.

REM onsets are at: t = 80, 160, 240, 320, 400 min.

The narration ends at approximately t = 80 min within each cycle. The final chapter (Chapter 5: recursive now-frame, specious present) arrives 10 minutes before each REM onset, landing in N1/N2 as a MILD-mechanism cue that primes the prospective memory activation REM delivers.

---

## Structural Design: Front 40 / Reverse 50

The narration is not in chapter-number order. It is structured in two halves:

```
[FRONT 40 MIN — ~5,200 words — Foundations]
  Ch0:  learning path + worthiness note
  Ch1:  grammar fundamentals (symbol, rule, derivation)
  Ch2:  Chomsky hierarchy mapped to loop phases
  Ch3:  hyper-inversion (the loop move)
  Ch4:  degrees of freedom
          ↕ PIVOT ↕
[BACK 50 MIN — ~6,500 words — Reverse complexity arc]
  Ch14: existential emotions (planned)
  Ch13: metageometry and the open frame
  Ch12: consolidative recurrence, protocols, territory access
  Ch11: fractal compression and metahyperrevision
  Ch10: necessity constraint form
  Ch9:  mensaclaused metaretrocausality
  Ch8:  corrective time syntropy
  Ch7:  transframe ontology
  Ch6:  recursive now-frame expanded
  Ch5:  recursive now-frame  ← last before REM onset
```

The reverse ordering in the back half is deliberate. See Chapter 12, Section 3.3 for full documentation of the TMR-optimal design rationale.

Short version: complex material (Ch14, Ch13) arrives during deepening N2/N3 in the consolidation window. Fundamental temporal material (Ch6, Ch5) arrives last, priming the temporal-parietal junction just as REM activates. Later sleep cycles have progressively longer REM windows, so the back half plays in increasingly rich REM territory on nights with more than four cycles.

---

## Voice Design

The MP3 is generated with VoxCPM2 (openbmb/VoxCPM2). Voice design is specified as a style descriptor prefix in the narration text.

**Model:** `openbmb/VoxCPM2`

**Vocal style descriptor:**
```
(A deep, calm, close male voice; dark-lux bedtime tone, velvety and soothing, west coast sandman vibe, soft sandalwood warmth, light ocean mist, relaxed tide-like rhythm, slow pacing, gentle breath, clean low resonance, comforting, dreamy, hypnotic, safe, elegant, midnight shoreline ambience)
```

Generation script: `docs/days/generate_mp3.py`

---

## File Inventory

| File | Type | Status | Notes |
|------|------|--------|-------|
| `04092026.md` | narration text | complete | 11,641 words, 89.5 min |
| `04092026.mp3` | audio artifact | pending | VoxCPM2 generation required |
| `generate_mp3.py` | generation script | complete | uses voxcpm library |
| `README.md` | production notes | this file | |

---


---

## Sleep Architecture and Loop Timing

Standard 90-minute sleep cycle model (Walker, Littlehales). Cycles are uniform at 90 minutes. N3 (deep/slow-wave sleep) dominates early cycles. REM dominates later cycles. The non-REM portion of each cycle shrinks by 10 minutes per cycle as REM expands by 10 minutes.

| Cycle | Non-REM (min) | REM onset from sleep onset | REM window |
|-------|--------------|--------------------------|------------|
| 1     | 80           | t = 80 min               | 80–90 min  |
| 2     | 70           | t = 160 min              | 160–180 min|
| 3     | 60           | t = 240 min              | 240–270 min|
| 4     | 50           | t = 320 min              | 320–360 min|
| 5     | 40           | t = 400 min              | 400–450 min|

6 hours of sleep = 4 complete cycles (360 min). 7.5 hours of sleep = 5 complete cycles (450 min).

---

## Loop Design

The full audio file is exactly 90 minutes. It loops continuously through the night.

```
[NARRATION: 18 min] + [SSILD AMBIENT: 72 min] = 90 min
```

The loop restarts at: t = 0, 90, 180, 270, 360 min from sleep onset.

REM onsets are at: t = 80, 160, 240, 320, 400 min.

**The narration plays 10 minutes before each REM onset.** This is the MILD mechanism (Chapter 12, Section 2.3): semantic content installed during the N1/N2 transition (light sleep at cycle start) primes the prospective memory that fires when REM arrives. The narration does not play during REM. It installs the cue that REM activates.

In cycle 1: narration lands in N1/N2, primes REM arriving at t=80.
In cycle 2: narration lands at t=90 (N1/N2 of cycle 2), primes REM at t=160.
In cycles 3–5: non-REM shrinks, so the narration lands closer to REM onset each cycle. By cycle 5, REM begins only 40 minutes after the narration ends.

For 4-cycle sleep: narration plays 4 times.
For 5-cycle sleep: narration plays 5 times.

---

## SSILD Ambient Segment (72 minutes)

The ambient portion should implement the sensory cycling protocol from Chapter 12, Section 2.4. Suggested structure:

- Minutes 0–18: narration (see above)
- Minutes 18–30: pink noise or 1/f noise, low volume transition from narration
- Minutes 30–60: binaural theta beats (4–7 Hz carrier) or continuous pink noise; sub-arousal threshold
- Minutes 60–72: fade toward silence or very low ambient hold; body natural sleep deepening
- Minutes 72–90: silence or breath-paced minimal ambient; N3 territory

The exact ambient content is outside the scope of the narration documents. The narration files specify content only.

---

## Narration Specifications

Target duration: 18 minutes.
Target word count at 130 wpm: 2,340 words.
Format: plain prose, no markdown, no symbols, no headers, no bullet points, no mathematical notation. Every sentence should be speakable without interpretation by the TTS model.
Naming convention: MMDDYYYY.md for the narration text, MMDDYYYY.mp3 for the final wrapped audio.

---

## Files

| File | Description |
|------|-------------|
| 04092026.md | April 9 2026 narration — founding session. 2,316 words (~17.8 min at 130 wpm). |
| 04092026.mp3 | To be generated. Full 90-min loop: narration + SSILD ambient. |
