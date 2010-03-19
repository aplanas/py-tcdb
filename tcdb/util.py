import cPickle
import ctypes

import tc


def serialize_obj(obj):
    """Serialize an object, ready to be used in put / get."""
    # Serialize an object using a simple rule:
    #
    #   -- if the object is a string do nothing
    #      else, pickle it.
    #
    # We can use this method to serialize all the keys and the put /
    # get (more generic) values.  This means that we can maximize the
    # flexibility of this Python module, and possibility the reuse of
    # stored data with other languages, specifically in C (using
    # put_xxx)
    #
    # We serialize all keys with this method, but we use two method to
    # serialize values.  This one can serialize the generic pair put /
    # get, but we need a different serializer because of add_xxx
    # functions, that works on native integer and double C datatype.

    c_obj = None
    c_obj_len = 0
    if isinstance(obj, str):
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)    # We don't need to store the last \x00
    elif obj:
        obj = cPickle.dumps(obj, cPickle.HIGHEST_PROTOCOL)
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)    # We don't need to store the last \x00
    return (c_obj, c_obj_len)


def deserialize_obj(c_obj, c_obj_len):
    """Deserialize an object used in put / get."""
    try:
        obj = ctypes.string_at(c_obj, c_obj_len)
        obj = cPickle.loads(obj)
    except cPickle.UnpicklingError:
        pass
    return obj


def serialize_value(obj):
    """Serialize an object, ready to be used as a value in put_xxx /
    get_xxx."""
    c_obj = None
    c_obj_len = 0
    if isinstance(obj, int):
        c_obj = tc.c_int_p(ctypes.c_int(obj))
        c_obj_len = ctypes.sizeof(ctypes.c_int(obj))
    elif isinstance(obj, float):
        c_obj = tc.c_double_p(ctypes.c_double(obj))
        c_obj_len = ctypes.sizeof(ctypes.c_double(obj))
    elif isinstance(obj, str):
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)       # We don't need to store the last \x00
    elif isinstance(obj, unicode):
        c_obj = ctypes.c_wchar_p(obj)
        c_obj_len = len(obj) << 2  # We don't need to store the last \x00
    elif obj:
        obj = cPickle.dumps(obj, cPickle.HIGHEST_PROTOCOL)
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)       # We don't need to store the last \x00
    return (c_obj, c_obj_len)


def deserialize_str(c_str, c_str_len):
    """Deserialize a string used in put_str / get_str."""
    return ctypes.string_at(c_str, c_str_len)


def deserialize_unicode(c_unicode, c_unicode_len):
    """Deserialize an unicode string used in put_unicode /
    get_unicode."""
    return ctypes.wstring_at(c_unicode, c_unicode_len.value >> 2)


def deserialize_int(c_int, c_int_len):
    """Deserialize an integer used in put_int / get_int."""
    return ctypes.cast(c_int, tc.c_int_p).contents.value


def deserialize_float(c_float, c_float_len):
    """Deserialize a float used in put_float / get_float."""
    return ctypes.cast(c_float, tc.c_double_p).contents.value


def deserialize_xstr_obj(xstr):
    """Deserialize an object, in format xstr, used in put / get."""
    try:
        obj = ctypes.string_at(tc.tcxstrptr(xstr), tc.tcxstrsize(xstr))
        obj = cPickle.loads(obj)
    except cPickle.UnpicklingError:
        pass
    return obj


def serialize_objs(objs):
    """Serialize an array of objects, ready to be used in putdup_iter."""
    tclist_vals = tc.tclistnew2(len(objs))
    for obj in objs:
        (c_obj, c_obj_len) = serialize_obj(obj)
        tc.tclistpush(tclist_vals, c_obj, c_obj_len)
    return tclist_vals


def deserialize_objs(tclist_objs):
    """Deserialize an array of objects used in putdup_iter."""
    objs = []
    for index in range(tc.tclistnum(tclist_objs)):
        (c_obj, c_obj_len) = tc.tclistval(tclist_objs, index)
        objs.append(deserialize_obj(c_obj, c_obj_len))
    return objs


def serialize_values(objs):
    """Serialize an array of objects, ready to be used in
    putdup_iter_xxx."""
    tclist_vals = tc.tclistnew2(len(objs))
    for obj in objs:
        (c_obj, c_obj_len) = serialize_value(obj)
        tc.tclistpush(tclist_vals, c_obj, c_obj_len)
    return tclist_vals


def deserialize_strs(tclist_strs):
    """Deserialize an array of strings used in getdup_str."""
    objs = []
    for index in range(tc.tclistnum(tclist_strs)):
        (c_str, c_str_len) = tc.tclistval(tclist_strs, index)
        objs.append(deserialize_str(c_str, c_str_len))
    return objs


def deserialize_unicodes(tclist_unicodes):
    """Deserialize an array of unicode strings used in
    getdup_unicode."""
    objs = []
    for index in range(tc.tclistnum(tclist_unicodes)):
        (c_unicode, c_unicode_len) = tc.tclistval(tclist_unicodes, index)
        objs.append(deserialize_unicode(c_unicode, c_unicode_len))
    return objs


def deserialize_ints(tclist_ints):
    """Deserialize an array of integers used in getdup_int."""
    objs = []
    for index in range(tc.tclistnum(tclist_ints)):
        (c_int, c_int_len) = tc.tclistval(tclist_ints, index)
        objs.append(deserialize_int(c_int, c_int_len))
    return objs


def deserialize_floats(tclist_floats):
    """Deserialize an array of floats used in getdup_float."""
    objs = []
    for index in range(tc.tclistnum(tclist_floats)):
        (c_float, c_float_len) = tc.tclistval(tclist_floats, index)
        objs.append(deserialize_float(c_float, c_float_len))
    return objs
