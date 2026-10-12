from proveit import USE_DEFAULTS, equality_prover, prover
from proveit import A, B, P, Q, S, X
from proveit.logic import InSet, Set, SetMembership, Union
# from proveit.numbers import num
# from proveit import m, A, x


class PartitionsMembership(SetMembership):
    '''
    Defines methods that apply to membership in Partitions(S), the
    set of partitions of set S. If set S is finite, Partitions(S)
    is a finite set; if S is infinite, Partitions(S) is infinite.
    A partition P of a set S is a set of non-empty subsets S1,S2,...
    of S such that elements of P are mutually disjoint and
    Union(S1,S2,...) = S.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    def side_effects(self, judgment):
        '''
        Main side effect is to unfold the basic definition of
        memberhip in the set of partitions. If P is an element
        of Partitions(S), then P is a set of non-empty disjoint
        subsets of S whose union is S.
        '''
        yield self.unfold

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        For self = [element in Partitions(S)], deduce and return the
        equality:
            [element in Partitions(S)] = 
            [element in SetOfAll(P, P, conditions)_{P in Pow(Pow(S))}]
        where the conditions are:
            * no element of P is the empty set
            * the elems of P are all mutually disjoint
            * the union of all elems of P is S
        '''
        from . import partitions_membership_def
        _X_sub = self.element
        _S_sub  = self.domain.operand
        return partitions_membership_def.instantiate(
                {S: _S_sub, X: _X_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        For self = [element in Partitions(S)], return the expression
        (NOT a judgment):
            [element in SetOfAll(P, P, conditions)_{P in Pow(Pow(S))}]
        where the conditions are:
            * no element of P is the empty set
            * the elems of P are all mutually disjoint
            * the union of all elems of P is S
        '''
        from proveit import A, B, P
        from proveit.logic import Equals, Forall, InSet, NotEquals
        from proveit.logic.sets import (
                Disjoint, EmptySet, PowerSet, SetOfAll, UnionAll)
        _S = self.domain.operand
        _X = self.element
        return InSet(_X,
               SetOfAll(P, P,
               conditions = [Equals(UnionAll(A, A, domain = P), S),
                             Forall(A, NotEquals(A, EmptySet), domain = P),
                             Forall((A, B), Disjoint(A, B), domain = P)],
               domain = PowerSet(PowerSet(S))))

    @prover
    def unfold(self, **defaults_config):
        '''
        Given self = [element in Partitions(S)] and knowing or
        assuming self is True, derive and return
            [element in SetOfAll(P, P, conditions)_{P in Pow(Pow(S))}]
        where the conditions are:
            * no element of P is the empty set
            * the elems of P are all mutually disjoint
            * the union of all elems of P is S
        '''
        from . import partitions_membership_unfolding
        _S_sub = self.domain.operand
        _X_sub = self.element
        return partitions_membership_unfolding.instantiate(
            {S: _S_sub, X:_X_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [elem in Partitions(S)], and knowing or
        assuming that:
            [elem in SetOfAll(P, P, conditions)_{P in Pow(Pow(S))}]
        where the conditions are:
            * no element of P is the empty set
            * the elems of P are all mutually disjoint
            * the union of all elems of P is S,
        derive and return self.
        We attempt to deal with several special cases:
        (1) unpartition, {S} in Partitions(S)
        (2) bipartition, {A, B} in Partitions(S)
        (3) partition-by-subdivision, (P U Q) in Partitions(S)
        '''
        elem = self.element
        _S   = self.domain.operand

        # (1) unpartition, {S} in Partitions(S)
        from proveit.logic import Set
        if (isinstance(elem, Set) and len(elem.elements) == 1
            and elem.operand == _S):
            from proveit.logic.sets.partitions import unipartition
            return unipartition.instantiate({S:_S})

        # (2) bipartition, {A, B} in Partitions(S) if:
        #     -- A, B ≠ EmptySet
        #     -- A U B = S
        #     -- A and B are disjoint
        if isinstance(elem, Set) and len(elem.elements) == 2:
            from proveit.logic.sets.partitions import bipartition
            _A = elem.elements[0]
            _B = elem.elements[1]
            return (bipartition.instantiate({S:_S, A:_A, B:_B}).
                    derive_consequent())

        '''
        (3) partition by subdivision
            To conclude that P U Q is a partition of S, we look to
            see if we have A and B such that:
            -- P is a partition of A
            -- Q is a partition of B
            -- and {A, B} is a partition of S.
            That is, P U Q is simply a finer-grain partition of S
            compared to some known partition {A, B} of S.
        '''
        if isinstance(elem, Union) and len(elem.operands) == 2:
            if self._readily_provable():
                super_partition = self._find_super_partition()[0]
                from . import partition_by_subdivision
                _A_sub = super_partition.operands[0]
                _B_sub = super_partition.operands[1]
                _P_sub = self.element.operands[0]
                _Q_sub = self.element.operands[1]
                _S_sub = self.domain.operand
                return (partition_by_subdivision.instantiate(
                        {A:_A_sub, B:_B_sub, P:_P_sub, Q:_Q_sub, S:_S_sub,}).
                        derive_consequent())

        # (4) otherwise, use most general case
        from . import partitions_membership_folding
        _S_sub = self.domain.operand
        _X_sub = self.element
        return partitions_membership_folding.instantiate({S: _S_sub, X:_X_sub})

    @prover
    def deduce_in_bool(self, **defaults_config):
        from . import partitions_membership_is_bool
        _S_sub = self.domain.operand
        _X_sub = self.element
        return partitions_membership_is_bool.instantiate(
            {S: _S_sub, X:_X_sub})

    def _readily_provable(self):
        '''
        Returns True if self.element is known to be in the domain
        Partitions(S) using fast checks. Returns False otherwise.
        Currently implemented only for self.element of the form P U Q,
        and called from self.conclude() for special cases utilizing
        the partition_by_subdivision theorem.
        '''
        if len(self._find_super_partition()) > 0:
            return True
        return False

    def _find_super_partition(self, **kwargs):
        '''
        A specialized method for use in coordination with the
        _readily_provable() and conclude() methods for the special
        case of self as [(P U Q) in Partitions(S)], and intended for
        coordinated use of the partition_by_subdivision theorem.
        self._find_super_partition() finds and returns a list of all
        known rougher-grained partitions {A, B} in Partitions(S) such
        that P in Partitions(A) and Q in Partitions(B).
        '''
        _elem = self.element
        _S    = self.domain.operand
        if (isinstance(self.element, Union) and len(_elem.operands) == 2 ):
            # We have the form (P U Q) in Partitions(S)
            from proveit.logic.sets import Partitions
            _P = _elem.operands[0]
            _Q = _elem.operands[1]
            p_partitions = set()
            q_partitions = set()

            # Collect sets A for which P in Partitions(A)
            for membership in InSet.yield_known_memberships(
                    _P, domain_type=Partitions._operator_):
                p_partitions.add(membership.domain.operand)

            # Collect sets B for which Q in Partitions(B)
            for membership in InSet.yield_known_memberships(
                    _Q, domain_type=Partitions._operator_):
                q_partitions.add(membership.domain.operand)

            # Construct all {A, B} sets
            a_b_sets = {Set(a, b) for a in p_partitions for b in q_partitions}
            final_a_b_sets = set()
            for a_b_set in a_b_sets:
                for membership in InSet.yield_known_memberships(a_b_set):
                    if (isinstance(membership.domain, Partitions) 
                        and membership.domain.operand == _S):
                        final_a_b_sets.add(a_b_set)

            return list(final_a_b_sets)

        return []



