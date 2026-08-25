from proveit import G, P, prover
from proveit.logic import SetMembership, SetNonmembership


class PathsOfMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set PathsOf(G)
    of all paths in graph G.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @prover
    def derive_element_as_subgraph(self, **defaults_config):
        '''
        From self = (P in PathsOf(G)), derive and return Subgraph(P, G).
        '''
        from . import path_is_subgraph
        _G_sub = self.domain.operand
        _P_sub = self.element
        return path_is_subgraph.instantiate(
                {G:_G_sub, P:_P_sub})


class PathsOfNonmembership(SetNonmembership):
    '''
    Defines methods that apply to non-membership in the set PathsOf(G)
    of all paths in graph G.
    '''

    def __init__(self, element, domain):
        SetNonmembership.__init__(self, element, domain)