from proveit import Function, Literal

class CycleSpace(Function):
    '''
    Given a graph G = G(V, E) with vertex set V and edge set E,
    CycleSpace(G) represents the cycle space of graph G, which
    consists of the set of all even-degree spanning subgraphs of G.
    The set of all even-degree spanning subgraphs of G is a vector
    space over the 2-element finite field {0, 1}, where vector addition
    is defined by the symmetric difference between the edge sets of
    the subgraphs.
    The cycle space of G can also be conceptualized as a subgroup of
    the edge space of G, but this is complicated by the need to
    identify a collection of edges of G with the associated "induced"
    spanning subgraph of G (see, e.g., Diestel's 2025 Graph Theory,
    pg 24).
    '''

    # the literal operator of the CycleSpaces operation
    _operator_ = Literal(string_format='C',
                         latex_format=r'\mathcal{C}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Represent C(G), the cycle space of the graph G.
        '''
        self.graph = G
        Function.__init__(
                self, CycleSpace._operator_, G, styles=styles)

    def membership_object(self, element):
        from .cyclespace_membership import CycleSpaceMembership
        return CycleSpaceMembership(element, self)

    def nonmembership_object(self, element):
        from .cyclespace_membership import CycleSpaceNonmembership
        return CycleSpaceNonmembership(element, self)




