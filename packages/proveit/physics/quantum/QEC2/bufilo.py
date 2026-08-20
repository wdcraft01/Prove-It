from proveit import (n, A, B, equality_prover, Function, Literal,
                     Operation, relation_prover, TransRelUpdater)
from proveit.logic import InSet
from proveit.logic.sets import Disjoint
from proveit.numbers import Complex, Integer, Natural, Real


class BufiloSetsLiteral(Literal):
    '''
    BufiloSetsLiteral() (formatted as BUF in outputs) represents
    the set of possible BUFILOs (standing for Bad Undetectable
    Fault-Induced Logical Operator) across a surface code. A BUFILO
    is itself a set of faults, the combination of which produce the
    equivalent of a logical operator L. The sets of interest can
    eventually be parameterized to specify a specific logical operator
    L, the logical operator L_{perp} with which it anti-commutes,
    and/or the specific QEC system of interest.

    'BufiloSets' is then defined in the QEC2 common notebook as
    BufiloSets = BufiloSetsLiteral().
    '''

    # the literal string for representing the BufiloSets
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='BUF', 
                         latex_format=r'\textsc{buf}',
                         styles=styles)


class BufiloSequencesLiteral(Literal):
    '''
    BufiloSequencesLiteral() (formatted as F_{l,w} in outputs)
    represents a restricted set of fault sequences, each sequence
    having the following properties:

      * its weight is less than or equal to w_{BUF}
      * the first fault in the sequence anti-commutes with the
        logical operator l (i.e., A_{l} f_{1} = 1)
      * consider as a _set_, the sequence is equivalent to an
        l^{perp}-BUFILO (i.e., letting f = {f1, f2, ..., fn}, we
        have H f = ZeroVector while A_{l} f = 1).

    See BufiloSetsLiteral class above for further description of the
    related BUFILO sets.

    These sequences could eventually be parameterized to specify a
    specific logical operator l with which the sequences anti-commute,
    and/or the specific QEC system of interest.

    'BufiloSequences' is then defined in the QEC2 common notebook as
    BufiloSequences = BufiloSequencesLiteral().
    '''

    # the literal string for representing the BufiloSequences
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='F_{l w_BUF}', 
            latex_format=r'\mathcal{F}_{\ell w_{\textsc{buf}}}^{\text{seq}}',
            styles=styles)


class MalignantSetsLiteral(Literal):
    '''
    MalignantSetsLiteral() (formatted as MALS in outputs) represents
    the set of possible "malignant sets." A malignant set is a specific
    set of faults that causes a quantum error correction system to 
    suffer a logical failure. In Beverland's notation, a malignant
    set e is a set of faults such that H(e+c)=0 while A(e+c)≠0, where
    H is the check matrix, A is the action matrix, and c = C(sigma)
    is the correction provided by the decoding algorithm C.

    As in the case of BUFILO sets, the malignant sets of interest can
    eventually be parameterized to specify a QEC of interest.
    '''

    # The literal string for representing the malignant sets
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='MALS', 
                         latex_format=r'\textsc{mals}',
                         styles=styles)


class Weight(Function):
    '''
    Weight(e), appearing as w(e) in outputs, represents the weight
    of error e, where error e consists of a set of faults. When
    e is represented as a vector over the 2-element finite field F,
    the weight is equivalent to the Hamming weight of the vector e.
    '''

    # the literal operator for the Weight operation
    _operator_ = Literal(
            string_format='w',
            latex_format=r'w\!', theory=__file__)

    def __init__(self, e, *, styles=None):
        '''
        Create Weight(e), the weight of error or fault set 'e'.
        '''
        Function.__init__(
                self, Weight._operator_, e, styles=styles)

    @equality_prover('shallow_simplified', 'shallow_simplify')
    def shallow_simplification(self, *, must_evaluate=False,
                               **defaults_config):
        '''
        Returns a proven simplification equation for this Weight
        expression assuming its operand has been simplified.
        
        Originally implemented to handles the following Weight
        expression "simplification":

             1. w(A U B) = w(A) + w(B) for Disjoint(A, B)

        but later decided not to make that an automatic simplification,
        and created a separate distribution_over_union() method instead.

        Left the shell of the shallow_simplification() method here for
        future development.

        '''
        expr = self
        # for convenience in updating our equation,
        # beginning with self = self
        eq = TransRelUpdater(expr)

        # (1) w(A U B) = w(A) + w(B) for Disjoint(A,B)
        # from proveit.logic.sets import Union
        # if isinstance(self.operand, Union):
        #     from proveit.logic.sets import Disjoint
        #     if Disjoint(*self.operand.operands).readily_provable():
        #         from proveit.physics.quantum.QEC2 import weight_additivity
        #         _A_sub = expr.operand.operands
        #         _n_sub = _A_sub.num_elements()
        #         expr = eq.update(weight_additivity.instantiate(
        #                     {n:_n_sub, A:_A_sub}))

        return eq.relation # Might be just [self = self]

    @equality_prover('distributed_over_union', 'distribute_over_union')
    def distribution_over_union(self, **defaults_config):
        '''
        Distribute a Weight(A U B) expression across its (binary)
        Union operand, returning an equality between the original
        expression and a sum of weights, as follows:

            1. The general case:
               w(A U B) = w(A) + w(B) - w(A n B)

            2. If Disjoint(A, B):
               w(A U B) = w(A) + w(B)
        
        Currently implemented only for the binary case, but could
        be generalized.
        '''
        from proveit.logic.sets import Union
        if (not isinstance(self.operand, Union)
            or not self.operand.operands.is_double()):
            raise ValueError(
                f"Weight.distribution_over_union() implemented only for "
                f"Weight() operation on a binary Union expression, but "
                f"received the expression: {self}.")

        _A_sub = self.operand.operands[0]
        _B_sub = self.operand.operands[1]
        if Disjoint(_A_sub, _B_sub).readily_provable():
            from proveit.physics.quantum.QEC2 import (
                    binary_disjoint_weight_additivity)
            return binary_disjoint_weight_additivity.instantiate(
                    {A:_A_sub, B:_B_sub})

        # Else return the more general case
        from proveit.physics.quantum.QEC2 import binary_weight_additivity
        return binary_weight_additivity.instantiate(
                {A:_A_sub, B:_B_sub})

        # raise NotImplementedError(
        #     f"Weight.distribution_over_union() not yet implemented for "
        #     f"the case of {self}. ")



    @relation_prover
    def deduce_in_number_set(self, number_set, **defaults_config):
        '''
        Attempt to prove that the given Weight expression is in the
        given number set number_set using the basic weight-defining
        set theorem. Weight(e) is always a Natural, and thus Weight(e)
        is also an Integer, a Real, and a Complex.
        '''
        
        if number_set in {Complex, Integer, Natural, Real}:
            from proveit.physics.quantum.QEC2 import weight_in_natural
            _A_sub = self.operand
            weight_in_natural_inst = weight_in_natural.instantiate({A:_A_sub})
            if number_set == Natural:
                return weight_in_natural_inst
            return InSet(self, number_set).prove()

        raise NotImplementedError(
            f"'Weight.deduce_in_number_set()' on {self} not "
            f"implemented for the {number_set} set. Remember that "
            f"Weight(e) is always a Natural number.")

    def readily_provable_number_set(self):
        '''
        Return the most restrictive number set we can readily
        prove contains the evaluation of this Weight operation.
        Generally, the most restrictive set is the set of Natural,
        but for an operand that is provably not the EmptySet, the
        most restrictive set would be the set NaturalPos.
        '''
        from proveit.logic import NotEquals
        from proveit.logic.sets import EmptySet
        from proveit.numbers import Natural, NaturalPos
        if NotEquals(self.operand, EmptySet).readily_provable():
            return NaturalPos
        return Natural


