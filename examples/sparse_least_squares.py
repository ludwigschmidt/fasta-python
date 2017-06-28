"""Solve the L1-penalized least-squares problem,

min mu|x| + .5||Ax-b||^2

using the FASTA solver."""

__author__ = "Noah Singer"

import numpy as np
from numpy import linalg as la
from fasta import fasta, harness, utils


def sparse_least_squares(A, b, mu, x0, **kwargs):
    f = lambda z: .5 * la.norm(z - b) ** 2
    gradf = lambda z: z - b
    g = lambda z: mu * la.norm(z, 1)
    proxg = lambda z, t: utils.shrink(z, t*mu)

    return fasta(A, A.T, f, gradf, g, proxg, x0, **kwargs)

if __name__ == "__main__":
    # Number of measurements
    M = 200

    # Dimension of spare signal
    N = 1000

    # Signal sparsity
    K = 10

    # Regularization parameter
    mu = 0.02

    # Noise level in b
    sigma = 0.01

    # Create sparse signal
    x = np.zeros((N,1))
    x[np.random.permutation(N)[:K]] = 1

    # Create matrix
    A = np.random.randn(M, N)
    A /= la.norm(A, 1)

    # Create noisy observation vector
    b = A @ x
    b += sigma * np.random.standard_normal(b.shape)

    # Initial iterate
    x0 = np.zeros((N, 1))

    print("Constructed sparse least-squares problem.")

    harness.test_modes(lambda **k: sparse_least_squares(A, b, mu, x0, **k), solution=x)