import random
import string
from unittest import TestCase
from redis import StrictRedis
from pprint import pprint
import sys
import os

# add the LSHash package to the current python path
sys.path.insert(0, os.path.abspath('../'))
# now we can use our lshash package and not the standard one
from lshash import LSHash


class TestLSHash(TestCase):
    num_elements = 100

    def setUp(self):
        self.els = []
        self.el_names = []
        for i in range(self.num_elements):
            el = [random.randint(0, 100) for _ in range(8)]
            elname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            self.els.append(tuple(el))
            self.el_names.append(elname)

    def test_lshash(self):
        lsh = LSHash(6, 8, 1)
        for i in range(self.num_elements):
            lsh.index(list(self.els[i]))
            lsh.index(list(self.els[i]))  # multiple insertions
        hasht = lsh.hash_tables[0]
        itms = [hasht.get_list(k) for k in hasht.keys()]
        for itm in itms:
            assert itms.count(itm) == 1
            for el in itm:
                assert el in self.els
        for el in self.els:
            res = lsh.query(list(el), num_results=1, distance_func='euclidean')[0]
            # res is a tuple containing the vector and the distance
            el_v, el_dist = res
            assert el_v in self.els
            assert el_dist == 0
        del lsh

    def test_lshash_extra_val(self):
        lsh = LSHash(6, 8, 1)
        for i in range(self.num_elements):
            lsh.index(list(self.els[i]), self.el_names[i])
        hasht = lsh.hash_tables[0]
        itms = [hasht.get_list(k) for k in hasht.keys()]
        for itm in itms:
            for el in itm:
                assert el[0] in self.els
                assert el[1] in self.el_names
        for el in self.els:
            # res is a list, so we need to select the first entry only
            res = lsh.query(list(el), num_results=1, distance_func='euclidean')[0]
            # vector an name are in the first element of the tuple res[0]
            el_v, el_name = res[0]
            # the distance is in the second element of the tuple
            el_dist = res[1]
            assert el_v in self.els
            assert el_name in self.el_names
            assert el_dist == 0
        del lsh

    def test_lshash_redis(self):
        """
        Test external lshash module
        """
        config = {"redis": {"host": 'localhost', "port": 6379, "db": 15}}
        sr = StrictRedis(**config['redis'])
        sr.flushdb()

        lsh = LSHash(6, 8, 1, config)
        for i in range(self.num_elements):
            lsh.index(list(self.els[i]))
            lsh.index(list(self.els[i]))  # multiple insertions should be prevented by the library

        hasht = lsh.hash_tables[0]
        itms = [hasht.get_list(k) for k in hasht.keys()]

        for itm in itms:
            for el in itm:
                assert itms.count(itm) == 1  # have multiple insertions been prevented?
                assert el in self.els

        for el in self.els:
            res = lsh.query(list(el), num_results=1, distance_func='euclidean')[0]
            el_v, el_dist = res
            assert el_v in self.els
            assert el_dist == 0
        del lsh
        sr.flushdb()

    def test_lshash_redis_extra_val(self):
        """
        Test external lshash module
        """
        config = {"redis": {"host": 'localhost', "port": 6379, "db": 15}}
        sr = StrictRedis(**config['redis'])
        sr.flushdb()

        lsh = LSHash(6, 8, 1, config)
        for i in range(self.num_elements):
            lsh.index(list(self.els[i]), self.el_names[i])
            lsh.index(list(self.els[i]), self.el_names[i])  # multiple insertions
        hasht = lsh.hash_tables[0]
        itms = [hasht.get_list(k) for k in hasht.keys()]
        for itm in itms:
            assert itms.count(itm) == 1
            for el in itm:
                assert el[0] in self.els
                assert el[1] in self.el_names
        for el in self.els:
            res = lsh.query(list(el), num_results=1, distance_func='euclidean')[0]
            # vector an name are in the first element of the tuple res[0]
            el_v, el_name = res[0]
            # the distance is in the second element of the tuple
            el_dist = res[1]
            assert el_v in self.els
            assert el_name in self.el_names
            assert el_dist == 0
        del lsh
        sr.flushdb()

