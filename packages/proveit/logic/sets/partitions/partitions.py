from proveit import Function, Literal


class Partitions(Function):
    '''
    For a set S, Partitions(S) represents the class of all possible
    partitions of S. An element P of Partitions(S) is a collection
    of non-empty subsets S1, S2, ... of S such that the elements
    of P are all pairwise disjoint and the union S1 U S2 U ...
    is equal to S. Partitions(S) is a subset of Pow(Pow(S)), 
    where 'Pow' stands for "power set."
    When S is finite, Partitions(S) is itself finite and thus a set.
    When S is infinite, Partitions(S) is still a set, as specified
    by the Axiom of Power Set in Zermelo-Fraenkel set theory.
    '''

    # the literal string for the Partitions operation
    _operator_ = Literal(
        string_format='Partitions',
        latex_format=r'\textrm{Partitions}',
        theory=__file__)

    def __init__(self, S, *, styles=None):
        '''
        Represent Partions(S), the set of partitions of set S.
        '''
        self.set = S
        Function.__init__(
                self, Partitions._operator_, S, styles=styles)

    @property
    def is_proper_class(self):
        '''
        For a finite set S, Partitions(S) is a finite set. For an
        infinite set S, Partitions(S) is infinite. In both cases,
        Partitions(S) is a set and not a proper class.
        '''
        return False

    def membership_object(self, element):
        from .partitions_membership import PartitionsMembership
        return PartitionsMembership(element, self)
    
