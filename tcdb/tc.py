# -*- coding: utf-8 -*-
# Tokyo Cabinet Python ctypes binding.

from ctypes import CDLL, CFUNCTYPE, POINTER
from ctypes import Structure
from ctypes import c_int, c_int8, c_int32, c_int64
from ctypes import c_uint, c_uint8, c_uint32, c_uint64
from ctypes import c_bool, c_size_t
from ctypes import c_double
from ctypes import c_char_p, c_void_p
from ctypes.util import find_library

c_int_p  = POINTER(c_int)

c_double_p = POINTER(c_double)

c_time_t = c_uint64              # This is valid in 64 bit architecture.

class tc_char_p(c_char_p):
    """Automatic garbage collectable ctypes.c_char_p type."""
    def __del__(self):
        if self.value:
            libtc.tcfree(self)

class tc_void_p(c_void_p):
    """Automatic garbage collectable ctypes.c_void_p type."""
    def __del__(self):
        if self.value:
            libtc.tcfree(self)


# Load Tokyo Cabinet library
libtc = CDLL(find_library('tokyocabinet'))

__version__ = c_char_p.in_dll(libtc, 'tcversion').value


# Every XXX_errmsg() message is driven by this class
class TCException(Exception):
    pass


# Extracted from 'cxcore.py' file
# ctypes-opencv - A Python wrapper for OpenCV using ctypes
# Copyright (c) 2008, Minh-Tri Pham
def cfunc(name, dll, result, *args):
    """Build and apply a ctypes prototype complete with parameter
    flags

    e.g.
    cvMinMaxLoc = cfunc('cvMinMaxLoc', _cxDLL, None,
                        ('image', IplImage_p, 1),
                        ('min_val', c_double_p, 2),
                        ('max_val', c_double_p, 2),
                        ('min_loc', CvPoint_p, 2),
                        ('max_loc', CvPoint_p, 2),
                        ('mask', IplImage_p, 1, None))

    Means locate cvMinMaxLoc in dll _cxDLL, it returns nothing.

    The first argument is an input parameter.  The next 4 arguments
    are output, and the last argument is input with an optional value.
    A typical call might look like:

    min_val,max_val,min_loc,max_loc = cvMinMaxLoc(img)

    """
    atypes = []
    aflags = []
    for arg in args:
        atypes.append(arg[1])
        aflags.append((arg[2], arg[0]) + arg[3:])
    return CFUNCTYPE(result, *atypes)((name, dll), tuple(aflags))


#
# Functions from tcutil.h
#

tcmalloc = cfunc('tcmalloc', libtc, c_void_p,
                 ('size', c_size_t, 1))
tcmalloc.__doc__ =\
"""Allocate a region on memory.

size -- specifies the size of the region.

The return value is the pointer to the allocated region.

This function handles failure of memory allocation implicitly.
Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

tccalloc = cfunc('tccalloc', libtc, c_void_p,
                 ('nmemb', c_size_t, 1),
                 ('size', c_size_t, 1))
tccalloc.__doc__ =\
"""Allocate a nullified region on memory.

nmemb -- specifies the number of elements.
size  -- specifies the size of each element.

The return value is the pointer to the allocated nullified region.

This function handles failure of memory allocation implicitly.
Because the region of the return value is allocated with the 'calloc'
call, it should be released with the free' call when it is no longer
in use.

"""

tcrealloc = cfunc('tcrealloc', libtc, c_void_p,
                  ('ptr', c_void_p, 1),
                  ('size', c_size_t, 1))
tcrealloc.__doc__ =\
"""Re-allocate a region on memory.

ptr  -- specifies the pointer to the region.
size -- specifies the size of the region.

The return value is the pointer to the re-allocated region.

This function handles failure of memory allocation implicitly.
Because the region of the return value is allocated with the 'realloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

tcmemdup = cfunc('tcmemdup', libtc, c_void_p,
                 ('ptr', c_void_p, 1),
                 ('size', c_size_t, 1))
tcmemdup.__doc__ =\
"""Duplicate a region on memory.

ptr  -- specifies the pointer to the region.
size -- specifies the size of the region.

The return value is the pointer to the allocated region of the
duplicate.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the free' call when it is no
longer in use.

"""

tcstrdup = cfunc('tcstrdup', libtc, c_char_p,
                 ('str', c_char_p, 1))
tcstrdup.__doc__ =\
"""Duplicate a string on memory.

str -- specifies the string.

The return value is the allocated string equivalent to the specified
string.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

tcfree = cfunc('tcfree', libtc, None,
               ('ptr', c_void_p, 1))
tcfree.__doc__ =\
"""Free a region on memory.

ptr -- specifies the pointer to the region.  If it is 'NULL', this
       function has no effect.

Although this function is just a wrapper of 'free' call, this is
useful in applications using another package of the 'malloc' series.

"""

# basic utilities (for experts)

TCCMP = CFUNCTYPE(c_int, c_char_p, c_int, c_char_p, c_int, c_void_p)
TCCMP.__doc__ =\
"""Type of the pointer to a comparison function.

aptr -- specifies the pointer to the region of one key.
asiz -- specifies the size of the region of one key.
bptr -- specifies the pointer to the region of the other key.
bsiz -- specifies the size of the region of the other key.
op   -- specifies the pointer to the optional opaque object.

The return value is positive if the former is big, negative if the
latter is big, 0 if both are equivalent.

"""

TCCMP_P = POINTER(TCCMP)

TCCODEC = CFUNCTYPE(c_void_p, c_void_p, c_int, c_int_p, c_void_p)
TCCODEC.__doc__ =\
"""Type of the pointer to a encoding or decoding function.

ptr  -- specifies the pointer to the region.
size -- specifies the size of the region.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.
op   -- specifies the pointer to the optional opaque object.

If successful, the return value is the pointer to the result object
allocated with 'malloc' call, else, it is 'NULL'.

"""

TCCODEC_P = POINTER(TCCODEC)

TCPDPROC = CFUNCTYPE(c_void_p, c_void_p, c_int, c_int_p, c_void_p)
TCPDPROC.__doc__ =\
"""Type of the pointer to a callback function to process record
duplication.

vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.
op   -- specifies the pointer to the optional opaque object.

The return value is the pointer to the result object allocated with
'malloc'.  It is released by the caller.  If it is 'NULL', the record
is not modified.

"""

TCPDPROC_P = POINTER(TCPDPROC)

TCITER = CFUNCTYPE(c_bool, c_void_p, c_int, c_void_p, c_int, c_void_p)
TCITER.__doc__ =\
"""Type of the pointer to a iterator function.

kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.
op   -- specifies the pointer to the optional opaque object.

The return value is true to continue iteration or false to stop
iteration.

"""

TCITER_P = POINTER(TCITER)

# extensible string

class TCXSTR(Structure):
    """Type of structure for an extensible string object."""
    _fields_ = [('ptr', c_void_p),         # pointer to the region
                ('size', c_int),           # size of the region
                ('asize', c_int)]          # size of the allocated region

TCXSTR_P = POINTER(TCXSTR)
TCXSTR_P.__del__ = lambda self : libtc.tcxstrdel(self)


tcxstrnew = cfunc('tcxstrnew', libtc, TCXSTR_P)
tcxstrnew.__doc__ =\
"""Create an extensible string object.

The return value is the new extensible string object.

"""

tcxstrnew2 = cfunc('tcxstrnew2', libtc, TCXSTR_P,
                   ('str', c_char_p, 1))
tcxstrnew2.__doc__ =\
"""Create an extensible string object from a character string.

str -- specifies the string of the initial content.

The return value is the new extensible string object containing the
specified string.

"""

tcxstrnew3 = cfunc('tcxstrnew3', libtc, TCXSTR_P,
                   ('asiz', c_int, 1))
tcxstrnew3.__doc__ =\
"""Create an extensible string object with the initial allocation
size.

asiz -- specifies the initial allocation size.

The return value is the new extensible string object.

"""

tcxstrdup = cfunc('tcxstrdup', libtc, TCXSTR_P,
                  ('xstr', TCXSTR_P, 1))
tcxstrdup.__doc__ =\
"""Copy an extensible string object.

xstr -- specifies the extensible string object.

The return value is the new extensible string object equivalent to the
specified object.

"""

tcxstrdel = cfunc('tcxstrdel', libtc, None,
                  ('xstr', TCXSTR_P, 1))
tcxstrdel.__doc__ =\
"""Delete an extensible string object.

xstr -- specifies the extensible string object.

Note that the deleted object and its derivatives can not be used
anymore.

"""

tcxstrcat = cfunc('tcxstrcat', libtc, None,
                  ('xstr', TCXSTR_P, 1),
                  ('ptr', c_void_p, 1),
                  ('size', c_int, 1))
tcxstrcat.__doc__ =\
"""Concatenate a region to the end of an extensible string object.

xstr -- specifies the extensible string object.
ptr  -- specifies the pointer to the region to be appended.
size -- specifies the size of the region.

"""

tcxstrcat2 = cfunc('tcxstrcat2', libtc, None,
                   ('xstr', TCXSTR_P, 1),
                   ('str', c_char_p, 1))
tcxstrcat2.__doc__ =\
"""Concatenate a character string to the end of an extensible string
object.

xstr -- specifies the extensible string object.
str  -- specifies the string to be appended.

"""

tcxstrptr = cfunc('tcxstrptr', libtc, c_void_p,
                  ('xstr', TCXSTR_P, 1))
tcxstrptr.__doc__ =\
"""Get the pointer of the region of an extensible string object.

xstr -- specifies the extensible string object.

The return value is the pointer of the region of the object.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.

"""

tcxstrsize = cfunc('tcxstrsize', libtc, c_int,
                   ('xstr', TCXSTR_P, 1))
tcxstrsize.__doc__ =\
"""Get the size of the region of an extensible string object.

xstr -- specifies the extensible string object.

The return value is the size of the region of the object.

"""

tcxstrclear = cfunc('tcxstrclear', libtc, None,
                    ('xstr', TCXSTR_P, 1))
tcxstrclear.__doc__ =\
"""Clear an extensible string object.

xstr -- specifies the extensible string object.

The internal buffer of the object is cleared and the size is set zero.

"""

# extensible string (for experts)

tcxstrtomalloc = cfunc('tcxstrtomalloc', libtc, tc_void_p,
                       ('xstr', TCXSTR_P, 1))
tcxstrtomalloc.__doc__ =\
"""Convert an extensible string object into a usual allocated region.

xstr -- specifies the extensible string object.

The return value is the pointer to the allocated region of the object.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.  Because the region of the original object is
deleted, it should not be deleted again.

"""

tcxstrfrommalloc = cfunc('tcxstrfrommalloc', libtc, TCXSTR_P,
                         ('ptr', c_void_p, 1),
                         ('size', c_int, 1))
tcxstrfrommalloc.__doc__ =\
"""Create an extensible string object from an allocated region.

ptr  -- specifies the pointer to the region allocated with 'malloc'
        call.
size -- specifies the size of the region.

The return value is the new extensible string object wrapping the
specified region.

Note that the specified region is released when the object is deleted.

"""

#  array list

class TCLISTDATUM(Structure):
    """Type of structure for an element of a list."""
    _fields_ = [('ptr', c_char_p),         # pointer to the region
                ('size', c_int)]           # size of the effective region

TCLISTDATUM_P = POINTER(TCLISTDATUM)


class TCLIST(Structure):
    """Type of structure for an array list."""
    _fields_ = [('array', TCLISTDATUM_P),  # array of data
                ('anum', c_int),           # number of the elements of the array
                ('start', c_int),          # start index of used elements
                ('num', c_int)]            # number of used elements

TCLIST_P = POINTER(TCLIST)
TCLIST_P.__del__ = lambda self : libtc.tclistdel(self)


tclistnew = cfunc('tclistnew', libtc, TCLIST_P)
tclistnew.__doc__ =\
"""Create a list object.

The return value is the new list object.

"""

tclistnew2 = cfunc('tclistnew2', libtc, TCLIST_P,
                   ('anum', c_int, 1))
tclistnew2.__doc__ =\
"""Create a list object with expecting the number of elements.

anum -- specifies the number of elements expected to be stored in the
        list.

The return value is the new list object.

"""

# XXX Fix params type
# tclistnew3 = cfunc('tclistnew3', libtc, TCLIST_P,
#                    ('str', c_char_p, 1))
# tclistnew3.__doc__ =\
# """Create a list object with initial string elements.

# str -- specifies the string of the first element.

# The other arguments are other elements.  They should be trailed by a
# 'NULL' argument.

# The return value is the new list object.
# """

tclistdup = cfunc('tclistdup', libtc, TCLIST_P,
                  ('list', TCLIST_P, 1))
tclistdup.__doc__ =\
"""Copy a list object.

list -- specifies the list object.

The return value is the new list object equivalent to the specified
object.

"""

tclistdel = cfunc('tclistdel', libtc, None,
                  ('list', TCLIST_P, 1))
tclistdel.__doc__ =\
"""Delete a list object.

list -- specifies the list object.

Note that the deleted object and its derivatives can not be used
anymore.

"""

tclistnum = cfunc('tclistnum', libtc, c_int,
                  ('list', TCLIST_P, 1))
tclistnum.__doc__ =\
"""Get the number of elements of a list object.

list -- specifies the list object.

The return value is the number of elements of the list.

"""

tclistval = cfunc('tclistval', libtc, c_void_p,
                  ('list', TCLIST_P, 1),
                  ('index', c_int, 1),
                  ('sp', c_int_p, 2))
tclistval.errcheck = lambda result, func, arguments : (result, arguments[2])
tclistval.__doc__ =\
"""Get the pointer to the region of an element of a list object.

list  -- specifies the list object.
index -- specifies the index of the element.
sp    -- specifies the pointer to the variable into which the size of
         the region of the return value is assigned.

The return value is the pointer to the region of the value.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  If 'index' is equal to or more than the number of elements,
the return value is 'NULL'.

"""

tclistval2 = cfunc('tclistval2', libtc, c_char_p,
                   ('list', TCLIST_P, 1),
                   ('index', c_int, 1))
tclistval2.__doc__ =\
"""Get the string of an element of a list object.

list  -- specifies the list object.
index -- specifies the index of the element.

The return value is the string of the value.

If 'index' is equal to or more than the number of elements, the return
value is 'NULL'.

"""

tclistpush = cfunc('tclistpush', libtc, None,
                   ('list', TCLIST_P, 1),
                   ('ptr', c_void_p, 1),
                   ('size', c_int, 1))
tclistpush.__doc__ =\
"""Add an element at the end of a list object.

list -- specifies the list object.
ptr  -- specifies the pointer to the region of the new element.
size -- specifies the size of the region.

"""

tclistpush2 = cfunc('tclistpush2', libtc, None,
                    ('list', TCLIST_P, 1),
                    ('str', c_char_p, 1))
tclistpush2.__doc__ =\
"""Add a string element at the end of a list object.

list -- specifies the list object.
str  -- specifies the string of the new element.

"""

tclistpop = cfunc('tclistpop', libtc, tc_void_p,
                  ('list', TCLIST_P, 1),
                  ('sp', c_int_p, 2))
tclistpop.errcheck = lambda result, func, arguments : (result, arguments[1])
tclistpop.__doc__ =\
"""Remove an element of the end of a list object.

list -- specifies the list object.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.

The return value is the pointer to the region of the removed element.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.  If the list is empty, the return value is 'NULL'.

"""

tclistpop2 = cfunc('tclistpop2', libtc, tc_char_p,
                   ('list', TCLIST_P, 1))
tclistpop2.__doc__ =\
"""Remove a string element of the end of a list object.

list -- specifies the list object.

The return value is the string of the removed element.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.  If the list is empty, the return value is 'NULL'.

"""

tclistunshift = cfunc('tclistunshift', libtc, None,
                      ('list', TCLIST_P, 1),
                      ('ptr', c_void_p, 1),
                      ('size', c_int, 1))
tclistunshift.__doc__ =\
"""Add an element at the top of a list object.

list -- specifies the list object.
ptr  -- specifies the pointer to the region of the new element.
size -- specifies the size of the region.

"""

tclistunshift2 = cfunc('tclistunshift2', libtc, None,
                       ('list', TCLIST_P, 1),
                       ('str', c_char_p, 1))
tclistunshift2.__doc__ =\
"""Add a string element at the top of a list object.

list -- specifies the list object.
str  -- specifies the string of the new element.

"""

tclistshift = cfunc('tclistshift', libtc, tc_void_p,
                    ('list', TCLIST_P, 1),
                    ('sp', c_int_p, 2))
tclistshift.errcheck = lambda result, func, arguments : (result, arguments[1])
tclistshift.__doc__ =\
"""Remove an element of the top of a list object.

list -- specifies the list object.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.

The return value is the pointer to the region of the removed element.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.  If the list is empty, the return value is 'NULL'.

"""

tclistshift2 = cfunc('tclistshift2', libtc, tc_char_p,
                     ('list', TCLIST_P, 1))
tclistshift2.__doc__ =\
"""Remove a string element of the top of a list object.

list -- specifies the list object.

The return value is the string of the removed element.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.  If the list is empty, the return value is 'NULL'.

"""

tclistinsert = cfunc('tclistinsert', libtc, None,
                     ('list', TCLIST_P, 1),
                     ('index', c_int, 1),
                     ('ptr', c_void_p, 1),
                     ('size', c_int, 1))
tclistinsert.__doc__ =\
"""Add an element at the specified location of a list object.

list  -- specifies the list object.
index -- specifies the index of the new element.
ptr   -- specifies the pointer to the region of the new element.
size  -- specifies the size of the region.

If 'index' is equal to or more than the number of elements, this
function has no effect.

"""

