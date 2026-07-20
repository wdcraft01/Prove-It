from proveit import x, A, Literal
from proveit.logic import Exists
from proveit.logic.irreducible_value import IrreducibleValue
from proveit.logic.sets import InSet


class EmptySetLiteral(Literal, IrreducibleValue):
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='emptyset', latex_format=r'\emptyset',
            styles=styles)

    # def deduce_not_equal(self, other, **defaults_config):
    #     '''
    #     Deduce that self (i.e., the empty set) is not equal to other.
    #     Currently we address two special cases:
    #     (1) We can conclude that A ≠ EmptySet if we know there exists
    #         some x in A.
    #     (2) We can conclude that A U B ≠ EmptySet if we know that
    #         either A ≠ EmptySet or B ≠ EmptySet (or both). This can
    #         be generalized to the case of A1 U A2 U ... U An ≠ EmptySet.
    #     '''

    #     # (1) There exists x in A.
    #     exists_x_in_A = Exists(x, InSet(x, A))
    #     if exists_x_in_A.readily_provable():

