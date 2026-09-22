# The definitional space

What `hypergrammar` is, what it may never become, and the primitives its lowest
level is made of.

Written 2026-09-22 from measurement of `hypermath`, `hyperlogic`, `hyperethics`
and `hyperphysics` as they stand on disk. Every structural claim below names the
file it was read from.

---

## 0. What this repository is

`hypergrammar` is the shared definitional space the four foundational domains are
referenceable *through*. It is not a fifth foundation, not their common ancestor,
and not a theory any of them imports.

The distinction is load-bearing, because two of the four have already written down
a test that a fifth foundation would fail:

- `hyperethics/lean4/lakefile.toml` — *"a foundation that needs a stage index, an
  ordinal notation, or a proof assistant to state its ground is not a foundation."*
- `hyperlogic/L0_triangle.hm`, GC-2 — *"if the triangle turns out to need a
  Form-like carrier in order to be stated at all, then hyperlogic is not a
  foundation, it is hypermath Section VIII with new spelling, and this repository
  should be archived."*

So the governing constraint is stated once and never relaxed:

> **hypergrammar contains positions, never occupants.** It has no ground, no
> constant, no carrier, and no theorem about anything that fills a position.

Section 7 turns that sentence into three machine-checkable tests, because a
commitment that lives only in prose is one refactor away from being false.

---

## 1. The measured problem: every theory is sealed

All three foundations that have an `.hm` ground declare the same seven positions.
Read from `hypermath/L0_ground.hm`, `hyperlogic/L0_triangle.hm`,
`hyperethics/L0_creation.hm`:

| position | hypermath | hyperlogic | hyperethics |
|---|---|---|---|
| carrier | `Form` | `Sign` | `Realm` |
| claim sort | `Prop` | `Claim` | `Norm` |
| constant | `ground` | `closure` | `archetype` |
| operation | `apply` | `turn` | `create` |
| relation 1 | `struct-distinct` | `log-advances` | `norm-other` |
| relation 2 | `struct-continues` | `log-derives` | `norm-inhabits` |
| relation 3 | `struct-orbits` | `log-returns` | `norm-returns` |

Each declares a claim *sort* — a first-class `Type`, not a metalanguage `Prop`.
`hypermath/L0_ground.hm` says why, in as many words: *"propositions are
first-class objects in this system, not metalanguage."*

**And not one of them declares a predicate over that sort.** The axioms assert the
claim-valued term bare:

```
axiom ax-diff:
    for-all x :: Form:
        struct-distinct(apply(x), ground)
```

`struct-distinct(apply(x), ground)` inhabits the declared claim sort. The `axiom`
keyword is what asserts it. Assertion is therefore a **keyword of the file format**,
not an operation in the object language.

### The consequence

A theory whose object language can form claims but cannot *mention* them is sealed.
Inside it you cannot:

- state a conditional between two claims without borrowing the host's implication;
- quantify over claims;
- say a claim is *held by* a bearer — which is exactly what a deontic domain needs;
- and, decisively, **relate a claim in one domain to a claim in another** — because
  a cross-domain statement mentions two claims and asserts neither.

That last point is the whole of it:

> **Folding is impossible until a claim can be mentioned without being asserted.**
> The content of a fold is a relation *between* claims, and a sealed theory has no
> syntax for one.

### The damage is already measurable, and it has a repeating shape

This is not a prediction. Every time two repositories have needed the same absent
mechanism, each has invented it separately and the inventions have collided. Three
instances, all present on disk today:

**1. The assertion predicate.** Both Lean translations hit the gap above and
repaired it differently, and neither repair is in the `.hm` source:

- `hyperethics/lean4/Hyperethics/L0Creation.lean` adds `Norm : Type` **plus**
  `Borne : Norm -> Prop` — an assertion predicate, invented by the translator.
- `hypermath/lean4/Hypermath/L0Ground.lean` instead collapses the claim sort into
  Lean's native `Prop`, deleting the reification its own `.hm` file declares and
  explains.