tclistinsert2 = cfunc('tclistinsert2', libtc, None,
                      ('list', TCLIST_P, 1),
                      ('index', c_int, 1),
                      ('str', c_char_p, 1))
tclistinsert2.__doc__ =\
"""Add a string element at the specified location of a list object.

list  -- specifies the list object.
index -- specifies the index of the new element.
str   -- specifies the string of the new element.

If 'index' is equal to or more than the number of elements, this
function has no effect.

"""

tclistremove = cfunc('tclistremove', libtc, tc_void_p,
                     ('list', TCLIST_P, 1),
                     ('index', c_int, 1),
                     ('sp', c_int_p, 2))
tclistremove.errcheck = lambda result, func, arguments : (result, arguments[2])
tclistremove.__doc__ =\
"""Remove an element at the specified location of a list object.

list  -- specifies the list object.
index -- specifies the index of the element to be removed.
sp    -- specifies the pointer to the variable into which the size of
         the region of the return value is assigned.

The return value is the pointer to the region of the removed element.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.  If `index' is equal to or more than the number of
elements, no element is removed and the return value is 'NULL'.

"""

tclistremove2 = cfunc('tclistremove2', libtc, tc_char_p,
                      ('list', TCLIST_P, 1),
                      ('index', c_int, 1))
tclistremove2.__doc__ =\
"""Remove a string element at the specified location of a list object.

list  -- specifies the list object.
index -- specifies the index of the element to be removed.

The return value is the string of the removed element.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.  If 'index' is equal to or more than the number of elements,
no element is removed and the return value is 'NULL'.

"""

tclistover = cfunc('tclistover', libtc, None,
                   ('list', TCLIST_P, 1),
                   ('index', c_int, 1),
                   ('ptr', c_void_p, 1),
                   ('size', c_int, 1))
tclistover.__doc__ =\
"""Overwrite an element at the specified location of a list object.

list  -- specifies the list object.
index -- specifies the index of the element to be overwritten.
ptr   -- specifies the pointer to the region of the new content.
size  -- specifies the size of the new content.

If 'index' is equal to or more than the number of elements, this
function has no effect.

"""

tclistover2 = cfunc('tclistover2', libtc, None,
                    ('list', TCLIST_P, 1),
                    ('index', c_int, 1),
                    ('str', c_char_p, 1))
tclistover2.__doc__ =\
"""Overwrite a string element at the specified location of a list
object.

list  -- specifies the list object.
index -- specifies the index of the element to be overwritten.
str   -- specifies the string of the new content.

If 'index' is equal to or more than the number of elements, this
function has no effect.

"""

tclistsort = cfunc('tclistsort', libtc, None,
                   ('list', TCLIST_P, 1))
tclistsort.__doc__ =\
"""Sort elements of a list object in lexical order.

list -- specifies the list object.

"""

tclistlsearch = cfunc('tclistlsearch', libtc, c_int,
                      ('list', TCLIST_P, 1),
                      ('ptr', c_void_p, 1),
                      ('size', c_int, 1))
tclistlsearch.__doc__ =\
"""Search a list object for an element using liner search.

list -- specifies the list object.
ptr  -- specifies the pointer to the region of the key.
size -- specifies the size of the region.

The return value is the index of a corresponding element or -1 if
there is no corresponding element.

If two or more elements correspond, the former returns.

"""

tclistbsearch = cfunc('tclistbsearch', libtc, c_int,
                      ('list', TCLIST_P, 1),
                      ('ptr', c_void_p, 1),
                      ('size', c_int, 1))
tclistbsearch.__doc__ =\
"""Search a list object for an element using binary search.

list -- specifies the list object.  It should be sorted in lexical
        order.
ptr  -- specifies the pointer to the region of the key.
size -- specifies the size of the region.

The return value is the index of a corresponding element or -1 if
there is no corresponding element.

If two or more elements correspond, which returns is not defined.

"""

tclistclear = cfunc('tclistclear', libtc, None,
                    ('list', TCLIST_P, 1))
tclistclear.__doc__ =\
"""Clear a list object.

list -- specifies the list object.

All elements are removed.

"""

tclistdump = cfunc('tclistdump', libtc, tc_void_p,
                   ('list', TCLIST_P, 1),
                   ('sp', c_int_p, 2))
tclistdump.errcheck = lambda result, func, arguments : (result, arguments[1])
tclistdump.__doc__ =\
"""Serialize a list object into a byte array.

list -- specifies the list object.
spcc -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.

The return value is the pointer to the region of the result serial
region.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

tclistload = cfunc('tclistload', libtc, TCLIST_P,
                   ('ptr', c_void_p, 1),
                   ('size', c_int, 1))
tclistload.__doc__ =\
"""Create a list object from a serialized byte array.

ptr  -- specifies the pointer to the region of serialized byte array.
size -- specifies the size of the region.

The return value is a new list object.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.

"""

# array list (for experts)

tclistpushmalloc = cfunc('tclistpushmalloc', libtc, None,
                         ('list', TCLIST_P, 1),
                         ('ptr', c_void_p, 1),
                         ('size', c_int, 1))
tclistpushmalloc.__doc__ =\
"""Add an allocated element at the end of a list object.

list -- specifies the list object.
ptr  -- specifies the pointer to the region allocated with 'malloc'
        call.
size -- specifies the size of the region.

Note that the specified region is released when the object is deleted.

"""

tclistsortci = cfunc('tclistsortci', libtc, None,
                     ('list', TCLIST_P, 1))
tclistsortci.__doc__ =\
"""Sort elements of a list object in case-insensitive lexical order.

list -- specifies the list object.

"""

# XXX Fix params type
# tclistsortex = cfunc('tclistsortex', libtc, None,
#                      ('list', TCLIST_P, 1),
#                      ('cmp', c_void_p, 1))
# tclistsortex.__doc__ =\
# """Sort elements of a list object by an arbitrary comparison function.

# list -- specifies the list object.
# cmp  -- specifies the pointer to the comparison function.  The
#         structure TCLISTDATUM has the member "ptr" which is the
#         pointer to the region of the element, and the member "size"
#         which is the size of the region.

# """

tclistinvert = cfunc('tclistinvert', libtc, None,
                     ('list', TCLIST_P, 1))
tclistinvert.__doc__ =\
"""Invert elements of a list object.

list -- specifies the list object.

"""

# XXX Fix params type
# tclistprintf = cfunc('tclistprintf', libtc, None,
#                      ('list', TCLIST_P, 1),
#                      ('format', c_char_p, 1))
# tclistprintf.__doc__ =\
# """Perform formatted output into a list object.

# list   -- specifies the list object.
# format -- specifies the printf-like format string.  The conversion
#           character '%' can be used with such flag characters as 's',
#           'd', 'o', 'u', 'x', 'X', 'c', 'e', 'E', 'f', 'g', 'G', '@',
#           '?', 'b', and '%'.  '@' works as with 's' but escapes meta
#           characters of XML.  '?' works as with 's' but escapes meta
#           characters of URL.  'b' converts an integer to the string as
#           binary numbers.  The other conversion character work as with
#           each original.

# The other arguments are used according to the format string.

# """

# enumeration for database type
THASH  = 0                      # hash table
TBTREE = 1                      # B+ tree
TFIXED = 2                      # fixed-length 
TTABLE = 3                      # table


#
# Functions from tcadb.h
#

# adb_new = cfunc('tcadbnew', libtc, c_void_p)
# adb_new.__doc__ =\
# """Create an abstract database object.

# The return value is the new abstract database object.

# """

# adb_del = cfunc('tcadbdel', libtc, None,
#                 ('adb', c_void_p, 1))
# adb_del.__doc__ =\
# """Delete an abstract database object.

# adb -- specifies the abstract database object.

# """

# adb_open = cfunc('tcadbopen', libtc, c_bool,
#                  ('adb', c_void_p, 1),
#                  ('name', c_char_p, 1))
# adb_open.__doc__ =\
# """Open an abstract database.

# adb  -- specifies the abstract database object.
# name -- specifies the name of the database.  If it is "*", the
#         database will be an on-memory hash database.  If it is "+",
#         the database will be an on-memory tree database.  If its
#         suffix is ".tch", the database will be a hash database.  If
#         its suffix is ".tcb", the database will be a B+ tree database.
#         If its suffix is ".tcf", the database will be a fixed-length
#         database. If its suffix is ".tct", the database will be a
#         table database.  Otherwise, this function fails.  Tuning
#         parameters can trail the name, separated by "#".  Each
#         parameter is composed of the name and the value, separated by
#         "=".  On-memory hash database supports "bnum", "capnum", and
#         "capsiz".  On-memory tree database supports "capnum" and
#         "capsiz".  Hash database supports "mode", "bnum", "apow",
#         "fpow", "opts", "rcnum", "xmsiz", and "dfunit".  B+ tree
#         database supports "mode", "lmemb", "nmemb", "bnum", "apow",
#         "fpow", "opts", "lcnum", "ncnum", "xmsiz", and "dfunit".
#         Fixed-length database supports "mode", "width", and "limsiz".
#         Table database supports "mode", "bnum", "apow", "fpow",
#         "opts", "rcnum", "lcnum", "ncnum", "xmsiz", "dfunit", and
#         "idx".

# If successful, the return value is true, else, it is false.

# The tuning parameter "capnum" specifies the capacity number of
# records.  "capsiz" specifies the capacity size of using memory.
# Records spilled the capacity are removed by the storing order.  "mode"
# can contain "w" of writer, "r" of reader, "c" of creating, "t" of
# truncating, "e" of no locking, and "f" of non-blocking lock.  The
# default mode is relevant to "wc".  "opts" can contains "l" of large
# option, "d" of Deflate option, "b" of BZIP2 option, and "t" of TCBS
# option.  "idx" specifies the column name of an index and its type
# separated by ":".

# For example, "casket.tch#bnum=1000000#opts=ld" means that the name of
# the database file is "casket.tch", and the bucket number is 1000000,
# and the options are large and Deflate.

# """

# adb_close = cfunc('tcadbclose', libtc, c_bool,
#                   ('adb', c_void_p, 1))
# adb_close.__doc__ =\
# """Close an abstract database object.

# adb -- specifies the abstract database object.

# If successful, the return value is true, else, it is false.

# Update of a database is assured to be written when the database is
# closed.  If a writer opens a database but does not close it
# appropriately, the database will be broken.

# """

# adb_put = cfunc('tcadbput', libtc, c_bool,
#                 ('adb', c_void_p, 1),
#                 ('kbuf', c_void_p, 1),
#                 ('ksiz', c_int, 1),
#                 ('vbuf', c_void_p, 1),
#                 ('vsiz', c_int, 1))
# adb_put.__doc__ =\
# """Store a record into an abstract database object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# vbuf -- specifies the pointer to the region of the value.
# vsiz -- specifies the size of the region of the value.

# If successful, the return value is true, else, it is false.

# If a record with the same key exists in the database, it is
# overwritten.

# """

# adb_put2 = cfunc('tcadbput2', libtc, c_bool,
#                  ('adb', c_void_p, 1),
#                  ('kstr', c_char_p, 1),
#                  ('vstr', c_char_p, 1))
# adb_put2.__doc__ =\
# """Store a string record into an abstract object.

# adb  -- specifies the abstract database object.
# kstr -- specifies the string of the key.
# vstr -- specifies the string of the value.

# If successful, the return value is true, else, it is false.

# If a record with the same key exists in the database, it is
# overwritten.

# """

# adb_putkeep = cfunc('tcadbputkeep', libtc, c_bool,
#                     ('adb', c_void_p, 1),
#                     ('kbuf', c_void_p, 1),
#                     ('ksiz', c_int, 1),
#                     ('vbuf', c_void_p, 1),
#                     ('vsiz', c_int, 1))
# adb_putkeep.__doc__ =\
# """Store a new record into an abstract database object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# vbuf -- specifies the pointer to the region of the value.
# vsiz -- specifies the size of the region of the value.

# If successful, the return value is true, else, it is false.

# If a record with the same key exists in the database, this function
# has no effect.

# """

# adb_putkeep2 = cfunc('tcadbputkeep2', libtc, c_bool,
#                      ('adb', c_void_p, 1),
#                      ('kstr', c_char_p, 1),
#                      ('vstr', c_char_p, 1))
# adb_putkeep2.__doc__ =\
# """Store a new string record into an abstract database object.

# adb  -- specifies the abstract database object.
# kstr -- specifies the string of the key.
# vstr -- specifies the string of the value.

# If successful, the return value is true, else, it is false.

# If a record with the same key exists in the database, this function
# has no effect.

# """

# adb_putcat = cfunc('tcadbputcat', libtc, c_bool,
#                    ('adb', c_void_p, 1),
#                    ('kbuf', c_void_p, 1),
#                    ('ksiz', c_int, 1),
#                    ('vbuf', c_void_p, 1),
#                    ('vsiz', c_int, 1))
# adb_putcat.__doc__ =\
# """Concatenate a value at the end of the existing record in an
# abstract database object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# vbuf -- specifies the pointer to the region of the value.
# vsiz -- specifies the size of the region of the value.

# If successful, the return value is true, else, it is false.

# If there is no corresponding record, a new record is created.

# """

# adb_putcat2 = cfunc('tcadbputcat2', libtc, c_bool,
#                     ('adb', c_void_p, 1),
#                     ('kstr', c_char_p, 1),
#                     ('vstr', c_char_p, 1))
# adb_putcat2.__doc__ =\
# """Concatenate a string value at the end of the existing record in an
# abstract database object.

# adb  -- specifies the abstract database object.
# kstr -- specifies the string of the key.
# vstr -- specifies the string of the value.

# If successful, the return value is true, else, it is false.

# If there is no corresponding record, a new record is created.

# """

# adb_out = cfunc('tcadbout', libtc, c_bool,
#                 ('adb', c_void_p, 1),
#                 ('kbuf', c_void_p, 1),
#                 ('ksiz', c_int, 1))
# adb_out.__doc__ =\
# """Remove a record of an abstract database object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.

# If successful, the return value is true, else, it is false.

# """

# adb_out2 = cfunc('tcadbput2', libtc, c_bool,
#                  ('adb', c_void_p, 1),
#                  ('kstr', c_char_p, 1))
# adb_out2.__doc__ =\
# """Remove a string record of an abstract database object.

# adb  -- specifies the abstract database object.
# kstr -- specifies the string of the key.

# If successful, the return value is true, else, it is false.

# """

# adb_get = cfunc('tcadbget', libtc, c_void_p,
#                 ('adb', c_void_p, 1),
#                 ('kbuf', c_void_p, 1),
#                 ('ksiz', c_int, 1),
#                 ('sp', c_int_p, 2))
# adb_get.__doc__ =\
# """Retrieve a record in an abstract database object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# sp   -- specifies the pointer to the variable into which the size of
#         the region of the return value is assigned.

# If successful, the return value is the pointer to the region of the
# value of the corresponding record.  'NULL' is returned if no record
# corresponds.

# Because an additional zero code is appended at the end of the region
# of the return value, the return value can be treated as a character
# string.  Because the region of the return value is allocated with the
# 'malloc' call, it should be released with the 'free' call when it is
# no longer in use.

# """

# adb_get2 = cfunc('tcadbget2', libtc, tc_char_p,
#                  ('adb', c_void_p, 1),
#                  ('kstr', c_char_p, 1))
# adb_get2.__doc__ =\
# """Retrieve a string record in an abstract database object.

# adb  -- specifies the abstract database object.
# kstr -- specifies the string of the key.

# If successful, the return value is the string of the value of the
# corresponding record. 'NULL' is returned if no record corresponds.

# Because the region of the return value is allocated with the 'malloc'
# call, it should be released with the 'free' call when it is no longer
# in use.

# """

# adb_vsiz = cfunc('tcadbvsiz', libtc, c_int,
#                  ('adb', c_void_p, 1),
#                  ('kbuf', c_void_p, 1),
#                  ('ksiz', c_int, 1))
# adb_vsiz.__doc__ =\
# """Get the size of the value of a record in an abstract database
# object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.

# If successful, the return value is the size of the value of the
# corresponding record, else, it is -1.

# """

# adb_vsiz2 = cfunc('tcadbvsiz2', libtc, c_int,
#                   ('adb', c_void_p, 1),
#                   ('kstr', c_char_p, 1))
# adb_vsiz2.__doc__ =\
# """Get the size of the value of a string record in an abstract
# database object.

# adb  -- specifies the abstract database object.
# kstr -- specifies the string of the key.

# If successful, the return value is the size of the value of the
# corresponding record, else, it is -1.

# """

# adb_iterinit = cfunc('tcadbiterinit', libtc, c_bool,
#                      ('adb', c_void_p, 1))
# adb_iterinit.__doc__ =\
# """Initialize the iterator of an abstract database object.

# adb -- specifies the abstract database object.

# If successful, the return value is true, else, it is false.

# The iterator is used in order to access the key of every record stored
# in a database.

# """

# adb_iternext = cfunc('tcadbiternext', libtc, c_void_p,
#                      ('adb', c_void_p, 1),
#                      ('sp', c_int_p, 2))
# adb_iternext.__doc__ =\
# """Get the next key of the iterator of an abstract database object.

# adb -- specifies the abstract database object.
# sp  -- specifies the pointer to the variable into which the size of
#        the region of the return value is assigned.

# If successful, the return value is the pointer to the region of the
# next key, else, it is 'NULL'.  'NULL' is returned when no record is to
# be get out of the iterator.

