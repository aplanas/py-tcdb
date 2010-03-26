import cPickle
import ctypes

import tc


def get_type(obj, as_raw):
    """Get the type of an object if as_raw is True."""
    type_ = None
    if isinstance(obj, int) and as_raw:
        type_ = int
    elif isinstance(obj, float) and as_raw:
        type_ = float
    elif isinstance(obj, str) and as_raw:
        type_ = str
    elif isinstance(obj, unicode) and as_raw:
        type_ = unicode
    return type_


def serialize(obj, as_raw=False):
    """Serialize an object, ready to be used in put / get."""
    c_obj = None
    c_obj_len = 0
    if isinstance(obj, int) and as_raw:
        c_obj = tc.c_int_p(ctypes.c_int(obj))
        c_obj_len = ctypes.sizeof(ctypes.c_int(obj))
    elif isinstance(obj, float) and as_raw:
        c_obj = tc.c_double_p(ctypes.c_double(obj))
        c_obj_len = ctypes.sizeof(ctypes.c_double(obj))
    elif isinstance(obj, str) and as_raw:
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)       # We don't need to store the last \x00
    elif isinstance(obj, unicode) and as_raw:
        c_obj = ctypes.c_wchar_p(obj)
        c_obj_len = len(obj) << 2  # We don't need to store the last \x00
    else:
        obj = cPickle.dumps(obj, cPickle.HIGHEST_PROTOCOL)
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)    # We don't need to store the last \x00
    return (c_obj, c_obj_len)


def deserialize(c_obj, c_obj_len, as_type=None):
    """Deserialize an object used in put / get."""
    obj = None
    if as_type is str:
        obj = ctypes.string_at(c_obj, c_obj_len)
    elif as_type is unicode:
        obj = ctypes.wstring_at(c_obj, c_obj_len.value >> 2)
    elif as_type is int:
        obj = ctypes.cast(c_obj, tc.c_int_p).contents.value
    elif as_type is float:
        obj = ctypes.cast(c_obj, tc.c_double_p).contents.value
    else:
        obj = cPickle.loads(ctypes.string_at(c_obj, c_obj_len))
    return obj


def serialize_tclist(objs, as_raw=False):
    """Serialize an array of objects, ready to be used in putdup."""
    tclist_vals = tc.tclistnew2(len(objs))
    for obj in objs:
        (c_obj, c_obj_len) = serialize(obj, as_raw)
        tc.tclistpush(tclist_vals, c_obj, c_obj_len)
    return tclist_vals


def deserialize_tclist(tclist_objs, as_type=None):
    """Deserialize an array of objects used in getdup."""
    objs = []
    for index in range(tc.tclistnum(tclist_objs)):
        (c_obj, c_obj_len) = tc.tclistval(tclist_objs, index)
        objs.append(deserialize(c_obj, c_obj_len, as_type))
    return objs


def deserialize_xstr(xstr, as_type=None):
    """Deserialize an object, in format xstr, used in put / get."""
    (c_obj, c_obj_len) = (tc.tcxstrptr(xstr), tc.tcxstrsize(xstr))
    obj = deserialize(c_obj, c_obj_len, as_type)
    return obj


def deserialize_tcuint64(tcuint64, size):
    """Deserialize an array of c_uint64_p to an array of integers."""
    ptr = ctypes.cast(tcuint64, tc.c_uint64_p)
    ints = [ptr[i] for i in range(size.value)]
    return ints
