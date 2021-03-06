"""
Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2016
"""

import numpy as np
import numpy.testing as npt

from segmentalist.kmeans_components import KMeansComponents


def test_mean_numerators():

    np.random.seed(1)

    # Generate data
    D = 3           # dimensions
    N = 10          # number of points to generate
    K_true = 4      # the true number of components
    mu_scale = 4.0
    covar_scale = 0.7
    z_true = np.random.randint(0, K_true, N)
    mu = np.random.randn(D, K_true)*mu_scale
    X = mu[:, z_true] + np.random.randn(D, N)*covar_scale
    X = X.T

    # Model
    K = 3
    assignments = np.random.randint(0, K, N)
    components = KMeansComponents(X, assignments, K)

    # Test mean_numerators
    n = 0
    for k in xrange(components.K):
        component_mean = components.mean_numerators[k]/components.counts[k]
        X_k = X[np.where(components.assignments == k)]
        n += X_k.shape[0]

        npt.assert_almost_equal(np.mean(X_k, axis=0), component_mean)
    assert n == N


def test_neg_sqrd_norm():

    np.random.seed(1)

    # Generate data
    D = 4           # dimensions
    N = 11          # number of points to generate
    K_true = 4      # the true number of components
    mu_scale = 4.0
    covar_scale = 0.7
    z_true = np.random.randint(0, K_true, N)
    mu = np.random.randn(D, K_true)*mu_scale
    X = mu[:, z_true] + np.random.randn(D, N)*covar_scale
    X = X.T

    # Model
    K = 5
    assignments = np.random.randint(0, K, N)

    # Make sure we have consequetive values
    for k in xrange(assignments.max()):
        while len(np.nonzero(assignments == k)[0]) == 0:
            assignments[np.where(assignments > k)] -= 1
        if assignments.max() == k:
            break

    components = KMeansComponents(X, assignments, K)

    # Test neg_sqrd_norm
    for i in xrange(N):
        x_i = X[i, :]
        expected_sqrd_norms = []
        for k in xrange(components.K):
            component_mean = components.mean_numerators[k]/components.counts[k]
            expected_sqrd_norms.append(np.linalg.norm(x_i - component_mean)**2)
        npt.assert_almost_equal(components.neg_sqrd_norm(i)[:components.K], -np.array(expected_sqrd_norms))


def test_expected_sum_neg_sqrd_norm():

    # Generate data
    D = 5           # dimensions
    N = 20          # number of points to generate
    K_true = 5      # the true number of components
    mu_scale = 5.0
    covar_scale = 0.6
    z_true = np.random.randint(0, K_true, N)
    mu = np.random.randn(D, K_true)*mu_scale
    X = mu[:, z_true] + np.random.randn(D, N)*covar_scale
    X = X.T

    # Model
    K = 6
    assignments = np.random.randint(0, K, N)

    # Make sure we have consequetive values
    for k in xrange(assignments.max()):
        while len(np.nonzero(assignments == k)[0]) == 0:
            assignments[np.where(assignments > k)] -= 1
        if assignments.max() == k:
            break

    components = KMeansComponents(X, assignments, K)

    # Test sum_neg_sqrd_norm
    expected_sum_neg_sqrd_norm = 0.
    for i in xrange(N):
        x_i = X[i, :]
        expected_sqrd_norms = []
        for k in xrange(components.K):
            component_mean = components.mean_numerators[k]/components.counts[k]
            expected_sqrd_norms.append(np.linalg.norm(x_i - component_mean)**2)
        expected_sum_neg_sqrd_norm += -np.array(expected_sqrd_norms)[components.assignments[i]]
    npt.assert_almost_equal(components.sum_neg_sqrd_norm(), expected_sum_neg_sqrd_norm)
