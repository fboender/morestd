#
# morestd: More standard libraries for Python
#
# Copyright 2010-2018 Ferry Boender, released under the MIT license
#

import os
import stat
import fnmatch

file_types = {
    4096: "fifo",
    8192: "char",
    16384: "dir",
    24576: "block",
    32768: "file",
    40960: "link",
    49152: "socket",
}


def find(root_dir, name=None, path=None, ftype=None, min_size=None,
         max_size=None, uid=None, gid=None, depth=None, one_fs=True,
         absolute=False, on_error=None):
    """
    Recursively find files and directories matching certain criteria.

    Basically the unix `find` command, but for Python. For each file that
    matches the criteria, a dict is yielded containing some basic information
    about that file. Example:

        {
            'filename': 'passwd',
            'dir': '/etc/',
            'path': '/etc/passwd',
            'type': 'file',
            'size': 2790,
            'uid': 0,
            'gid': 0
        }

    `root_dir` is the starting directory from which to find files.

    If `name` is provided, only files matching the given shell globbing pattern
    will be included. If `path` is provided, the same is done but for the
    file's entire path. `ftype` can be used to limit the files to a certain
    type. Valid values are 'fifo', 'char', 'dir', 'block', 'file', 'link',
    'socket'. `min_size` and `max_size` limit files to those who's size is >=
    `min_size` and <= `max_size` respectively. `uid` and `gid` limit files to
    those that match the given owner user and group id.

    `depth` determines how deep to scan. E.g. `depth=2` will only scan two
    directories deep (relative to `root_dir`). `one_fs` limits the scan to the
    same file system / device that `root_fs` is on.

    If `absolute` is set to True, `dirs` and `path` will be made absolute
    (relative to the `/` directory).

    `on_error` is a callable which will be called when an error occurs. It
    should receive one parameter, which is the full path to the file that
    caused the problem. If `on_error` is None (default), an exception is raised
    instead.
    """
    # Figure out device which root_dir is on, so we can honor `one_fs`
    root_stat = os.stat(root_dir)
    root_dev = root_stat.st_dev

    # Stack with dirs we still need to visit
    stack = []
    stack.append(root_dir)

    while stack:
        cur_dir = stack.pop(0)
        if absolute is True:
            cur_dir = os.path.abspath(cur_dir)

        try:
            for fname in os.listdir(cur_dir):
                fpath = os.path.join(cur_dir, fname)
                try:
                    fstat = os.lstat(fpath)
                except Exception as err:
                    if on_error is None:
                        raise
                    else:
                        on_error(fpath, err)

                ftype = file_types.get(stat.S_IFMT(fstat.st_mode), "unknown")
                fileinfo = {
                    "filename": fname,
                    "dir": cur_dir,
                    "path": fpath,
                    "type": ftype,
                    "size": fstat.st_size,
                    "uid": fstat.st_uid,
                    "gid": fstat.st_gid,
                }
                if (
                    (name is None or fnmatch.fnmatch(fname, name)) and
                    (path is None or fnmatch.fnmatch(fpath, path)) and
                    (ftype is None or ftype == fileinfo["type"]) and
                    (min_size is None or fstat.st_size >= min_size) and
                    (max_size is None or fstat.st_size <= max_size) and
                    (uid is None or fstat.st_uid == uid) and
                    (gid is None or fstat.st_gid == gid)
                ):
                    yield fileinfo

                # Recurse into dir?
                if stat.S_ISDIR(fstat.st_mode):
                    this_depth = fpath.lstrip(os.path.sep).count(os.path.sep)
                    if (
                        (depth is None or this_depth <= depth) and
                        (one_fs is True and fstat.st_dev == root_dev)
                    ):
                        stack.append(fpath)
        except Exception as err:
            if on_error is None:
                raise
            else:
                on_error(cur_dir, err)