class FaultsLiteral(Literal):
    '''
    FaultsLiteral() (formatted as FAULTS in outputs) represents the
    set of possible faults across a QEC system. An error e consists
    of a set of such faults, and as described elsewhere, a BUFILO is
    a special set of such faults.

    See BufiloSetsLiteral class above for further description of the
    related BUFILO sets.

    'Faults' is then defined in the QEC2 common notebook as
    Faults = FaultsLiteral().
    '''

    # the literal string for representing the set of Faults
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='FAULTS', 
            latex_format=r'\textsc{faults}',
            styles=styles)


class ErrorsLiteral(Literal):
    '''
    ErrorsLiteral() (formatted as ERRS in outputs) represents the set
    of all possible errors across a QEC system, with an error simply
    being a set of faults.

    'Errors' is then defined in the QEC2 common notebook as
    Errors = ErrorsLiteral().

    The Errors class is a convenience to help facilitate expressiveness.
    One might use [e in Errors], for example, but often one could
    instead simply directly consider a set {f1, f2, ..., fn} of faults.
    '''

    # the literal string for representing the set of Errors
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='ERRS', 
            latex_format=r'\textsc{errs}',
            styles=styles)


class SyndromesLiteral(Literal):
    '''
    SyndromesLiteral() (formatted as mathcal{S} in outputs) represents
    the set of all possible syndromes, equivalent to the power set of
    the set of all detectors.
    This might eventually need to be generalized to a function 
    parameterized with an operator type, etc.
    '''
    # the literal string for representing the set of Syndromes
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='Syndromes', 
            latex_format=r'\mathcal{S}',
            styles=styles)


class DetectorsLiteral(Literal):
    '''
    DetectorsLiteral() (formatted as mathcal{D} in outputs) represents
    the set of all possible detectors.
    This might eventually need to be generalized to a function 
    parameterized with an operator type, etc.
    '''

    # the literal string for representing the set of Detectors
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='Detectors', 
            latex_format=r'\mathcal{D}',
            styles=styles)


class CheckFunction(Function):
    '''
    CheckFunction(e) is a function version of the 'check matrix',
    taking an error e as input (and recall that an error e is just
    a set of faults) and producing/representing a syndrome output
    (i.e., a set of checks or detectors)
    '''

    # operator for the CheckFunction function.
    _operator_ = Literal(
            string_format='H',
            latex_format=r'H',
            theory=__file__)

    def __init__(self, e, *, styles=None):
        '''
        Create CheckFunction(e), as H(e), the syndrome associated
        with error e.
        '''
        super().__init__(
                CheckFunction._operator_, e, styles=styles)


class ActionFunction(Function):
    '''
    ActionFunction(l, e) is a function version of the 'action matrix',
    taking a logical operator l and error e as input (and recall that
    an error e is just a set of faults) and producing/representing 
    the logical action (relative to the logical operator l), which
    should be 0 (no action) or 1 (logical l applied).
    '''

    # operator for the ActionFunction function.
    _operator_ = Literal(
            string_format='A',
            latex_format=r'A',
            theory=__file__)

    def __init__(self, l, e, *, styles=None):
        '''
        Create ActionFunction(e), as A_{l}(e), the logical action
        l resulting from error e.
        '''
        super().__init__(
                ActionFunction._operator_, (l, e), styles=styles)

    def string(self, **kwargs):
        return ('A_{' + self.operands[0].string()
                + '}(' + self.operands[1].string() + ')')

    def latex(self, **kwargs):
        return (r'A_{' + self.operands[0].latex()
                + r'}(' + self.operands[1].latex() + r')')


