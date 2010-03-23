# -*- coding: utf-8 -*-

import datetime
import os
import unittest
import warnings

from tcdb import bdb
from tcdb import tc


class TestBDB(unittest.TestCase):
    def setUp(self):
        self.bdb = bdb.BDB()
        self.bdb.open('test.bdb', lmemb=128, lcnum=1024, ncnum=0, xmsiz=100)

    def tearDown(self):
        self.bdb.close()
        self.bdb = None
        os.remove('test.bdb')

    def test_setgetitem(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj1 in objs:
            self.bdb['obj'] = obj1
            obj2 = self.bdb['obj']
            self.assertEqual(obj1, obj2)

            self.bdb[obj1] = obj1
            obj2 = self.bdb[obj1]
            self.assertEqual(obj1, obj2)
        self.assertRaises(KeyError, self.bdb.__getitem__, 'nonexistent key')

    def test_put(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj1 in objs:
            self.bdb.put(obj1, obj1)
            obj2 = self.bdb.get(obj1)
            self.assertEqual(obj1, obj2)
            self.bdb.put(obj1, obj1, raw_key=True)
            obj2 = self.bdb.get(obj1, raw_key=True)
            self.assertEqual(obj1, obj2)
        self.assertRaises(KeyError, self.bdb.get, 'nonexistent key')

    def test_put_str(self):
        str1 = 'some text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put_str(obj, str1)
            str2 = self.bdb.get_str(obj)
            self.assertEqual(str1, str2)
            self.bdb.put_str(obj, str1, as_raw=True)
            str2 = self.bdb.get_str(obj, as_raw=True)
            self.assertEqual(str1, str2)
        unicode1 = u'unicode text [áéíóú]'
        for obj in objs:
            self.bdb.put_str(obj, unicode1.encode('utf8'))
            unicode2 = unicode(self.bdb.get_str(obj), 'utf8')
            self.assertEqual(unicode1, unicode2)
        self.assertRaises(AssertionError, self.bdb.put_str, 'key', 10)
        self.assertRaises(KeyError, self.bdb.get_str, 'nonexistent key')

    def test_put_unicode(self):
        unicode1 = u'unicode text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put_unicode(obj, unicode1)
            unicode2 = self.bdb.get_unicode(obj)
            self.assertEqual(unicode1, unicode2)
            self.bdb.put_unicode(obj, unicode1, as_raw=True)
            unicode2 = self.bdb.get_unicode(obj, as_raw=True)
            self.assertEqual(unicode1, unicode2)
        self.assertRaises(AssertionError, self.bdb.put_unicode, 'key', 10)
        self.assertRaises(KeyError, self.bdb.get_unicode, 'nonexistent key')

    def test_put_int(self):
        int1 = 10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put_int(obj, int1)
            int2 = self.bdb.get_int(obj)
            self.assertEqual(int1, int2)
        self.assertRaises(AssertionError, self.bdb.put_int, 'key', '10')
        self.assertRaises(KeyError, self.bdb.get_int, 'nonexistent key')

    def test_put_float(self):
        float1 = 10.10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put_float(obj, float1)
            float2 = self.bdb.get_float(obj)
            self.assertEqual(float1, float2)
        self.assertRaises(AssertionError, self.bdb.put_float, 'key', 10)
        self.assertRaises(KeyError, self.bdb.get_float, 'nonexistent key')

    def test_putkeep(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj1 in objs:
            self.bdb.putkeep(obj1, obj1)
            obj2 = self.bdb.get(obj1)
            self.assertEqual(obj1, obj2)
            self.bdb.putkeep(obj1, 'Never stored')
            obj2 = self.bdb.get(obj1)
            self.assertEqual(obj1, obj2)

    def test_putkeep_str(self):
        str1 = 'some text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putkeep_str(obj, str1)
            str2 = self.bdb.get_str(obj)
            self.assertEqual(str1, str2)
            self.bdb.putkeep_str(obj, 'Never stored')
            str2 = self.bdb.get_str(obj)
            self.assertEqual(str1, str2)
        self.assertRaises(AssertionError, self.bdb.putkeep_str, 'key', 10)

    def test_putkeep_unicode(self):
        unicode1 = u'unicode text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putkeep_unicode(obj, unicode1)
            unicode2 = self.bdb.get_unicode(obj)
            self.assertEqual(unicode1, unicode2)
            self.bdb.putkeep_unicode(obj, u'Never stored')
            unicode2 = self.bdb.get_unicode(obj)
            self.assertEqual(unicode1, unicode2)
        self.assertRaises(AssertionError, self.bdb.putkeep_unicode, 'key', 10)

    def test_putkeep_int(self):
        int1 = 10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putkeep_int(obj, int1)
            int2 = self.bdb.get_int(obj)
            self.assertEqual(int1, int2)
            self.bdb.putkeep_int(obj, int1*10)
            int2 = self.bdb.get_int(obj)
            self.assertEqual(int1, int2)
        self.assertRaises(AssertionError, self.bdb.putkeep_int, 'key', '10')

    def test_putkeep_float(self):
        float1 = 10.10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putkeep_float(obj, float1)
            float2 = self.bdb.get_float(obj)
            self.assertEqual(float1, float2)
            self.bdb.putkeep_float(obj, float1*10)
            float2 = self.bdb.get_float(obj)
            self.assertEqual(float1, float2)
        self.assertRaises(AssertionError, self.bdb.put_float, 'key', 10)

    def test_putcat_str(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putcat_str(obj, 'some')
        for obj in objs:
            self.bdb.putcat_str(obj, ' text')
        for obj in objs:
            self.assertEquals(self.bdb.get_str(obj), 'some text')

    def test_putcat_unicode(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putcat_unicode(obj, u'some')
        for obj in objs:
            self.bdb.putcat_unicode(obj, u' text')
        for obj in objs:
            self.assertEquals(self.bdb.get_unicode(obj), u'some text')

    def test_putdup(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj1 in objs:
            self.bdb.putdup(obj1, obj1)
            obj2 = self.bdb.get(obj1)
            self.assertEqual(obj1, obj2)
            self.bdb.putdup(obj1, 'duplicate key')
            obj2 = self.bdb.get(obj1)
            self.assertEqual(obj1, obj2)
            allobjs = self.bdb.getdup(obj1)
            self.assertEqual(allobjs, [obj1, 'duplicate key'])
        self.assertRaises(KeyError, self.bdb.getdup, 'nonexistent key')

    def test_putdup_str(self):
        str1 = 'some text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_str(obj, str1)
            str2 = self.bdb.get_str(obj)
            self.assertEqual(str1, str2)
            self.bdb.putdup_str(obj, 'duplicate key')
            str2 = self.bdb.get_str(obj)
            self.assertEqual(str1, str2)
            allstrs = self.bdb.getdup_str(obj)
            self.assertEqual(allstrs, [str1, 'duplicate key'])
        self.assertRaises(KeyError, self.bdb.getdup_str, 'nonexistent key')

    def test_putdup_unicode(self):
        unicode1 = u'unicode text [áéíóú]'
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_unicode(obj, unicode1)
            unicode2 = self.bdb.get_unicode(obj)
            self.assertEqual(unicode1, unicode2)
            self.bdb.putdup_unicode(obj, u'duplicate key')
            unicode2 = self.bdb.get_unicode(obj)
            self.assertEqual(unicode1, unicode2)
            allunicodes = self.bdb.getdup_unicode(obj)
            self.assertEqual(allunicodes, [unicode1, u'duplicate key'])
        self.assertRaises(KeyError, self.bdb.getdup_unicode, 'nonexistent key')

    def test_putdup_int(self):
        int1 = 10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_int(obj, int1)
            int2 = self.bdb.get_int(obj)
            self.assertEqual(int1, int2)
            self.bdb.putdup_int(obj, 20)
            int2 = self.bdb.get_int(obj)
            self.assertEqual(int1, int2)
            allints = self.bdb.getdup_int(obj)
            self.assertEqual(allints, [int1, 20])
        self.assertRaises(KeyError, self.bdb.getdup_int, 'nonexistent key')

    def test_putdup_float(self):
        float1 = 10.10
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_float(obj, float1)
            float2 = self.bdb.get_float(obj)
            self.assertEqual(float1, float2)
            self.bdb.putdup_float(obj, 20.20)
            float2 = self.bdb.get_float(obj)
            self.assertEqual(float1, float2)
            allfloats = self.bdb.getdup_float(obj)
            self.assertEqual(allfloats, [float1, 20.20])
        self.assertRaises(KeyError, self.bdb.getdup_float, 'nonexistent key')

    def test_putdup_iter(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj1 in objs:
            self.bdb.putdup_iter(obj1, objs)
            obj2 = self.bdb.get(obj1)
            self.assertEqual(obj2, objs[0])
            allobjs = self.bdb.getdup(obj1)
            self.assertEqual(allobjs, objs)

    def test_putdup_iter_str(self):
        strs = ['some text [áéíóú]', 'other text']
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_iter_str(obj, strs)
            str1 = self.bdb.get_str(obj)
            self.assertEqual(str1, strs[0])
            allstrs = self.bdb.getdup_str(obj)
            self.assertEqual(allstrs, strs)

    def test_putdup_iter_unicode(self):
        unicodes = [u'unicode text [áéíóú]', u'other text']
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_iter_unicode(obj, unicodes)
            unicode1 = self.bdb.get_unicode(obj)
            self.assertEqual(unicode1, unicodes[0])
            allunicodes = self.bdb.getdup_unicode(obj)
            self.assertEqual(allunicodes, unicodes)

    def test_putdup_iter_int(self):
        ints = [10, 20]
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_iter_int(obj, ints)
            int1 = self.bdb.get_int(obj)
            self.assertEqual(int1, ints[0])
            allints = self.bdb.getdup_int(obj)
            self.assertEqual(allints, ints)

    def test_putdup_iter_float(self):
        floats = [10.10, 20.20]
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.putdup_iter_float(obj, floats)
            float1 = self.bdb.get_float(obj)
            self.assertEqual(float1, floats[0])
            allfloats = self.bdb.getdup_float(obj)
            self.assertEqual(allfloats, floats)

    def test_out_and_contains(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put(obj, obj)
            self.assert_(obj in self.bdb)
            del self.bdb[obj]
            self.assert_(obj not in self.bdb)

        for obj in objs:
            self.bdb.putdup_iter(obj, objs)
            self.assert_(obj in self.bdb)
            del self.bdb[obj]
            allobjs = self.bdb.getdup(obj)
            self.assertEqual(allobjs, objs[1:])
            self.bdb.outdup(obj)
            self.assert_(obj not in self.bdb)

    def test_vsiz(self):
        obj = 1+1j
        self.bdb.put(obj, obj)
        vsiz = self.bdb.vsiz(obj)
        self.assertEqual(vsiz, 48)

        obj = 'some text [áéíóú]'
        self.bdb.put_str(obj, obj)
        vsiz = self.bdb.vsiz(obj)
        self.assertEqual(vsiz, 22)

        obj = u'unicode text [áéíóú]'
        self.bdb.put_str(obj, obj.encode('utf8'))
        vsiz = self.bdb.vsiz(obj)
        self.assertEqual(vsiz, 25)

        obj = 10
        self.bdb.put_int(obj, obj)
        vsiz = self.bdb.vsiz(obj)
        self.assertEqual(vsiz, 4)

        obj = 10.10
        self.bdb.put_float(obj, obj)
        vsiz = self.bdb.vsiz(obj)
        self.assertEqual(vsiz, 8)

    def test_iters(self):
        self.assertEqual(self.bdb.keys(), [])
        self.assertEqual(self.bdb.values(), [])
        self.assertEqual(self.bdb.items(), [])

        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put(obj, obj)

        self.assertEqual(len(self.bdb.values()), len(objs))
        self.assertEqual(self.bdb.keys(), self.bdb.values())
        self.assertEqual(self.bdb.items(),
                         zip(self.bdb.keys(), self.bdb.values()))

        for key in self.bdb:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.assert_(key in objs)

        for value in self.bdb.itervalues():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.assert_(value in objs)

    def test_range(self):
        objs = zip([10**x for x in range(6)], range(6))
        for k, v in objs:
            self.bdb.put_int(k, v, as_raw=True)

        # Be careful: ints are stores as little endian
        self.assertEqual(self.bdb.range(10, True, 10000, True), [10, 10000])
        self.assertEqual(self.bdb.range(10, True, 10000, False), [10])
        self.assertEqual(self.bdb.range(10, False, 10000, False), [])

    def test_fwmkeys(self):
        objs = ['aa', 'ab', 'ac', 'xx', 'ad']
        for obj in objs:
            self.bdb.put(obj, 'same value', raw_key=True)
        self.assertEqual(self.bdb.fwmkeys('a'), ['aa', 'ab', 'ac', 'ad'])
        self.assertEqual(self.bdb.fwmkeys('x'), ['xx'])
        self.assertEqual(self.bdb.fwmkeys('nonexistent key'), [])

    def test_add_int(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put_int(obj, 10)
        for key in self.bdb:
            self.bdb.add_int(key, 2)
        for key in self.bdb:
            self.assertEqual(self.bdb.get_int(key), 12)

    def test_add_float(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put_float(obj, 10.0)
        for key in self.bdb:
            self.bdb.add_float(key, 2.0)
        for key in self.bdb:
            self.assertEqual(self.bdb.get_float(key), 12.0)

    def test_admin_functions(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        for obj in objs:
            self.bdb.put(obj, obj)

        self.assertEqual(self.bdb.path(), 'test.bdb')

        self.bdb.sync()
        self.assertEqual(len(self.bdb), 5)
        self.assertEqual(self.bdb.fsiz(), 136192)

        self.bdb.vanish()
        self.assertEqual(self.bdb.fsiz(), 135680)

        self.assert_(self.bdb.memsync(True))
        self.assert_(self.bdb.cacheclear())
        self.assertEqual(self.bdb.lmemb(), 128)
        self.assertEqual(self.bdb.lnum(), 1)
        self.assertEqual(self.bdb.nnum(), 0)
        self.assertEqual(self.bdb.bnum(), 32749)
        self.assertEqual(self.bdb.align(), 256)
        self.assertEqual(self.bdb.fbpmax(), 1024)

        self.assert_(self.bdb.inode())
        self.assert_((datetime.datetime.now()-self.bdb.mtime()).seconds <= 1)
        self.assertEqual(self.bdb.flags(), bdb.FOPEN)
        self.assertEqual(self.bdb.opts(), 0)
        self.assertEqual(self.bdb.opaque(), '')
        self.assertEqual(self.bdb.bnumused(), 1)
        self.assertEqual(self.bdb.dfunit(), 0)
        self.assert_(self.bdb.defrag(5))
        self.assert_(self.bdb.cacheclear())

    def test_transaction(self):
        objs = [1+1j, 'some text [áéíóú]', u'unicode text [áéíóú]', 10, 10.0]
        with self.bdb as db:
            for obj in objs:
                db.put(obj, obj)
        self.assertEquals(len(self.bdb), 5)
        self.bdb.vanish()
        try:
            with self.bdb:
                for obj in objs:
                    self.bdb.put(obj, obj)
                self.bdb.get('Not exist key')
        except KeyError:
            pass
        self.assertEquals(len(self.bdb), 0)

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
            self.bdb.put(obj, obj)
        self.bdb.foreach(proc, 'test')


if __name__ == '__main__':
    unittest.main()