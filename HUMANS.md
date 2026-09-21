# HUMANS.md — Hyper-Grammar

## Purpose

This file is for humans working on the `hyper-grammar` repo. It is written in plain language. For the exact formal rules agents follow, read `AGENTS.md`. If the two files ever disagree, record it in `TIME.md`. Open frames — unstated or unformalized structure — also belong in `TIME.md`.

## What this repo is

A symbolic library with one operation (`□`) and one starting point (`□`, typed `$` in files).

Everything you build here is a loop: you start at `□`, apply `□` some number of times, and come back to `□`. If your derivation comes back, it's a **form** — it works, it's verified, it's reusable. If it doesn't come back, it's an **open frame** — it's unfinished, or it's telling you something can't close.

That's the whole idea. Loops succeed. Severed chains are either incomplete or informative.

## The six concepts

You only need six things. They fall into three groups.

### Ground

**□ (universality)** — the starting point. This universe, here, now. There is no symbol for "nothing" because there is nothing to name.

### Operation and states

**□ (closure loop)** — the one operation. `□(x)` closes `x` back toward `□`. It's not a step forward; it's a step back toward the base. Every layer loops home.

**Continuation** — work in progress. A derivation you haven't finished yet. It either closes (becomes a form) or stays open (becomes an open frame).

### Three ways to compare things

These go from most foundational to most derived:

- **~ (similarity)** — some overlap in what they can continue into. The primary relation. The only one that survives if you strip away all history — it requires a next, not a past.
- **≡ (congruence)** — same outcome regardless of derivation depth or path. ~ plus structural coincidence.
- **= (equality)** — identical symbol-for-symbol. The finest comparison, but derived — earned by closure, not presupposed. ≡ plus path coincidence.

Dependence runs from ~, not =. Similarity is foundational; equality is the reward at the end.

At `□` itself these three all mean the same thing. They only spread apart as you move away from the base.

## The three rules

1. **Closure isn't collapse.** `□(x)` always produces something — it doesn't erase `x` back to nothing. (`□(x) ≠ □`)
2. **Closure carries the ground.** Every form shares something with `□`. (`□(x) ~ □`)
3. **Double closure returns you home.** Closing twice is similar to where you started. (`□(□(x)) ~ x`)

## How to read a derivation

Derivation files use the `.hg` extension. Each line is one □-application. Read top to bottom to replay the derivation.

```
$            -- start: ground state
□($)         -- first closure
□(□($))      -- second closure: ~ $ by rule 3
```

`$` is how you type `□` in a file. The last line should be `~` the first line. If it isn't, the file is either unfinished or a proof that something external can't close.

The file is its own proof. No separate proof document needed.

## What "closed" and "open" mean

- **Form** — a derivation that loops back to `□`. Verified. Reusable. You can simplify it into a new term (this simplification is called **wcf**, "with form" — it's where "hyper" in hypergrammar comes from, because wcf links simplified terms back to their full derivations like hyperlinks).
- **Open frame** — a derivation that stops without closing. This is not a bug. It's a **revelatory frame**: a proof that whatever system you were modeling can't close in this way.

The inversion from normal computing: in classical programming, a loop is usually bad (infinite loop) and halting is good. Here it's the opposite. Loops are success. Halting means the chain broke.

## Key distinctions

When talking about work in this repo, these pairs mean specific things:

- **Explicit vs. implicit** — explicit means every `□` is spelled out; implicit means you've simplified using wcf.
- **Form vs. frame** — a form has closed; a frame hasn't yet.
- **Verified vs. unverified** — verified means a set of statements closes into its own universe; unverified means it doesn't, or can't.
- **Complete vs. incomplete** — complete means the universe is itself an explicit form; incomplete means it depends on something outside itself.
- **Universe vs. domain** — a universe is the simplest thing that can exist anywhere; a domain is a limited view of one.

## Self-reference

When something refers to itself, don't chase it in circles. Solve for the fixed point — the thing where `F` and `F(F)` are similar — and return that. Self-reference in this system settles, it doesn't regress.

## How this relates to other systems

The grammar type ladder (regular → context-free → context-sensitive → unrestricted) needs a metatheory outside itself to describe the ladder. Hypergrammar has no ladder. Those "types" are cross-sections of the loop at different phases. They look like a hierarchy because the cross-section discards the closure structure.

When you encounter another system and want to see how it fits:

1. Find where it steps outside itself (its frame break).
2. Try to derive its primitives as a phase of the `□`-loop.
3. If you can: it's a subgrammar. If you can't: that's a theorem about its limits.

## How to work here

- Write plain language unless a symbol is necessary to be precise.
- If you change something, consider whether it changes meaning for agents reading `AGENTS.md`.
- Keep explanations short.

## Prime collaboration loop

To keep the repo self-correcting without heavy enforcement, use this default loop:

1. If behavior changed, update the explicit rule in `AGENTS.md`.
2. In the same change, mirror that meaning in plain language in `HUMANS.md`.
3. If any mismatch remains, add one row to `TIME.md` before merge.

Make correction easier than drift:

- Copy the exact source statement into `TIME.md`.
- Describe the mismatch in one sentence.
- Mark status as open, resolved, or under review.

Residual enforcement (intentional):

- If a contradiction is severe or time-critical, contact @timelordraps quickly as required in `AGENTS.md`.

## Contradiction and open frame handling

If you see a mismatch between this file and `AGENTS.md`, or discover unstated/unformalized structure:

1. Note the source statement in `TIME.md`.
2. Describe the mismatch or open frame in one sentence.
3. Mark it open, resolved, or under review.

`TIME.md` is a shared record. Both humans and agents write to it. Tyler Roost (@TimeLordRaps) evaluates entries only in repos where he has committed code.

## Contribution rule

This repo is designed so humans and agents can inspect each other's work. `AGENTS.md` is the explicit spec. This file is the implicit understanding. `TIME.md` is where the two get reconciled.
