import lshash
import numpy as np

def test_code():
    """ test codes are of the correct length and work with multiple hash tables """
    l = lshash.LSHash(10, 20)

    assert len(l.code(np.random.randn(20))) == 1
    assert len(l.code(np.random.randn(20))[0]) == 10

    l = lshash.LSHash(10, 20, num_hashtables=3)

    assert len(l.code(np.random.randn(20))) == 3

    for hash in l.code(np.random.randn(20)):
        assert len(hash) == 10
