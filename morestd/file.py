#
# morestd: More standard libraries for Python
#
# Copyright 2010-2019 Ferry Boender, released under the MIT license
#

import re
import mmap


def egrep(path, regex):
    """
    Grep for regex `regex` in file `path`. Should be reasonably fast. `regex`
    may be both an instance of a `re.compile()` regex, or a string. Files are
    opened in binary mode, so the regexp must also be binary (e.g.
    `b".*foo.*"`)

    Returns match objects.
    """
    with open(path, "r") as f:
        if hasattr(regex, 'search'):
            return regex.search(mmap.mmap(f.fileno(),
                                          0,
                                          access=mmap.ACCESS_READ))
        else:
            return re.search(regex, mmap.mmap(f.fileno(),
                                              0,
                                              access=mmap.ACCESS_READ))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
