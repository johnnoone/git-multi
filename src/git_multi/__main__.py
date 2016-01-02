#!/usr/bin/env python

from __future__ import absolute_import

import sys
from git_multi.cli import dispatch


def main():
    return dispatch(sys.argv[1:])

if __name__ == '__main__':
    main()
