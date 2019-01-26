#
# morestd: More standard libraries for Python
#
# Copyright 2010-2019 Ferry Boender, released under the MIT license
#

import os
import pwd
import ipaddress

import morestd


# Enum of all TCP port states (from tcp_states.h)
tcp_port_states = {
    1: "ESTABLISHED",
    2: "SYN_SENT",
    3: "SYN_RECV",
    4: "FIN_WAIT1",
    5: "FIN_WAIT2",
    6: "TIME_WAIT",
    7: "CLOSE",
    8: "CLOSE_WAIT",
    9: "LAST_ACK",
    10: "LISTEN",
    11: "CLOSING",
}


def _parse_proc_net_v4(line, proto):
    """
    Parse an IPv4 (tcp / udp) line from /proc/net/ to a dict.
    """
    parts = line.strip().split()
    local_addr_hex, local_port_hex = parts[1].split(':')
    remote_addr_hex, remote_port_hex = parts[2].split(':')
    local_addr_int = morestd.net.ip4_hex_to_int(local_addr_hex)
    local_addr = ipaddress.ip_address(local_addr_int)
    local_port = int(local_port_hex, 16)
    remote_addr_int = morestd.net.ip4_hex_to_int(remote_addr_hex)
    remote_addr = ipaddress.ip_address(remote_addr_int)
    remote_port = int(remote_port_hex, 16)
    state = int(parts[3], 16)
    inode = int(parts[9])

    port = {
        "local_address": local_addr,
        "local_port": local_port,
        "remote_address": remote_addr,
        "remote_port": remote_port,
        "uid": int(parts[7]),
        "user": pwd.getpwuid(int(parts[7])).pw_name,
        "pid": _socket_inode_to_pid(inode),
    }

    # UDP has no state
    if proto.startswith("tcp"):
        port["state"] = tcp_port_states[state]
    else:
        port["state"] = "UNCONN"

    return port


def _socket_inode_to_pid(inode):
    """
    Go through all PID dirs in /proc and see if they have a file descriptor
    open to socket `inode`. Requires root permissions to work properly.
    """
    if inode == 0:
        return None

    for fname in os.listdir('/proc/'):
        try:
            pid = int(fname)
        except ValueError:
            # Filename is not int, so not a pid
            continue

        path_fd = os.path.join("/proc", str(pid), "fd")
        try:
            for fd in os.listdir(path_fd):
                fd_link = os.readlink(os.path.join(path_fd, fd))
                if fd_link.startswith("socket"):
                    fd_inode = int(fd_link[8:-1])
                else:
                    continue

                if fd_inode == inode:
                    return pid
        except OSError:
            # Probably no permissions
            pass

    return None


def net_open_ports():
    """
    """
    ports = []

    for proto in ["tcp", "udp"]:
        path = os.path.join('/proc/net/', proto)
        with open(path, 'r') as f:
            for line in f.readlines()[1:]:
                port = _parse_proc_net_v4(line, proto)
                port['proto'] = '{}4'.format(proto)
                ports.append(port)

    return ports


if __name__ == '__main__':
    import doctest
    doctest.testmod()
