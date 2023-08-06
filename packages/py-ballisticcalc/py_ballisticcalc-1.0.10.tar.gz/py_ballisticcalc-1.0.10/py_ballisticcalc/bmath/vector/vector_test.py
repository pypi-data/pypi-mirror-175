import timeit
import unittest
import pyximport
import math
pyximport.install()
from py_ballisticcalc.bmath.vector import Vector


class TestVector(unittest.TestCase):

    def test_create(self):
        v = Vector(1, 2, 3)
        mag = v.magnitude()
        mc = v.multiply_by_const(10)

        b = Vector(1, 2, 3)
        mv = v.multiply_by_vector(b)
        a = v.add(b)
        s = v.subtract(b)
        neg = v.negate()
        norm = v.normalize()
        # print('\n'.join([str(i) for i in [mag, mc, mv, a, s, neg, norm]]))
        x = v.x

    # @unittest.SkipTest
    def test_time(self):
        t = timeit.timeit(self.test_create, number=50000)
        print(t)


class TestVectorCreation(unittest.TestCase):

    def test_create(self):
        v = Vector(1, 2, 3)

        self.assertTrue(v.x == 1 and v.y == 2 and v.z == 3, "Create failed")

        c = v.copy()
        self.assertTrue(c.x == 1 and c.y == 2 and c.z == 3, "Copy failed")


class TestUnary(unittest.TestCase):

    def test_unary(self):
        v1 = Vector(1, 2, 3)

        self.assertFalse(math.fabs(v1.magnitude() - 3.74165738677) > 1e-7, "Magnitude failed")

        v2 = v1.negate()
        self.assertTrue(v2.x() == -1.0 and v2.y() == -2.0 and v2.z() == -3.0, "Negate failed")

        v2 = v1.normalize()
        self.assertFalse(v2.x() > 1.0 or v2.y() > 1.0 or v2.z() > 1.0, "Normalize failed")

        v1 = Vector(0, 0, 0)
        v2 = v1.normalize()

        self.assertFalse(v2.x() != 0.0 or v2.y() != 0.0 or v2.z() != 0.0, "Normalize failed")


class TestBinary(unittest.TestCase):

    def test_binary(self):
        v1 = Vector(1, 2, 3)

        v2 = v1.add(v1.copy())
        self.assertFalse(v2.x() != 2.0 or v2.y() != 4.0 or v2.z() != 6.0, "Add failed")

        v2 = v1.subtract(v2)
        self.assertFalse(v2.x() != -1.0 or v2.y() != -2.0 or v2.z() != -3.0, "Subtract failed")

        self.assertFalse(v1.multiply_by_vector(v1.copy()) != float(1 + 4 + 9), "MultiplyByVector failed")

        v2 = v1.multiply_by_const(3)
        self.assertFalse(v2.x() != 3.0 or v2.y() != 6.0 or v2.z() != 9.0, "MultiplyByConst failed")
