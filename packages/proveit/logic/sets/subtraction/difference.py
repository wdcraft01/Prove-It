from proveit import Literal, Operation, TransRelUpdater, USE_DEFAULTS
from proveit import x, A, B


class Difference(Operation):
    # operator of the Difference operation
    _operator_ = Literal(string_format='-', theory=__file__)

    def __init__(self, A, B, *, styles=None):
        Operation.__init__(self, Difference._operator_, [A, B],
                           styles=styles)
    
    def membership_object(self, element):
        from .difference_membership import DifferenceMembership
        return DifferenceMembership(element, self)

    def nonmembership_object(self, element):
        from .difference_membership import DifferenceNonmembership
        return DifferenceNonmembership(element, self)

    '''
    In some of the Difference methods below, we adopt the "factor"
    terminology from the Add class and consider expressions such as
    (A n B) - (C n B) to be "factorable" into (A - C) n B, where each
    Intersect term in the difference has an intersection operand or
    "factor" in common.
    It's interesting and important to note that such distribution and
    factorization identities do NOT apply for a Difference of Unions.
    '''

    def readily_factorable(self, factor):
        '''
        Return True iff 'factor' is factorable from 'self' in an
        obvious manner.  For this set Difference, a "factor" is
        readily factorable if it is an Intersect operand in each of
        the Difference operands. For example, the set Difference:

            (B n A) - (C n B)

        is readily factorable for factor B, and

            self.readily_factorable(B)

        should return True.
        '''
        from proveit.logic.sets import Intersect
        for op in self.operands:
            if not isinstance(op, Intersect):
                return False
            if factor not in op.operands:
                return False
        return True

    # @auto_equality_prover('factorized', 'factor')
    def factorization(self, the_factors, pull="left",
                      group_factors=True, group_remainder=True,
                      **defaults_config):
        '''
        Factor out the "factors" from this set Difference, pulling the
        factors out either to the "left" or "right".
        As mentioned more generally in comments above, we adopt the
        "factor" terminology from the Add class and model this
        factorization method on the Add.factorization() method,
        considering expressions such as (A n B) - (C n B) to be
        "factorable" into (A - C) n B, where each Intersect term in
        the difference has an intersection operand or "factor" in
        common.

        Other factorizations might be possible and can be added in
        future installments. It's interesting and important to note
        that such factorization (and related distribution) identities
        do NOT apply for a Difference of Unions.

        If group_factors is True, the factors are grouped
        together as a sub-product.

        In the set Difference case, the remainder will always be
        grouped (we have 'group_remainder' as a parameter just for
        recursion compatibility).
        '''
        from proveit.numbers.multiplication import distribute_through_sum
        from proveit.numbers import one, Mult

        from proveit.logic.sets import Intersect

        # Confirm that each Difference operand is an Intersect, and
        # each Intersect has the desired "factors" operands
        for op in self.operands:
            if not isinstance(op, Intersect):
                raise ValueError(
                        "Difference.factorization() currently only "
                        "applies to a Difference of Intersections, but "
                        f"factorization was attempted on: {self} .")

            # Confirm that each Intersect has all the desired "factor"
            # operands, but not ONLY those factors
            for factor in the_factors:
                if factor not in op.operands:
                    raise ValueError(
                            "In calling Difference.factorization() on "
                            f"{self}, factor/operand {factor} is "
                            f"missing from Difference operand {op}.")
            _extra_intersect_op = False
            for _intersect_op in op.operands:
                if _intersect_op not in the_factors:
                    _extra_intersect_op = True
            if not _extra_intersect_op:
                raise ValueError(
                        "In calling Difference.factorization() on "
                        f"{self}, one of the Intersect operands is "
                        "completely subsumed by the desired factors, "
                        "which is not currently allowed.")

        if pull not in ('left', 'right'):
            raise ValueError(
                    "In calling Difference.factorization(), 'pull' "
                    "must be set to 'left' or 'right'.")

        # Yay! We seem to have plausible operands and plausible factors!

        expr = self
        # For convenience in updating our equation
        eq = TransRelUpdater(expr)

        display(eq.relation)

        # replacements = list(defaults.replacements)
        # _b = []

        # if not isinstance(the_factors, Expression):
        #     # If 'the_factors' is not an Expression, assume it is
        #     # an iterable and make it an Intersect.
        #     the_factors = Intersect(*the_factors)

        # # factor the_factor from each term
        # for _i in range(expr.terms.num_entries()):
        #     term = expr.terms[_i]
        #     if term == the_factors:
        #         if pull == 'left':
        #             replacements.append(Mult(term, one).one_elimination(1))
        #         else:
        #             replacements.append(Mult(one, term).one_elimination(0))
        #         _b.append(one)
        #     else:
        #         if not hasattr(term, 'factorization'):
        #             raise ValueError(
        #                 "Factor, %s, is not present in the term at "
        #                 "index %d of %s!" %
        #                 (the_factors, _i, self))
        #         term_factorization = term.factorization(
        #             the_factors, pull, group_factors=group_factors,
        #             group_remainder=True)
        #         if not isinstance(term_factorization.rhs, Mult):
        #             raise ValueError(
        #                 "Expecting right hand side of each factorization "
        #                 "to be a product. Instead obtained: {0} for term "
        #                 "number {1} (0-based index).".
        #                 format(term_factorization.rhs, _i))
        #         if pull == 'left':
        #             # the grouped remainder on the right
        #             _b.append(term_factorization.rhs.operands[-1])
        #         else:
        #             # the grouped remainder on the left
        #             _b.append(term_factorization.rhs.operands[0])
        #         # substitute in the factorized term
        #         expr = eq.update(term_factorization.substitution(
        #             expr.inner_expr().terms[_i]))
        # if not group_factors and isinstance(the_factors, Mult):
        #     factor_sub = the_factors.operands
        # else:
        #     factor_sub = ExprTuple(the_factors)
        # if pull == 'left':
        #     _a = factor_sub
        #     _c = ExprTuple()
        # else:
        #     _a = ExprTuple()
        #     _c = factor_sub
        # _b = ExprTuple(*_b)
        # _i = _a.num_elements()
        # _j = _b.num_elements()
        # _k = _c.num_elements()
        # distribution = distribute_through_sum.instantiate(
        #     {i: _i, j: _j, k: _k, a: _a, b: _b, c: _c},
        #     preserve_expr=expr, replacements=replacements)
        # eq.update(distribution.derive_reversed())
        # return eq.relation