# Because an additional zero code is appended at the end of the region
# of the return value, the return value can be treated as a character
# string.  Because the region of the return value is allocated with the
# 'malloc' call, it should be released with the 'free' call when it is
# no longer in use.  It is possible to access every record by iteration
# of calling this function. It is allowed to update or remove records
# whose keys are fetched while the iteration. However, it is not assured
# if updating the database is occurred while the iteration.  Besides,
# the order of this traversal access method is arbitrary, so it is not
# assured that the order of storing matches the one of the traversal
# access.

# """

# adb_iternext2 = cfunc('tcadbiternext2', libtc, tc_char_p,
#                       ('adb', c_void_p, 1))
# adb_iternext2.__doc__ =\
# """Get the next key string of the iterator of an abstract database object.

# adb -- specifies the abstract database object.

# If successful, the return value is the string of the next key, else,
# it is 'NULL'.  'NULL' is returned when no record is to be get out of
# the iterator.

# Because the region of the return value is allocated with the 'malloc'
# call, it should be released with the 'free' call when it is no longer
# in use.  It is possible to access every record by iteration of calling
# this function.  However, it is not assured if updating the database is
# occurred while the iteration.  Besides, the order of this traversal
# access method is arbitrary, so it is not assured that the order of
# storing matches the one of the traversal access.

# """

# # FIX params type
# adb_fwmkeys = cfunc('tcadbfwmkeys', libtc, c_void_p,
#                     ('adb', c_void_p, 1),
#                     ('pbuf', c_void_p, 1),
#                     ('psiz', c_int, 1),
#                     ('max', c_int, 1))
# adb_fwmkeys.__doc__ =\
# """Get forward matching keys in an abstract database object.

# adb  -- specifies the abstract database object.
# pbuf -- specifies the pointer to the region of the prefix.
# psiz -- specifies the size of the region of the prefix.
# max  -- specifies the maximum number of keys to be fetched.  If it is
#         negative, no limit is specified.

# The return value is a list object of the corresponding keys.  This
# function does never fail. It returns an empty list even if no key
# corresponds.

# Because the object of the return value is created with the function
# 'tclistnew', it should be deleted with the function 'tclistdel' when
# it is no longer in use.  Note that this function may be very slow
# because every key in the database is scanned.

# """

# # FIX params type
# adb_fwmkeys2 = cfunc('tcadbfwmkeys2', libtc, c_void_p,
#                      ('adb', c_void_p, 1),
#                      ('pstr', c_char_p, 1),
#                     ('max', c_int, 1))
# adb_fwmkeys2.__doc__ =\
# """Get forward matching string keys in an abstract database object.

# adb  -- specifies the abstract database object.
# pstr -- specifies the string of the prefix.
# max  -- specifies the maximum number of keys to be fetched.  If it is
#         negative, no limit is specified.

# The return value is a list object of the corresponding keys.  This
# function does never fail. It returns an empty list even if no key
# corresponds.

# Because the object of the return value is created with the function
# 'tclistnew', it should be deleted with the function 'tclistdel' when
# it is no longer in use.  Note that this function may be very slow
# because every key in the database is scanned.

# """

# adb_addint = cfunc('tcadbaddint', libtc, c_int,
#                    ('adb', c_void_p, 1),
#                    ('kbuf', c_void_p, 1),
#                    ('ksiz', c_int, 1),
#                    ('num', c_int, 1))
# adb_addint.__doc__ =\
# """Add an integer to a record in an abstract database object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# num  -- specifies the additional value.

# If successful, the return value is the summation value, else, it is
# 'INT_MIN'.

# If the corresponding record exists, the value is treated as an integer
# and is added to.  If no record corresponds, a new record of the
# additional value is stored.

# """

# adb_adddouble = cfunc('tcadbadddouble', libtc, c_double,
#                       ('adb', c_void_p, 1),
#                       ('kbuf', c_void_p, 1),
#                       ('ksiz', c_int, 1),
#                       ('num', c_double, 1))
# adb_adddouble.__doc__ =\
# """Add a real number to a record in an abstract database object.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# num  -- specifies the additional value.

# If successful, the return value is the summation value, else, it is
# Not-a-Number.

# If the corresponding record exists, the value is treated as a real
# number and is added to.  If no record corresponds, a new record of the
# additional value is stored.

# """

# adb_sync = cfunc('tcadbsync', libtc, c_bool,
#                  ('adb', c_void_p, 1))
# adb_sync.__doc__ =\
# """Synchronize updated contents of an abstract database object with
# the file and the device.

# adb -- specifies the abstract database object.

# If successful, the return value is true, else, it is false.

# """

# adb_optimize = cfunc('tcadboptimize', libtc, c_bool,
#                      ('adb', c_void_p, 1),
#                      ('params', c_char_p, 1))
# adb_optimize.__doc__ =\
# """Optimize the storage of an abstract database object.

# adb    -- specifies the abstract database object.
# params -- specifies the string of the tuning parameters, which works
# as with the tuning of parameters the function 'tcadbopen'.  If it is
# 'NULL', it is not used.

# If successful, the return value is true, else, it is false.

# This function is useful to reduce the size of the database storage
# with data fragmentation by successive updating.

# """

# adb_vanish = cfunc('tcadbvanish', libtc, c_bool,
#                    ('adb', c_void_p, 1))
# adb_vanish.__doc__ =\
# """Remove all records of an abstract database object.

# adb -- specifies the abstract database object.

# If successful, the return value is true, else, it is false.

# """

# adb_copy = cfunc('tcadbcopy', libtc, c_bool,
#                  ('adb', c_void_p, 1),
#                  ('path', c_char_p, 1))
# adb_copy.__doc__ =\
# """Copy the database file of an abstract database object.

# adb  -- specifies the abstract database object.
# path -- specifies the path of the destination file.  If it begins with
# '@', the trailing substring is executed as a command line.

# If successful, the return value is true, else, it is false.  False is
# returned if the executed command returns non-zero code.

# The database file is assured to be kept synchronized and not modified
# while the copying or executing operation is in progress.  So, this
# function is useful to create a backup file of the database file.

# """

# adb_tranbegin = cfunc('tcadbtranbegin', libtc, c_bool,
#                       ('adb', c_void_p, 1))
# adb_tranbegin.__doc__ =\
# """Begin the transaction of an abstract database object.

# adb -- specifies the abstract database object.

# If successful, the return value is true, else, it is false.

# The database is locked by the thread while the transaction so that
# only one transaction can be activated with a database object at the
# same time.  Thus, the serializable isolation level is assumed if every
# database operation is performed in the transaction.  All updated
# regions are kept track of by write ahead logging while the
# transaction.  If the database is closed during transaction, the
# transaction is aborted implicitly.

# """

# adb_trancommit = cfunc('tcadbtrancommit', libtc, c_bool,
#                        ('adb', c_void_p, 1))
# adb_trancommit.__doc__ =\
# """Commit the transaction of an abstract database object.

# adb -- specifies the abstract database object.

# If successful, the return value is true, else, it is false.

# Update in the transaction is fixed when it is committed successfully.

# """

# adb_tranabort = cfunc('tcadbtranabort', libtc, c_bool,
#                       ('adb', c_void_p, 1))
# adb_tranabort.__doc__ =\
# """Abort the transaction of an abstract database object.

# adb -- specifies the abstract database object.

# If successful, the return value is true, else, it is false.

# Update in the transaction is discarded when it is aborted.  The state
# of the database is rollbacked to before transaction.

# """

# adb_path = cfunc('tcadbpath', libtc, c_char_p,
#                  ('adb', c_void_p, 1))
# adb_path.__doc__ =\
# """Get the file path of an abstract database object.

# adb -- specifies the abstract database object.

# The return value is the path of the database file or 'NULL' if the
# object does not connect to any database.  "*" stands for on-memory
# hash database.  "+" stands for on-memory tree database.

# """

# adb_rnum = cfunc('tcadbrnum', libtc, c_uint64,
#                  ('adb', c_void_p, 1))
# adb_rnum.__doc__ =\
# """Get the number of records of an abstract database object.

# adb -- specifies the abstract database object.

# The return value is the number of records or 0 if the object does not
# connect to any database instance.

# """

# adb_size = cfunc('tcadbsize', libtc, c_uint64,
#                  ('adb', c_void_p, 1))
# adb_size.__doc__ =\
# """Get the size of the database of an abstract database object.

# adb -- specifies the abstract database object.

# The return value is the size of the database or 0 if the object does
# not connect to any database instance.

# """

# # FIX params type
# adb_misc = cfunc('tcadbmisc', libtc, c_void_p,
#                  ('adb', c_void_p, 1),
#                  ('name', c_char_p, 1),
#                  ('args', c_void_p, 1))
# adb_misc.__doc__ =\
# """Call a versatile function for miscellaneous operations of an
# abstract database object.

# adb  -- specifies the abstract database object.
# name -- specifies the name of the function.  All databases support
#         "put", "out", "get", "putlist", "outlist", and "getlist".
#         "put" is to store a record.  It receives a key and a value,
#         and returns an empty list.  "out" is to remove a record.  It
#         receives a key, and returns an empty list.  "get" is to
#         retrieve a record.  It receives a key, and returns a list of
#         the values.  "putlist" is to store records.  It receives keys
#         and values one after the other, and returns an empty list.
#         "outlist" is to remove records.  It receives keys, and returns
#         an empty list.  "getlist" is to retrieve records.  It receives
#         keys, and returns keys and values of corresponding records one
#         after the other.
# args -- specifies a list object containing arguments.

# If successful, the return value is a list object of the result.
# 'NULL' is returned on failure.

# Because the object of the return value is created with the function
# 'tclistnew', it should be deleted with the function 'tclistdel' when
# it is no longer in use.

# """

# # features for experts

# # FIX params type
# adb_setskel = cfunc('tcadbsetskel', libtc, c_bool,
#                     ('adb', c_void_p, 1),
#                     ('skel', c_void_p, 1))
# adb_setskel.__doc__ =\
# """Set an extra database skeleton to an abstract database object.

# adb  -- specifies the abstract database object.
# skel -- specifies the extra database skeleton.

# If successful, the return value is true, else, it is false.

# """

# adb_setskelmulti = cfunc('tcadbsetskelmulti', libtc, c_bool,
#                          ('adb', c_void_p, 1),
#                          ('num', c_int, 1))
# adb_setskelmulti.__doc__ =\
# """Set the multiple database skeleton to an abstract database object.

# adb -- specifies the abstract database object.
# num -- specifies the number of inner databases.

# If successful, the return value is true, else, it is false.

# """

# adb_omode = cfunc('tcadbomode', libtc, c_int,
#                   ('adb', c_void_p, 1))
# adb_omode.__doc__ =\
# """Get the open mode of an abstract database object.

# adb -- specifies the abstract database object.

# The return value is 'ADBOVOID' for not opened database, 'ADBOMDB' for
# on-memory hash database, 'ADBONDB' for on-memory tree database,
# 'ADBOHDB' for hash database, 'ADBOBDB' for B+ tree database, 'ADBOFDB'
# for fixed-length database, 'ADBOTDB' for table database.

# """

# adb_reveal = cfunc('tcadbreveal', libtc, c_void_p,
#                    ('adb', c_void_p, 1))
# adb_reveal.__doc__ =\
# """Get the concrete database object of an abstract database object.

# adb -- specifies the abstract database object.

# The return value is the concrete database object depend on the open
# mode or 0 if the object does not connect to any database instance.

# """

# # FIX params type
# adb_putproc = cfunc('tcadbputproc', libtc, c_bool,
#                     ('adb', c_void_p, 1),
#                     ('kbuf', c_void_p, 1),
#                     ('ksiz', c_int, 1),
#                     ('vbuf', c_void_p, 1),
#                     ('vsiz', c_int, 1),
#                     ('proc', c_void_p, 1),
#                     ('op', c_void_p, 1)
# adb_putproc.__doc__ =\
# """Store a record into an abstract database object with a duplication
# handler.

# adb  -- specifies the abstract database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# vbuf -- specifies the pointer to the region of the value.
# vsiz -- specifies the size of the region of the value.
# proc -- specifies the pointer to the callback function to process
#         duplication.
# opXX -- specifies an arbitrary pointer to be given as a parameter of
#         the callback function.  If it is not needed, 'NULL' can be
#         specified.

# If successful, the return value is true, else, it is false.

# This function does not work for the table database.

# """

# # FIX params type
# adb_foreach = cfunc('tcadbforeach', libtc, c_bool,
#                     ('adb', c_void_p, 1),
#                     ('iter', c_void_p, 1),
#                     ('op', c_void_p, 1))
# adb_foreach.__doc__ =\
# """Process each record atomically of an abstract database object.

# adb  -- specifies the abstract database object.
# iter -- specifies the pointer to the iterator function called for each
#         record.
# opxx -- specifies an arbitrary pointer to be given as a parameter of
#         the iterator function.  If it is not needed, 'NULL' can be
#         specified.

# If successful, the return value is true, else, it is false.

# """

# # FIX params type
# adb_mapbdb = cfunc('tcadbmapbdb', libtc, c_bool,
#                    ('adb', c_void_p, 1),
#                    ('keys', c_void_p, 1),
#                    ('bdb', c_void_p, 1),
#                    ('op', c_void_p, 1),
#                    ('csiz', c_int64, 1, -1))
# adb_mapbdb.__doc__ =\
# """Map records of an abstract database object into another B+ tree database.

# adb  -- specifies the abstract database object.
# keys -- specifies a list object of the keys of the target records.  If
#         it is 'NULL', every record is processed.
# bdb  -- specifies the B+ tree database object into which records
#         emitted by the mapping function are stored.
# proc -- specifies the pointer to the mapping function called for each
#         record.
# op   -- specifies specifies the pointer to the optional opaque object
#         for the mapping function.
# csiz -- specifies the size of the cache to sort emitted records.  If
#         it is negative, the default size is specified.  The default
#         size is 268435456.

# If successful, the return value is true, else, it is false.

# """

# adb_mapbdbemit = cfunc('tcadbmapbdbemit', libtc, c_bool,
#                        ('map', c_void_p, 1),
#                        ('kbuf', c_void_p, 1),
#                        ('ksiz', c_int, 1),
#                        ('vbuf', c_void_p, 1),
#                        ('vsiz', c_int, 1))

# adb_mapbdbemit.__doc__ =\
# """Emit records generated by the mapping function into the result map.

# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# vbuf -- specifies the pointer to the region of the value.
# vsiz -- specifies the size of the region of the value.

# If successful, the return value is true, else, it is false.

# """


#
# Functions from tchdb.h
#

hdb_errmsg = cfunc('tchdberrmsg', libtc, c_char_p,
                   ('ecode', c_int, 1))
hdb_errmsg.__doc__ =\
"""Get the message string corresponding to an error code.

ecode -- specifies the error code.

The return value is the message string of the error code.

"""

hdb_new = cfunc('tchdbnew', libtc, c_void_p)
hdb_new.__doc__ =\
"""Create a hash database object.

The return value is the new hash database object.

"""

hdb_del = cfunc('tchdbdel', libtc, None,
                ('hdb', c_void_p, 1))
hdb_del.__doc__ =\
"""Delete a hash database object.

hdb -- specifies the hash database object.

If the database is not closed, it is closed implicitly.  Note that the
deleted object and its derivatives can not be used anymore.

"""

hdb_ecode = cfunc('tchdbecode', libtc, c_int,
                  ('hdb', c_void_p, 1))
hdb_ecode.__doc__ =\
"""Get the last happened error code of a hash database object.

hdb -- specifies the hash database object.

The return value is the last happened error code.

The following error codes are defined:
  'ESUCCESS' for success,
  'ETHREAD' for threading error,
  'EINVALID' for invalid operation,
  'ENOFILE' for file not found,
  'ENOPERM' for no permission,
  'EMETA' for invalid meta data,
  'ERHEAD' for invalid record header,
  'EOPEN' for open error,
  'ECLOSE' for close error,
  'ETRUNC' for trunc error,
  'ESYNC' for sync error,
  'ESTAT' for stat error,
  'ESEEK' for seek error,
  'EREAD' for read error,
  'EWRITE' for write error,
  'EMMAP' for mmap error,
  'ELOCK' for lock error,
  'EUNLINK' for unlink error,
  'ERENAME' for rename error,
  'EMKDIR' for mkdir error,
  'ERMDIR' for rmdir error,
  'EKEEP' for existing record,
  'ENOREC' for no record found, and
  'EMISC' for miscellaneous error.

"""

hdb_setmutex = cfunc('tchdbsetmutex', libtc, c_bool,
                     ('hdb', c_void_p, 1))
hdb_setmutex.__doc__ =\
"""Set mutual exclusion control of a hash database object for
threading.

hdb -- specifies the hash database object which is not opened.

If successful, the return value is true, else, it is false.

Note that the mutual exclusion control is needed if the object is
shared by plural threads and this function should be called before the
database is opened.

"""

hdb_tune = cfunc('tchdbtune', libtc, c_bool,
                 ('hdb', c_void_p, 1),
                 ('bnum', c_int64, 1, 0),
                 ('apow', c_int8, 1, -1),
                 ('fpow', c_int8, 1, -1),
                 ('opts', c_uint8, 1))
