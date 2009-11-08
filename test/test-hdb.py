# -*- coding: utf-8 -*-

import datetime
import os
import unittest
import warnings

from tcdb import hdb
from tcdb import tc


class TestHdb(unittest.TestCase):
    def setUp(self):
        self.hdb = hdb.hdb()
        self.hdb.open('test.hdb')

    def tearDown(self):
        self.hdb.close()
        self.hdb = None
        os.remove('test.hdb')

    def test_put(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj1 in objs:
            self.hdb.put('obj', obj1)
            obj2 = self.hdb.get('obj')
            self.assertEqual(obj1, obj2)

            self.hdb.put(obj1, obj1)
            obj2 = self.hdb.get(obj1)
            self.assertEqual(obj1, obj2)
        self.assertRaises(KeyError, self.hdb.get, 'nonexistent key')

    def test_put_str(self):
        str1 = 'some text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.put_str(obj, str1)
            str2 = self.hdb.get_str(obj)
            self.assertEqual(str1, str2)
        unicode1 = u'unicode text [áéíóú]'
        for obj in objs:
            self.hdb.put_str(obj, unicode1.encode('utf8'))
            unicode2 = unicode(self.hdb.get_str(obj), 'utf8')
            self.assertEqual(unicode1, unicode2)
        self.assertRaises(KeyError, self.hdb.get_str, 'nonexistent key')

    def test_put_unicode(self):
        unicode1 = u'unicode text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.put_unicode(obj, unicode1)
            unicode2 = self.hdb.get_unicode(obj)
            self.assertEqual(unicode1, unicode2)
        self.assertRaises(KeyError, self.hdb.get_unicode, 'nonexistent key')

    def test_put_int(self):
        int1 = 10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.put_int(obj, int1)
            int2 = self.hdb.get_int(obj)
            self.assertEqual(int1, int2)
        self.assertRaises(KeyError, self.hdb.get_int, 'nonexistent key')

    def test_put_float(self):
        float1 = 10.10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.put_float(obj, float1)
            float2 = self.hdb.get_float(obj)
            self.assertEqual(float1, float2)
        self.assertRaises(KeyError, self.hdb.get_float, 'nonexistent key')

    def test_putkeep(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
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

    def test_putcat_str(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.putcat_str(obj, 'some')
        for obj in objs:
            self.hdb.putcat_str(obj, ' text')
        for obj in objs:
            self.assertEquals(self.hdb.get_str(obj), 'some text')

    def test_putcat_unicode(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.putcat_unicode(obj, u'some')
        for obj in objs:
            self.hdb.putcat_unicode(obj, u' text')
        for obj in objs:
            self.assertEquals(self.hdb.get_unicode(obj), u'some text')

    def test_putasync(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj1 in objs:
            self.hdb.putasync('obj', obj1)
            obj2 = self.hdb.get('obj')
            self.assertEqual(obj1, obj2)

            self.hdb.putasync(obj1, obj1)
            obj2 = self.hdb.get(obj1)
            self.assertEqual(obj1, obj2)

    def test_out_and_contains(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
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

        obj = 'some text [áéíóú]'
        self.hdb.put_str(obj, obj)
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 22)

        obj = u'unicode text [áéíóú]'
        self.hdb.put_str(obj, obj.encode('utf8'))
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 25)

        obj = 10
        self.hdb.put_int(obj, obj)
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 4)

        obj = 10.10
        self.hdb.put_float(obj, obj)
        vsiz = self.hdb.vsiz(obj)
        self.assertEqual(vsiz, 8)

    def ntest_iters(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
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
        self.assertEqual(self.hdb.fwmkeys('nonexistent key'), [])

    def test_add_int(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.put_int(obj, 10)
        for key in self.hdb:
            self.hdb.add_int(key, 2)
        for key in self.hdb:
            self.assertEqual(self.hdb.get_int(key), 12)

    def test_add_float(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.put_float(obj, 10.0)
        for key in self.hdb:
            self.hdb.add_float(key, 2.0)
        for key in self.hdb:
            self.assertEqual(self.hdb.get_float(key), 12.0)

    def test_admin_functions(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.hdb.put(obj, obj)

        self.assertEquals(self.hdb.path(), 'test.hdb')

        self.hdb.sync()
        self.assertEquals(len(self.hdb), 5)
        self.assertEquals(self.hdb.fsiz(), 529056)

        self.hdb.vanish()
        self.assertEquals(self.hdb.fsiz(), 528704)

        self.assert_(self.hdb.memsync(True))
        self.assert_(self.hdb.cacheclear())
        self.assertEquals(self.hdb.bnum(), 131071)
        self.assertEquals(self.hdb.align(), 16)
        self.assertEquals(self.hdb.fbpmax(), 1024)
        self.assertEquals(self.hdb.xmsiz(), 67108864)
        self.assert_(self.hdb.inode())
        self.assert_((datetime.datetime.now()-self.hdb.mtime()).seconds <= 1)
        # Why OTRUNC?!?
        self.assertEquals(self.hdb.omode(), hdb.OWRITER|hdb.OCREAT|hdb.OTRUNC)
        self.assertEquals(self.hdb.type(), tc.THASH)
        self.assertEquals(self.hdb.flags(), hdb.FOPEN)
        self.assertEquals(self.hdb.opts(), 0)
        self.assertEquals(self.hdb.opaque(), '')
        self.assertEquals(self.hdb.bnumused(), 0)
        self.assertEquals(self.hdb.dfunit(), 0)
        self.assert_(self.hdb.defrag(5))

    def test_transaction(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        with self.hdb as db:
            for obj in objs:
                db.put(obj, obj)
        self.assertEquals(len(self.hdb), 5)
        self.hdb.vanish()
        try:
            with self.hdb:
                for obj in objs:
                    self.hdb.put(obj, obj)
                self.hdb.get('Not exist key')
        except KeyError:
            pass
        self.assertEquals(len(self.hdb), 0)

    def test_foreach(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]

        def proc(key, value, op):
            self.assertEquals(key, value)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.assert_(key in objs)
            self.assertEquals(op, 'test')
            return True

        for obj in objs:
            self.hdb.put(obj, obj)
        self.hdb.foreach(proc, 'test')


if __name__ == '__main__':
    unittest.main()
