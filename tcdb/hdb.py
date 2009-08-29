# -*- coding: utf-8 -*-
# Tokyo Cabinet Python ctypes binding.

"""
HDB is an implementation of bsddb-like API for Tokyo Cabinet hash
database.

We need to import 'hdb' class, and use like that:

>>> from tcdb.hdb import hdb

>>> db = hdb()             # Create a new database object
>>> db.open('casket.tch')  # By default create it if don't exist

>>> db.put("foo", "hop")
True
>>> db.put("bar", "step")
True
>>> db.put("baz", "jump")
True

>>> db.get("foo")
'hop'

>>> db.close()

"""

import cPickle
import ctypes

import tc


# enumeration for tuning options
TLARGE   = 1 << 0               # use 64-bit bucket array
TDEFLATE = 1 << 1               # compress each record with Deflate
TBZIP    = 1 << 2               # compress each record with BZIP2
TTCBS    = 1 << 3               # compress each record with TCBS
TEXCODEC = 1 << 4               # compress each record with custom functions

# enumeration for open modes
OREADER  = 1 << 0               # open as a reader
OWRITER  = 1 << 1               # open as a writer
OCREAT   = 1 << 2               # writer creating
OTRUNC   = 1 << 3               # writer truncating
ONOLCK   = 1 << 4               # open without locking
OLCKNB   = 1 << 5               # lock without blocking
OTSYNC   = 1 << 6               # synchronize every transaction