hdb_tune.__doc__ =\
"""Set the tuning parameters of a hash database object.

hdb  -- specifies the hash database object which is not opened.
bnum -- specifies the number of elements of the bucket array.  If it
        is not more than 0, the default value is specified.  The
        default value is 131071.  Suggested size of the bucket array
        is about from 0.5 to 4 times of the number of all records to
        be stored.
apow -- specifies the size of record alignment by power of 2.  If it
        is negative, the default value is specified.  The default
        value is 4 standing for 2^4=16.
pow  -- specifies the maximum number of elements of the free block pool
        by power of 2. If it is negative, the default value is
        specified.  The default value is 10 standing for 2^10=1024.
opts -- specifies options by bitwise-or:
        'HDBTLARGE' specifies that the size of the database can be
         larger than 2GB by using 64-bit bucket array,
        'HDBTDEFLATE' specifies that each record is compressed with
         Deflate encoding,
        'HDBTBZIP' specifies that each record is compressed with BZIP2
         encoding,
        'HDBTTCBS' specifies that each record is compressed with TCBS
         encoding.

If successful, the return value is true, else, it is false.

Note that the tuning parameters should be set before the database is
opened.

"""

hdb_setcache = cfunc('tchdbsetcache', libtc, c_bool,
                     ('hdb', c_void_p, 1),
                     ('rcnum', c_int32, 1, 0))
hdb_setcache.__doc__ =\
"""Set the caching parameters of a hash database object.

hdb   -- specifies the hash database object which is not opened.
rcnum -- specifies the maximum number of records to be cached.  If it
         is not more than 0, the record cache is disabled.  It is
         disabled by default.

If successful, the return value is true, else, it is false.

Note that the caching parameters should be set before the database is
opened.

"""

hdb_setxmsiz = cfunc('tchdbsetxmsiz', libtc, c_bool,
                     ('hdb', c_void_p, 1),
                     ('xmsiz', c_int64, 1, 0))
hdb_setxmsiz.__doc__ =\
"""Set the size of the extra mapped memory of a hash database object.

hdb   -- specifies the hash database object which is not opened.
xmsiz -- specifies the size of the extra mapped memory.  If it is not
         more than 0, the extra mapped memory is disabled.  The
         default size is 67108864.

If successful, the return value is true, else, it is false.

Note that the mapping parameters should be set before the database is
opened.

"""

hdb_setdfunit = cfunc('tchdbsetdfunit', libtc, c_bool,
                      ('hdb', c_void_p, 1),
                      ('dfunit', c_int32, 1, 0))
hdb_setdfunit.__doc__ =\
"""Set the unit step number of auto defragmentation of a hash database
object.

hdb    -- specifies the hash database object which is not opened.
dfunit -- specifie the unit step number. If it is not more than 0, the
          auto defragmentation is disabled.  It is disabled by
          default.

If successful, the return value is true, else, it is false.

Note that the defragmentation parameters should be set before the
database is opened.

"""

hdb_open = cfunc('tchdbopen', libtc, c_bool,
                 ('hdb', c_void_p, 1),
                 ('path', c_char_p, 1),
                 ('omode', c_int, 1))
hdb_open.__doc__ =\
"""Open a database file and connect a hash database object.

hdb   -- specifies the hash database object which is not opened.
path  -- specifies the path of the database file.
omode -- specifies the connection mode:
         'HDBOWRITER' as a writer,
         'HDBOREADER' as a reader.
         If the mode is 'HDBOWRITER', the following may be added by
         bitwise-or:
         'HDBOCREAT', which means it creates a new database if not exist,
         'HDBOTRUNC', which means it creates a new database regardless if one
          exists,
         'HDBOTSYNC', which means every transaction synchronizes
          updated contents with the device.
         Both of 'HDBOREADER' and 'HDBOWRITER' can be added to by
         bitwise-or:
         'HDBONOLCK', which means it opens the database file without
          file locking, or
         'HDBOLCKNB', which means locking is performed without
          blocking.

If successful, the return value is true, else, it is false.

"""

hdb_close = cfunc('tchdbclose', libtc, c_bool,
                  ('hdb', c_void_p, 1))
hdb_close.__doc__ =\
"""Close a hash database object.

hdb -- specifies the hash database object.

If successful, the return value is true, else, it is false.

Update of a database is assured to be written when the database is
closed.  If a writer opens a database but does not close it
appropriately, the database will be broken.

"""

hdb_put = cfunc('tchdbput', libtc, c_bool,
                ('hdb', c_void_p, 1),
                ('kbuf', c_void_p, 1),
                ('ksiz', c_int, 1),
                ('vbuf', c_void_p, 1),
                ('vsiz', c_int, 1))
hdb_put.__doc__ =\
"""Store a record into a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, it is
overwritten.

"""

hdb_put2 = cfunc('tchdbput2', libtc, c_bool,
                 ('hdb', c_void_p, 1),
                 ('kstr', c_char_p, 1),
                 ('vstr', c_char_p, 1))
hdb_put2.__doc__ =\
"""Store a string record into a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, it is
overwritten.

"""

hdb_putkeep = cfunc('tchdbputkeep', libtc, c_bool,
                    ('hdb', c_void_p, 1),
                    ('kbuf', c_void_p, 1),
                    ('ksiz', c_int, 1),
                    ('vbuf', c_void_p, 1),
                    ('vsiz', c_int, 1))
hdb_putkeep.__doc__ =\
"""Store a new record into a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, this function
has no effect.

"""

hdb_putkeep2 = cfunc('tchdbputkeep2', libtc, c_bool,
                     ('hdb', c_void_p, 1),
                     ('kstr', c_char_p, 1),
                     ('vstr', c_char_p, 1))
hdb_putkeep2.__doc__ =\
"""Store a new string record into a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, this function
has no effect.

"""

hdb_putcat = cfunc('tchdbputcat', libtc, c_bool,
                   ('hdb', c_void_p, 1),
                   ('kbuf', c_void_p, 1),
                   ('ksiz', c_int, 1),
                   ('vbuf', c_void_p, 1),
                   ('vsiz', c_int, 1))
hdb_putcat.__doc__ =\
"""Concatenate a value at the end of the existing record in a hash
database object.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If there is no corresponding record, a new record is created.

"""

hdb_putcat2 = cfunc('tchdbputcat2', libtc, c_bool,
                    ('hdb', c_void_p, 1),
                    ('kstr', c_char_p, 1),
                    ('vstr', c_char_p, 1))
hdb_putcat2.__doc__ =\
"""Concatenate a string value at the end of the existing record in a
hash database object.

hdb  -- specifies the hash database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If there is no corresponding record, a new record is created.

"""

hdb_putasync = cfunc('tchdbputasync', libtc, c_bool,
                     ('hdb', c_void_p, 1),
                     ('kbuf', c_void_p, 1),
                     ('ksiz', c_int, 1),
                     ('vbuf', c_void_p, 1),
                     ('vsiz', c_int, 1))
hdb_putasync.__doc__ =\
"""Store a record into a hash database object in asynchronous fashion.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, it is
overwritten.  Records passed to this function are accumulated into the
inner buffer and wrote into the file at a blast.

"""

hdb_putasync2 = cfunc('tchdbputasync2', libtc, c_bool,
                      ('hdb', c_void_p, 1),
                      ('kstr', c_char_p, 1),
                      ('vstr', c_char_p, 1))
hdb_putasync2.__doc__ =\
"""Store a string record into a hash database object in asynchronous
fashion.

hdb  -- specifies the hash database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, it is
overwritten.  Records passed to this function are accumulated into the
inner buffer and wrote into the file at a blast.

"""

hdb_out = cfunc('tchdbout', libtc, c_bool,
                ('hdb', c_void_p, 1),
                ('kbuf', c_void_p, 1),
                ('ksiz', c_int, 1))
hdb_out.__doc__ =\
"""Remove a record of a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is true, else, it is false.

"""

hdb_out2 = cfunc('tchdbout2', libtc, c_bool,
                 ('hdb', c_void_p, 1),
                 ('kstr', c_char_p, 1))
hdb_out2.__doc__ =\
"""Remove a string record of a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kstr -- specifies the string of the key.

If successful, the return value is true, else, it is false.

"""

hdb_get = cfunc('tchdbget', libtc, tc_void_p,
                ('hdb', c_void_p, 1),
                ('kbuf', c_void_p, 1),
                ('ksiz', c_int, 1),
                ('sp', c_int_p, 2))
hdb_get.errcheck = lambda result, func, arguments : (result, arguments[3])
hdb_get.__doc__ =\
"""Retrieve a record in a hash database object.

hdb  -- specifies the hash database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
value of the corresponding record.  'NULL' is returned if no record
corresponds.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.

"""

hdb_get2 = cfunc('tchdbget2', libtc, tc_char_p,
                 ('hdb', c_void_p, 1),
                 ('kstr', c_char_p, 1))
hdb_get2.__doc__ =\
"""Retrieve a string record in a hash database object.

hdb  -- specifies the hash database object.
kstr -- specifies the string of the key.

If successful, the return value is the string of the value of the
corresponding record.  'NULL' is returned if no record corresponds.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

hdb_get3 = cfunc('tchdbget3', libtc, c_int,
                 ('hdb', c_void_p, 1),
                 ('kbuf', c_void_p, 1),
                 ('ksiz', c_int, 1),
                 ('vbuf', c_void_p, 1),
                 ('max', c_int, 1))
hdb_get3.__doc__ =\
"""Retrieve a record in a hash database object and write the value
into a buffer.

hdb  -- specifies the hash database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the buffer into which the value of
        the corresponding record is written.
max  -- specifies the size of the buffer.

If successful, the return value is the size of the written data, else,
it is -1.  -1 is returned if no record corresponds to the specified
key.

Note that an additional zero code is not appended at the end of the
region of the writing buffer.

"""

hdb_vsiz = cfunc('tchdbvsiz', libtc, c_int,
                 ('hdb', c_void_p, 1),
                 ('kbuf', c_void_p, 1),
                 ('ksiz', c_int, 1))
hdb_vsiz.__doc__ =\
"""Get the size of the value of a record in a hash database object.

hdb  -- specifies the hash database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is the size of the value of the
corresponding record, else, it is -1.

"""

hdb_vsiz2 = cfunc('tchdbvsiz2', libtc, c_int,
                  ('hdb', c_void_p, 1),
                  ('kstr', c_char_p, 1))
hdb_vsiz2.__doc__ =\
"""Get the size of the value of a string record in a hash database
object.

hdb  -- specifies the hash database object.
kstr -- specifies the string of the key.

If successful, the return value is the size of the value of the
corresponding record, else, it is -1.

"""

hdb_iterinit = cfunc('tchdbiterinit', libtc, c_bool,
                     ('hdb', c_void_p, 1))
hdb_iterinit.__doc__ =\
"""Initialize the iterator of a hash database object.

hdb -- specifies the hash database object.

If successful, the return value is true, else, it is false.

The iterator is used in order to access the key of every record stored
in a database.

"""

hdb_iternext = cfunc('tchdbiternext', libtc, tc_void_p,
                     ('hdb', c_void_p, 1),
                     ('sp', c_int_p, 2))
hdb_iternext.errcheck = lambda result, func, arguments : (result, arguments[1])
hdb_iternext.__doc__ =\
"""Get the next key of the iterator of a hash database object.

hdb -- specifies the hash database object.
sp  -- specifies the pointer to the variable into which the size of the
       region of the return value is assigned.

If successful, the return value is the pointer to the region of the
next key, else, it is 'NULL'.  'NULL' is returned when no record is to
be get out of the iterator.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.  It is possible to access every record by iteration
of calling this function.

It is allowed to update or remove records whose keys are fetched while
the iteration.

However, it is not assured if updating the database is occurred while
the iteration.  Besides, the order of this traversal access method is
arbitrary, so it is not assured that the order of storing matches the
one of the traversal access.

"""

hdb_iternext2 = cfunc('tchdbiternext2', libtc, tc_char_p,
                      ('hdb', c_void_p, 1))
hdb_iternext2.__doc__ =\
"""Get the next key string of the iterator of a hash database object.

hdb -- specifies the hash database object.

If successful, the return value is the string of the next key, else,
it is 'NULL'.  'NULL' is returned when no record is to be get out of
the iterator.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.  It is possible to access every record by iteration of calling
this function.

However, it is not assured if updating the database is occurred while
the iteration.  Besides, the order of this traversal access method is
arbitrary, so it is not assured that the order of storing matches the
one of the traversal access.

"""

hdb_iternext3 = cfunc('tchdbiternext3', libtc, c_bool,
                      ('hdb', c_void_p, 1),
                      ('kxstr', TCXSTR_P, 1),
                      ('vxstr', TCXSTR_P, 1))
hdb_iternext3.__doc__ =\
"""Get the next extensible objects of the iterator of a hash database
object.

hdb   -- specifies the hash database object.
kxstr -- specifies the object into which the next key is wrote down.
vxstr -- specifies the object into which the next value is wrote down.

If successful, the return value is true, else, it is false.  False is
returned when no record is to be get out of the iterator.

"""

hdb_fwmkeys = cfunc('tchdbfwmkeys', libtc, TCLIST_P,
                    ('hdb', c_void_p, 1),
                    ('pbuf', c_void_p, 1),
                    ('psiz', c_int, 1),
                    ('max', c_int, 1, -1))
hdb_fwmkeys.__doc__ =\
"""Get forward matching keys in a hash database object.

hdb  -- specifies the hash database object.
pbuf -- specifies the pointer to the region of the prefix.
psiz -- specifies the size of the region of the prefix.
max  -- specifies the maximum number of keys to be fetched.  If it is
        negative, no limit is specified.

The return value is a list object of the corresponding keys.  This
function does never fail.  It returns an empty list even if no key
corresponds.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.  Note that this function may be very slow
because every key in the database is scanned.

"""

hdb_fwmkeys2 = cfunc('tchdbfwmkeys2', libtc, TCLIST_P,
                     ('hdb', c_void_p, 1),
                     ('pstr', c_char_p, 1),
                     ('max', c_int, 1, -1))
hdb_fwmkeys2.__doc__ =\
"""Get forward matching string keys in a hash database object.

hdb  -- specifies the hash database object.
pstr -- specifies the string of the prefix.
max  -- specifies the maximum number of keys to be fetched.  If it is
        negative, no limit is specified.

The return value is a list object of the corresponding keys.  This
function does never fail.  It returns an empty list even if no key
corresponds.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.  Note that this function may be very slow
because every key in the database is scanned.

"""

hdb_addint = cfunc('tchdbaddint', libtc, c_int,
                   ('hdb', c_void_p, 1),
                   ('kbuf', c_void_p, 1),
                   ('ksiz', c_int, 1),
                   ('num', c_int, 1))
hdb_addint.__doc__ =\
"""Add an integer to a record in a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
num  -- specifies the additional value.

If successful, the return value is the summation value, else, it is
'INT_MIN'.

If the corresponding record exists, the value is treated as an integer
and is added to.  If no record corresponds, a new record of the
additional value is stored.

"""

hdb_adddouble = cfunc('tchdbadddouble', libtc, c_double,
                      ('hdb', c_void_p, 1),
                      ('kbuf', c_void_p, 1),
                      ('ksiz', c_int, 1),
                      ('num', c_double, 1))
hdb_adddouble.__doc__ =\
"""Add a real number to a record in a hash database object.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
num  -- specifies the additional value.

If successful, the return value is the summation value, else, it is
Not-a-Number.

If the corresponding record exists, the value is treated as a real
number and is added to.  If no record corresponds, a new record of the
additional value is stored.

"""

hdb_sync = cfunc('tchdbsync', libtc, c_bool,
                 ('hdb', c_void_p, 1))
hdb_sync.__doc__ =\
"""Synchronize updated contents of a hash database object with the
file and the device.

hdb -- specifies the hash database object connected as a writer.

If successful, the return value is true, else, it is false.

This function is useful when another process connects to the same
database file.

"""

hdb_optimize = cfunc('tchdboptimize', libtc, c_bool,
                     ('hdb', c_void_p, 1),
                     ('bnum', c_int64, 1, 0),
                     ('apow', c_int8, 1, -1),
                     ('fpow', c_int8, 1, -1),
                     ('opts', c_uint8, 1,))
hdb_optimize.__doc__ =\
"""Optimize the file of a hash database object.

hdb  -- specifies the hash database object connected as a writer.
bnum -- specifies the number of elements of the bucket array.  If it
        is not more than 0, the default value is specified.  The
        default value is two times of the number of records.
apow -- specifies the size of record alignment by power of 2.  If it
        is negative, the current setting is not changed.
fpow -- specifies the maximum number of elements of the free block
        pool by power of 2.  If it is negative, the current setting is
        not changed.
opts -- specifies options by bitwise-or:
        'HDBTLARGE' specifies that the size of the database can be
         larger than 2GB by using 64-bit bucket array,
        'HDBTDEFLATE' specifies that each record is compressed with
         Deflate encoding,
        'HDBTBZIP' specifies that each record is compressed with BZIP2
         encoding,
        'HDBTTCBS' specifies that each record is compressed with TCBS
         encoding.
        If it is 'UINT8_MAX', the current setting is not changed.

If successful, the return value is true, else, it is false.

This function is useful to reduce the size of the database file with
data fragmentation by successive updating.

"""

hdb_vanish = cfunc('tchdbvanish', libtc, c_bool,
                   ('hdb', c_void_p, 1))
hdb_vanish.__doc__ =\
"""Remove all records of a hash database object.

hdb -- specifies the hash database object connected as a writer.

If successful, the return value is true, else, it is false.

"""

hdb_copy = cfunc('tchdbcopy', libtc, c_bool,
                 ('hdb', c_void_p, 1),
                 ('path', c_char_p, 1))
hdb_copy.__doc__ =\
"""Copy the database file of a hash database object.

