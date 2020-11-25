"""Functionals used to define the dual sets."""
from .symbolic import subs, x, t
from .vectors import vdot


class BaseFunctional:
    """A functional."""

    def eval(self, fun):
        """Apply to the functional to a function."""
        raise NotImplementedError

    def dof_point(self):
        """Get the location of the DOF in the cell."""
        return tuple(None for i in range(self.reference.gdim))

    def dof_direction(self):
        """Get the direction of the DOF."""
        return None

    def entity_dim(self):
        """Get the dimension of the entitiy this DOF is associated with."""
        return None

    name = None


class PointEvaluation(BaseFunctional):
    """A point evaluation."""

    def __init__(self, point, entity_dim=None):
        self.point = point
        self._entity_dim = entity_dim

    def eval(self, function):
        """Apply to the functional to a function."""
        return subs(function, x, self.point)

    def dof_point(self):
        """Get the location of the DOF in the cell."""
        return self.point

    def entity_dim(self):
        """Get the dimension of the entitiy this DOF is associated with."""
        return self._entity_dim

    name = "Point evaluation"


class DotPointEvaluation(BaseFunctional):
    """A point evaluation in a given direction."""

    def __init__(self, point, vector, entity_dim=None):
        self.point = point
        self.vector = vector
        self._entity_dim = entity_dim

    def eval(self, function):
        """Apply to the functional to a function."""
        return subs(vdot(function, self.vector), x, self.point)

    def dof_point(self):
        """Get the location of the DOF in the cell."""
        return self.point

    def dof_direction(self):
        """Get the direction of the DOF."""
        return self.vector

    def entity_dim(self):
        """Get the dimension of the entitiy this DOF is associated with."""
        return self._entity_dim

    name = "Dot point evaluation"


class IntegralMoment(BaseFunctional):
    """An integral moment."""

    def __init__(self, reference, f, dof):
        self.reference = reference
        self.dof = dof
        self.f = subs(f, x, t)
        if isinstance(self.f, tuple):
            self.f = tuple(
                sum(self.reference.scaled_axes()[j][i] * c for j, c in enumerate(self.f))
                for i, o in enumerate(self.reference.origin)
            )

    def eval(self, function):
        """Apply to the functional to a function."""
        point = [i for i in self.reference.origin]
        for i, a in enumerate(zip(*self.reference.axes)):
            for j, k in zip(a, t):
                point[i] += j * k
        integrand = self.dot(subs(function, x, point))
        return self.reference.integral(integrand)

    def dot(self, function):
        """Dot a function with the moment function."""
        return vdot(function, self.f)

    def dof_point(self):
        """Get the location of the DOF in the cell."""
        p = self.dof.dof_point()
        return tuple(
            o + sum(self.reference.axes[j][i] * c for j, c in enumerate(p))
            for i, o in enumerate(self.reference.origin)
        )

    def dof_direction(self):
        """Get the direction of the DOF."""
        p = self.dof.dof_direction()
        if p is None:
            return None
        return tuple(
            sum(self.reference.axes[j][i] * c for j, c in enumerate(p))
            for i in range(self.reference.gdim)
        )

    def entity_dim(self):
        """Get the dimension of the entitiy this DOF is associated with."""
        return self.reference.tdim

    name = "Integral moment"


class VecIntegralMoment(IntegralMoment):
    """An integral moment applied to a component of a vector."""

    def __init__(self, reference, f, dot_with, dof):
        super().__init__(reference, f, dof)
        self.dot_with = dot_with

    def dot(self, function):
        """Dot a function with the moment function."""
        return vdot(function, self.dot_with) * self.f

    def dof_direction(self):
        """Get the direction of the DOF."""
        return self.dot_with

    name = "Vector integral moment"


class TangentIntegralMoment(VecIntegralMoment):
    """An integral moment in the tangential direction."""

    def __init__(self, reference, f, dof):
        super().__init__(reference, f, reference.tangent(), dof)

    name = "Tangential integral moment"


class NormalIntegralMoment(VecIntegralMoment):
    """An integral moment in the normal direction."""

    def __init__(self, reference, f, dof):
        super().__init__(reference, f, reference.normal(), dof)

    name = "Normal integral moment"
