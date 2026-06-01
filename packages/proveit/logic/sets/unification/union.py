from proveit import (
        equality_prover, ExprRange, Literal, Operation, USE_DEFAULTS,
        relation_prover, SimplificationDirectives)
from proveit import i, j, k, m, n, A, B, C, S, x
from proveit.abstract_algebra.generic_methods import (
        apply_association_thm, apply_commutation_thm,
        apply_disassociation_thm, group_commutation)


class Union(Operation):
    # operator of the Intersect operation
    _operator_ = Literal(
        string_format='union',
        latex_format=r'\cup',
        theory=__file__)

    _simplification_directives_ = SimplificationDirectives(
            ungroup=True)

    def __init__(self, *operands, styles=None):
        '''
        Union any number of sets: A union B union C
        '''
        Operation.__init__(self, Union._operator_, operands,
                           styles=styles)

    def membership_object(self, element):
        from .union_membership import UnionMembership
        return UnionMembership(element, self)

    def nonmembership_object(self, element):
        from .union_membership import UnionNonmembership
        return UnionNonmembership(element, self)

    @relation_prover
    def deduce_superset_eq_relation(self, superset, **defaults_config):
        # Check for special case of a union subset
        # A_1 union ... union ... A_m \subseteq S
        from . import union_inclusion
        _A = self.operands
        _m = _A.num_elements()
        _S = superset
        return union_inclusion.instantiate(
                    {A:_A, m:_m, S:_S})

    @equality_prover('unary_reduced', 'unary_reduce')
    def unary_reduction(self, **defaults_config):
        '''
        Given self = [Union(A)], derive and return the equality
        between self and A (i.e., |- Union(A) = A).
        '''
        from . import unary_union_reduction
        if not self.operands.is_single():
            raise ValueError("Union expression must have a single operand "
                             "in order to invoke unary_reduction. ")
        operand = self.operands[0]
        return unary_union_reduction.instantiate({A: operand})

    @equality_prover('redundancy_reduced', 'redundancy_reduce')
    def redundancy_reduction(self, **defaults_config):
        '''
        Given self = Union(A, A, ..., A), derive and return the
        equality between self A:

            |- Union(A, A, ..., A) = A
        '''

        # Case (1) Union(A, A)
        if (len(self.operands) == 2):
            if self.operands[0] == self.operands[1]:
                from . import redundant_union_binary
                _A_sub = self.operands[0]
                return redundant_union_binary.instantiate({A: _A_sub})

        # Case (2) Union(A, ..., A) but not using ExprRange
        # TBA

        # Case (3) Union(A,...,A) using ExprRange as single operand
        if (self.operands.num_entries() == 1
            and isinstance(self.operands[0], ExprRange)):

            expr_range = self.operands[0]
            _A_sub = expr_range.body

            from proveit.numbers import one

            if expr_range.true_start_index == one:
                from . import redundant_union_range
                return redundant_union_range.instantiate(
                    {n: expr_range.true_end_index, A: _A_sub})
            else:
                from . import redundant_union_range_general
                _i_sub = expr_range.true_start_index
                _j_sub = expr_range.true_end_index
                return redundant_union_range_general.instantiate(
                    {i:_i_sub, j:_j_sub, A:_A_sub})

    @equality_prover('consolidated_to_unionall', 'consolidate_to_unionall')
    def consolidation_to_unionall(self, instance_param=None, **defaults_config):
        '''
        From self = Union(A(i), A(i+1), ..., A(j)) using a single
        ExprRange operand, derive and return the equality of self with
        its alternative UnionAll form:

            |- Union(A(i), A(i+1), ..., A(j))
               = Unionall(k, A(k), for k in {i,...,j})

        If 'instance_param' is provided, use it as the 'k' parameter.
        Otherwise, use the parameter of the given ExprRange (which
        will be some generic canonical such as '_a').
        '''
        # from proveit import ExprRange
        # from proveit.logic import InSet
        # from proveit.numbers import Interval
        if (self.operands.num_entries() != 1
            or not isinstance(self.operands[0], ExprRange)):
            raise ValueError(
                    "'Union.unionall_equation()' method may only be "
                    "used on a Union with a single ExprRange operand.")

        from . import union_eq_unionall
        expr_range = self.operands[0]
        _i_sub = expr_range.true_start_index
        _j_sub = expr_range.true_end_index
        _k_sub = (expr_range.parameter if instance_param is None
                  else instance_param)
        _A_sub = expr_range.lambda_map

        proven_unionall = union_eq_unionall.instantiate(
                {i:_i_sub, j:_j_sub, k:_k_sub, A:_A_sub})
        
        return proven_unionall

    @equality_prover('commuted', 'commute')
    def commutation(self, init_idx=None, final_idx=None, **defaults_config):
        '''
        Deduce that this Union expression is equal to a form in which
        the operand at index init_idx has been moved to index final_idx.
        For example, (a U b U ... U y U z).commutation(1, -2) will
        produce: |-  (a U b U ... U y U z) = (a U ... U y U b U z).
        '''
        from . import commutation, leftward_commutation, rightward_commutation
        return apply_commutation_thm(
            self, init_idx, final_idx, commutation,
            leftward_commutation, rightward_commutation)

    @equality_prover('group_commuted', 'group_commute')
    def group_commutation(self, init_idx, final_idx, length,
                          disassociate=True, **defaults_config):
        '''
        Deduce that this Union expression is equal to a form in which
        the operands at indices [init_idx, init_idx+length) have been
        moved to [final_idx, final_idx+length).
        It will do this by performing association first.
        If disassociate is True (the default), the specified operands
        will be disassociated before returning.
        '''
        return group_commutation(
            self, init_idx, final_idx, length, disassociate=disassociate)

    # @equality_prover('moved', 'move')
    # def permutation_move(self, init_idx=None, final_idx=None,
    #                      **defaults_config):
    #     '''
    #     Given numerical operands, deduce that this expression is equal 
    #     to a form in which the operand
    #     at index init_idx has been moved to final_idx.
    #     For example, (a · b · ... · y · z) = (a · ... · y · b · z)
    #     via init_idx = 1 and final_idx = -2.
    #     '''
    #     return self.commutation(init_idx=init_idx, final_idx=final_idx)

    # @equality_prover('permuted', 'permute')
    # def permutation(self, new_order=None, cycles=None, **defaults_config):
    #     '''
    #     Deduce that this Add expression is equal to an Add in which
    #     the terms at indices 0, 1, …, n-1 have been reordered as
    #     specified EITHER by the new_order list OR by the cycles list
    #     parameter. For example,
    #         (a·b·c·d).permutation_general(new_order=[0, 2, 3, 1])
    #     and
    #         (a·b·c·d).permutation_general(cycles=[(1, 2, 3)])
    #     would both return ⊢ (a·b·c·d) = (a·c·d·b).
    #     '''
    #     return generic_permutation(self, new_order, cycles)

    @equality_prover('associated', 'associate')
    def association(self, start_idx, length, **defaults_config):
        '''
        Deduce that this expression is equal to a form in which
        operands in the range [start_idx, start_idx+length) are
        grouped together. For example,

            (A U B U C U D U E U ... U Y U Z).association(2, 3)

        would derive and return:

            |- (A U B U C U D U E U ... U Y U Z)
               = (A U B U (C U D U E) U ... U Y U Z)
        '''
        from . import association
        return apply_association_thm(self, start_idx, length, association)

    @equality_prover('disassociated', 'disassociate')
    def disassociation(self, idx, **defaults_config):
        '''
        Deduce that this expression is equal to a form in which the
        operand at index idx is no longer grouped together.
        For example,

            (A U B U (C U D U E) U ... U Y U Z).disassociation(2)

        would derive and return:

            |- (A U B U (C U D U E) U ... U Y U Z)
               = (A U B U C U D U E U ... U Y U Z)
        
        Multiple indices can be provided for multiple disassociations
        simultaneously, e.g. expr.disassociation(2, 3, 4)
        '''
        from . import disassociation
        return apply_disassociation_thm(self, idx, disassociation)

    @equality_prover('distributed_over_intersection',
                     'distribute_over_intersection')
    def distribution_over_intersection(self, target='right', **defaults_config):
        '''
        Given self = Union(A, Intersect(B1, B2, ..., Bn)), and
        target='right' (the default), derive and return the equality
        between self and its distributed form:

        |- Union(A, Intersect(B1, B2, ..., Bn))
           = Intersect(Union(A, B1), Union(A, B2),..., Union(A, Bn))

        A could be a single set or some more complex expression
        representing a set, but will be kept as a unit.

        Similarly, given self = Union(Intersect(A1, A2, ..., Am), B),
        and target='left', derive and return the equality between self
        and its distributed form:

        |- Union(Intersect(A1, A2, ..., Am), B)
           = Intersect(Union(A1, B), Union(A2, B),..., Union(Am, B))

        For a full cross distribution of both sides, use
        target = 'both'.
        '''
        from proveit.logic.sets import Intersect
        from proveit.numbers import two
        if not (self.operands.is_double() and
               (isinstance(self.operands[0], Intersect)
                or isinstance(self.operands[1], Intersect))):
            raise ValueError(
                    "'Union.distribution_over_intersection()' method "
                    "only valid for Union with 2 operands with at least "
                    "one of the operands being an Intersect().")

        # Case: target = 'right' (the default)
        if target == 'right':
            if not isinstance(self.operands[1], Intersect):
                raise ValueError(
                        "'Union.distribution_over_intersection()'' method "
                        "with target = 'right' only valid for Union with "
                        "second of two operands being an Intersect().")
            from . import distribution_over_intersection_right
            from proveit.numbers import num
            _n_sub = self.operands[1].operands.num_elements()
            _A_sub = self.operands[0]
            _B_sub = self.operands[1].operands
            return distribution_over_intersection_right.instantiate(
                    {n:_n_sub, A:_A_sub, B:_B_sub})

        # Case: target = 'left'
        if target == 'left':
            if not isinstance(self.operands[0], Intersect):
                raise ValueError(
                        "'Union.distribution_over_intersection()'' method "
                        "with target = 'left' only valid for Union with "
                        "first of two operands being an Intersect().")
            from . import distribution_over_intersection_left
            from proveit.numbers import num
            _m_sub = self.operands[0].operands.num_elements()
            _A_sub = self.operands[0].operands
            _B_sub = self.operands[1]
            return distribution_over_intersection_left.instantiate(
                    {m:_m_sub, A:_A_sub, B:_B_sub})

        # Case: target = 'both'
        if target == 'both':
            if not (isinstance(self.operands[0], Intersect)
                    and isinstance(self.operands[1], Intersect)):
                raise ValueError(
                        "'Union.distribution_over_intersection()'' method "
                        "with target = 'both' only valid for Union with "
                        "two operands, each of which is an Intersect().")

            # Both operands are Intersect()
            if (isinstance(self.operands[0], Intersect)
                and isinstance(self.operands[1], Intersect)):
                from . import distribution_over_intersection_left_right
                _m_sub = self.operands[0].operands.num_elements()
                _n_sub = self.operands[1].operands.num_elements()
                _A_sub = self.operands[0].operands
                _B_sub = self.operands[1].operands
                print(f"_m_sub = {_m_sub}")
                print(f"_n_sub = {_n_sub}")
                print(f"_A_sub = {_A_sub}")
                print(f"_B_sub = {_B_sub}")
                return distribution_over_intersection_left_right.instantiate(
                        {m:_m_sub, n:_n_sub, A:_A_sub, B:_B_sub})

            # Both operands are IntersectAll()
            # TBA

            