hdb  -- specifies the hash database object.
path -- specifies the path of the destination file.  If it begins with
`@', the trailing substring is executed as a command line.

If successful, the return value is true, else, it is false.  False is
returned if the executed command returns non-zero code.

The database file is assured to be kept synchronized and not modified
while the copying or executing operation is in progress.  So, this
function is useful to create a backup file of the database file.

"""

hdb_tranbegin = cfunc('tchdbtranbegin', libtc, c_bool,
                      ('hdb', c_void_p, 1))
hdb_tranbegin.__doc__ =\
"""Begin the transaction of a hash database object.

hdb -- specifies the hash database object connected as a writer.

If successful, the return value is true, else, it is false.

The database is locked by the thread while the transaction so that
only one transaction can be activated with a database object at the
same time.  Thus, the serializable isolation level is assumed if every
database operation is performed in the transaction.  All updated
regions are kept track of by write ahead logging while the
transaction.  If the database is closed during transaction, the
transaction is aborted implicitly.

"""

hdb_trancommit = cfunc('tchdbtrancommit', libtc, c_bool,
                       ('hdb', c_void_p, 1))
hdb_trancommit.__doc__ =\
"""Commit the transaction of a hash database object.

hdb -- specifies the hash database object connected as a writer.

If successful, the return value is true, else, it is false.

Update in the transaction is fixed when it is committed successfully.

"""

hdb_tranabort = cfunc('tchdbtranabort', libtc, c_bool,
                      ('hdb', c_void_p, 1))
hdb_tranabort.__doc__ =\
"""Abort the transaction of a hash database object.

hdb -- specifies the hash database object connected as a writer.

If successful, the return value is true, else, it is false.

Update in the transaction is discarded when it is aborted.  The state
of the database is rollbacked to before transaction.

"""

hdb_path = cfunc('tchdbpath', libtc, c_char_p,
                 ('hdb', c_void_p, 1))
hdb_path.__doc__ =\
"""Get the file path of a hash database object.

hdb -- specifies the hash database object.

The return value is the path of the database file or 'NULL' if the
object does not connect to any database file.

"""

hdb_rnum = cfunc('tchdbrnum', libtc, c_uint64,
                 ('hdb', c_void_p, 1))
hdb_rnum.__doc__ =\
"""Get the number of records of a hash database object.

hdb -- specifies the hash database object.

The return value is the number of records or 0 if the object does not
connect to any database file.

"""

hdb_fsiz = cfunc('tchdbfsiz', libtc, c_uint64,
                 ('hdb', c_void_p, 1))
hdb_fsiz.__doc__ =\
"""Get the size of the database file of a hash database object.

hdb -- specifies the hash database object.

The return value is the size of the database file or 0 if the object
does not connect to any database file.

"""

# features for experts

hdb_setecode = cfunc('tchdbsetecode', libtc, None,
                     ('hdb', c_void_p, 1),
                     ('ecode', c_int, 1),
                     ('filename', c_char_p, 1),
                     ('line', c_int, 1),
                     ('func', c_char_p, 1))
hdb_setecode.__doc__ =\
"""Set the error code of a hash database object.

hdb   -- specifies the hash database object.
ecode -- specifies the error code.
file  -- specifies the file name of the code.
line  -- specifies the line number of the code.
func  -- specifies the function name of the code.

"""

hdb_settype = cfunc('tchdbsettype', libtc, None,
                    ('hdb', c_void_p, 1),
                    ('type', c_uint8, 1))
hdb_settype.__doc__ =\
"""Set the type of a hash database object.

hdb  -- specifies the hash database object.
type -- specifies the database type.

"""

hdb_setdbgfd = cfunc('tchdbsetdbgfd', libtc, None,
                     ('hdb', c_void_p, 1),
                     ('fd', c_int, 1))
hdb_setdbgfd.__doc__ =\
"""Set the file descriptor for debugging output.

hdb -- specifies the hash database object.
fd  -- specifies the file descriptor for debugging output.

"""

hdb_dbgfd = cfunc('tchdbdbgfd', libtc, c_int,
                  ('hdb', c_void_p, 1))
hdb_dbgfd.__doc__ =\
"""Get the file descriptor for debugging output.

hdb -- specifies the hash database object.

The return value is the file descriptor for debugging output.

"""

hdb_hasmutex = cfunc('tchdbhasmutex', libtc, c_bool,
                     ('hdb', c_void_p, 1))
hdb_hasmutex.__doc__ =\
"""Check whether mutual exclusion control is set to a hash database
object.

hdb -- specifies the hash database object.

If mutual exclusion control is set, it is true, else it is false.

"""

hdb_memsync = cfunc('tchdbmemsync', libtc, c_bool,
                    ('hdb', c_void_p, 1),
                    ('phys', c_bool, 1))
hdb_memsync.__doc__ =\
"""Synchronize updating contents on memory of a hash database object.

hdb  -- specifies the hash database object connected as a writer.
phys -- specifies whether to synchronize physically.

If successful, the return value is true, else, it is false.

"""

hdb_cacheclear = cfunc('tchdbcacheclear', libtc, c_bool,
                       ('hdb', c_void_p, 1))
hdb_cacheclear.__doc__ =\
"""Clear the cache of a hash tree database object.

hdb -- specifies the hash tree database object.

If successful, the return value is true, else, it is false.

"""

hdb_bnum = cfunc('tchdbbnum', libtc, c_uint64,
                 ('hdb', c_void_p, 1))
hdb_bnum.__doc__ =\
"""Get the number of elements of the bucket array of a hash database
object.

hdb -- specifies the hash database object.

The return value is the number of elements of the bucket array or 0 if
the object does not connect to any database file.

"""

hdb_align = cfunc('tchdbalign', libtc, c_uint32,
                  ('hdb', c_void_p, 1))
hdb_align.__doc__ =\
"""Get the record alignment of a hash database object.

hdb -- specifies the hash database object.

The return value is the record alignment or 0 if the object does not
connect to any database file.

"""

hdb_fbpmax = cfunc('tchdbfbpmax', libtc, c_uint32,
                   ('hdb', c_void_p, 1))
hdb_fbpmax.__doc__ =\
"""Get the maximum number of the free block pool of a a hash database
object.

hdb -- specifies the hash database object.

The return value is the maximum number of the free block pool or 0 if
the object does not connect to any database file.

"""

hdb_xmsiz = cfunc('tchdbxmsiz', libtc, c_uint64,
                  ('hdb', c_void_p, 1))
hdb_xmsiz.__doc__ =\
"""Get the size of the extra mapped memory of a hash database object.

hdb -- specifies the hash database object.

The return value is the size of the extra mapped memory or 0 if the
object does not connect to any database file.

"""

hdb_inode = cfunc('tchdbinode', libtc, c_uint64,
                  ('hdb', c_void_p, 1))
hdb_inode.__doc__ =\
"""Get the inode number of the database file of a hash database
object.

hdb -- specifies the hash database object.

The return value is the inode number of the database file or 0 if the
object does not connect to any database file.

"""

hdb_mtime = cfunc('tchdbmtime', libtc, c_time_t,
                  ('hdb', c_void_p, 1))
hdb_mtime.__doc__ =\
"""Get the modification time of the database file of a hash database
object.

hdb -- specifies the hash database object.

The return value is the inode number of the database file or 0 if the
object does not connect to any database file.

"""

hdb_omode = cfunc('tchdbomode', libtc, c_int,
                  ('hdb', c_void_p, 1))
hdb_omode.__doc__ =\
"""Get the connection mode of a hash database object.

hdb -- specifies the hash database object.

The return value is the connection mode.

"""

hdb_type = cfunc('tchdbtype', libtc, c_uint8,
                 ('hdb', c_void_p, 1))
hdb_type.__doc__ =\
"""Get the database type of a hash database object.

hdb -- specifies the hash database object.

The return value is the database type.

"""

hdb_flags = cfunc('tchdbflags', libtc, c_uint8,
                  ('hdb', c_void_p, 1))
hdb_flags.__doc__ =\
"""Get the additional flags of a hash database object.

hdb -- specifies the hash database object.

The return value is the additional flags.

"""

hdb_opts = cfunc('tchdbopts', libtc, c_uint8,
                 ('hdb', c_void_p, 1))
hdb_opts.__doc__ =\
"""Get the options of a hash database object.

hdb -- specifies the hash database object.

The return value is the options.

"""

hdb_opaque = cfunc('tchdbopaque', libtc, c_char_p,
                   ('hdb', c_void_p, 1))
hdb_opaque.__doc__ =\
"""Get the pointer to the opaque field of a hash database object.

hdb -- specifies the hash database object.

The return value is the pointer to the opaque field whose size is 128
bytes.

"""

hdb_bnumused = cfunc('tchdbbnumused', libtc, c_uint64,
                     ('hdb', c_void_p, 1))
hdb_bnumused.__doc__ =\
"""Get the number of used elements of the bucket array of a hash
database object.

hdb -- specifies the hash database object.

The return value is the number of used elements of the bucket array or
0 if the object does not connect to any database file.

"""

hdb_setcodecfunc = cfunc('tchdbsetcodecfunc', libtc, c_bool,
                         ('hdb', c_void_p, 1),
                         ('enc', TCCODEC, 1),
                         ('encop', c_void_p, 1),
                         ('dec', TCCODEC, 1),
                         ('decop', c_void_p, 1))
hdb_setcodecfunc.__doc__ =\
"""Set the custom codec functions of a hash database object.

hdb   -- specifies the hash database object.
enc   -- specifies the pointer to the custom encoding function.  It
         receives four parameters.  The first parameter is the pointer
         to the region.  The second parameter is the size of the
         region.  The third parameter is the pointer to the variable
         into which the size of the region of the return value is
         assigned.  The fourth parameter is the pointer to the
         optional opaque object.  It returns the pointer to the result
         object allocated with 'malloc' call if successful, else, it
         returns 'NULL'.
encop -- specifies an arbitrary pointer to be given as a parameter of
         the encoding function.  If it is not needed, 'NULL' can be
         specified.
dec   -- specifies the pointer to the custom decoding function.
decop -- specifies an arbitrary pointer to be given as a parameter of
         the decoding function.  If it is not needed, 'NULL' can be
         specified.

If successful, the return value is true, else, it is false.

Note that the custom codec functions should be set before the database
is opened and should be set every time the database is being opened.

"""

# FIX I think that it is not implementable. Test it.
# hdb_codecfunc = cfunc('tchdbcodecfunc', libtc, None,
#                       ('hdb', c_void_p, 1),
#                       ('ep', TCCODEC_P, 1),
#                       ('eop', c_void_p, 1),
#                       ('dp', TCCODEC_P, 1),
#                       ('dop', c_void_p, 1))
# hdb_codecfunc.__doc__ =\
# """Get the custom codec functions of a hash database object.

# hdb -- specifies the hash database object.
# ep  -- specifies the pointer to a variable into which the pointer to
#        the custom encoding function is assigned
# eop -- specifies the pointer to a variable into which the arbitrary
#        pointer to be given to the encoding function is assigned.
# dp  -- specifies the pointer to a variable into which the pointer to
#        the custom decoding function is assigned
# dop -- specifies the pointer to a variable into which the arbitrary
#        pointer to be given to the decoding function is assigned.

# """

hdb_dfunit = cfunc('tchdbdfunit', libtc, c_uint32,
                   ('hdb', c_void_p, 1))
hdb_dfunit.__doc__ =\
"""Get the unit step number of auto defragmentation of a hash database
object.

hdb -- specifies the hash database object.

The return value is the unit step number of auto defragmentation.

"""

hdb_defrag = cfunc('tchdbdefrag', libtc, c_bool,
                   ('hdb', c_void_p, 1),
                   ('step', c_int64, 1))
hdb_defrag.__doc__ =\
"""Perform dynamic defragmentation of a hash database object.

hdb  -- specifies the hash database object connected as a writer.
step -- specifie the number of steps.  If it is not more than 0, the
        whole file is defragmented gradually without keeping a
        continuous lock.

If successful, the return value is true, else, it is false.

"""

hdb_putproc = cfunc('tchdbputproc', libtc, c_bool,
                    ('hdb', c_void_p, 1),
                    ('kbuf', c_void_p, 1),
                    ('ksiz', c_int, 1),
                    ('vbuf', c_void_p, 1),
                    ('vsiz', c_int, 1),
                    ('proc', TCPDPROC, 1),
                    ('op', c_void_p, 1))
hdb_putproc.__doc__ =\
"""Store a record into a hash database object with a duplication
handler.

hdb  -- specifies the hash database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.  'NULL'
        means that record addition is ommited if there is no
        corresponding record.
vsiz -- specifies the size of the region of the value.
proc -- specifies the pointer to the callback function to process
        duplication.  It receives four parameters.  The first
        parameter is the pointer to the region of the value.  The
        second parameter is the size of the region of the value.  The
        third parameter is the pointer to the variable into which the
        size of the region of the return value is assigned.  The
        fourth parameter is the pointer to the optional opaque object.
        It returns the pointer to the result object allocated with
        'malloc'.  It is released by the caller.  If it is 'NULL', the
        record is not modified.  If it is '(void *)-1', the record is
        removed.
op   -- specifies an arbitrary pointer to be given as a parameter of
        the callback function.  If it is not needed, 'NULL' can be
        specified.

If successful, the return value is true, else, it is false.

Note that the callback function can not perform any database operation
because the function is called in the critical section guarded by the
same locks of database operations.

"""

hdb_getnext = cfunc('tchdbgetnext', libtc, tc_void_p,
                    ('hdb', c_void_p, 1),
                    ('kbuf', c_void_p, 1),
                    ('ksiz', c_int, 1),
                    ('sp', c_int_p, 2))
hdb_getnext.errcheck = lambda result, func, arguments : (result, arguments[2])
hdb_getnext.__doc__ =\
"""Retrieve the next record of a record in a hash database object.

hdb  -- specifies the hash database object.
kbuf -- specifies the pointer to the region of the key.  If it is
        'NULL', the first record is retrieved.
ksiz -- specifies the size of the region of the key.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
key of the next record. 'NULL' is returned if no record corresponds.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.

"""

hdb_getnext2 = cfunc('tchdbgetnext2', libtc, tc_char_p,
                     ('hdb', c_void_p, 1),
                     ('kstr', c_char_p, 1))
hdb_getnext2.__doc__ =\
"""Retrieve the next string record in a hash database object.

hdb  -- specifies the hash database object.
kstr -- specifies the string of the key.  If it is 'NULL', the first
        record is retrieved.

If successful, the return value is the string of the key of the next
record.  'NULL' is returned if no record corresponds.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

# FIX look this 'vbp' char ** param
# hdb_getnext3 = cfunc('tchdbgetnext3', libtc, tc_char_p,
#                      ('hdb', c_void_p, 1),
#                      ('kbuf', c_void_p, 1),
#                      ('ksiz', c_int, 1),
#                      ('sp', c_int_p, 2),
#                      ('vbp', c_char_pp, 2),
#                      ('vsp', c_int_p, 2))
# hdb_getnext3.__doc__ =\
# """Retrieve the key and the value of the next record of a record in a
# hash database object.

# hdb  -- specifies the hash database object.
# kbuf -- specifies the pointer to the region of the key.
# ksiz -- specifies the size of the region of the key.
# sp   -- specifies the pointer to the variable into which the size of
#         the region of the return value is assigned.
# vbp  -- specifies the pointer to the variable into which the pointer
#         to the value is assigned.
# vsp  -- specifies the pointer to the variable into which the size of
#         the value is assigned.

# If successful, the return value is the pointer to the region of the
# key of the next record.

# Because the region of the return value is allocated with the 'malloc'
# call, it should be released with the 'free' call when it is no longer
# in use.  The retion pointed to by 'vbp' should not be released.

# """

hdb_iterinit2 = cfunc('tchdbiterinit2', libtc, c_bool,
                      ('hdb', c_void_p, 1),
                      ('kbuf', c_void_p, 1),
                      ('ksiz', c_int, 1))
hdb_iterinit2.__doc__ =\
"""Move the iterator to the record corresponding a key of a hash
database object.

hdb  -- specifies the hash database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is true, else, it is false.  False is
returned if there is no record corresponding the condition.

"""

hdb_iterinit3 = cfunc('tchdbiterinit3', libtc, c_bool,
                      ('hdb', c_void_p, 1),
                      ('kstr', c_char_p, 1))
hdb_iterinit3.__doc__ =\
"""Move the iterator to the record corresponding a key string of a
hash database object.

hdb  -- specifies the hash database object.
kstr -- specifies the string of the key.

If successful, the return value is true, else, it is false.  False is
returned if there is no record corresponding the condition.

"""

hdb_foreach = cfunc('tchdbforeach', libtc, c_bool,
                    ('hdb', c_void_p, 1),
                    ('iter', TCITER, 1),
                    ('op', c_char_p, 1))
hdb_foreach.__doc__ =\
"""Process each record atomically of a hash database object.

 hdb  -- specifies the hash database object.
 iter -- specifies the pointer to the iterator function called for
         each record.  It receives five parameters.  The first
         parameter is the pointer to the region of the key.  The
         second parameter is the size of the region of the key.  The
         third parameter is the pointer to the region of the value.
         The fourth parameter is the size of the region of the value.
         The fifth parameter is the pointer to the optional opaque
         object.  It returns true to continue iteration or false to
         stop iteration.
op    -- specifies an arbitrary pointer to be given as a parameter of
         the iterator function.  If it is not needed, 'NULL' can be
         specified.

If successful, the return value is true, else, it is false.

Note that the callback function can not perform any database operation
because the function is called in the critical section guarded by the
same locks of database operations.

"""

hdb_tranvoid = cfunc('tchdbtranvoid', libtc, c_bool,
                     ('hdb', c_void_p, 1))
hdb_tranvoid.__doc__ =\
"""Void the transaction of a hash database object.

hdb -- specifies the hash database object connected as a writer.

If successful, the return value is true, else, it is false.

This function should be called only when no update in the transaction.

"""


#
# Functions from tcbdb.h
#

bdb_errmsg = cfunc('tcbdberrmsg', libtc, c_char_p,
                   ('ecode', c_int, 1))
bdb_errmsg.__doc__ =\
"""Get the message string corresponding to an error code.

ecode -- specifies the error code.

The return value is the message string of the error code.

"""

bdb_new = cfunc('tcbdbnew', libtc, c_void_p)
bdb_new.__doc__ =\
"""Create a B+ tree database object.

The return value is the new B+ tree database object.

"""

bdb_del = cfunc('tcbdbdel', libtc, None,
                ('bdb', c_void_p, 1))
bdb_del.__doc__ =\
"""Delete a B+ tree database object.

bdb -- specifies the B+ tree database object.

If the database is not closed, it is closed implicitly.  Note that the
deleted object and its derivatives can not be used anymore.

"""

bdb_ecode = cfunc('tcbdbecode', libtc, c_int,
                  ('bdb', c_void_p, 1))
bdb_ecode.__doc__ =\
"""Get the last happened error code of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the last happened error code.

The following error codes are defined:
  'ESUCCESS' for success,
  'ETHREAD' for threading error,
  'EINVALID' for invalid operation,
  'ENOFILE' for file not found,
  'ENOPERM' for no permission,
  'EMETA' for invalid meta data,
  'ERHEAD' for invalid record header,
  'EOPEN' for open error,
  'ECLOSE' for close error,
  'ETRUNC' for trunc error,
  'ESYNC' for sync error,
  'ESTAT' for stat error,
  'ESEEK' for seek error,
  'EREAD' for read error,
  'EWRITE' for write error,
  'EMMAP' for mmap error,
  'ELOCK' for lock error,
  'EUNLINK' for unlink error,
  'ERENAME' for rename error,
  'EMKDIR' for mkdir error,
  'ERMDIR' for rmdir error,
  'EKEEP' for existing record,
  'ENOREC' for no record found, and
  'EMISC' for miscellaneous error.

"""

bdb_setmutex = cfunc('tcbdbsetmutex', libtc, c_bool,
                     ('bdb', c_void_p, 1))
bdb_setmutex.__doc__ =\
"""Set mutual exclusion control of a B+ tree database object for
threading.

hdb -- specifies the B+ tree database object which is not opened.

If successful, the return value is true, else, it is false.

Note that the mutual exclusion control is needed if the object is
shared by plural threads and this function should be called before the
database is opened.

"""

bdb_setcmpfunc = cfunc('tcbdbsetcmpfunc', libtc, c_bool,
                       ('bdb', c_void_p, 1),
                       ('cmp', TCCMP, 1),
                       ('cmpop', c_void_p, 1))
bdb_setcmpfunc.__doc__=\
"""Set the custom comparison function of a B+ tree database object.

bdb   -- specifies the B+ tree database object which is not opened.
cmp   -- specifies the pointer to the custom comparison function.  It
         receives five parameters.  The first parameter is the pointer
         to the region of one key.  The second parameter is the size
         of the region of one key.  The third parameter is the pointer
         to the region of the other key.  The fourth parameter is the
         size of the region of the other key.  The fifth parameter is
         the pointer to the optional opaque object.  It returns
         positive if the former is big, negative if the latter is big,
         0 if both are equivalent.
cmpop -- specifies an arbitrary pointer to be given as a parameter of
         the comparison function.  If it is not needed, 'NULL' can be
         specified.

If successful, the return value is true, else, it is false.

The default comparison function compares keys of two records by
lexical order.  The functions 'tctccmplexical' (default),
'tctccmpdecimal', 'tctccmpint32', and 'tctccmpint64' are built-in.
Note that the comparison function should be set before the database is
opened.  Moreover, user-defined comparison functions should be set
every time the database is being opened.

"""

bdb_tune = cfunc('tcbdbtune', libtc, c_bool,
                 ('bdb', c_void_p, 1),
                 ('lmemb', c_int32, 1, 0),
                 ('nmemb', c_int32, 1, 0),
                 ('bnum', c_int64, 1, 0),
                 ('apow', c_int8, 1, -1),
                 ('fpow', c_int8, 1, -1),
                 ('opts', c_uint8, 1))
bdb_tune.__doc__ =\
"""Set the tuning parameters of a B+ tree database object.

bdb   -- specifies the B+ tree database object which is not opened.
lmemb -- specifies the number of members in each leaf page.  If it is
         not more than 0, the default value is specified.  The default
         value is 128.
nmemb -- specifies the number of members in each non-leaf page.  If it
         is not more than 0, the default value is specified.  The
         default value is 256.
bnum  -- specifies the number of elements of the bucket array.  If it
         is not more than 0, the default value is specified.  The
         default value is 32749.  Suggested size of the bucket array
         is about from 1 to 4 times of the number of all pages to be
         stored.
apow  -- specifies the size of record alignment by power of 2.  If it
         is negative, the default value is specified.  The default
         value is 8 standing for 2^8=256.
fpow  -- specifies the maximum number of elements of the free block
         pool by power of 2.  If it is negative, the default value is
         specified.  The default value is 10 standing for 2^10=1024.
opts  -- specifies options by bitwise-or:
         'BDBTLARGE' specifies that the size of the database can be
          larger than 2GB by using 64-bit bucket array,
         'BDBTDEFLATE' specifies that each page is compressed with
          Deflate encoding,
         'BDBTBZIP' specifies that each page is compressed with BZIP2
          encoding,
         'BDBTTCBS' specifies that each page is compressed with TCBS
          encoding.

If successful, the return value is true, else, it is false.

Note that the tuning parameters should be set before the database is
opened.

"""

bdb_setcache = cfunc('tcbdbsetcache', libtc, c_bool,
                     ('bdb', c_void_p, 1),
                     ('lcnum', c_int32, 1, 0),
                     ('ncnum', c_int32, 1, 0))
bdb_setcache.__doc__ =\
"""Set the caching parameters of a B+ tree database object.

bdb   -- specifies the B+ tree database object which is not opened.
lcnum -- specifies the maximum number of leaf nodes to be cached.  If
         it is not more than 0, the default value is specified.  The
         default value is 1024.
ncnum -- specifies the maximum number of non-leaf nodes to be cached.
         If it is not more than 0, the default value is specified.
         The default value is 512.

If successful, the return value is true, else, it is false.

Note that the caching parameters should be set before the database is
opened.

"""

bdb_setxmsiz = cfunc('tcbdbsetxmsiz', libtc, c_bool,
                     ('bdb', c_void_p, 1),
                     ('xmsiz', c_int64, 1, 0))
bdb_setxmsiz.__doc__ =\
"""Set the size of the extra mapped memory of a B+ tree database
object.

bdb   -- specifies the B+ tree database object which is not opened.
xmsiz -- specifies the size of the extra mapped memory.  If it is not
         more than 0, the extra mapped memory is disabled.  It is
         disabled by default.

If successful, the return value is true, else, it is false.

Note that the mapping parameters should be set before the database is
opened.

"""

bdb_setdfunit = cfunc('tcbdbsetdfunit', libtc, c_bool,
                      ('bdb', c_void_p, 1),
                      ('dfunit', c_int32, 1, 0))
bdb_setdfunit.__doc__ =\
"""Set the unit step number of auto defragmentation of a B+ tree
database object.

bdb    -- specifies the B+ tree database object which is not opened.
dfunit -- specifie the unit step number. If it is not more than 0, the
          auto defragmentation is disabled.  It is disabled by
          default.

If successful, the return value is true, else, it is false.

Note that the defragmentation parameters should be set before the
database is opened.

"""

bdb_open = cfunc('tcbdbopen', libtc, c_bool,
                 ('bdb', c_void_p, 1),
                 ('path', c_char_p, 1),
                 ('omode', c_int, 1))
bdb_open.__doc__ =\
"""Open a database file and connect a B+ tree database object.

bdb   -- specifies the B+ tree database object which is not opened.
path  -- specifies the path of the database file.
omode -- specifies the connection mode:
         'BDBOWRITER' as a writer,
         'BDBOREADER' as a reader.
         If the mode is 'BDBOWRITER', the following may be added by
         bitwise-or:
         'BDBOCREAT', which means it creates a new database if not exist,
         'BDBOTRUNC', which means it creates a new database regardless if one
          exists,
         'BDBOTSYNC', which means every transaction synchronizes
          updated contents with the device.
         Both of 'BDBOREADER' and 'BDBOWRITER' can be added to by
         bitwise-or:
         'BDBONOLCK', which means it opens the database file without
          file locking, or
         'BDBOLCKNB', which means locking is performed without
          blocking.

If successful, the return value is true, else, it is false.

"""

bdb_close = cfunc('tcbdbclose', libtc, c_bool,
                  ('bdb', c_void_p, 1))
bdb_close.__doc__ =\
"""Close a B+ tree database object.

bdb -- specifies the B+ tree database object.

If successful, the return value is true, else, it is false.

Update of a database is assured to be written when the database is
closed.  If a writer opens a database but does not close it
appropriately, the database will be broken.

"""

bdb_put = cfunc('tcbdbput', libtc, c_bool,
                ('bdb', c_void_p, 1),
                ('kbuf', c_void_p, 1),
                ('ksiz', c_int, 1),
                ('vbuf', c_void_p, 1),
                ('vsiz', c_int, 1))
bdb_put.__doc__ =\
"""Store a record into a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, it is
overwritten.

"""

bdb_put2 = cfunc('tcbdbput2', libtc, c_bool,
                 ('bdb', c_void_p, 1),
                 ('kstr', c_char_p, 1),
                 ('vstr', c_char_p, 1))
bdb_put2.__doc__ =\
"""Store a string record into a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, it is
overwritten.

"""

bdb_putkeep = cfunc('tcbdbputkeep', libtc, c_bool,
                    ('bdb', c_void_p, 1),
                    ('kbuf', c_void_p, 1),
                    ('ksiz', c_int, 1),
                    ('vbuf', c_void_p, 1),
                    ('vsiz', c_int, 1))
bdb_putkeep.__doc__ =\
"""Store a new record into a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, this function
has no effect.

"""

bdb_putkeep2 = cfunc('tcbdbputkeep2', libtc, c_bool,
                     ('bdb', c_void_p, 1),
                     ('kstr', c_char_p, 1),
                     ('vstr', c_char_p, 1))
bdb_putkeep2.__doc__ =\
"""Store a new string record into a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, this function
has no effect.

"""

bdb_putcat = cfunc('tcbdbputcat', libtc, c_bool,
                   ('bdb', c_void_p, 1),
                   ('kbuf', c_void_p, 1),
                   ('ksiz', c_int, 1),
                   ('vbuf', c_void_p, 1),
                   ('vsiz', c_int, 1))
bdb_putcat.__doc__ =\
"""Concatenate a value at the end of the existing record in a B+ tree
database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If there is no corresponding record, a new record is created.

"""

bdb_putcat2 = cfunc('tcbdbputcat2', libtc, c_bool,
                    ('bdb', c_void_p, 1),
                    ('kstr', c_char_p, 1),
                    ('vstr', c_char_p, 1))
bdb_putcat2.__doc__ =\
"""Concatenate a string value at the end of the existing record in a
B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If there is no corresponding record, a new record is created.

"""

bdb_putdup = cfunc('tcbdbputdup', libtc, c_bool,
                   ('bdb', c_void_p, 1),
                   ('kbuf', c_void_p, 1),
                   ('ksiz', c_int, 1),
                   ('vbuf', c_void_p, 1),
                   ('vsiz', c_int, 1))
bdb_putdup.__doc__ =\
"""Store a record into a B+ tree database object with allowing
duplication of keys.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, the new record
is placed after the existing one.

"""

bdb_putdup2 = cfunc('tcbdbputdup2', libtc, c_bool,
                    ('bdb', c_void_p, 1),
                    ('kstr', c_char_p, 1),
                    ('vstr', c_char_p, 1))
bdb_putdup2.__doc__ =\
"""Store a string record into a B+ tree database object with allowing
duplication of keys.

bdb  -- specifies the B+ tree database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, the new record
is placed after the existing one.

"""

bdb_putdup3 = cfunc('tcbdbputdup3', libtc, c_bool,
                    ('bdb', c_void_p, 1),
                    ('kbuf', c_void_p, 1),
                    ('ksiz', c_int, 1),
                    ('vals', TCLIST_P, 1))
bdb_putdup3.__doc__ =\
"""Store records into a B+ tree database object with allowing
duplication of keys.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the common key.
ksiz -- specifies the size of the region of the common key.
vals -- specifies a list object containing values.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, the new records
are placed after the existing one.

"""

bdb_out = cfunc('tcbdbout', libtc, c_bool,
                ('bdb', c_void_p, 1),
                ('kbuf', c_void_p, 1),
                ('ksiz', c_int, 1))
bdb_out.__doc__ =\
"""Remove a record of a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is true, else, it is false.

If the key of duplicated records is specified, the first one is
selected.

"""

bdb_out2 = cfunc('tcbdbout2', libtc, c_bool,
                 ('bdb', c_void_p, 1),
                 ('kstr', c_char_p, 1))
bdb_out2.__doc__ =\
"""Remove a string record of a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kstr -- specifies the string of the key.

If successful, the return value is true, else, it is false.

If the key of duplicated records is specified, the first one is
selected.

"""

bdb_out3 = cfunc('tcbdbout3', libtc, c_bool,
                 ('bdb', c_void_p, 1),
                 ('kbuf', c_void_p, 1),
                 ('ksiz', c_int, 1))
bdb_out3.__doc__ =\
"""Remove records of a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is true, else, it is false.

If the key of duplicated records is specified, all of them are
removed.

"""

bdb_get = cfunc('tcbdbget', libtc, tc_void_p,
                ('bdb', c_void_p, 1),
                ('kbuf', c_void_p, 1),
                ('ksiz', c_int, 1),
                ('sp', c_int_p, 2))
bdb_get.errcheck = lambda result, func, arguments : (result, arguments[3])
bdb_get.__doc__ =\
"""Retrieve a record in a B+ tree database object.

bdb  -- specifies the B+ tree database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
value of the corresponding record.  'NULL' is returned if no record
corresponds.

If the key of duplicated records is specified, the first one is
selected.  Because an additional zero code is appended at the end of
the region of the return value, the return value can be treated as a
character string.  Because the region of the return value is allocated
with the 'malloc' call, it should be released with the 'free' call
when it is no longer in use.

"""

bdb_get2 = cfunc('tcbdbget2', libtc, tc_char_p,
                 ('bdb', c_void_p, 1),
                 ('kstr', c_char_p, 1))
bdb_get2.__doc__ =\
"""Retrieve a string record in a B+ tree database object.

bdb  -- specifies the B+ tree database object.
kstr -- specifies the string of the key.

If successful, the return value is the string of the value of the
corresponding record.  'NULL' is returned if no record corresponds.

If the key of duplicated records is specified, the first one is
selected.  Because the region of the return value is allocated with
the 'malloc' call, it should be released with the 'free' call when it
is no longer in use.

"""

bdb_get3 = cfunc('tcbdbget3', libtc, tc_void_p,
                 ('bdb', c_void_p, 1),
                 ('kbuf', c_void_p, 1),
                 ('ksiz', c_int, 1),
                 ('sp', c_int_p, 2))
bdb_get3.errcheck = lambda result, func, arguments : (result, arguments[3])
bdb_get3.__doc__ =\
"""Retrieve a record in a B+ tree database object as a volatile
buffer.

bdb  -- specifies the B+ tree database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
sp   -- specifies the pointer to the variable into which the size of
        the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
value of the corresponding record.  'NULL' is returned if no record
corresponds.

If the key of duplicated records is specified, the first one is
selected.  Because an additional zero code is appended at the end of
the region of the return value, the return value can be treated as a
character string.  Because the region of the return value is volatile
and it may be spoiled by another operation of the database, the data
should be copied into another involatile buffer immediately.

"""

bdb_get4 = cfunc('tcbdbget4', libtc, TCLIST_P,
                 ('bdb', c_void_p, 1),
                 ('kbuf', c_void_p, 1),
                 ('ksiz', c_int, 1))
bdb_get4.__doc__ =\
"""Retrieve records in a B+ tree database object.

bdb  -- specifies the B+ tree database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is a list object of the values of the
corresponding records.  'NULL' is returned if no record corresponds.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.

"""

bdb_vnum = cfunc('tcbdbvnum', libtc, int,
                 ('bdb', c_void_p, 1),
                 ('kbuf', c_void_p, 1),
                 ('ksiz', c_int, 1))
bdb_vnum.__doc__ =\
"""Get the number of records corresponding a key in a B+ tree database
object.

bdb  -- specifies the B+ tree database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is the number of the corresponding
records, else, it is 0.

"""

bdb_vnum2 = cfunc('tcbdbvnum2', libtc, int,
                  ('bdb', c_void_p, 1),
                  ('kstr', c_char_p, 1))
bdb_vnum2.__doc__ =\
"""Get the number of records corresponding a string key in a B+ tree
database object.

bdb  -- specifies the B+ tree database object.
kstr -- specifies the string of the key.

If successful, the return value is the number of the corresponding
records, else, it is 0.

"""

bdb_vsiz = cfunc('tcbdbvsiz', libtc, c_int,
                 ('bdb', c_void_p, 1),
                 ('kbuf', c_void_p, 1),
                 ('ksiz', c_int, 1))
bdb_vsiz.__doc__ =\
"""Get the size of the value of a record in a B+ tree database object.

bdb  -- specifies the B+ tree database object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is the size of the value of the
corresponding record, else, it is -1.

If the key of duplicated records is specified, the first one is
selected.

"""

bdb_vsiz2 = cfunc('tcbdbvsiz2', libtc, c_int,
                  ('bdb', c_void_p, 1),
                  ('kstr', c_char_p, 1))
bdb_vsiz2.__doc__ =\
"""Get the size of the value of a string record in a B+ tree database
object.

bdb  -- specifies the B+ tree database object.
kstr -- specifies the string of the key.

If successful, the return value is the size of the value of the
corresponding record, else, it is -1.

If the key of duplicated records is specified, the first one is
selected.

"""

bdb_range = cfunc('tcbdbrange', libtc, TCLIST_P,
                  ('bdb', c_void_p, 1),
                  ('bkbuf', c_void_p, 1),
                  ('bksiz', c_int, 1),
                  ('binc', c_bool, 1),
                  ('ekbuf', c_void_p, 1),
                  ('eksiz', c_int, 1),
                  ('einc', c_bool, 1),
                  ('max', c_int, 1))
bdb_range.__doc__ =\
"""Get keys of ranged records in a B+ tree database object.

bdb   -- specifies the B+ tree database object.
bkbuf -- specifies the pointer to the region of the key of the
         beginning border.  If it is 'NULL', the first record is
         specified.
bksiz -- specifies the size of the region of the beginning key.
binc  -- specifies whether the beginning border is inclusive or not.
ekbuf -- specifies the pointer to the region of the key of the ending
         border.  If it is 'NULL', the last record is specified.
eksiz -- specifies the size of the region of the ending key.
einc  -- specifies whether the ending border is inclusive or not.
max   -- specifies the maximum number of keys to be fetched.  If it is
         negative, no limit is specified.

The return value is a list object of the keys of the corresponding
records.  This function does never fail.  It returns an empty list
even if no record corresponds.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.

"""

bdb_range2 = cfunc('tcbdbrange2', libtc, TCLIST_P,
                   ('bdb', c_void_p, 1),
                   ('bkstr', c_char_p, 1),
                   ('binc', c_bool, 1),
                   ('ekstr', c_char_p, 1),
                   ('einc', c_bool, 1),
                   ('max', c_int, 1))
bdb_range2.__doc__ =\
"""Get string keys of ranged records in a B+ tree database object.

bdb   -- specifies the B+ tree database object.
bkstr -- specifies the string of the key of the beginning border.  If
         it is 'NULL', the first record is specified.
binc  -- specifies whether the beginning border is inclusive or not.
ekstr -- specifies the string of the key of the ending border.  If it
         is 'NULL', the last record is specified.
einc  -- specifies whether the ending border is inclusive or not.
max   -- specifies the maximum number of keys to be fetched.  If it is
         negative, no limit is specified.

The return value is a list object of the keys of the corresponding
records.  This function does never fail.  It returns an empty list
even if no record corresponds.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.

"""

bdb_fwmkeys = cfunc('tcbdbfwmkeys', libtc, TCLIST_P,
                    ('bdb', c_void_p, 1),
                    ('pbuf', c_void_p, 1),
                    ('psiz', c_int, 1),
                    ('max', c_int, 1))
bdb_fwmkeys.__doc__ =\
"""Get forward matching keys in a B+ tree database object.

bdb  -- specifies the B+ tree database object.
pbuf -- specifies the pointer to the region of the prefix.
psiz -- specifies the size of the region of the prefix.
max  -- specifies the maximum number of keys to be fetched.  If it is
        negative, no limit is specified.

The return value is a list object of the corresponding keys.  This
function does never fail.  It returns an empty list even if no key
corresponds.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.

"""

bdb_fwmkeys2 = cfunc('tcbdbfwmkeys2', libtc, TCLIST_P,
                     ('bdb', c_void_p, 1),
                     ('pstr', c_char_p, 1),
                     ('max', c_int, 1))
bdb_fwmkeys2.__doc__ =\
"""Get forward matching string keys in a B+ tree database object.

bdb  -- specifies the B+ tree database object.
pstr -- specifies the string of the prefix.
max  -- specifies the maximum number of keys to be fetched.  If it is
        negative, no limit is specified.

The return value is a list object of the corresponding keys.  This
function does never fail.  It returns an empty list even if no key
corresponds.

Because the object of the return value is created with the function
'tclistnew', it should be deleted with the function 'tclistdel' when
it is no longer in use.

"""

bdb_addint = cfunc('tcbdbaddint', libtc, c_int,
                   ('bdb', c_void_p, 1),
                   ('kbuf', c_void_p, 1),
                   ('ksiz', c_int, 1),
                   ('num', c_int, 1))
bdb_addint.__doc__ =\
"""Add an integer to a record in a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
num  -- specifies the additional value.

If successful, the return value is the summation value, else, it is
'INT_MIN'.

If the corresponding record exists, the value is treated as an integer
and is added to.  If no record corresponds, a new record of the
additional value is stored.

"""

bdb_adddouble = cfunc('tcbdbadddouble', libtc, c_double,
                      ('bdb', c_void_p, 1),
                      ('kbuf', c_void_p, 1),
                      ('ksiz', c_int, 1),
                      ('num', c_double, 1))
bdb_adddouble.__doc__ =\
"""Add a real number to a record in a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
num  -- specifies the additional value.

If successful, the return value is the summation value, else, it is
Not-a-Number.

If the corresponding record exists, the value is treated as a real
number and is added to.  If no record corresponds, a new record of the
additional value is stored.

"""

bdb_sync = cfunc('tcbdbsync', libtc, c_bool,
                 ('bdb', c_void_p, 1))
bdb_sync.__doc__ =\
"""Synchronize updated contents of a B+ tree database object with the
file and the device.

bdb -- specifies the B+ tree database object connected as a writer.

If successful, the return value is true, else, it is false.

This function is useful when another process connects to the same
database file.

"""

bdb_optimize = cfunc('tcbdboptimize', libtc, c_bool,
                     ('bdb', c_void_p, 1),
                     ('lmemb', c_int32, 1, 0),
                     ('nmemb', c_int32, 1, 0),
                     ('bnum', c_int64, 1, 0),
                     ('apow', c_int8, 1, -1),
                     ('fpow', c_int8, 1, -1),
                     ('opts', c_uint8, 1))
bdb_optimize.__doc__ =\
"""Optimize the file of a B+ tree database object.

bdb   -- specifies the B+ tree database object connected as a writer.
lmemb -- specifies the number of members in each leaf page.  If it is
         not more than 0, the current setting is not changed.
nmemb -- specifies the number of members in each non-leaf page.  If it
         is not more than 0, the current setting is not changed.
bnum  -- specifies the number of elements of the bucket array.  If it
         is not more than 0, the default value is specified.  The
         default value is two times of the number of pages.
apow  -- specifies the size of record alignment by power of 2.  If it
         is negative, the current setting is not changed.
fpow  -- specifies the maximum number of elements of the free block
         pool by power of 2.  If it is negative, the current setting
         is not changed.
opts  -- specifies options by bitwise-or:
         'BDBTLARGE' specifies that the size of the database can be
          larger than 2GB by using 64-bit bucket array,
         'BDBTDEFLATE' specifies that each record is compressed with
          Deflate encoding,
         'BDBTBZIP' specifies that each page is compressed with BZIP2
          encoding,
         'BDBTTCBS' specifies that each page is compressed with TCBS
          encoding.
         If it is 'UINT8_MAX', the current setting is not changed.

If successful, the return value is true, else, it is false.

This function is useful to reduce the size of the database file with
data fragmentation by successive updating.

"""

bdb_vanish = cfunc('tcbdbvanish', libtc, c_bool,
                   ('bdb', c_void_p, 1))
bdb_vanish.__doc__ =\
"""Remove all records of a B+ tree database object.

bdb -- specifies the B+ tree database object connected as a writer.

If successful, the return value is true, else, it is false.

"""

bdb_copy = cfunc('tcbdbcopy', libtc, c_bool,
                 ('bdb', c_void_p, 1),
                 ('path', c_char_p, 1))
bdb_copy.__doc__ =\
"""Copy the database file of a B+ tree database object.

bdb  -- specifies the B+ tree database object.
path -- specifies the path of the destination file.  If it begins with
        '@', the trailing substring is executed as a command line.

If successful, the return value is true, else, it is false.  False is
returned if the executed command returns non-zero code.

The database file is assured to be kept synchronized and not modified
while the copying or executing operation is in progress.  So, this
function is useful to create a backup file of the database file.

"""

bdb_tranbegin = cfunc('tcbdbtranbegin', libtc, c_bool,
                      ('bdb', c_void_p, 1))
bdb_tranbegin.__doc__ =\
"""Begin the transaction of a B+ tree database object.

bdb -- specifies the B+ tree database object connected as a writer.

If successful, the return value is true, else, it is false.

The database is locked by the thread while the transaction so that
only one transaction can be activated with a database object at the
same time.  Thus, the serializable isolation level is assumed if every
database operation is performed in the transaction.  Because all pages
are cached on memory while the transaction, the amount of referred
records is limited by the memory capacity.  If the database is closed
during transaction, the transaction is aborted implicitly.

"""

bdb_trancommit = cfunc('tcbdbtrancommit', libtc, c_bool,
                       ('bdb', c_void_p, 1))
bdb_trancommit.__doc__ =\
"""Commit the transaction of a B+ tree database object.

bdb -- specifies the B+ tree database object connected as a writer.

If successful, the return value is true, else, it is false.

Update in the transaction is fixed when it is committed successfully.

"""

bdb_tranabort = cfunc('tcbdbtranabort', libtc, c_bool,
                      ('bdb', c_void_p, 1))
bdb_tranabort.__doc__ =\
"""Abort the transaction of a B+ tree database object.

bdb -- specifies the B+ tree database object connected as a writer.

If successful, the return value is true, else, it is false.

Update in the transaction is discarded when it is aborted.  The state
of the database is rollbacked to before transaction.

"""

bdb_path = cfunc('tcbdbpath', libtc, c_char_p,
                 ('bdb', c_void_p, 1))
bdb_path.__doc__ =\
"""Get the file path of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the path of the database file or 'NULL' if the
object does not connect to any database file.

"""

bdb_rnum = cfunc('tcbdbrnum', libtc, c_uint64,
                 ('bdb', c_void_p, 1))
bdb_rnum.__doc__ =\
"""Get the number of records of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the number of records or 0 if the object does not
connect to any database file.

"""

bdb_fsiz = cfunc('tcbdbfsiz', libtc, c_uint64,
                 ('bdb', c_void_p, 1))
bdb_fsiz.__doc__ =\
"""Get the size of the database file of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the size of the database file or 0 if the object
does not connect to any database file.

"""

bdb_curnew = cfunc('tcbdbcurnew', libtc, c_void_p,
                   ('bdb', c_void_p, 1))
bdb_curnew.__doc__ =\
"""Create a cursor object.

bdb -- specifies the B+ tree database object.

The return value is the new cursor object.

Note that the cursor is available only after initialization with the
'tcbdbcurfirst' or the `tcbdbcurjump' functions and so on.  Moreover,
the position of the cursor will be indefinite when the database is
updated after the initialization of the cursor.

