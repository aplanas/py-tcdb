import os
import unittest

from tcdb import hdb


class TestHdb(unittest.TestCase):
    def setUp(self):
        self.hdb = hdb.hdb()
        self.hdb.open('test.hdb')

    def tearDown(self):
        self.hdb.close()
        self.hdb = None
        os.remove('test.hdb')

    def test_put(self):
        objs = [1+1j, 'some text', 10, 10.0]
        for obj1 in objs:
            self.hdb.put('obj', obj1)
            obj2 = self.hdb.get('obj')
            self.assertEqual(obj1, obj2)

            self.hdb.put(obj1, obj1)
            obj2 = self.hdb.get(obj1)
            self.assertEqual(obj1, obj2)

    def test_put_str(self):
        str1 = 'some text'
        objs = [1+1j, 'some text', 10, 10.0]
        for obj in objs:
            self.hdb.put_str(obj, str1)
            str2 = self.hdb.get_str(obj)
            self.assertEqual(str1, str2)

    def test_put_int(self):
        int1 = 10
        objs = [1+1j, 'some text', 10, 10.0]
        for obj in objs:
            self.hdb.put_int(obj, int1)
            int2 = self.hdb.get_int(obj)
            self.assertEqual(int1, int2)

    def test_put_float(self):
        float1 = 10.10
        objs = [1+1j, 'some text', 10, 10.0]
        for obj in objs:
            self.hdb.put_float(obj, float1)
            float2 = self.hdb.get_float(obj)
            self.assertEqual(float1, float2)

    def no_test_putkeep(self):
        objs = [1+1j, 'some text', 10, 10.0]
        for obj1 in objs:
            self.hdb.put('obj', obj1)
            obj2 = self.hdb.get('obj')
            self.assertEqual(obj1, obj2)
            self.hdb.putkeep('obj', 'Never stored')
            obj2 = self.hdb.get('obj')
            self.assertEqual(obj1, obj2)

            self.hdb.putkeep(obj1, obj1)
            obj2 = self.hdb.get(obj1)
            self.assertEqual(obj1, obj2)
            self.hdb.putkeep(obj1, 'Never stored')
            obj2 = self.hdb.get(obj1)
            self.assertEqual(obj1, obj2)

    def test_putasync(self):
        objs = [1+1j, 'some text', 10, 10.0]
        for obj1 in objs:
            self.hdb.putasync('obj', obj1)
            obj2 = self.hdb.get('obj')
            self.assertEqual(obj1, obj2)

            self.hdb.putasync(obj1, obj1)
            obj2 = self.hdb.get(obj1)
            self.assertEqual(obj1, obj2)

    def test_out_and_contains(self):
        objs = [1+1j, 'some text', 10, 10.0]
        for obj in objs:
            self.hdb.put(obj, obj)
            self.assert_(obj in self.hdb)
            self.hdb.out(obj)
            self.assert_(obj not in self.hdb)

    def test_vsiz(self):
        obj = 1+1j
        self.hdb.put(obj, obj)
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 48)

        obj = 'some text'
        self.hdb.put_str(obj, obj)
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 9)

        obj = 10
        self.hdb.put_int(obj, obj)
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 4)

        obj = 10.10
        self.hdb.put_float(obj, obj)
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 8)

    def test_iters(self):
        objs = [1+1j, 'some text', 10, 10.0]
        for obj in objs:
            self.hdb.put(obj, obj)

        self.assertEqual(self.hdb.keys(), objs)
        for key in self.hdb:
            self.assert_(key in objs)

        self.assertEqual(self.hdb.values(), objs)
        for value in self.hdb.itervalues():
            self.assert_(value in objs)

        zobjs = zip(objs, objs)
        self.assertEqual(list(self.hdb.iteritems()), zobjs)

    def test_fwmkeys(self):
        objs = ['aa', 'ab', 'ac', 'xx', 'ad']
        for obj in objs:
            self.hdb.put(obj, 'same value')
        self.assertEqual(self.hdb.fwmkeys('a'), ['aa', 'ab', 'ac', 'ad'])
        self.assertEqual(self.hdb.fwmkeys('x'), ['xx'])

    def test_add_int(self):
        objs = [1+1j, 'some text', 10, 10.0]
        for obj in objs:
            self.hdb.put_int(obj, 10)
        for key in self.hdb:
            self.hdb.add_int(key, 2)
        for key in self.hdb:
            self.assertEqual(self.hdb.get_int(key), 12)

    def test_add_float(self):
        objs = [1+1j, 'some text', 10, 10.0]
        for obj in objs:
            self.hdb.put_float(obj, 10.0)
        for key in self.hdb:
            self.hdb.add_float(key, 2.0)
        for key in self.hdb:
            self.assertEqual(self.hdb.get_float(key), 12.0)

if __name__ == '__main__':
    unittest.main()
