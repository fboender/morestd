#
# morestd: More standard libraries for Python
#
# Copyright 2010-2018 Ferry Boender, released under the MIT license
#

import socket


def fqdn():
    """
    Return Fully qualified domain name for this machine.

    Many machines have their fully qualified domain name (fqdn) incorrectly
    configured. For example, the hostname may contain the fqdn while the
    domainname part is empty. This function attempts to return a correct FQDN.
    """
    fqdn = socket.gethostname()
    if '.' not in fqdn:
        fqdn = socket.getfqdn()
    return fqdn


if __name__ == '__main__':
    import doctest
    doctest.testmod()