**2. The warrant ladder.** Two repositories define an enum named `Warrant`, with
the same first member and different ladders:

- `hyperphysics/src/hyperphysics/transport.py` — `BORROWED_FORM`, `DIMENSIONAL`,
  `DERIVED`.
- `metamathethicology/src/metamathethicology/will_electrophysics.py` —
  `BORROWED_FORM`, `TERMFORMED`.

Same name, incomparable gradings. A claim carrying one cannot be ordered against a
claim carrying the other, which is the one thing a warrant is for.

**3. The cross-domain bridge.** `metamathethicology/src/metamathethicology/spaces.py`
requires one — `Rule.__post_init__` raises *"cross-domain inference needs an
explicit bridge"* when a rule's premises span domains without one — and then
validates it only as a nonempty string. The gate exists; nothing resolves what it
names.

The pattern is the argument. A mechanism that four independent repositories each
need, each build, and each build incompatibly is a position that belongs in a
shared space and is currently in no one's.

---

## 2. Primitives

Eight. Each is about positions and the relations between them; none mentions any
occupant, which is what keeps the space from becoming a ground.

### P1. Position

A named hole with a declared shape: a name, an arity, and a sort-discipline
(carrier-valued, claim-valued, or a sort itself). A position is never filled inside
`hypergrammar`. Nothing can be derived from a hole, which is precisely the property
wanted.

### P2. Signature

A finite set of positions together with the constraints among them. A domain's
declared shape.

hypermath's and hyperlogic's signatures have **the same positions and are different
objects**, because their constraints differ: hypermath's orbit constraint closes at
`apply(apply(x))`, hyperlogic's at `turn(turn(turn(x)))`. Same seven holes, an
involution in one and a three-cycle in the other.

### P3. Judgement

The layer `.hm` is missing. Three forms, and the first two must be distinguished
because the file format currently conflates them:

```
C claim @ S          -- C is a well-formed claim in signature S    (formation)
|-_S C               -- C is asserted in S                         (assertion)
C @ S ~=_w D @ T     -- C in S corresponds to D in T at warrant w  (correspondence)
```

The third form is why the space exists. It mentions two claims, asserts neither,
and belongs to neither domain — so it can live nowhere except here.

**Most of this is already built, in the wrong place and in the wrong language.**
`metamathethicology/src/metamathethicology/spaces.py` has `Judgment` — *"an
uninterpreted, domain-tagged ground proposition available at a stage"* — carrying a
`domain` and a `stage`, with equal predicates in different domains held distinct.
`Assumption` separates a premise from its declared basis. `Rule` carries premises,
a conclusion, a justification, and `bridge: str | None`, and refuses to construct a
cross-domain rule without one.

That is the judgement layer, and it is good. Three things are wrong with where it
sits:

- It is **at height 2 only**. Its `Domain` enum is closed over `metamath`,
  `metaphysics`, `metaethics`, `metalogic` — the meta level. The foundations it
  ultimately rests on cannot use it, and the `.hm` files it reads cannot express it.
- **The bridge never resolves.** `bridge` is validated as a nonempty string. The
  gate is real; the referent is not checked. This is the reference mechanism's
  missing half, locatable to one line.
- It is **Python**, so no proof object crosses it.

So P3 is a relocation with two additions: resolve the bridge, and state the
correspondence form the bridge is currently standing in for.

### P4. Fold

A **partial** map of positions from signature S to signature T, together with a
named **residue**: the positions that do not map and the constraints that do not
survive.

The residue is the content, not the failure. The hypermath-to-hyperlogic fold maps
all seven positions and its residue is the orbit period — an involution against a
three-cycle. That residue is a fact about the family, and a design that quantified
the period away as a parameter would have deleted it.

### Folds are not the only edge, and they are not the enforced one

Measured across the family, two different relations are both being called
"dependency", and only the second is enforced anywhere:

