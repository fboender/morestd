#
# morestd: More standard libraries for Python
#
# Copyright 2010-2018 Ferry Boender, released under the MIT license
#


def to_bool(s):
    """
    Convert string `s` into a boolean.

    `s` can be 'true', 'True', 1, 'false', 'False', 0.
    """
    if isinstance(s, bool):
        return s
    elif s.lower() in ['true', '1']:
        return True
    elif s.lower() in ['false', '0']:
        return False
    else:
        raise ValueError("Can't cast '%s' to bool" % (s))
