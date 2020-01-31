#
# morestd: More standard libraries for Python
#
# Copyright 2010-2019 Ferry Boender, released under the MIT license
#

import os
import errno


def is_pid_running(pid):
    """
    Test if a process is running with PID `pid`. Returns True or False.

    >>> is_pid_running(1)
    True
    >>> is_pid_running(32769)  # max_pid + 1
    False
    """
    try:
        os.kill(pid, 0)
        return True
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
        elif err.errno == errno.EPERM:
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise


if __name__ == '__main__':
    import doctest
    doctest.testmod()
