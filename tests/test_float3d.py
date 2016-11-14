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
        lsh = LSHash(32, D, num_hashtables=D)
        for x in X:
            lsh.index(x)
            x /= np.linalg.norm(x)
        # closest = lsh.query(X[0] + np.array([0.001] * D), distance_func="cosine")
        x = np.random.normal(size=(D,))
        x /= np.linalg.norm(x)
        closest = lsh.query(x, distance_func='cosine')
        N = len(closest)
        tenthclosest += [[D, N, closest[min(9, N - 1)][-1] if N else None]]
        print(tenthclosest[-1])
    for i, tc in enumerate(tenthclosest):
        assert 1e-9 < tc[-1] or 1e-6 < 0.2
    return tenthclosest