class hdb(object):
    def __init__(self):
        """Create a hash database object."""
        self.db = tc.hdb_new()

    def __del__(self):
        """Delete a hash database object."""
        tc.hdb_del(self.db)

    def setmutex(self):
        """Set mutual exclusion control of a hash database object for
        threading."""
        return tc.hdb_setmutex(self.db)
        
    def tune(self, bnum, apow, fpow, opts):
        """Set the tuning parameters of a hash database object."""
        return tc.hdb_tume(self.db, bnum, apow, fpow, opts)

    def setcache(self, rcnum):
        """Set the caching parameters of a hash database object."""
        return tc.hdb_setcache(self.db, rcnum)

    def setxmsiz(self, xmsiz):
        """Set the size of the extra mapped memory of a hash database
        object."""
        return tc.hdb_setxmsiz(self.db, xmsiz)

    def setdfunit(self, dfunit):
        """Set the unit step number of auto defragmentation of a hash
        database object."""
        return tc.hdb_setdfunit(self.db, dfunit)

    def open(self, path, omode=OWRITER|OCREAT, bnum=None, apow=None, fpow=None,
             opts=None, rcnum=None, xmsiz=None, dfunit=None):
        """Open a database file and connect a hash database object."""
        if rcnum:
            self.setcache(rcnum)

        if xmsiz:
            self.setxmsiz(xmsiz)

        if dfunit:
            self.setdfunit(dfunit)

        kwargs = dict([x for x in (('bnum', bnum),
                                   ('apow', apow),
                                   ('fpow', fpow),
                                   ('opts', opts)) if x[1]])
        if kwargs:
            if not tc.hdb_tune(self.db, *kwargs):
                raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))

        if not tc.hdb_open(self.db, path, omode):
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))

    def close(self):
        """Close a hash database object."""
        result = tc.hdb_close(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def __setitem__(self, key, value):
        """Store any Python object into a hash database object."""
        return self.put(key, value)

    def put(self, key, value):
        """Store any Python object into a hash database object."""
        return self.put_str(key, cPickle.dumps(value, cPickle.HIGHEST_PROTOCOL))

    def put_str(self, key, value):
        """Store a string record into a hash database object."""
        result = tc.hdb_put2(self.db, key, value)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def put_int(self, key, value):
        """Store an integer record into a hash database object."""
        c_key = ctypes.c_char_p(key)
        c_value = ctypes.c_int(value)
        result = tc.hdb_put(self.db, c_key, len(key), ctypes.byref(c_value),
                            ctypes.sizeof(c_value))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def put_double(self, key, value):
        """Store a double precision record into a hash database
        object."""
        c_key = ctypes.c_char_p(key)
        c_value = ctypes.c_double(value)
        result = tc.hdb_put(self.db, c_key, len(key)+1, ctypes.byref(c_value),
                            ctypes.sizeof(c_value))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def putkeep(self, key, value):
        """Store a new Python object into a hash database object."""
        return self.putkeep_str(key, cPickle.dumps(value,
                                                   cPickle.HIGHEST_PROTOCOL))

    def putkeep_str(self, key, value):
        """Store a new string record into a hash database object."""
        result = tc.hdb_putkeep2(self.db, key, value)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def putkeep_int(self, key, value):
        """Store a new integer record into a hash database object."""
        c_key = ctypes.c_char_p(key)
        c_value = ctypes.c_int(value)
        result = tc.hdb_putkeep(self.db, c_key, len(key), ctypes.byref(c_value),
                                ctypes.sizeof(c_value))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def putkeep_double(self, key, value):
        """Store a new double precision record into a hash database
        object."""
        c_key = ctypes.c_char_p(key)
        c_value = ctypes.c_double(value)
        result = tc.hdb_putkeep(self.db, c_key, len(key), ctypes.byref(c_value),
                                ctypes.sizeof(c_value))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def putcat_str(self, key, value):
        """Concatenate a string value at the end of the existing
        record in a hash database object."""
        result = tc.hdb_putcat2(self.db, key, value)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def putasync(self, key, value):
        """Store a Python object into a hash database object in
        asynchronous fashion."""
        return self.putasync_str(key, cPickle.dumps(value,
                                                    cPickle.HIGHEST_PROTOCOL))

    def putasync_str(self, key, value):
        """Store a string record into a hash database object in
        asynchronous fashion."""
        result = tc.hdb_putasync2(self.db, key, value)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def putasync_int(self, key, value):
        """Store an integer record into a hash database object in
        asynchronous fashion."""
        c_key = ctypes.c_char_p(key)
        c_value = ctypes.c_int(value)
        result = tc.hdb_putasync(self.db, c_key, len(key),
                                 ctypes.byref(c_value), ctypes.sizeof(c_value))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def putasync_double(self, key, value):
        """Store a double precision record into a hash database object
        in asynchronous fashion."""
        c_key = ctypes.c_char_p(key)
        c_value = ctypes.c_double(value)
        result = tc.hdb_putasync(self.db, c_key, len(key),
                                 ctypes.byref(c_value), ctypes.sizeof(c_value))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def __delitem__(self, key):
        """Remove a Python object of a hash database object."""
        return self.out(key)

    def out(self, key):
        """Remove a Python object of a hash database object."""
        return self.out_str(key)

    def out_str(self, key):
        """Remove a string record of a hash database object."""
        result = tc.hdb_out2(self.db, key)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def out_int(self, key):
        """Remove a integer record of a hash database object."""
        c_key = ctypes.c_char_p(key)
        result = tc.hdb_out(self.db, c_key, len(key))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def out_double(self, key):
        """Remove a double precision record of a hash database
        object."""
        c_key = ctypes.c_char_p(key)
        result = tc.hdb_out(self.db, c_key, len(key))
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def __getitem__(self, key):
        """Retrieve a Python object in a hash database object."""
        return self.get(key)

    def get(self, key):
        """Retrieve a Python object in a hash database object."""
        return cPickle.loads(self.get_str(key))

    def get_str(self, key):
        """Retrieve a string record in a hash database object."""
        result = tc.hdb_get2(self.db, key)
        if not result.value:
            raise KeyError(key)
        return result.value

    def get_int(self, key):
        """Retrieve an integer record in a hash database object."""
        c_key = ctypes.c_char_p(key)
        (result, size) = tc.hdb_get(self.db, c_key, len(key))
        if not result.value:
            raise KeyError(key)
        return ctypes.cast(result, tc.c_int_p).contents.value
        
    def get_double(self, key):
        """Retrieve a double precision record in a hash database
        object."""
        c_key = ctypes.c_char_p(key)
        (result, size) = tc.hdb_get(self.db, c_key, len(key))
        if not result.value:
            raise KeyError(key)
        return ctypes.cast(result, tc.c_double_p).contents.value

    def vsiz(self, key):
        """Get the size of the value of a Python object in a hash
        database object."""
        return self.vsiz_str(key)

    def vsiz_str(self, key):
        """Get the size of the value of a string record in a hash
        database object."""
        result = tc.hdb_vsiz2(self.db, key)
        if result == -1:
            raise KeyError(key)
        return result

    def vsiz_int(self, key):
        """Get the size of the value of a integer record in a hash
        database object."""
        c_key = ctypes.c_char_p(key)
        result = tc.hdb_vsiz2(self.db, c_key, len(key))
        if result == -1:
            raise KeyError(key)
        return result

    def vsiz_double(self, key):
        """Get the size of the value of a double precision record in a
        hash database object."""
        c_key = ctypes.c_char_p(key)
        result = tc.hdb_vsiz2(self.db, c_key, len(key))
        if result == -1:
            raise KeyError(key)
        return result

    def keys(self):
        """Get all the keys of a hash database object."""
        return list(self.iterkeys())

    def iterkeys(self):
        """Iterate for every key in a hash database object."""
        if not tc.hdb_iterinit(self.db):
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        while True:
            c_key = tc.hdb_iternext2(self.db)
            if not c_key.value:
                break
            yield c_key.value

    def values(self):
        """Get all the values of a hash database object."""
        return list(self.itervalues())

    def itervalues(self):
        """Iterate for every value in a hash database object."""
        if not tc.hdb_iterinit(self.db):
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        while True:
            c_key = tc.hdb_iternext2(self.db)
            if not c_key.value:
                break
            yield self.get(c_key.value)

    def iteritems(self):
        """Iterate for every key / value in a hash database object."""
        if not tc.hdb_iterinit(self.db):
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        while True:
            xstr_key = tc.tcxstrnew()
            xstr_value = tc.tcxstrnew()
            result = tc.hdb_iternext3(self.db, xstr_key, xstr_value)
            if not result:
                break
            yield (xstr_key.contents.ptr,
                   cPickle.loads(xstr_value.contents.ptr))

    def __iter__(self):
        """Iterate for every key in a hash database object."""
        return self.iterkeys()

    def fwmkeys(self, prefix):
        """Get forward matching string keys in a hash database
        object."""
        tclist = tc.hdb_fwmkeys2(self.db, prefix)
        start = tclist.contents.start
        num = tclist.contents.num
        array = tclist.contents.array
        result = [d.ptr for d in array[start:start+num]]
        return result

    def add_int(self, key, num):
        """Add an integer to a record in a hash database object."""
        c_key = ctypes.c_char_p(key)
        return tc.hdb_addint(self.db, c_key, len(key), num)

    def add_double(self, key, num):
        """Add a real number to a record in a hash database object."""
        c_key = ctypes.c_char_p(key)
        return tc.hdb_adddouble(self.db, c_key, len(key), num)

    def sync(self):
        """Synchronize updated contents of a hash database object with
        the file and the device."""
        result = tc.hdb_sync(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def optimize(self, bnum=None, apow=None, fpow=None, opts=None):
        """Optimize the file of a hash database object."""
        kwargs = dict([x for x in (('bnum', bnum),
                                   ('apow', apow),
                                   ('fpow', fpow),
                                   ('opts', opts)) if x[1]])
        result = tc.hdb_optimize(self.db, *kwargs)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))

    def vanish(self):
        """Remove all records of a hash database object."""
        result = tc.hdb_vanish(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def copy(self, path):
        """Copy the database file of a hash database object."""
        result = tc.hdb_copy(self.db, path)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def tranbegin(self):
        """Begin the transaction of a hash database object."""
        result = tc.hdb_tranbegin(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def trancommit(self):
        """Commit the transaction of a hash database object."""
        result = tc.hdb_trancommit(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def tranabort(self):
        """Abort the transaction of a hash database object."""
        result = tc.hdb_tranabort(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def __enter__(self):
        """Enter in the 'with' statement and begin the transaction."""
        self.tranbegin()

    def __exit__(self, type, value, traceback):
        """Exit from 'with' statement and ends the transaction."""
        if type is None:
            self.trancommit()
        else:
            self.tranabort()

    def path(self):
        """Get the file path of a hash database object."""
        return tc.hdb_path(self.db)

    def __len__(self):
        """Get the number of records of a hash database object."""
        return tc.hdb_rnum(self.db)

    def fsiz(self):
        """Get the size of the database file of a hash database
        object."""
        return tc.hdb_fsiz(self.db)

    def setecode(self, ecode, filename, line, func):
        """Set the error code of a hash database object."""
        tc.setecode(self.db, ecode, filename, line, func)

    def settype(self, type_):
        """Set the type of a hash database object."""
        tc.settype(self.db, type_)

    def setdbgfd(self, fd):
        """Set the file descriptor for debugging output."""
        tc.setdbgfd(self.db, fd)

    def dbgfd(self):
        """Get the file descriptor for debugging output."""
        return tc.dbgfd(self.db)

    def hasmutex(self):
        """Check whether mutual exclusion control is set to a hash
        database object."""
        return tc.hdb_hasmutex(self.db)

    def memsync(self, phys):
        """Synchronize updating contents on memory of a hash database
        object."""
        result = tc.hdb_memsync(self.db, phys)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def cacheclear(self):
        """Clear the cache of a hash tree database object."""
        result = tc.hdb_cacheclear(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def bnum(self):
        """Get the number of elements of the bucket array of a hash
        database object."""
        return tc.hdb_bnum(self.db)

    def align(self):
        """Get the record alignment of a hash database object."""
        return tc.hdb_align(self.db)

    def fbdmax(self):
        """Get the maximum number of the free block pool of a a hash
        database object."""
        return tc.hdb_fbpmax(self.db)

    def xmsiz(self):
        """Get the size of the extra mapped memory of a hash database
        object."""
        return tc.hdb_xmsiz(self.db)

    def inode(self):
        """Get the inode number of the database file of a hash
        database object."""
        return tc.hdb_inode(self.db)

    def mtime(self):
        """Get the modification time of the database file of a hash
        database object."""
        return tc.hdb_mtime(self.db)

    def omode(self):
        """Get the connection mode of a hash database object."""
        return tc.omode(self.db)

    def type(self):
        """Get the database type of a hash database object."""
        return tc.hdb_type(self.db)

    def flags(self):
        """Get the additional flags of a hash database object."""
        return tc.hdb_flags(self.db)

    def opts(self):
        """Get the options of a hash database object."""
        return tc.hdb_opts(self.db)

    def opaque(self):
        """Get the pointer to the opaque field of a hash database
        object."""
        return tc.hdb_opaque(self.db)

    def bnumused(self):
        """Get the number of used elements of the bucket array of a
        hash database object."""
        return tc.hdb_bnumused(self.db)

    # def setcodecfunc(self, enc, encop, dec, decop):
    #     """Set the custom codec functions of a hash database
    #     object."""
    #     result = tc.hdb_setcodecfunc(self.db, TCCODEC(enc), encop,
    #                                  TCCODEC(dec), decop)
    #     if not result:
    #         raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
    #     return result

    # def codecfunc(self):
    #     """Get the custom codec functions of a hash database
    #     object."""
    #     # See tc.hdb_codecfunc

    def dfunit(self):
        """Get the unit step number of auto defragmentation of a hash
        database object."""
        return tc.hdb_dfunit(self.db)

    def defrag(self, step):
        """Perform dynamic defragmentation of a hash database
        object."""
        result = tc.hdb_defrag(self.db, step)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    # def putproc(self, key, value, proc, op):
    #     """Store a record into a hash database object with a
    #     duplication handler."""
    #     # See tc.hdb_putproc

    def foreach(self, proc, op):
        """Process each record atomically of a hash database
        object."""
        result = tc.hdb_foreach(TCITER(proc), op)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def tranvoid(self):
        """Void the transaction of a hash database object."""
        result = tc.hdb_tranvoid(self.db)
        if not result:
            raise tc.TCError(tc.hdb_errmsg(tc.hdb_ecode()))
        return result

    def __contains__(self, key):
        """Return True in hash database object has the key."""
        return tc.hdb_iterinit3(self.db, key)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
