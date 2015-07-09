import lshash
import numpy as np

def test_fixed_seed():
    """ fixed seeds should generate the same uniform_planes """
    fixed_seed_lsh = [lshash.LSHash(10, 100, seed=20) for i in range(10)]
    uniform_plane_sum = [np.sum(ls.uniform_planes) for ls in fixed_seed_lsh]
    assert len(set(uniform_plane_sum)) == 1

def test_nonfixed_seed():
    """ when seed is not specified uniform planes should be different """
    nonfixed_seed_lsh = [lshash.LSHash(10, 100) for i in range(10)]
    uniform_plane_sum = [np.sum(ls.uniform_planes) for ls in nonfixed_seed_lsh]
    assert len(set(uniform_plane_sum)) > 1

