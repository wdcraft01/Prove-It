from proveit import Literal, Operation, USE_DEFAULTS, relation_prover
from proveit import m, n, A, S, x


class Union(Operation):
    # operator of the Intersect operation
    _operator_ = Literal(
        string_format='union',
        latex_format=r'\cup',
        theory=__file__)

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

    # @prover
    def prove_by_cases(self, forall_stmt, **defaults_config):
        '''
        UNDER CONSTRUCTION.
        BASED ON SET.PROVE_BY_CASES().

        For the Union S = A1 U A2 U ... U Am (i.e., self), and given
        a universal quantification 'forall_stmt' over the set S of the
        form [Forall_{x in S} P(x)], conclude and return the Forall
        expression knowing/assuming:

            Forall_{x in A1} P(x) AND Forall_{x in A2} P(x) AND ...
                AND Forall_{x in Am} P(x)
        '''
        from proveit import P, ExprTuple, Function, var_range
        from proveit.logic import Forall, InSet
        from proveit.numbers import one
        assert(isinstance(forall_stmt, Forall)), (
            "May only call the prove_by_cases() method of the Union "
            "class using a Forall (universally quantified) expression "
            "as the first argument. Union.prove_by_cases() was called "
            f"with arg 'forall_stmt' = {forall_stmt}.")
        assert(forall_stmt.conditions.num_entries() >= 1), (
            "When calling the prove_by_cases() method of the Union "
            "class, the Forall argument should have (at least) "
            "a domain condition consisting of a Union.")
        assert(isinstance(forall_stmt.conditions[0], InSet)), (
            "When calling the prove_by_cases() method of the Union "
            "class, the domain condition for the Forall argument "
            "should appear as the first element in the Forall.conditions. "
            "Consider using the 'domain=' kwarg when specifying the "
            "domain when constructing your Forall expression, or "
            "specify the domain using an InSet expression as the first "
            "of the conditions you specify.")

        from . import true_in_each_then_true_in_union

        if (forall_stmt.conditions.num_entries() > 1):
            raise NotImplementedError(
                "Union.prove_by_cases() implemented only for Forall "
                "expressions without explicit conditions. The 'forall_stmt' "
                f"argument was {forall_stmt}.")

        # forall_{x in A1 U A2 U ... U Am} P(x), assuming/knowing P(x)
        # for all x in A1, for all x in A2, ... for all x in Am.
        # This is the basic case where the only condition in the
        # forall_stmt argument is the domain specification.

        # Number of sets [A1, A2, ..., Am] making up the Union
        _m_sub = self.operands.num_elements()

        # Union component elements to substitute
        var_range_update = var_range(A, one, _m_sub)
        _var_range_sub = self.operands

        # Predicate re-definition (using user-supplied instance_var)
        Px = Function(P, forall_stmt.instance_var)

        # Predicate to substitute
        _Px_sub = forall_stmt.instance_expr

        # Instance var to substitute
        _x_sub = forall_stmt.instance_var

        return (true_in_each_then_true_in_union.instantiate(
            {m: _m_sub, ExprTuple(var_range_update): _var_range_sub,
             x: _x_sub, Px: _Px_sub}, num_forall_eliminations=2).
            derive_consequent())
            