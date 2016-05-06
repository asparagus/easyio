#!/usr/bin/python
# -*- coding: utf8 -*-
"""Helper methods for dealing with directories and files."""
import os


def remove(paths):
    """Remove all files in the given array."""
    for path in paths:
        os.remove(path)


def get_files(path, extensions='*'):
    """Get the paths to files in a given path."""
    if path[-1] is not '/' and path[-1] is not '\\':
        path = path + '/'

    if isinstance(extensions, str) or isinstance(extensions, unicode):
        extensions = [extensions]

    all_files = [os.path.join(root, filename)
                 for root, dirnames, filenames in os.walk(path)
                 for filename in filenames]

    filtered_files = [
        filename for filename in all_files
        if get_extension(filename) in extensions or '*' in extensions
    ]

    return filtered_files


def path_leaf(path):
    """Get the file name (without path) from a full path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_extension(path):
    """
    Get the extension of a file.

    >>> path = 'dir/file.txt'
    >>> get_extension(path)
    '.txt'
    """
    return os.path.splitext(path)[1]


def unit_test():
    """Test the module."""
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    unit_test()
