from proveit import (u, v, G, equality_prover, Expression, ExprTuple,
                     Function, Literal, Operation)

class Vertices(Function):
    '''
    Given a graph G(V, E) with vertex set V and edge set E,
    Vertices(G(V, E)) represents the set V of vertices ---
    that is, Vertices(G(V,E)) = V.
    '''

    # the literal operator of the Vertices operation
    _operator_ = Literal(string_format='Vertices',
                         latex_format=r'\mathrm{Vertices}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Given a graph G(V,E) = (V,E), represent the vertex set of G.
        '''
        self.graph = G
        Function.__init__(
                self, Vertices._operator_, G, styles=styles)

    def membership_object(self, element):
        from .vertices_membership import VerticesMembership
        return VerticesMembership(element, self)

    def nonmembership_object(self, element):
        from .vertices_membership import VerticesNonmembership
        return VerticesNonmembership(element, self)


class Degree(Function):
    '''
    Degree(v, G), denoted deg(v), represents the degree or valency of
    the vertex v occuring in the graph G. For an undirected graph with
    no loops, deg(v) will be equal to the number of edges incident
    with vertex v. For vertex v in a directed graph, deg(v) will equal
    the sum of the in-degree and out-degree of vertex v.
    '''

    # the literal operator of the Degree operation
    _operator_ = Literal(string_format='deg',
                         latex_format=r'\mathrm{deg}',
                         theory=__file__)

    def __init__(self, v, G, *, styles=None):
        '''
        Given a vertex v of a graph G(V,E) = (V,E), represent the
        degree of the vertex v.
        '''
        Function.__init__(
                self, Degree._operator_, (v, G), styles=styles)


class OddVertices(Function):
    '''
    OddVertices(G) represents the set of odd-degree vertices in
    graph G.
    '''

    # the literal operator of the OddVertices operation
    _operator_ = Literal(string_format='OddVertices',
                         latex_format=r'\mathrm{OddVertices}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Given a graph G (which mmight be very general, or might
        be specified as G(V, E)), represent the set of odd-degree
        vertices in the graph G.
        '''
        self.graph = G
        Function.__init__(
                self, OddVertices._operator_, G, styles=styles)

    def membership_object(self, element):
        from .vertices_membership import OddVerticesMembership
        return OddVerticesMembership(element, self)

    # def nonmembership_object(self, element):
    #     from .vertices_membership import OddVerticesNonmembership
    #     return OddVerticesNonmembership(element, self)


class AdjacentVertices(Function):
    '''
    For vertices u, v in graph G, AdjacentVertices(u, v, G) denotes
    the claim that vertices u and v are adjacent in graph G (i.e., 
    AdjacentVertices(u, v, G) means that {u, v} is an edge in graph G).
    We use the full 'AdjacentVertices()' for naming and calling the
    class to distinguish the situation from adjacent edges.
    '''
    # the literal operator of the Adjacent operation
    _operator_ = Literal(string_format='Adjacent',
                         latex_format=r'\mathrm{Adjacent}',
                         theory=__file__)

    def __init__(self, u, v, G, *, styles=None):
        '''
        Given vertices u, v in graph G, represent the claim that
        vertices u and v are adjacent in G.
        '''
        self.graph = G
        self.vertices = (u, v)
        Function.__init__(
                self, AdjacentVertices._operator_, (u, v, G), styles=styles)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = AdjacentVertices(u, v, G), deduce and return the
        equality: AdjacentVertices(u, v, G) = {u, v} in Edges(G).
        '''
        from . import adjacent_vertices_def
        _u_sub = self.operands[0]
        _v_sub = self.operands[1]
        _G_sub = self.operands[2]
        return adjacent_vertices_def.instantiate(
            {u:_u_sub, v:_v_sub, G:_G_sub}, auto_simplify=False)


# See further below for most recent dev attempt using an Operation
# approach
# class VertexSequence(ExprTuple):
#     '''
#     VertexSequence(v_0, v_1, ..., v_n) represents an ordered sequence
#     of vertices v_0, v_1, ..., v_n.
#     '''

#     def __init__(self, *vertices, styles=None):
#         super().__init__(*vertices, styles=styles)
#         # and update the Expression identity to include both tags
#         # from proveit._core_.expression.expr import Expression
#         Expression.__init__(self, ['VertexSequence', 'ExprTuple'],
#                             self.entries, styles=styles)
#         # Expression.__init__(self, ['VertexSequence'],
#         #                     self.entries, styles=styles)

#     def formatted(self, format_type, **kwargs):
#         # (1) Get the std tuple formatting from parent
#         content = super().formatted(format_type, **kwargs)
#         # (2) Add our desired prefix
#         if format_type == 'latex':
#             return r'\text{VertexSeq}' + content
#         return 'VertexSeq' + content

#     def string(self, **kwargs):
#         return 'VertexSeq' + super().formatted('string', **kwargs)

#     def latex(self, **kwargs):
#         return r'\text{VertexSeq}' + super().formatted('latex', **kwargs)
#         # content = super().formatted('latex', fence=True, **kwargs)
#         # return r"\text{VertexSeq}" + content

#     def order(self, **kwargs):
#         from proveit import n, v
#         from proveit.core_expr_types import Len
#         from proveit.numbers import one, num, subtract
#         from proveit.graphs import vertex_seq_def
#         _n_sub = subtract(ExprTuple(*self.entries).num_elements(**kwargs), one)
#         _v_sub = self.entries
#         unfolding = (vertex_seq_def.instantiate({n:_n_sub, v:_v_sub}, **kwargs).
#                      derive_reversed(**kwargs))
#         len_proof = Len(unfolding.lhs).computation(**kwargs)
#         return len_proof.inner_expr().lhs.operands.substitute(
#                 unfolding, **kwargs)

#     # a new temp version W20260325, trying to get the substitution to
#     # work correctly, but now trying to construct our own Judgment
#     def order2(self, **kwargs):
#         from proveit import n, v, Judgment
#         from proveit.core_expr_types import Len
#         from proveit.logic import Equals
#         from proveit.numbers import one, num, subtract
#         from proveit.graphs import vertex_seq_def
#         _n_sub = subtract(ExprTuple(*self.entries).num_elements(**kwargs), one)
#         _v_sub = self.entries
#         unfolding = (vertex_seq_def.instantiate({n:_n_sub, v:_v_sub}, **kwargs).
#                      derive_reversed(**kwargs))
#         len_proof = Len(unfolding.lhs).computation(**kwargs)
#         # then we try something different
#         old_lhs = len_proof.expr.lhs # i.e. the |proxy|
#         # use same operator 'Len' but self (VerteSequence) as operand
#         new_lhs = Len(self)
#         # create the desired equality
#         new_expr = Equals(new_lhs, len_proof.expr.rhs)
#         # wrap in Judgment?
#         # return new_expr.prove(assumptions=len_proof.assumptions)
#         return Judgment(new_expr,
#                         assumptions=len_proof.assumptions,
#                         num_lit_gen=len_proof.num_lit_gen)


#     def length(self):
#         '''
#         Returns the number of (implied) edges as a Python int.
#         Length is 0 for a single vertex (a trivial walk).
#         NO claim is being made here that the implied/inferred edges
#         are actual valid edges in some graph.
#         '''
#         return max(0, len(self) - 1)

#     def is_trivial(self):
#         '''
#         A order-1 sequence represents a "trivial" walk.
#         '''
#         return self.order() == 1

#     def edges(self):
#         '''
#         Returns a list of tuples of vertices representing the
#         implied/inferred edges. NO claim is being made here that
#         the implied/inferred edges actually exist in some graph.
#         Possibly should be a list of 2-element lists or Sets instead
#         of tuples.
#         '''
#         from proveit.logic import Set
#         return [Set(self[i], self[i+1]) for i in range(self.length())]


# alt approach 20260325 using an extension of Operation
# the ExprTuple-based approach above will likely be deleted
class VertexSequence(Operation):
    '''
    VertexSequence(v_0, v_1, ..., v_n) represents an ordered sequence
    of vertices v_0, v_1, ..., v_n. The VertexSequence() operation is
    designed to take a variable number of arguments, which are then
    encapsulated into an ExprTuple. This allows the use of 1 or more
    individual vertices to be provided but also allows an ExprRange
    to be used. For example, we can produce the vertex sequence:

        VertexSeq(a, b, v_1,..,v_n, c)

    using VertexSequence(a, b, expr_range, c), where:

        expr_range = ExprRange(k, IndexedVar(v, k), one, n)

    The vertex sequence is independent of any particular graph, and
    the construction of such a vertex sequence makes no claim about
    the vertices actually existing in or belonging to any particular
    graph.

    '''

    # The Literal operator for the VertexSequence() Operation.
    # This helps distinguish the output from a bare ExprTuple.
    _operator_ = Literal(string_format='VertexSeq',
                         latex_format=r'\textrm{VertexSeq}',
                         theory=__file__)

    def __init__(self, *vertices, styles=None):
        '''
        Initialize a VertexSequence(vertices) object, an ordered
        sequence of vertices, taking a variable number of arguments
        representing the desired vertices.
        '''
        self.entries = ExprTuple(*vertices)
        super().__init__(self._operator_, self.entries, styles=styles)

    def formatted(self, format_type, **kwargs):
        # (1) Get the std tuple formatting from parent
        content = self.entries.formatted(format_type, fenced=True, **kwargs)
        # (2) Add our desired prefix
        if format_type == 'latex':
            return r'\text{VertexSeq}' + content
        return 'VertexSeq' + content

    # def string(self, **kwargs):
    #     return 'VertexSeq' + self.entries.string(**kwargs)

    def string(self, **kwargs):
        return self.formatted('string', **kwargs)

    # def latex(self, **kwargs):
    #     return r'\text{VertexSeq}' + self.entries.latex(fenced=True, **kwargs)

    def latex(self, **kwargs):
        return self.formatted('latex', **kwargs)

    def order(self, **defaults_config):
        '''
        Derive and return the equality |VertexSeq(v1,...,vn)| = n,
        giving the number of vertices in the vertex sequence
        VertexSeq(). Having some trouble substituting a VertexSeq for
        an ExprTuple _inside_ the Len operator, so we first derive
        the equality Len(VertexSeq) = Len(ExprTuple) and use that for
        the substitution.
        '''
        from proveit import n, v, x, Lambda
        from proveit.core_expr_types import Len
        from proveit.numbers import one, num, subtract
        from proveit.graphs import vertex_seq_def
        # (1) Instantiate axiomatic equality between VertexSeq
        #     and ExprTuple
        _n_sub = ExprTuple(*self.entries).num_elements(**defaults_config)
        _v_sub = self.entries
        unfolding = (vertex_seq_def.instantiate({n:_n_sub, v:_v_sub}, **defaults_config).
                     derive_reversed(**defaults_config))
        # (2) Apply Len() to both sides of axiomatic equality
        len_equality = unfolding.substitution(Lambda(x, Len(x)))
        # (3) Use internal ExprTuple to derive order (i.e. the number
        #     of vertices)
        len_proof = Len(unfolding.lhs).computation(**defaults_config)
        # (4) substitute internally and return
        return len_proof.inner_expr().lhs.substitute(len_equality)

    def step_count(self, **defaults_config):
        '''
        Derive and return a Judgment giving the step count for this
        VertexSequence. The step count for an ordered sequence of
        vertices is equivalent to the walk-length of the sequence
        of vertices IF the sequence is interpreted as a walk in some
        graph. A vertex sequence such as v0, v1, ..., vn would have
        a step count of n.
        '''
        from proveit import n, v
        from proveit.core_expr_types import Len
        from proveit.graphs import step_count_def
        # (1) Derive relation between StepCount and underlying ExprTuple
        _n_sub = self.entries.num_elements(**defaults_config)
        _v_sub = self.entries
        step_count_def_inst = step_count_def.instantiate(
                {n:_n_sub, v:_v_sub}, **defaults_config)
        # (2) Derive length of underlying ExprTuple
        expr_tuple_len_judgment = (
                Len(self.entries).computation(**defaults_config))
        # (3) Substitute and return
        return (step_count_def_inst.inner_expr().
                rhs.operands[0].substitute(expr_tuple_len_judgment))

    def length(self):
        '''
        Returns the number of (implied) edges as a Python int.
        Length is 0 for a single vertex (a trivial walk).
        NO claim is being made here that the implied/inferred edges
        are actual valid edges in some graph.
        '''
        return max(0, len(self) - 1)

    def is_trivial(self):
        '''
        A order-1 sequence represents a "trivial" walk.
        '''
        return self.order() == 1

    def edges(self):
        '''
        Returns a list of tuples of vertices representing the
        implied/inferred edges. NO claim is being made here that
        the implied/inferred edges actually exist in some graph.
        Possibly should be a list of 2-element lists or Sets instead
        of tuples.
        '''
        from proveit.logic import Set
        return [Set(self[i], self[i+1]) for i in range(self.length())]


class StepCount(Operation):
    '''
    StepCount(vertex_seq) represents the number of steps or transitions
    in a VertexSequence vertex_seq when "stepping" from the first
    vertex in the sequence to the last vertex in the sequence. For
    a VertexSequence consisting of n vertices, there should generally
    be (n-1) steps. When vertex_seq corresponds to a walk in a graph,
    StepCount(vertex_seq) corresponds to the length of the walk.
    '''

    # The Literal operator for the StepCount() Operation
    _operator_ = Literal(string_format='StepCount',
                         latex_format=r'\textrm{StepCount}',
                         theory=__file__)

    def __init__(self, vertex_seq, *, styles=None):
        '''
        Initialize a StepCount(vertex_seq) object, a representation
        of the number of steps in the vertex_seq.
        '''
        self.seq = vertex_seq
        super().__init__(self._operator_, vertex_seq, styles=styles)

    def string(self, **kwargs):
        return 'StepCount(' + self.seq.string(**kwargs) + ')'

    def latex(self, **kwargs):
        return r'\text{StepCount}(' + self.seq.latex(**kwargs) + r')'


class AllDistinct(Operation):
    '''
    AllDistinct(S) represents the claim that all vertices in the 
    VertexSequence S are distinct (i.e., no vertex appears more than
    once). This is the core requirement for a Walk to be considered a
    Path.
    '''
    _operator_ = Literal(string_format='AllDistinct',
                         latex_format=r'\textrm{AllDistinct}',
                         theory=__file__)

    def __init__(self, vertex_seq, *, styles=None):
        self.seq = vertex_seq
        super().__init__(self._operator_, vertex_seq, styles=styles)

    def string(self, **kwargs):
        return 'AllDistinct(' + self.seq.string(**kwargs) + ')'

    def latex(self, **kwargs):
        return r'\text{AllDistinct}(' + self.seq.latex(**kwargs) + r')'