- **Fold** — signature S corresponds to signature T. A relation between
  *presentations*. Carries a warrant. Nothing enforces one today.
- **Supply** — theory B consumes structure that theory A declares. A relation
  between *artifacts*. It is not graded, because it is not an analogy: either the
  structure is there or the build fails.

The one mechanically-enforced edge in the whole family is a supply edge, and it
runs **opposite** to the way the family is usually described:
`hypermath/lean4/lakefile.toml` requires `Ordinatics` by path, and
`Hypermath/L3Ordinatics.lean` imports it. `ordinatics/lean4/lakefile.toml` has no
requires at all and imports nothing from hypermath. ordinatics states the same
direction in its own words — hypermath *"assumes one instance of the structure
instead of restating the clauses"*, and calls that a dependency edge rather than a
citation.

So ordinatics is not an arithmetic built over hypermath; it is a substrate hypermath
consumes. A space that had only folds would have had to record that edge as a
correspondence, which would have been false.

**And the family's own descriptor gets this wrong.** `docs/family/family-graph.json`
labels the hypermath→ordinatics edge `"kind": "citation"`, downgrading the single
enforced build edge to the weakest kind it has — and it also records the reverse
edge, so the one real relation appears twice, in both directions, both mislabelled.
The descriptor is additionally **forked**: it ships in ten repositories under two
different digests, an older six-node cluster with no dependency edges at all and a
newer eleven-node cluster, and no repository holds both.

### P5. Warrant

The strength grading on folds and correspondences. Written in
`hyperphysics/src/hyperphysics/transport.py`:

```
BORROWED_FORM   -- algebraic shape reused, nothing else claimed
DIMENSIONAL     -- target argued to share dimensional structure
DERIVED         -- target derived independently and agrees
```

Only `DERIVED` licenses transporting a theorem. `hyperlogic/L0_triangle.hm` already
says its own shared shape is the weakest rung — *"The shape is deliberate and is
not evidence that the content is the same"* — it just had no grading to say it in.

**There is a second, incompatible `Warrant` enum** in
`metamathethicology/src/metamathethicology/will_electrophysics.py`:
`BORROWED_FORM`, `TERMFORMED`. Shared name, shared bottom rung, incomparable tops.
Two claims carrying different ladders cannot be ordered against each other, which
defeats the purpose of grading them.

A warrant is meaningless unless it is the *same* warrant everywhere, so the space
must own exactly one ladder and both repositories must cite it rather than declare
it. Which ladder, and where `TERMFORMED` sits in it, is a decision this document
does not take — but it cannot stay two.

### P6. Height

**A level's height is one more than the height of what its variables range over.**

```
0  foundation   hypermath, hyperlogic, hyperethics, hyperphysics
                quantifies over its own carrier
1  theory       quantifies over constructions in a foundation
2  meta         metamath, metalogic, metaethics, metaphysics
                quantifies over theories of a domain
3  field        quantifies over tuples of meta-levels across domains
```

This is checkable rather than assertable, because "what the variables range over"
is readable off a signature. Two consequences of measuring it rather than assuming
it:

- **Height 1 is currently empty, or nearly so.** `ordinatics` looks like the
  obvious inhabitant and is not one — P4 shows it supplying structure *downward*
  into hypermath rather than being built over it. `grounded-hyperset-theory` names
  hypermath and ordinatics as what it builds on, in prose, with no mechanical
  binding. Whether either has a height is an open measurement, not a filled row.
- **Height 3 is where `metamathethicology`'s files sit, not the repository.** Its
  `Domain` enum is closed over the four meta-domains, and each of its `.hm` files
  declares its own combination over them — so the files are height-3 fields and the
  repository is their home. See P7.

A height is a property of a presentation, not of a directory, and the family's
directory names do not determine it.

### P7. Field

A tuple of signatures at one height across different domains, plus the folds among
them.