"""

bdb_curdel = cfunc('tcbdbcurdel', libtc, None,
                   ('cur', c_void_p, 1))
bdb_curdel.__doc__ =\
"""Delete a cursor object.

cur -- specifies the cursor object.

"""

bdb_curfirst = cfunc('tcbdbcurfirst', libtc, c_bool,
                     ('cur', c_void_p, 1))
bdb_curfirst.__doc__ =\
"""Move a cursor object to the first record.

cur -- specifies the cursor object.

If successful, the return value is true, else, it is false.  False is
returned if there is no record in the database.

"""

bdb_curlast = cfunc('tcbdbcurlast', libtc, c_bool,
                    ('cur', c_void_p, 1))
bdb_curlast.__doc__ =\
"""Move a cursor object to the last record.

cur -- specifies the cursor object.

If successful, the return value is true, else, it is false.  False is
returned if there is no record in the database.

"""

bdb_curjump = cfunc('tcbdbcurjump', libtc, c_bool,
                    ('cur', c_void_p, 1),
                    ('kbuf', c_void_p, 1),
                    ('ksiz', c_int, 1))
bdb_curjump.__doc__ =\
"""Move a cursor object to the front of records corresponding a key.

cur  -- specifies the cursor object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is true, else, it is false.  False is
returned if there is no record corresponding the condition.

