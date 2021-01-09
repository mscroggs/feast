"""Crouzeix-Raviart elements on simplices."""

from ..core.finite_element import FiniteElement
from ..core.polynomials import polynomial_set
from ..core.functionals import PointEvaluation, PointNormalDerivativeEvaluation
from ..core.symbolic import sym_sum


class Morley(FiniteElement):
    """Morley finite element."""

    def __init__(self, reference, order):
        from symfem import create_reference
        assert order == 2
        assert reference.name == "triangle"
        dofs = []
        for vs in reference.sub_entities(0):
            dofs.append(PointEvaluation(vs, entity_dim=0))
        for vs in reference.sub_entities(1):
            sub_ref = create_reference(
                reference.sub_entity_types[1],
                vertices=[reference.reference_vertices[v] for v in vs])
            midpoint = tuple(sym_sum(i) / len(i)
                             for i in zip(*[reference.vertices[i] for i in vs]))
            dofs.append(
                PointNormalDerivativeEvaluation(midpoint, sub_ref))

        super().__init__(
            reference, polynomial_set(reference.tdim, 1, order), dofs, reference.tdim, 1
        )

    names = ["Morley"]
    references = ["triangle"]
    min_order = 2
    max_order = 2