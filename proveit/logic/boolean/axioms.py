from proveit.logic import Booleans, TRUE, FALSE, inBool, Forall, Exists, NotExists, And, Or, Not, Implies, Iff, \
Union, Singleton, Equals, NotEquals
from proveit.common import A, B, C, P, Q, S, x, Px, Qx, Aetc, Betc, Cetc, PxEtc, Qetc, xEtc, etc_QxEtc
from proveit import beginAxioms, endAxioms

beginAxioms(locals())

trueAxiom = TRUE
trueAxiom

boolsDef = Equals(Booleans, Union(Singleton(TRUE), Singleton(FALSE)))
boolsDef

boolsDef = Equals(Booleans, Union(Singleton(TRUE), Singleton(FALSE)))
boolsDef

boolsDef = Equals(Booleans, Union(Singleton(TRUE), Singleton(FALSE)))
boolsDef

falseNotTrue = NotEquals(FALSE, TRUE)
falseNotTrue

eqTrueIntro = Forall(A, Equals(A, TRUE), conditions=[A])
eqTrueIntro

eqTrueElim = Forall(A, A, conditions=[Equals(A, TRUE)])
eqTrueElim

endAxioms(locals(), __package__)


