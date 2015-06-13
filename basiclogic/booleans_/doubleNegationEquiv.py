from proveit.basiclogic import *

# A => Not(Not(A))
doubleNegationImplied = booleans.doubleNegation.specialize().prove()
# Not(Not(A)) => A
impliesDoubleNegation = booleans.fromDoubleNegation.specialize().prove()
# [A => Not(Not(A))] in BOOLEANS if A in BOOLEANS
doubleNegationImplied.deduceInBool().prove({inBool(A)})
# [Not(Not(A)) => A] in BOOLEANS if A in BOOLEANS
impliesDoubleNegation.deduceInBool().prove({inBool(A)})
# forall_{A} A = Not(Not(A))
booleans.qed('doubleNegationEquiv', Iff(A, Not(Not(A))).concludeViaComposition().deriveEquality().generalize(A, inBool(A)))
