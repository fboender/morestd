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


def hex_ip4(ip):
    """
    Convert a hex IPv4 as found in /proc/net/tcp to a dotted IP.

    >>> hex_ip4("0E01A8C0")
    '192.168.1.14'
    """
    return(".".join([
        str(int(ip[6:8], 16)),
        str(int(ip[4:6], 16)),
        str(int(ip[2:4], 16)),
        str(int(ip[0:2], 16)),
    ]))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