`metamathethicology` is **not one field** — it is the *home* for fields, and each
of its files declares its own width. The declaration syntax already exists, and it
is corpus-wide: line 3 of every `.hm` file is `-- <repo> | <what>`. In the
foundations the right-hand side is prose (`hyperethics | moral-grounding`). In
`metamathethicology` it is a combination expression:

```
-- metamathethicology | metaethics x metamathematics x metalogic
-- metamathethicology | metaethics x metaphysics
```

`x` is the combination operator, it takes a different arity per file, and no parser
anywhere reads that line. So P7 is a factoring, not an invention: promote line 3
from comment to declaration.

The repository's own rule for what belongs there is already written —
*"a field states its own subject once, and anything COMBINING fields is a
combination field"* — and its constraint on such a field is *"combines two fields
this package does not depend on"*, which is the non-importing, cite-only discipline
P8 formalises.

Fields are combinatorial: over four domains there is a field for each non-empty
subset. A field's warrant is the **minimum over its folds**, so a field is exactly
as strong as its weakest link and never stronger.

### P8. Reference

A resolvable citation from a position in one signature to a position in another,
travelling **along a fold** and inheriting that fold's warrant.

This is the resolution mechanism that exists nowhere today. Across the whole `.hm`
corpus every filename mention sits inside a `--` comment and `import` appears only
as header prose.

**The targets exist. Nothing can follow the pointer.** Three cross-repo `.hm`
references were previously recorded as naming files that were in no repository; all
three were re-measured 2026-09-22 and **all three resolve** — to
`metamathethicology/p0_barrier.hm`, `metamathethicology/will_electrophysics.hm`,
and `formal-universality/hypermath/P0_perpetual_uncertainty.hm`, the last being a
hypermath P0 layer living outside hypermath with no counterpart inside it. Two of
the three are untracked, so they resolve on this disk and would not survive a
clone.

That is the sharper statement of the problem, and a better one: the references are
not dangling, they are **unfollowable**. A pointer no mechanism can dereference is
indistinguishable from a broken one, and the cost of the confusion is a repeated
report that work does not exist when it does.

A reference is therefore machine-checked twice: its target must resolve, **and** a
fold or supply edge must exist beneath it. The second check is the new one, and it
is what makes cross-domain citation honest instead of decorative.

---

## 3. The composition law

This is the one invention rather than a factoring, and it is forced by P4.

**`DERIVED` folds compose. `BORROWED_FORM` folds do not.**

Along a path of folds, a correspondence's warrant is the minimum of the links —
and a path containing more than one `BORROWED_FORM` link carries **no warrant at
all**, rather than carrying `BORROWED_FORM`.

The reason is partiality. Folds carry residue; composing partial maps compounds the
residues. Two shape-similarities do not make a shape-similarity, because by the
second hop the surviving positions may agree only where nothing was ever measured.
So at the weak rung the relation is reflexive and symmetric but **not transitive**.

That shape has a name — a **tolerance relation** — and it is already in this
repository's own ancestry. The precursor engine's `relation_similar` is reflexive
and symmetric and deliberately not transitive; it is the one genuinely non-trivial
idea in the earlier work. It was correct, and it was attached to the wrong thing.
It belongs on folds.

So the space is **a tolerance at the bottom and a category at the top**: strong
correspondences compose associatively, weak ones only neighbour.

### What this computes today

hypermath and hyperlogic fold at `BORROWED_FORM` and no higher, on the measured
evidence and by hyperlogic's own statement. Therefore any claim relating an
arithmetic built over hypermath to a logic built over hyperlogic is
`BORROWED_FORM` — **it cannot be a theorem**, and it never becomes one by being
restated. Raising it requires an actual derivation, which is what `DERIVED` means.

The rule bites hardest on the widest fields. `metamathethicology`'s files declare
their own widths on line 3 — one spans two meta-domains, two span three — and any
path across three or more domains on today's folds crosses more than one weak link,
so those files compute to **no warrant**. That is not a criticism of them; it is the
first thing the space says about them, and it names the upgrade path exactly: which
folds must reach `DERIVED`, and in which order.

