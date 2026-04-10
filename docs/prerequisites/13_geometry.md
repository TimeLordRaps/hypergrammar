# Geometry (Chapter 13)

> **Chapter relationship:** Chapters 01–12 built the hypergrammar loop, its fractal compression, and its biological substrate. Before the system can look at its own geometry (Chapter 14, Meta-Geometry), it needs to state what geometry *is* — what the system is about to meta-level. This chapter is the base formalism. It provides the vocabulary that meta-geometry will generalize.

> **Why here, not earlier:** Geometry was implicitly present since Chapter 01 — parse trees have closure-native description, the grammar type ladder has inclusion structure, degrees of freedom are geometric. But its explicit status as a discipline with axioms, methods, and known limitations was never stated. Meta-geometry cannot generalize what has not been named.

---

## Part I: What Geometry Studies

### 1.1 The Subject Matter

Geometry is the study of **space**, **shape**, **measurement**, and **structure**. More precisely: geometry studies the properties of figures that are preserved under transformations.

The word derives from Greek *geo-* (earth) + *-metria* (measurement). Its origin is surveying — measuring land after the Nile's annual floods erased boundary markers. From this practical root grew the most abstract of mathematical disciplines.

### 1.2 The Flat-Geometry Method

The *Elements* (c. 300 BCE) established the paradigm: begin with definitions, postulates (axioms), and common notions, then derive everything else by logical deduction.

**Five postulates:**

1. A straight line can be drawn between any two points.
2. A straight line can be extended indefinitely.
3. A circle can be drawn with any center and radius.
4. All right angles are equal.
5. *(The parallel postulate)* If a line crossing two lines makes the interior angles on one side less than two right angles, the two lines, if extended, meet on that side.

Postulates 1–4 are simple. Postulate 5 is conspicuously complex. Two thousand years of effort to derive it from the others failed — because it is independent of them. That independence is the crack through which meta-geometry enters.

### 1.3 What Geometry Assumes

Every geometry presupposes:

- **A space** — a set of elements (points, lines, planes) with specified relations.
- **A metric** — a way to measure distance between elements. Flat-geometry distance: $d(p,q) = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$.
- **Transformations** — operations that move figures within the space (translation, rotation, reflection, scaling).
- **Invariants** — properties that survive the transformations. Flat geometry's invariants: distance, angle, area. Projective geometry's invariants: cross-ratio, incidence.

The choice of which transformations to admit determines which invariants exist, which determines what the geometry *is*. This was the insight of the transformation-group classification (1872): a geometry is defined by its transformation group.

---

## Part II: The Geometries

### 2.1 Flat Geometry

The geometry of flat space. Curvature = 0 everywhere. The parallel postulate holds: through a point not on a line, exactly one parallel can be drawn.

**Key properties:**
- Angles of a triangle sum to $\pi$ (180°).
- The right-triangle distance relation holds: $a^2 + b^2 = c^2$.
- Similar figures exist at every scale.
- The space is infinite, homogeneous, and isotropic.

This is the geometry of everyday experience at human scales. It is also a special case — the zero-curvature limit of a more general family.

### 2.2 Non-Flat Geometries

**Hyperbolic geometry:** The parallel postulate is replaced: through a point not on a line, *infinitely many* parallels can be drawn. Curvature is negative. Triangles' angles sum to less than $\pi$. The space expands faster than flat space as you move outward. No similar figures at different scales.

**Elliptic (spherical) geometry:** No parallels exist — all lines eventually meet. Curvature is positive. Triangles' angles sum to more than $\pi$. The space is finite but unbounded (like the surface of a sphere). Straight lines are great circles.

The three cases — positive, zero, negative curvature — are exhaustive for spaces of constant curvature. Real spaces can have curvature that varies from point to point (variable-curvature geometry).

### 2.3 Projective Geometry

Projective geometry studies the properties preserved under *projection* — the operation of viewing a figure from a point (like a shadow cast by a light source). It discards metric information (distance, angle) and retains only incidence (which points lie on which lines) and cross-ratio.

Every pair of lines meets in projective space (there are no parallel lines — "parallel" lines meet at a point at infinity). This is achieved by adding *points at infinity* to the flat plane, one for each direction. The resulting space is the projective plane.

The projective-Absolute unification: flat, hyperbolic, and elliptic geometries are all subgeometries of projective geometry, obtained by choosing different *Absolutes* — a distinguished conic in the projective plane that determines the metric.

### 2.4 Variable-Curvature Geometry

The manifold generalization (1854) generalized all of the above. A variable-curvature manifold is a space where:

- Each point has a local coordinate system (a neighborhood that looks flat).
- The *metric tensor* $g_{ij}$ at each point determines how distances and angles are measured locally.
- The curvature can vary smoothly from point to point.

Flat space, spheres, hyperbolic planes, and every smooth surface are special cases. So are the spacetimes of general relativity. The key move: **curvature became a variable, not a constant**.

---

## Part III: Why This Matters for Hypergrammar

### 3.1 Geometry as Comprehension

The NOTE in [Chapter 00 (Learning Path)](./00_learning_path.md) distinguishes comprehension from understanding. Geometry is the comprehension side: the ability to see closure-native description, trace derivation paths, manipulate derivation-native relations.

The parse trees of Chapter 01, the inclusion chain of Chapter 02, the loop of Chapter 03 — all of these are geometric objects. The hypergrammar derivation chain $\square \to L(\square) \to L(L(\square)) \sim \square$ is a path in a space. The relations $=$, $\equiv$, $\sim$ are metrics at different resolutions.

### 3.2 The Hidden Parameter

Every geometry carries a hidden parameter: its **curvature**. Flat geometry hides it by setting it to zero and never varying it. The parallel postulate is the sentence that encodes this hidden zero — which is why it looks unlike the other postulates. It is not axiom-shaped. It is parameter-shaped.

This is the crack. Meta-geometry (Chapter 14) enters through it.

### 3.3 The Transformation-Group Connection

The transformation-group classification says: a geometry is its transformation group. Different groups → different geometries. The group is the *invariant-selector*: it determines what properties are visible and what properties are destroyed by motion.

In hypergrammar terms: the transformation group is the closure operator $L$. Different choices of $L$ produce different geometries of the derivation space. The three relations ($=$, $\equiv$, $\sim$) correspond to three increasingly permissive transformation groups — the finest preserving syntactic identity, the coarsest preserving only continuation overlap.

---

## Scaffold

- Script: [`13_geometry_scaffold.py`](./13_geometry_scaffold.py)
- Artifact target: `./scaffolds/13_geometry/`

Next step: read [`14_meta_geometry.md`](./14_meta_geometry.md) to see what happens when geometry becomes aware of its own hidden parameter.

---

## Legend

| Structural Term | Classical Cross-Reference |
|----------------|---------------------------|
| flat geometry / zero-curvature geometry | Euclidean geometry (Euclid, c. 300 BCE) |
| flat-geometry method | Euclid's method (*Elements*, c. 300 BCE) |
| non-flat geometries | non-Euclidean geometries (19th century) |
| hyperbolic geometry | Lobachevsky–Bolyai geometry (1829–1832) |
| variable-curvature geometry | Riemannian geometry (Riemann, 1854) |
| variable-curvature manifold | Riemannian manifold |
| manifold generalization (1854) | Riemann's 1854 Habilitationsschrift |
| transformation-group classification (1872) | Klein's Erlangen Programme (1872) |
| projective-Absolute unification | Cayley–Klein unification |
| grammar type ladder | Chomsky hierarchy (Chomsky, 1956) |
| right-triangle distance relation | Pythagorean theorem (Pythagoras, c. 500 BCE) |
