from proveit import (
        m, n, x, A, B, C, S, Judgment, Lambda, Literal, relation_prover)
from proveit.logic import Exists, NotEquals
from proveit.logic.irreducible_value import IrreducibleValue
from proveit.logic.sets import InSet

class EmptySetLiteral(Literal, IrreducibleValue):
    '''
    EmptySet represents the standard empty set, which has no elements.
    EmptySet is then defined in the logic/sets common notebook as
    EmptySet = EmptySetLiteral(), so one can import and use 'EmptySet'
    itself.
    '''

    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='emptyset', latex_format=r'\emptyset',
            styles=styles)
    
    def membership_object(self, element):
        from .empty_set_membership import EmptySetMembership
        return EmptySetMembership(element, self)

    def nonmembership_object(self, element):
        from .empty_set_membership import EmptySetNonmembership
        return EmptySetNonmembership(element, self)

    def not_equals_side_effects(self, judgment):
        '''
        For a judgment or assumption of the form A ≠ EmptySet,
        derive the existential Judgment:

          |- Exists_{x} [x in A]

        (i.e., if A is not empty, there must exist an element in A).
        This side-effect method is called from NotEquals.side_effects().
        '''

        from . import EmptySet
        if not isinstance(judgment, Judgment):
            raise ValueError(
                    "EmptySet.not_equals_side_effects() expecting 'judgment' "
                    f"argument to be Judgment but got {judgment}.")
        if not isinstance(judgment.expr, NotEquals):
            raise ValueError(
                    "EmptySet.not_equals_side_effects() expecting "
                    "'judgment' argument to be an inequality Judgment "
                    f"but got {judgment}.")
        if not isinstance(judgment.rhs, EmptySetLiteral):
            raise ValueError(
                    "EmptySet.not_equals_side_effects() expecting "
                    "'judgment' argument have rhs be EmptySet, "
                    f"but got {judgment.rhs}.")
        from proveit.logic.sets import non_empty_unfolding
        _A_sub = judgment.lhs
        yield (lambda : non_empty_unfolding.instantiate({A:_A_sub}))

    @relation_prover
    def deduce_not_equal(self, other, **defaults_config):
        '''
        Deduce that self (i.e., the empty set) is not equal to other.
        Currently we address two special union-related cases:
        
        (1) We can conclude that A U B ≠ EmptySet if we know that
            either A ≠ EmptySet or B ≠ EmptySet (or both), and we can
            generalized to the case of A1 U A2 U ... U An ≠ EmptySet.

        (2) We can conclude that UnionAll_{t}(A(t)) ≠ EmptySet if we
            know that A(t) is non-empty for at least one value of t.
        
        We can also automatically prove that A ≠ EmptySet if we know
        there exists some x in A, but that automaticity is built-in
        as a side-effect in Exists.side_effects(), which in turn calls
        InSet.existential_side_effects().

        '''

        # (1) A Union is non-empty if any set in the Union is non-empty
        from proveit.logic.sets import EmptySet, Union
        if isinstance(other, Union):
            if other.operands.is_double():
                # A U B ≠ EmptySet if A ≠ EmptySet or B ≠ EmptySet.
                if NotEquals(other.operands[0], EmptySet).readily_provable():
                    from proveit.logic.sets.unification import (
                            union_with_nonempty_left)
                    _A_sub = other.operands[0]
                    _B_sub = other.operands[1]
                    return union_with_nonempty_left.instantiate(
                            {A:_A_sub, B:_B_sub}).derive_reversed()
                if NotEquals(other.operands[1], EmptySet).readily_provable():
                    from proveit.logic.sets.unification import (
                            union_with_nonempty_right)
                    _A_sub = other.operands[0]
                    _B_sub = other.operands[1]
                    return union_with_nonempty_right.instantiate(
                            {A:_A_sub, B:_B_sub}).derive_reversed()

            if other.operands.num_elements().as_int() > 2:
                _nonempty_idx = -1
                # find the first Union element ≠ EmptySet (if any)
                for _idx, _op in enumerate(other.operands):
                    if NotEquals(_op, EmptySet).readily_provable():
                        _nonempty_idx = _idx
                        break
                if _nonempty_idx != -1:
                    # we found a Union element ≠ EmptySet
                    from proveit.logic.sets.unification import (
                            union_with_nonempty)
                    _A_sub = other.operands[:_idx]
                    _B_sub = other.operands[_idx]
                    _C_sub = other.operands[_idx+1:]
                    _m_sub = _A_sub.num_elements()
                    _n_sub = _C_sub.num_elements()
                    return (union_with_nonempty.instantiate(
                            {m:_m_sub, n:_n_sub,
                             A:_A_sub, B:_B_sub, C:_C_sub}).
                           derive_reversed())

        # (2) A UnionAll(A(i)) is non-empty if A(i) is non-empty for
        #     for some i.
        from proveit.logic.sets import UnionAll
        if (isinstance(other, UnionAll)
            and other.instance_params.is_single()):

            _param = other.instance_params[0]
            _expr = other.instance_expr
            _domain = other.domain
            _A_sub = Lambda(_param, _expr)
            _existential_claim = (
                Exists(_param, NotEquals(_expr, EmptySet), domain = _domain))
            if _existential_claim.readily_provable():
                from proveit.logic.sets.unification import (
                        union_all_with_nonempty_exists_folding)
                _S_sub = _domain
                return (union_all_with_nonempty_exists_folding.instantiate(
                        {A:_A_sub, S:_S_sub}).derive_reversed())
            else:
                # If the UnionAll domain is explicit and finite,
                # we can try a little harder to make the existential
                # claim provable.
                from proveit.numbers import Interval, num
                if (isinstance(_domain, Interval)
                    and _domain.lower_bound.is_irreducible_value()
                    and _domain.upper_bound.is_irreducible_value()):
                    # Look for domain elem i s.t. A(i) ≠ EmptySet
                    _min = _domain.lower_bound.as_int()
                    _max = _domain.upper_bound.as_int()
                    _example_found = False
                    for _i in range(_min, _max + 1):
                        _ne = NotEquals(_A_sub.apply(num(_i)), EmptySet)
                        if _ne.readily_provable():
                            _existential_claim.conclude_via_example(num(_i))
                            _example_found = True
                            break
                    if _example_found:
                        from proveit.logic.sets.unification import (
                                union_all_with_nonempty_exists_folding)
                        _S_sub = _domain
                        return (union_all_with_nonempty_exists_folding.
                                instantiate(
                                {A:_A_sub, S:_S_sub}).derive_reversed())

                from proveit.logic.sets import Set
                if isinstance(_domain, Set):
                    # Look for domain elem i s.t. A(i) ≠ EmptySet
                    _example_found = False
                    for item in _domain.operands:
                        _ne = NotEquals(_A_sub.apply(item), EmptySet)
                        if _ne.readily_provable():
                            _existential_claim.conclude_via_example(item)
                            _example_found = True
                            break
                    if _example_found:
                        from proveit.logic.sets.unification import (
                                union_all_with_nonempty_exists_folding)
                        _S_sub = _domain
                        return (union_all_with_nonempty_exists_folding.
                                instantiate(
                                {A:_A_sub, S:_S_sub}).derive_reversed())


        # (3) If it isn't a special case treated here, just use
        #     conclude-as-folded.
        return NotEquals(self, other).conclude_as_folded()
