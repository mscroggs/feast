"""Argyris elements on simplices."""

from ..core.finite_element import FiniteElement
from ..core.polynomials import polynomial_set
from ..core.functionals import (PointEvaluation, PointDirectionalDerivativeEvaluation,
                                PointNormalDerivativeEvaluation,
                                PointComponentSecondDerivativeEvaluation)
from ..core.symbolic import sym_sum


class Argyris(FiniteElement):
    """Argyris finite element."""

    def __init__(self, reference, order):
        from symfem import create_reference
        assert order == 5
        assert reference.name == "triangle"
        dofs = []
        for vs in reference.sub_entities(0):
            dofs.append(PointEvaluation(vs, entity_dim=0))
            for i in range(reference.tdim):
                dir = tuple(1 if i == j else 0 for j in range(reference.tdim))
                dofs.append(PointDirectionalDerivativeEvaluation(vs, dir, entity_dim=0))
            for i in range(reference.tdim):
                for j in range(i + 1):
                    dofs.append(PointComponentSecondDerivativeEvaluation(
                        vs, (i, j), entity_dim=0))
        for vs in reference.sub_entities(1):
            sub_ref = create_reference(
                reference.sub_entity_types[1],
                vertices=[reference.reference_vertices[v] for v in vs])
            midpoint = tuple(sym_sum(i) / len(i)
                             for i in zip(*[reference.vertices[i] for i in vs]))
            dofs.append(PointNormalDerivativeEvaluation(midpoint, sub_ref))

        super().__init__(
            reference, polynomial_set(reference.tdim, 1, order), dofs, reference.tdim, 1
        )

    names = ["Argyris"]
    references = ["triangle"]
    min_order = 5
    max_order = 5