---

## 4. The two prefixes: one is adjudicated, the other is undefined

It is tempting to read the family's two prefixes as opposite directions on the
height axis — `hyper-` descending toward a ground, `meta-` ascending toward
reflection. **That reading must not be adopted, and the reason is a finding rather
than a preference.**

`metamathethicology/VOCABULARY_BOUNDARY.md` is the one file in the family that
adjudicates vocabulary, and it records that `hyper-` is already used in two
incompatible ways across one author's corpus:

- **arity-raised / multi-valued** — one input, a nonempty class as output. The
  sense in hyperoperation, hypergraph, hyperstructure, hyperfield.
- **recursive across levels** — `hyperstratum`'s sense.

It rules for the first, on the grounds that it is the one with published
mathematics behind it and the one already dominant in the corpus, and it rules
against adopting `hyperstratum`'s vocabulary at all. (The same audit checked
`hyperstratum`'s claim to be upstream of four named repositories and found three of
the four carry no reference to it.)

A corpus whose own audit names a two-meaning collision as the root cause does not
need a third meaning. **So `hyper-` is settled, this document does not reopen it,
and nothing below depends on reading it as a direction.**

`meta-` is the opposite situation: **no file in the family defines it.** Searching
`hypermath`, `hyperlogic`, `hyperethics`, `hyperphysics`, `hyperstratum` and
`metamathethicology` for a definition of the prefix returns only `hyperstratum`'s —
*"representation, interpretation, constraint, transformation, or condition of the
base"* — and that account was rejected wholesale along with the rest of its
vocabulary. `VOCABULARY_BOUNDARY.md` adjudicates `hyper-` and is silent on `meta-`.

In practice `meta-` is used with a consistent operational meaning that nobody has
written down: **the combination level** — the place a claim goes when it spans
fields, which is exactly the placement rule of P7. Defining it is in scope for a
definitional space, and it is one of the few naming jobs here that is open rather
than already decided.

### The question the height axis creates, stated without the prefixes

Independent of what the prefixes mean: **is there a level that is its own
foundation and its own reflection** — a fixed point of descending and ascending in
P6's sense? That is the self-containment the family is circling, and `hypermath`
already names it. `Hypermath.selfDerivation` is a `def`, not a `theorem`; the
proposition is stated and unproved, and the audit reports precisely that.

The space does not answer this. It makes the question statable, which is the first
thing that has been true of it.

---

## 5. Why folding needs the judgement layer, concretely

The interaction this space exists to permit, in the author's words, is *"a logic
defined over hyperlogic (grounded-hyperset-theory) interacting with an arithmetic
formed from hypermath (ordinatics), all over an ethical system of values formed
from hyperethics."*

**That stack is the target, not the current state, and the difference is worth
stating plainly before designing for it.** Measured 2026-09-22:

- `grounded-hyperset-theory` names `hypermath` and `ordinatics` as what it builds
  on. The string `hyperlogic` does not occur anywhere in it outside a generated
  descriptor file. The citation runs the other way: `hyperlogic` cites *it*.
- `ordinatics` is a substrate `hypermath` consumes, not an arithmetic formed over
  it — see P4.
- The value system over `hyperethics` does not exist yet, which the author already
  says. The only artifact built over `hyperethics` is `metamathethicology`, and its
  dependency on it is a git pin in an optional extra that no source file imports.

So all three legs of the intended stack are currently either absent, prose-only, or
pointing the opposite way. **This is an argument for the space rather than against
it**: the stack is not buildable today precisely because nothing can express the
edges it needs, and the design below is what those edges would be.

A statement like *"this ordinal construction is admissible under that set-theoretic
logic and satisfies that value constraint"* decomposes into exactly the primitives
above:

1. Three claims, one per domain, each **mentioned and not asserted** — needs P3.
2. Two correspondences relating them — needs P3's third form and P4.
3. A warrant on each correspondence — P5.
4. A resolvable reference from each citing position to each cited one — P8.
5. A composite warrant, the minimum along the path, with the two-weak-links rule
   applying — section 3.

