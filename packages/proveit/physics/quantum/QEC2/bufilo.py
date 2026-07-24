from proveit import Literal, Operation


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
                         latex_format=r'\textrm{BUF}',
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
                         latex_format=r'\textrm{MALS}',
                         styles=styles)


class Weight(Operation):
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
        Operation.__init__(
                self, Weight._operator_, e, styles=styles)




