from proveit import A, B, Function, Literal, prover

class Disjoint(Function):
    '''
    The Disjoint operation defines a property for a collection of sets.
    It evaluates to True iff the sets are mutually/pairwise disjoint;
    that is, the intersection of any two of the sets is the empty set.
    We define this property to be True when given zero or one set
    (there are no pairs of sets, so all pairs are vacuously disjoint).
    '''
    _operator_ = Literal('disjoint', r'\textrm{disjoint}', theory=__file__)

    def __init__(self, *sets, styles=None):
        Function.__init__(self, Disjoint._operator_, sets,
                          styles=styles)
        self.sets = self.operands

    @prover
    def conclude(self, **defaults_config):
        '''
        Conclude that sets are Disjoint. For this method to work,
        we have three possibilities:

        * Special case of Disjoint(A-B, B-A);
        * special case of Disjoint(A-B, A n B);
        * or one of the sets has a 'deduce_disjointness' method.
        '''
        # Check for special case: Disjoint(A-B, B-A)
        from proveit.logic.sets import Intersect, Difference

        sets = self.sets

        # Check for special two-set cases
        if sets.is_double():
            set_0, set_1 = sets[0], sets[1]

            # Check for Disjoint(A-B, B-A)
            if (isinstance(set_0, Difference)
                and isinstance(set_1, Difference)):

                if (set_0.operands[0] == set_1.operands[1]
                    and set_0.operands[1] == set_1.operands[0]):
                    # We have sets of the form (A-B) and (B-A),
                    # which are always disjoint
                    from proveit.logic.sets.disjointness import (
                            set_diff_commuted_disjoint)
                    _A_sub = set_0.operands[0]
                    _B_sub = set_0.operands[1]
                    inst = set_diff_commuted_disjoint.instantiate(
                            {A:_A_sub, B:_B_sub})
                    return inst

            # Check for Disjoint(A-B, A n B)
            # and its commuted variations
            is_diff_0 = isinstance(set_0, Difference)
            is_diff_1 = isinstance(set_1, Difference)
            is_intersect_0 = isinstance(set_0, Intersect)
            is_intersect_1 = isinstance(set_1, Intersect)

            diff_expr, int_expr = None, None
            if is_diff_0 and is_intersect_1:
                diff_expr, int_expr = set_0, set_1
            elif is_diff_1 and is_intersect_0:
                diff_expr, int_expr = set_1, set_0

            if diff_expr and int_expr:
                # We found something of the form Disjoint(A-B, AnB)
                print(f"Found form Disjoint(A-B,AnB).")
                _A_sub = diff_expr.operands[0]
                _B_sub = diff_expr.operands[1]
                intersect_operands = set(int_expr.operands)
                if intersect_operands == {_A_sub, _B_sub}:
                    from proveit.logic.sets.disjointness import (
                            diff_and_intersect_disjoint)
                    inst = diff_and_intersect_disjoint.instantiate(
                            {A:_A_sub, B:_B_sub})
                    return inst
    
        for operand in self.sets:
            if hasattr(operand, 'deduce_disjointness'):
                return operand.deduce_disjointness(self)

        raise NotImplementedError(
                "Cannot conclude %s; non of the sets have a "
                "'deduce_disjointness' method."%self)