The cursor is set to the first record corresponding the key or the
next substitute if completely matching record does not exist.

"""

bdb_curjump2 = cfunc('tcbdbcurjump2', libtc, c_bool,
                     ('cur', c_void_p, 1),
                     ('kstr', c_char_p, 1))
bdb_curjump2.__doc__ =\
"""Move a cursor object to the front of records corresponding a key
string.

cur  -- specifies the cursor object.
kstr -- specifies the string of the key.

If successful, the return value is true, else, it is false.  False is
returned if there is no record corresponding the condition.

The cursor is set to the first record corresponding the key or the
next substitute if completely matching record does not exist.

"""

bdb_curprev = cfunc('tcbdbcurprev', libtc, c_bool,
                    ('cur', c_void_p, 1))
bdb_curprev.__doc__ =\
"""Move a cursor object to the previous record.

cur -- specifies the cursor object.

If successful, the return value is true, else, it is false.  False is
returned if there is no previous record.

"""

bdb_curnext = cfunc('tcbdbcurnext', libtc, c_bool,
                    ('cur', c_void_p, 1))
bdb_curnext.__doc__ =\
"""Move a cursor object to the next record.

cur -- specifies the cursor object.

If successful, the return value is true, else, it is false.  False is
returned if there is no next record.

"""

bdb_curput = cfunc('tcbdbcurput', libtc, c_bool,
                   ('cur', c_void_p, 1),
                   ('vbuf', c_void_p, 1),
                   ('vsiz', c_int, 1),
                   ('cpmode', c_int, 1))
bdb_curput.__doc__ =\
"""Insert a record around a cursor object.

cur    -- pecifies the cursor object of writer connection.
vbuf   -- specifies the pointer to the region of the value.
vsiz   -- specifies the size of the region of the value.
cpmode -- specifies detail adjustment:
          'BDBCPCURRENT', which means that the value of the current
           record is overwritten,
          'BDBCPBEFORE', which means that the new record is inserted
           before the current record,
          'BDBCPAFTER', which means that the new record is inserted
           after the current record.

If successful, the return value is true, else, it is false.  False is
returned when the cursor is at invalid position.

After insertion, the cursor is moved to the inserted record.

"""

bdb_curput2 = cfunc('tcbdbcurput2', libtc, c_bool,
                    ('cur', c_void_p, 1),
                    ('vstr', c_char_p, 1),
                    ('cpmode', c_int, 1))
bdb_curput2.__doc__ =\
"""Insert a string record around a cursor object.

cur    -- specifies the cursor object of writer connection.
vstr   -- specifies the string of the value.
cpmode -- specifies detail adjustment:
          'BDBCPCURRENT', which means that the value of the current
           record is overwritten,
          'BDBCPBEFORE', which means that the new record is inserted
           before the current record,
          'BDBCPAFTER', which means that the new record is inserted
           after the current record.

If successful, the return value is true, else, it is false.  False is
returned when the cursor is at invalid position.

After insertion, the cursor is moved to the inserted record.

"""

bdb_curout = cfunc('tcbdbcurout', libtc, c_bool,
                   ('cur', c_void_p, 1))
bdb_curout.__doc__ =\
"""Remove the record where a cursor object is.

cur -- specifies the cursor object of writer connection.

If successful, the return value is true, else, it is false.  False is
returned when the cursor is at invalid position.

After deletion, the cursor is moved to the next record if possible.

"""

bdb_curkey = cfunc('tcbdbcurkey', libtc, c_void_p,
                   ('cur', c_void_p, 1),
                   ('sp', c_int_p, 2))
bdb_curkey.errcheck = lambda result, func, arguments : (result, arguments[1])
bdb_curkey.__doc__ =\
"""Get the key of the record where the cursor object is.

cur -- specifies the cursor object.
sp  -- specifies the pointer to the variable into which the size of
       the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
key, else, it is 'NULL'.  'NULL' is returned when the cursor is at
invalid position.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.

"""

bdb_curkey2 = cfunc('tcbdbcurkey2', libtc, c_char_p,
                    ('cur', c_void_p, 1))
bdb_curkey2.__doc__ =\
"""Get the key string of the record where the cursor object is.

cur -- specifies the cursor object.

If successful, the return value is the string of the key, else, it is
'NULL'.  'NULL' is returned when the cursor is at invalid position.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

bdb_curkey3 = cfunc('tcbdbcurkey3', libtc, c_void_p,
                    ('cur', c_void_p, 1),
                    ('sp', c_int_p, 2))
bdb_curkey3.errcheck = lambda result, func, arguments : (result, arguments[1])
bdb_curkey3.__doc__ =\
"""Get the key of the record where the cursor object is, as a volatile
buffer.

cur -- specifies the cursor object.
sp  -- specifies the pointer to the variable into which the size of
       the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
key, else, it is 'NULL'.  'NULL' is returned when the cursor is at
invalid position.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is volatile and it may
be spoiled by another operation of the database, the data should be
copied into another involatile buffer immediately.

"""

