"""Functions to handle derivatives."""

from .vectors import vdot
from .symbolic import x, sym_sum


def derivative(f, dir):
    """Find the directional derivative of a function."""
    return vdot(grad(f, len(dir)), dir)


def grad(f, dim):
    """Find the gradient of a scalar function."""
    return tuple(f.diff(x[i]) for i in range(dim))


def jacobian_component(f, component):
    """Find a component of the Jacobian."""
    return f.diff(x[component[0]]).diff(x[component[1]])


def jacobian(f, dim):
    """Find the Jacobian."""
    return [[f.diff(x[i]).diff(x[j]) for i in range(dim)] for j in range(dim)]


def div(f):
    """Find the divergence of a vector function."""
    return sym_sum(j.diff(x[i]) for i, j in enumerate(f))
