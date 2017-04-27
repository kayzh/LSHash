#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import
from builtins import int, round, str,  object  # noqa
from future import standard_library
standard_library.install_aliases()  # noqa: Counter, OrderedDict, 
from past.builtins import basestring   # noqa:

import numpy as np

import future        # noqa
import builtins      # noqa
import past          # noqa
import six           # noqa
from lshash.lshash import LSHash

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


def test_hyperspheres(X=np.random.uniform(size=(200000, 10))):
    """ Demonstrate curse of dimensionality and where LSH starts to fail 

    Returns:
      lsh, X, secondclosest, tenthclosest

    """
    tenthclosest = []
    secondclosest = []
    for D in range(2, X.shape[1]):
        lsh = LSHash(int(512. / D) + 1, D, num_hashtables=D)

        # query vector
        q = np.random.uniform(size=(D,))
        q /= np.linalg.norm(q)

        distances = []
        for x in X[:, :D]:
            lsh.index(x)
            x /= np.linalg.norm(x)
            distances += [1. - np.sum(x * q)]  # cosine similarity
        distances = sorted(distances)
        closest = lsh.query(q, num_results=10, distance_func='cosine')

        N = len(closest)
        rank = min(10, N)
        tenthclosest += [[D, N - 1, closest[rank - 1][-1] if N else None, distances[rank - 1]]]
        print(tenthclosest[-1])
        secondclosest += [[D, N - 1, closest[min(2, N) - 1][-1] if N else None, distances[rank - 1]]]
        print(secondclosest[-1])
    for i, tc in enumerate(tenthclosest):
        assert 1e-9 < tc[-2] or 1e-6 < 0.2
    return lsh, X, secondclosest, tenthclosest