bdb_curval = cfunc('tcbdbcurval', libtc, c_void_p,
                   ('cur', c_void_p, 1),
                   ('sp', c_int_p, 2))
bdb_curval.errcheck = lambda result, func, arguments : (result, arguments[1])
bdb_curval.__doc__ =\
"""Get the value of the record where the cursor object is.

cur -- specifies the cursor object.
sp  -- specifies the pointer to the variable into which the size of
       the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
value, else, it is 'NULL'.  'NULL' is returned when the cursor is at
invalid position.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is allocated with the
'malloc' call, it should be released with the 'free' call when it is
no longer in use.

"""

bdb_curval2 = cfunc('tcbdbcurval2', libtc, c_char_p,
                    ('cur', c_void_p, 1))
bdb_curval2.__doc__ =\
"""Get the value string of the record where the cursor object is.

cur -- specifies the cursor object.

If successful, the return value is the string of the value, else, it
is 'NULL'.  'NULL' is returned when the cursor is at invalid position.

Because the region of the return value is allocated with the 'malloc'
call, it should be released with the 'free' call when it is no longer
in use.

"""

bdb_curval3 = cfunc('tcbdbcurval3', libtc, c_void_p,
                    ('cur', c_void_p, 1),
                    ('sp', c_int_p, 2))
bdb_curval3.errcheck = lambda result, func, arguments : (result, arguments[1])
bdb_curval3.__doc__ =\
"""Get the value of the record where the cursor object is, as a
volatile buffer.

cur -- specifies the cursor object.
sp  -- specifies the pointer to the variable into which the size of
       the region of the return value is assigned.

If successful, the return value is the pointer to the region of the
value, else, it is 'NULL'.  'NULL' is returned when the cursor is at
invalid position.

Because an additional zero code is appended at the end of the region
of the return value, the return value can be treated as a character
string.  Because the region of the return value is volatile and it may
be spoiled by another operation of the database, the data should be
copied into another involatile buffer immediately.

"""

bdb_currec = cfunc('tcbdbcurrec', libtc, c_bool,
                   ('cur', c_void_p, 1),
                   ('kxstr', TCXSTR_P, 1),
                   ('vxstr', TCXSTR_P, 1))
bdb_currec.__doc__ =\
"""Get the key and the value of the record where the cursor object is.

cur   -- specifies the cursor object.
kxstr -- specifies the object into which the key is wrote down.
vxstr -- specifies the object into which the value is wrote down.

If successful, the return value is true, else, it is false.  False is
returned when the cursor is at invalid position.

"""

# features for experts

bdb_setecode = cfunc('tcbdbsetecode', libtc, None,
                     ('bdb', c_void_p, 1),
                     ('ecode', c_int, 1),
                     ('filename', c_char_p, 1),
                     ('line', c_int, 1),
                     ('func', c_char_p, 1))
bdb_setecode.__doc__ =\
"""Set the error code of a B+ tree database object.

bdb   -- specifies the B+ tree database object.
ecode -- specifies the error code.
file  -- specifies the file name of the code.
line  -- specifies the line number of the code.
func  -- specifies the function name of the code.

"""

bdb_setdbgfd = cfunc('tcbdbsetdbgfd', libtc, None,
                     ('bdb', c_void_p, 1),
                     ('fd', c_int, 1))
bdb_setdbgfd.__doc__ =\
"""Set the file descriptor for debugging output.

bdb -- specifies the B+ tree database object.
fd  -- specifies the file descriptor for debugging output.

"""

bdb_dbgfd = cfunc('tcbdbdbgfd', libtc, c_int,
                  ('bdb', c_void_p, 1))
bdb_dbgfd.__doc__ =\
"""Get the file descriptor for debugging output.

bdb -- specifies the B+ tree database object.

The return value is the file descriptor for debugging output.

"""

bdb_hasmutex = cfunc('tcbdbhasmutex', libtc, c_bool,
                     ('bdb', c_void_p, 1))
bdb_hasmutex.__doc__ =\
"""Check whether mutual exclusion control is set to a B+ tree database
object.

bdb -- specifies the B+ tree database object.

If mutual exclusion control is set, it is true, else it is false.

"""

bdb_memsync = cfunc('tcbdbmemsync', libtc, c_bool,
                    ('bdb', c_void_p, 1),
                    ('phys', c_bool, 1))
bdb_memsync.__doc__ =\
"""Synchronize updating contents on memory of a B+ tree database
object.

bdb  -- specifies the B+ tree database object connected as a writer.
phys -- specifies whether to synchronize physically.

If successful, the return value is true, else, it is false.

"""

bdb_cacheclear = cfunc('tcbdbcacheclear', libtc, c_bool,
                       ('bdb', c_void_p, 1))
bdb_cacheclear.__doc__ =\
"""Clear the cache of a B+ tree database object.

bdb -- specifies the B+ tree database object.

If successful, the return value is true, else, it is false.

"""

bdb_cmpfunc = cfunc('tcbdbcmpfunc', libtc, TCCMP,
                    ('bdb', c_void_p, 1))
bdb_cmpfunc.__doc__ =\
"""Get the comparison function of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the pointer to the comparison function.

"""

bdb_cmpop = cfunc('tcbdbcmpop', libtc, c_void_p,
                  ('bdb', c_void_p, 1))
bdb_cmpop.__doc__ =\
"""Get the opaque object for the comparison function of a B+ tree
database object.

bdb -- specifies the B+ tree database object.

The return value is the opaque object for the comparison function.

"""

bdb_lmemb = cfunc('tcbdblmemb', libtc, c_uint32,
                  ('bdb', c_void_p, 1))
bdb_lmemb.__doc__ =\
"""Get the maximum number of cached leaf nodes of a B+ tree database
object.

bdb -- specifies the B+ tree database object.

The return value is the maximum number of cached leaf nodes.

"""

bdb_lnum = cfunc('tcbdblnum', libtc, c_uint64,
                 ('bdb', c_void_p, 1))
bdb_lnum.__doc__ =\
"""Get the number of the leaf nodes of B+ tree database object.

bdb -- specifies the B+ tree database object.

If successful, the return value is the number of the leaf nodes or 0
if the object does not connect to any database file.

"""

bdb_nnum = cfunc('tcbdbnnum', libtc, c_uint64,
                 ('bdb', c_void_p, 1))
bdb_nnum.__doc__ =\
"""Get the number of the non-leaf nodes of B+ tree database object.

bdb -- specifies the B+ tree database object.

If successful, the return value is the number of the non-leaf nodes or
0 if the object does not connect to any database file.

"""

bdb_bnum = cfunc('tcbdbbnum', libtc, c_uint64,
                 ('bdb', c_void_p, 1))
bdb_bnum.__doc__ =\
"""Get the number of elements of the bucket array of a B+ tree
database object.

bdb -- specifies the B+ tree database object.

The return value is the number of elements of the bucket array or 0 if
the object does not connect to any database file.

"""

bdb_align = cfunc('tcbdbalign', libtc, c_uint32,
                  ('bdb', c_void_p, 1))
bdb_align.__doc__ =\
"""Get the record alignment of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the record alignment or 0 if the object does not
connect to any database file.

"""

bdb_fbpmax = cfunc('tcbdbfbpmax', libtc, c_uint32,
                   ('bdb', c_void_p, 1))
bdb_fbpmax.__doc__ =\
"""Get the maximum number of the free block pool of a B+ tree database
object.

bdb -- specifies the B+ tree database object.

The return value is the maximum number of the free block pool or 0 if
the object does not connect to any database file.

"""

bdb_inode = cfunc('tcbdbinode', libtc, c_uint64,
                  ('bdb', c_void_p, 1))
bdb_inode.__doc__ =\
"""Get the inode number of the database file of a B+ tree database
object.

bdb -- specifies the B+ tree database object.

The return value is the inode number of the database file or 0 if the
object does not connect to any database file.

"""

bdb_mtime = cfunc('tcbdbmtime', libtc, c_time_t,
                  ('bdb', c_void_p, 1))
bdb_mtime.__doc__ =\
"""Get the modification time of the database file of a B+ tree
database object.

bdb -- specifies the B+ tree database object.

The return value is the inode number of the database file or 0 if the
object does not connect to any database file.

"""

bdb_flags = cfunc('tcbdbflags', libtc, c_uint8,
                  ('bdb', c_void_p, 1))
bdb_flags.__doc__ =\
"""Get the additional flags of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the additional flags.

"""

bdb_opts = cfunc('tcbdbopts', libtc, c_uint8,
                 ('bdb', c_void_p, 1))
bdb_opts.__doc__ =\
"""Get the options of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the options.

"""

bdb_opaque = cfunc('tcbdbopaque', libtc, c_char_p,
                   ('bdb', c_void_p, 1))
bdb_opaque.__doc__ =\
"""Get the pointer to the opaque field of a B+ tree database object.

bdb -- specifies the B+ tree database object.

The return value is the pointer to the opaque field whose size is 128
bytes.

"""

bdb_bnumused = cfunc('tcbdbbnumused', libtc, c_uint64,
                     ('bdb', c_void_p, 1))
bdb_bnumused.__doc__ =\
"""Get the number of used elements of the bucket array of a B+ tree
database object.

bdb -- specifies the B+ tree database object.

The return value is the number of used elements of the bucket array or
0 if the object does not connect to any database file.

"""

bdb_setlsmax = cfunc('tcbdbsetlsmax', libtc, c_bool,
                     ('bdb', c_void_p, 1),
                     ('lsmax', c_uint32, 1, 0))
bdb_setlsmax.__doc__ =\
"""Set the maximum size of each leaf node.

bdb   -- specifies the B+ tree database object which is not opened.
lsmax -- specifies the maximum size of each leaf node.  If it is not
         more than 0, the default value is specified.  The default
         value is 16386.

If successful, the return value is true, else, it is false.

Note that the tuning parameters of the database should be set before
the database is opened.

"""

bdb_setcapnum = cfunc('tcbdbsetcapnum', libtc, c_bool,
                      ('bdb', c_void_p, 1),
                      ('capnum', c_uint64, 1))
bdb_setcapnum.__doc__ =\
"""Set the capacity number of records.

bdb    -- specifies the B+ tree database object which is not opened.
capnum -- specifies the capacity number of records.  If it is not more
          than 0, the capacity is unlimited.

If successful, the return value is true, else, it is false.

When the number of records exceeds the capacity, forehand records are
removed implicitly. Note that the tuning parameters of the database
should be set before the database is opened.

"""

bdb_setcodecfunc = cfunc('tcbdbsetcodecfunc', libtc, c_bool,
                         ('bdb', c_void_p, 1),
                         ('enc', TCCODEC, 1),
                         ('encop', c_void_p, 1),
                         ('dec', TCCODEC, 1),
                         ('decop', c_void_p, 1))
bdb_setcodecfunc.__doc__ =\
"""Set the custom codec functions of a B+ tree database object.

bdb   -- specifies the B+ tree database object.
enc   -- specifies the pointer to the custom encoding function.  It
         receives four parameters. The first parameter is the pointer
         to the region.  The second parameter is the size of the
         region.  The third parameter is the pointer to the variable
         into which the size of the region of the return value is
         assigned.  The fourth parameter is the pointer to the
         optional opaque object.  It returns the pointer to the result
         object allocated with 'malloc' call if successful, else, it
         returns 'NULL'.
encop -- specifies an arbitrary pointer to be given as a parameter of
         the encoding function.  If it is not needed, 'NULL' can be
         specified.
dec   -- specifies the pointer to the custom decoding function.
decop -- specifies an arbitrary pointer to be given as a parameter of
         the decoding function.  If it is not needed, 'NULL' can be
         specified.

If successful, the return value is true, else, it is false.

Note that the custom codec functions should be set before the database
is opened and should be set every time the database is being opened.

"""

bdb_dfunit = cfunc('tcbdbdfunit', libtc, c_uint32,
                   ('bdb', c_void_p, 1))
bdb_dfunit.__doc__ =\
"""Get the unit step number of auto defragmentation of a B+ tree
database object.

bdb -- specifies the B+ tree database object.

The return value is the unit step number of auto defragmentation.

"""

bdb_defrag = cfunc('tcbdbdefrag', libtc, c_bool,
                   ('bdb', c_void_p, 1),
                   ('step', c_int64, 1, 0))
bdb_defrag.__doc__ =\
"""Perform dynamic defragmentation of a B+ tree database object.

bdb  -- specifies the B+ tree database object connected as a writer.
step -- specifie the number of steps.  If it is not more than 0, the
        whole file is defragmented gradually without keeping a
        continuous lock.

If successful, the return value is true, else, it is false.

"""

bdb_putdupback = cfunc('tcbdbputdupback', libtc, c_bool,
                       ('bdb', c_void_p, 1),
                       ('kbuf', c_void_p, 1),
                       ('ksiz', c_int, 1),
                       ('vbuf', c_void_p, 1),
                       ('vsiz', c_int, 1))
bdb_putdupback.__doc__ =\
"""Store a new record into a B+ tree database object with backward
duplication.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.
vsiz -- specifies the size of the region of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, the new record
is placed after the existing one.

"""

bdb_putdupback2 = cfunc('tcbdbputdupback2', libtc, c_bool,
                        ('bdb', c_void_p, 1),
                        ('kstr', c_char_p, 1),
                        ('vstr', c_char_p, 1))
bdb_putdupback2.__doc__ =\
"""Store a new string record into a B+ tree database object with
backward duplication.

bdb  -- specifies the B+ tree database object connected as a writer.
kstr -- specifies the string of the key.
vstr -- specifies the string of the value.

If successful, the return value is true, else, it is false.

If a record with the same key exists in the database, the new record
is placed after the existing one.

"""

bdb_putproc = cfunc('tcbdbputproc', libtc, c_bool,
                    ('bdb', c_void_p, 1),
                    ('kbuf', c_void_p, 1),
                    ('ksiz', c_int, 1),
                    ('vbuf', c_void_p, 1),
                    ('vsiz', c_int, 1),
                    ('proc', TCPDPROC, 1),
                    ('op', c_void_p, 1))
bdb_putproc.__doc__ =\
"""Store a record into a B+ tree database object with a duplication
handler.

bdb  -- specifies the B+ tree database object connected as a writer.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.
vbuf -- specifies the pointer to the region of the value.  'NULL'
        means that record addition is ommited if there is no
        corresponding record.
vsiz -- specifies the size of the region of the value.
proc -- specifies the pointer to the callback function to process
        duplication.  It receives four parameters.  The first
        parameter is the pointer to the region of the value.  The
        second parameter is the size of the region of the value.  The
        third parameter is the pointer to the variable into which the
        size of the region of the return value is assigned.  The
        fourth parameter is the pointer to the optional opaque object.
        It returns the pointer to the result object allocated with
        'malloc'.  It is released by the caller.  If it is 'NULL', the
        record is not modified.  If it is '(void *)-1', the record is
        removed.
op   -- specifies an arbitrary pointer to be given as a parameter of
        the callback function.  If it is not needed, 'NULL' can be
        specified.

If successful, the return value is true, else, it is false.

Note that the callback function can not perform any database operation
because the function is called in the critical section guarded by the
same locks of database operations.

"""

bdb_curjumpback = cfunc('tcbdbcurjumpback', libtc, c_bool,
                        ('cur', c_void_p, 1),
                        ('kbuf', c_void_p, 1),
                        ('ksiz', c_int, 1))
bdb_curjumpback.__doc__ =\
"""Move a cursor object to the rear of records corresponding a key.

cur  -- specifies the cursor object.
kbuf -- specifies the pointer to the region of the key.
ksiz -- specifies the size of the region of the key.

If successful, the return value is true, else, it is false.  False is
returned if there is no record corresponding the condition.

The cursor is set to the last record corresponding the key or the
previous substitute if completely matching record does not exist.

"""

bdb_curjumpback2 = cfunc('tcbdbcurjumpback2', libtc, c_bool,
                         ('cur', c_void_p, 1),
                         ('kstr', c_char_p, 1))
bdb_curjumpback2.__doc__ =\
"""Move a cursor object to the rear of records corresponding a key
string.

cur  -- specifies the cursor object.
kstr -- specifies the string of the key.

If successful, the return value is true, else, it is false.  False is
returned if there is no record corresponding the condition.

The cursor is set to the last record corresponding the key or the
previous substitute if completely matching record does not exist.

"""

bdb_foreach = cfunc('tcbdbforeach', libtc, c_bool,
                    ('bdb', c_void_p, 1),
                    ('iter', TCITER, 1),
                    ('op', c_char_p, 1))
bdb_foreach.__doc__ =\
"""Process each record atomically of a B+ tree database object.

bdb  -- specifies the B+ tree database object.
iter -- specifies the pointer to the iterator function called for each
        record.  It receives five parameters.  The first parameter is
        the pointer to the region of the key.  The second parameter is
        the size of the region of the key.  The third parameter is the
        pointer to the region of the value.  The fourth parameter is
        the size of the region of the value.  The fifth parameter is
        the pointer to the optional opaque object.  It returns true to
        continue iteration or false to stop iteration.
op   -- specifies an arbitrary pointer to be given as a parameter of
        the iterator function.  If it is not needed, 'NULL' can be
        specified.

If successful, the return value is true, else, it is false.

Note that the callback function can not perform any database operation
because the function is called in the critical section guarded by the
same locks of database operations.

"""
