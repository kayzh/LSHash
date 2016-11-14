#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy as np

from lshash import LSHash

__author__ = "Hobson Lane"
__copyright__ = "Kay Zhu (a.k.a He Zhu)"
__license__ = "MIT"


def test_sphere():
    X = np.random.normal(size=(1000, 3))
    lsh = LSHash(10, 3, num_hashtables=5)
    for x in X:
        x /= np.linalg.norm(x)
        lsh.index(x)
    closest = lsh.query(X[0] + np.array([-0.001, 0.001, -0.001]), distance_func="cosine")
    assert len(closest) >= 10
    assert 0.05 >= closest[9][-1] > 0.0003


def test_hyperspheres():
    tenthclosest = []
    for D in range(2, 11):
        X = np.random.normal(size=(200000, D))
        lsh = LSHash(int(64 / D) + D, D, num_hashtables=D)

        # query vector
        q = np.random.normal(size=(D,))
        q /= np.linalg.norm(q)

        distances = []
        for x in X:
            lsh.index(x)
            x /= np.linalg.norm(x)
            distances += [1 - np.sum(x * q)]
        distances = sorted(distances)
        closest = lsh.query(q, distance_func='cosine')
        N = len(closest)
        rank = min(10, N)
        tenthclosest += [[D, N - 1, closest[rank - 1][-1] if N else None, distances[rank - 1]]]
        print(tenthclosest[-1])
    for i, tc in enumerate(tenthclosest):
        assert 1e-9 < tc[-2] or 1e-6 < 0.2
    return tenthclosest