Remove the judgement layer and step 1 fails, so the statement cannot be *written* —
which is the situation today. Every one of the other pieces already exists somewhere
in the family. This is the missing one.

---

## 6. The assertion position, and what its naming reveals

Section 1 found that all four domains need a predicate on the claim sort and none
declares one. In the space this is a position like any other: **assertion**, of
discipline claim-valued.

Each domain names it, and the naming is a residue worth keeping rather than
normalising away. `hyperethics`' translator reached for `Borne`, because in an
ethical domain assertion *is* bearing — a norm can exist without anyone bearing it.
That is the deontic character of the domain showing up in what it calls a shared
position.

This is the general rule, found by accident here and worth stating:

> **The residues are where the domains' distinctive content lives.** What a domain
> names differently, or fails to map, is its substance. A design that abstracted the
> differences away in order to share the shape would throw away precisely the part
> that was interesting.

---

## 7. Three tests, so that section 0 is checked rather than promised

The commitment "a space, not a ground" must be mechanical, because a prose
commitment is one refactor away from being silently false.

1. **`no_terminal`** — there is no signature that every other signature folds into.
   (No universal ground.)
2. **`no_initial`** — there is no signature that folds into every other.
   (No universal substrate.)
3. **Vacancy** — the signature module declares no axiom, no constant, no carrier,
   and no theorem about any occupant. A structural test over the source, not a
   convention.

Together these are the machine-checkable form of the answer to hyperlogic's GC-2
and hyperethics' lakefile commitment. GC-2 fires if hyperlogic needs *a Form-like
carrier* — a hypermath object — to be stated. A carrier-shaped **hole** in a
repository that provably contains no carrier is a different thing, and tests 1-3
are what make that unarguable instead of asserted.

---

## 8. What the space buys, stated as things that become possible

- A claim can be mentioned without being asserted, so a cross-domain statement can
  be written down at all.
- A cross-domain citation is followable, or fails loudly — replacing prose
  references whose targets exist but which no mechanism can dereference.
- One warrant ladder instead of two incompatible ones, so two claims can be
  ordered against each other.
- Every cross-domain claim carries a computed warrant, and the weak ones are
  visibly weak instead of reading like theorems.
- Folds and supply edges stop being called the same thing, so the family's one
  enforced build edge stops being recorded as a citation running both ways.
- `metamathethicology`'s files each get a height, a width, a current rating, and a
  named upgrade path.
- Height becomes a measured property of a presentation instead of an inference
  from a directory name.
- The asymmetries — orbit period, the claim sort's naming, an ethical domain
  calling assertion *bearing*, `hyperphysics` refusing a layer index entirely —
  are recorded as content rather than normalised into parameters.

---

## 9. Open, and deliberately not decided here

- **Does `hyperphysics` have a signature at all?** It declares no carrier, no
  ground, no operation, and refuses a layer index on purpose — *"it graduates as a
  citation surface"*. It may be a transport surface **over** the other three rather
  than a fourth instance of the shape, in which case the space needs a second kind
  of object and not a row of empty columns.
- **Which warrant ladder is canonical**, and where `TERMFORMED` sits relative to
  `DIMENSIONAL` and `DERIVED`. The space must own one; this document does not
  choose it.
- **What `meta-` means.** Nothing in the family defines it, its operational use is
  "the combination level", and writing that down is in scope here. `hyper-` is
  already adjudicated and is not reopened.
- **Is the height fixed point reachable**, and does the family's self-containment
  claim depend on it?
- **Which fold should be raised first.** Every cross-domain result is capped by the
  weakest link on its path, so the ordering here decides what becomes provable and
  in what order. It is a research question, not a build step.
- **Does height 1 have any inhabitant today?** Both obvious candidates turned out
  not to be built over a foundation in any enforced sense.
