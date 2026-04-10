$( 
  Extended Metamath test file for hypergrammar stack-level proof execution.
  Exercises: multi-step proofs, substitution, disjoint-variable enforcement.

  Based on propositional calculus from metamath/set.mm (develop branch).
  Source: https://github.com/metamath/set.mm/blob/develop/set.mm
  Upstream commit: e4c0fea5b90d4d807e6f588a064025cec1d3adbb
$)

  $( Constants. $)
  $c ( $.
  $c ) $.
  $c -> $.
  $c -. $.
  $c wff $.
  $c |- $.

  $( Variables. $)
  $v ph $.
  $v ps $.
  $v ch $.

  $( Floating hypotheses. $)
  wph $f wff ph $.
  wps $f wff ps $.
  wch $f wff ch $.

  $( Syntax: negation. $)
  wn $a wff -. ph $.

  $( Syntax: implication. $)
  wi $a wff ( ph -> ps ) $.

  $(
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    Core axioms
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  $)

  ${
    min $e |- ph $.
    maj $e |- ( ph -> ps ) $.
    $( Modus ponens. $)
    ax-mp $a |- ps $.
  $}

  $( Axiom 1 (Simp). $)
  ax-1 $a |- ( ph -> ( ps -> ph ) ) $.

  $( Axiom 2 (Frege). $)
  ax-2 $a |- ( ( ph -> ( ps -> ch ) ) -> ( ( ph -> ps ) -> ( ph -> ch ) ) ) $.

  $( Axiom 3 (Transp). $)
  ax-3 $a |- ( ( -. ph -> -. ps ) -> ( ps -> ph ) ) $.

  $(
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    Identity inference (trivial compressed proof, exercises B index)
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  $)

  ${
    idi.1 $e |- ph $.
    idi $p |- ph $=
      ( ) B $.
  $}

  $(
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    a1i: from |- ph derive |- ( ps -> ph )
    Uncompressed proof exercises multi-step substitution.
    Proof: a1i.1, wph, wps, ax-1, wph, wps, wph, wi, ax-mp
    (push hyp, build wi instance, push ax-1, apply ax-mp)
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  $)

  ${
    a1i.1 $e |- ph $.
    $( Add antecedent. $)
    a1i $p |- ( ps -> ph ) $=
      wph wps wph wi a1i.1 wph wps ax-1 ax-mp $.
  $}

  $(
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    DV exercise section
  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  $)

  $c setvar $.
  $c e. $.
  $c class $.

  $v x $.
  $v y $.
  $v z $.
  $v A $.

  vx $f setvar x $.
  vy $f setvar y $.
  vz $f setvar z $.
  cA $f class A $.

  $( x is element of A. $)
  wel $a wff x e. A $.

  $( Disjoint variable restrictions. $)
  $d x y $.
  $d x z $.
  $d y z $.

  $( Axiom using disjoint set variables: if x e. A then y e. A.
     The $d x y restriction on dvel means any application must substitute
     distinct set variables for x and y. $)
  ${
    dvel.1 $e |- x e. A $.
    $( From x e. A derive y e. A (with distinct x, y). $)
    dvel $a |- y e. A $.
  $}

  $( Theorem: from z e. A derive y e. A.
     Substitutes x->z, y->y in dvel.
     The mandatory $d pair (x,y) from dvel requires that the images of x and y
     under substitution have disjoint variables: {z} and {y} are disjoint. $)
  ${
    dvth.1 $e |- z e. A $.
    dvth $p |- y e. A $=
      vz vy cA dvth.1 dvel $.
  $}
