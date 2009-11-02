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
    # We serialize all keys with this method, but we user two method
    # to serialize values.  This one can serialize the generic pair
    # put /get, but we need a different serializer because of add_xxx
    # functions, that works on native integer and double C datatype.

    if isinstance(obj, str):
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)    # We don't need to store the last \x00
    else:
        obj = cPickle.dumps(obj, cPickle.HIGHEST_PROTOCOL)
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)    # We don't need to store the last \x00
    return (c_obj, c_obj_len)


def deserialize_obj(c_obj, c_obj_len):
    """Deserialize an object used in put / get."""
    try:
        obj = ctypes.string_at(c_obj.value, c_obj_len)
        obj = cPickle.loads(obj)
    except cPickle.UnpicklingError:
        pass
    return obj


def deserialize_str(c_str, c_str_len):
    """Deserialize a string used in put_str / get_str."""
    return ctypes.string_at(c_str.value, c_str_len)


def deserialize_int(c_int, c_int_len):
    """Deserialize an integer used in put_int / get_int."""
    return ctypes.cast(c_int, tc.c_int_p).contents.value


def deserialize_float(c_float, c_float_len):
    """Deserialize a float used in put_float / get_float."""
    return ctypes.cast(c_float, tc.c_double_p).contents.value


def deserialize_xstr_obj(xstr):
    """Deserialize an object, in format xstr, used in put / get."""
    try:
        obj = ctypes.string_at(xstr.contents.ptr, xstr.contents.size)
        obj = cPickle.loads(obj)
    except cPickle.UnpicklingError:
        pass
    return obj


def serialize_value(obj):
    """Serialize an object, ready to be used as a value in put_xxx /
    get_xxx."""
    if isinstance(obj, int):
        c_obj = tc.c_int_p(ctypes.c_int(obj))
        c_obj_len = ctypes.sizeof(ctypes.c_int(obj))
    elif isinstance(obj, float):
        c_obj = tc.c_double_p(ctypes.c_double(obj))
        c_obj_len = ctypes.sizeof(ctypes.c_double(obj))
    elif isinstance(obj, str):
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)    # We don't need to store the last \x00
    else:
        obj = cPickle.dumps(obj, cPickle.HIGHEST_PROTOCOL)
        c_obj = ctypes.c_char_p(obj)
        c_obj_len = len(obj)    # We don't need to store the last \x00
    return (c_obj, c_obj_len)
